"""Deterministic mock LLM for the evaluator-optimizer sample.

Three call shapes, one per role in the loop:

1. draft     - the generator's first attempt
2. critique  - the critic's structured verdict (JSON)
3. rewrite   - the generator's revision from the critique

The mock is deterministic so tests and replay are stable: the same task
always yields the same first draft, the same verdict, and the same rewrite.
In production each marker is a real prompt against a model; the contract
between the calls does not change.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

DRAFT_MARKER = "TASK:DRAFT"
CRITIQUE_MARKER = "TASK:CRITIQUE"
REWRITE_MARKER = "TASK:REWRITE"

DAY_CLAIM = re.compile(r"(\d+)[\s-]*(?:calendar\s+)?day", re.IGNORECASE)
MONTH_CLAIM = re.compile(r"(\d+)[\s-]*month", re.IGNORECASE)


@dataclass
class LLMResponse:
    text: str


class LLM:
    def complete(self, system: str, user: str) -> LLMResponse:  # pragma: no cover
        raise NotImplementedError


class MockLLM(LLM):
    """Stand-in model. The first draft is wrong on purpose.

    A sample that starts from a correct draft cannot show the loop doing
    anything. This draft states a 90-day return window and offers a refund
    on an opened item with no review - both violations of the policy store.
    """

    def __init__(self, first_draft: str | None = None) -> None:
        self._first_draft = first_draft or (
            "You can return your Acme Widget within 90 days for a full refund, "
            "even if you have opened it."
        )

    def complete(self, system: str, user: str) -> LLMResponse:
        if DRAFT_MARKER in system:
            return LLMResponse(text=self._first_draft)
        if CRITIQUE_MARKER in system:
            payload = json.loads(user)
            return LLMResponse(
                text=json.dumps(_judge(payload["draft"], payload["policy"]))
            )
        if REWRITE_MARKER in system:
            payload = json.loads(user)
            return LLMResponse(
                text=_revise(payload["draft"], payload["violations"], payload["policy"])
            )
        return LLMResponse(text="Please restate the request.")


def _judge(draft: str, policy: list[dict]) -> dict:
    """Grade a draft against policy rows. The critic's external signal.

    The mock delegates to the real in-process checker so the sample shows
    the *contract* (evidence in, verdict out), not a second opinion from the
    same model. A deployed critic sends the same payload to a model and
    parses the same JSON back.
    """

    from core.policy import PolicyStore, rules_from_evidence

    store = PolicyStore(rules=[])
    verdict = store.check_rules(draft, rules_from_evidence(policy))
    return {
        "passed": verdict.passed,
        "violations": [
            {"rule": v.rule, "detail": v.detail} for v in verdict.violations
        ],
        "score": verdict.score,
    }


def _revise(draft: str, violations: list[dict], policy: list[dict]) -> str:
    """Apply the cited violations to the draft.

    Bounded on purpose: it corrects the named facts and nothing else, so the
    rewrite cannot silently change an unrelated criterion.
    """

    facts: dict[str, int] = {}
    for row in policy:
        facts.update(row.get("facts", {}))

    rules = {v["rule"] for v in violations}
    revised = draft

    if "returns" in rules:
        if "return_window_days" in facts:
            revised = DAY_CLAIM.sub(f"{facts['return_window_days']} day", revised)
        if facts.get("opened_requires_review"):
            revised = revised.replace(
                "even if you have opened and used it.", ""
            ).replace("even if you have opened it.", "")
            revised = revised.replace(
                "No approval is needed.",
                "Opened items need manager review for a refund.",
            )
            if "manager review" not in revised.lower():
                revised = revised.rstrip(" ,.") + "."
                revised += " Opened items need manager review for a refund."

    if "warranty" in rules and "warranty_months" in facts:
        revised = MONTH_CLAIM.sub(f"{facts['warranty_months']} month", revised)

    return revised.strip()
