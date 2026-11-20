"""Evaluator-optimizer: draft, critique against policy, rewrite, capped.

The loop length is a runtime decision: the critic's verdict decides whether
a rewrite happens, and a hard cap decides how many can happen. Everything
else - which policy rows count as evidence, how a verdict is shaped, how a
run is recorded - is fixed by contract.
"""

from __future__ import annotations

import json

from core.contracts import Attempt, Run, Verdict, VerdictHook
from core.llm import CRITIQUE_MARKER, DRAFT_MARKER, REWRITE_MARKER, LLM
from core.policy import PolicyStore, verdict_from_dict

DEFAULT_MAX_REWRITES = 1

DRAFT_PROTOCOL = (
    f"{DRAFT_MARKER}\n"
    "You are Acme Manufacturing tier-1 support. Draft a reply to the customer "
    "using only the supplied context. State policy values exactly. Be concise."
)

CRITIQUE_PROTOCOL = (
    f"{CRITIQUE_MARKER}\n"
    "You are an Acme policy critic. Grade the draft against the supplied policy "
    "rows only - do not grade from memory and do not rewrite. Return JSON: "
    '{"passed": <bool>, "violations": [{"rule": "<rule id>", "detail": "<what is '
    'wrong>"}], "score": <0..1>}. Cite only the rows you were given.'
)

REWRITE_PROTOCOL = (
    f"{REWRITE_MARKER}\n"
    "You are Acme Manufacturing tier-1 support. Rewrite the draft so it fixes "
    "every cited violation and changes nothing else. Keep the same intent."
)


def generate(llm: LLM, task: str, context: str) -> str:
    """The generator's first attempt."""

    return llm.complete(DRAFT_PROTOCOL, f"Task: {task}\nContext: {context}").text


def evaluate(llm: LLM, draft: str, store: PolicyStore) -> Verdict:
    """The critic: evidence in, structured verdict out.

    The evidence is read from the policy store *first*. A critic that grades
    without it is the failure mode CRITIC documents - so an empty evidence
    set is recorded rather than silently treated as a pass.
    """

    evidence = store.evidence(draft)
    payload = json.dumps({"draft": draft, "policy": evidence})
    raw = llm.complete(CRITIQUE_PROTOCOL, payload).text
    try:
        return verdict_from_dict(json.loads(raw))
    except (ValueError, TypeError):
        # Unparseable verdict: fall back to the deterministic checker rather
        # than shipping unchecked or blocking every reply on a bad JSON day.
        return store.check(draft)


def revise(llm: LLM, draft: str, verdict: Verdict, store: PolicyStore) -> str:
    """The optimizer: rewrite bounded to the cited violations."""

    payload = json.dumps(
        {
            "draft": draft,
            "violations": [{"rule": v.rule, "detail": v.detail} for v in verdict.violations],
            "policy": store.evidence(draft),
        }
    )
    return llm.complete(REWRITE_PROTOCOL, payload).text.strip() or draft


def run_evaluator_optimizer(
    llm: LLM,
    task: str,
    *,
    context: str = "",
    store: PolicyStore | None = None,
    max_rewrites: int = DEFAULT_MAX_REWRITES,
    on_verdict: VerdictHook | None = None,
) -> Run:
    """Draft -> critique -> (rewrite -> critique)* until pass or cap.

    ``on_verdict`` is the online eval hook: it fires for every attempt, so a
    failed draft is scored next to its trace even when the rewrite saves it.
    """

    store = store or PolicyStore()
    draft = generate(llm, task, context)
    verdict = evaluate(llm, draft, store)
    run = Run(final_text=draft, attempts=[Attempt("draft", draft, verdict)])
    if on_verdict:
        on_verdict(verdict.as_telemetry())

    while not verdict.passed and run.rewrites < max_rewrites:
        draft = revise(llm, draft, verdict, store)
        verdict = evaluate(llm, draft, store)
        run.rewrites += 1
        run.attempts.append(Attempt("rewrite", draft, verdict))
        if on_verdict:
            on_verdict(verdict.as_telemetry())

    run.final_text = draft
    return run
