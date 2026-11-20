"""w06 — evaluator-optimizer for the Acme support reply.

The w05 stage shipped whatever the merged worker context produced. This stage
adds the step that was missing: the draft is graded against the policy store
before the customer sees it, and the generator rewrites it once if the verdict
cites a violation.

Design rules, all from the ADR:

- The critic reads the **policy store**, not just the draft (CRITIC). Without
  that external signal the critic agrees with the draft — there is a test for
  the blind case.
- The loop is capped at ``MAX_REWRITES`` and the cap lives in code, not in a
  prompt.
- Every attempt emits a verdict, so the score is available as telemetry even
  when the rewrite saves the reply.
- An unparseable verdict falls back to the deterministic checker instead of
  shipping unchecked or blocking every reply.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Callable

from core.llm import LLM

CRITIQUE_MARKER = "TASK:CRITIQUE"
REWRITE_MARKER = "TASK:REWRITE"

MAX_REWRITES = 1

DAY_CLAIM = re.compile(r"(\d+)[\s-]*(?:calendar\s+)?day", re.IGNORECASE)
MONTH_CLAIM = re.compile(r"(\d+)[\s-]*month", re.IGNORECASE)

CRITIQUE_SYSTEM = (
    f"{CRITIQUE_MARKER}\n"
    "You are an Acme policy critic. Grade the draft against the supplied policy "
    "rows only. Do not grade from memory and do not rewrite the draft. Return "
    'JSON: {"passed": <bool>, "violations": [{"rule": "<policy id>", "detail": '
    '"<what is wrong>"}], "score": <0..1>}.'
)

REWRITE_SYSTEM = (
    f"{REWRITE_MARKER}\n"
    "You are Acme Manufacturing tier-1 support. Rewrite the draft so it fixes "
    "every cited violation and changes nothing else."
)


@dataclass(frozen=True)
class Violation:
    rule: str
    detail: str


@dataclass
class Verdict:
    """The critic's structured output. Loggable as-is."""

    passed: bool
    violations: list[Violation] = field(default_factory=list)
    score: float = 1.0

    def as_telemetry(self) -> dict:
        return {
            "passed": self.passed,
            "score": self.score,
            "violations": [v.rule for v in self.violations],
        }


@dataclass
class CriticResult:
    answer: str
    draft: str
    verdicts: list[dict]
    rewrites: int
    verdict: Verdict


DraftFn = Callable[[], str]
VerdictHook = Callable[[dict], None]


# --- the external signal --------------------------------------------------


def rule_facts(policies: list[dict]) -> dict:
    """Merge the checkable values from every policy row."""

    facts: dict = {}
    for row in policies:
        facts.update(row.get("facts", {}))
    return facts


def relevant_policies(draft: str, policies: list[dict]) -> list[dict]:
    """The rows the draft actually touches — the critic's evidence set."""

    text = draft.lower()
    return [p for p in policies if any(k in text for k in p.get("keywords", []))]


def check_policy(draft: str, policies: list[dict]) -> Verdict:
    """Deterministic policy check over the cited rows.

    This is the critic's tool *and* its fallback: it can be run with no model
    call, which is what makes the verdict reproducible.
    """

    facts = rule_facts(policies)
    ids = {p["id"] for p in relevant_policies(draft, policies)}
    text = draft.lower()
    violations: list[Violation] = []

    if "returns" in ids:
        expected = facts.get("return_window_days")
        for days in [int(n) for n in DAY_CLAIM.findall(draft)]:
            if expected is not None and days != expected:
                violations.append(
                    Violation(
                        "returns",
                        f"return window stated as {days} days; policy is {expected}",
                    )
                )
        if facts.get("opened_requires_review") and (
            "opened" in text or "used" in text
        ):
            if "review" not in text:
                violations.append(
                    Violation(
                        "returns",
                        "refund offered on an opened item without manager review",
                    )
                )

    if "warranty" in ids:
        expected = facts.get("warranty_months")
        for months in [int(n) for n in MONTH_CLAIM.findall(draft)]:
            if expected is not None and months != expected:
                violations.append(
                    Violation(
                        "warranty",
                        f"warranty stated as {months} months; policy is {expected}",
                    )
                )

    score = 1.0 if not violations else max(0.0, 1.0 - 0.25 * len(violations))
    return Verdict(passed=not violations, violations=violations, score=score)


# --- the critic call ------------------------------------------------------


def _verdict_from_json(raw: str) -> Verdict | None:
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        return None
    violations = [
        Violation(str(v.get("rule", "unknown")), str(v.get("detail", "")))
        for v in data.get("violations", [])
        if isinstance(v, dict)
    ]
    passed = bool(data.get("passed", not violations))
    score = float(data.get("score", 1.0 if passed else 0.5))
    return Verdict(passed=passed and not violations, violations=violations, score=score)


def critique(llm: LLM, draft: str, policies: list[dict]) -> Verdict:
    """Grade a draft. The critic is handed the policy rows, not asked to recall."""

    evidence = relevant_policies(draft, policies)
    payload = json.dumps({"draft": draft, "policies": evidence})
    raw = llm.complete(CRITIQUE_SYSTEM, payload).text
    verdict = _verdict_from_json(raw)
    if verdict is None:
        # Fail back to the deterministic check: never ship on a bad JSON day.
        return check_policy(draft, policies)
    return verdict


def revise_draft(draft: str, violations: list[dict], policies: list[dict]) -> str:
    """Apply the cited violations. Bounded: it corrects only what was cited."""

    facts = rule_facts(policies)
    rules = {v.get("rule") for v in violations}
    text = draft

    if "returns" in rules and "return_window_days" in facts:
        text = DAY_CLAIM.sub(f"{facts['return_window_days']} day", text)
    if "warranty" in rules and "warranty_months" in facts:
        text = MONTH_CLAIM.sub(f"{facts['warranty_months']} month", text)
    if "returns" in rules and facts.get("opened_requires_review"):
        for clause in ("even if you have opened it.", "even if you have opened and used it."):
            text = text.replace(clause, "")
        if "manager review" not in text.lower():
            text = text.rstrip(" ,.") + "."
            text = text.rstrip() + " Opened items need manager review for a refund."

    return text.strip() or draft


def rewrite(llm: LLM, draft: str, verdict: Verdict, policies: list[dict]) -> str:
    payload = json.dumps(
        {
            "draft": draft,
            "violations": [{"rule": v.rule, "detail": v.detail} for v in verdict.violations],
            "policies": relevant_policies(draft, policies),
        }
    )
    return llm.complete(REWRITE_SYSTEM, payload).text.strip() or draft


# --- the loop -------------------------------------------------------------


def answer_with_critic(
    llm: LLM,
    question: str,
    *,
    policies: list[dict] | None = None,
    draft_fn: DraftFn | None = None,
    max_rewrites: int = MAX_REWRITES,
    on_verdict: VerdictHook | None = None,
    allow_tools: bool = False,
) -> CriticResult:
    """Draft → critique → (rewrite → critique)* until the verdict passes or the cap fires."""

    if policies is None:
        from core.support import load_policies

        policies = load_policies()

    if draft_fn is None:
        from core.orchestrator import default_orchestrator

        draft_fn = lambda: default_orchestrator(  # noqa: E731
            llm, question, allow_tools=allow_tools
        ).text

    draft = draft_fn()
    first_draft = draft
    verdict = critique(llm, draft, policies)
    verdicts = [verdict.as_telemetry()]
    if on_verdict:
        on_verdict(verdicts[-1])

    rewrites = 0
    while not verdict.passed and rewrites < max_rewrites:
        draft = rewrite(llm, draft, verdict, policies)
        verdict = critique(llm, draft, policies)
        rewrites += 1
        verdicts.append(verdict.as_telemetry())
        if on_verdict:
            on_verdict(verdicts[-1])

    return CriticResult(
        answer=draft,
        draft=first_draft,
        verdicts=verdicts,
        rewrites=rewrites,
        verdict=verdict,
    )
