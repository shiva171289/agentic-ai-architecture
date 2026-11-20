"""The policy store: the critic's external signal.

The point of the pattern is that the critic checks something *outside the
draft*. This module is that something. It is deliberately model-free, so it
can also serve as the fallback when the model critic is unavailable or its
verdict cannot be parsed.

Swap the in-memory list for a real store (DynamoDB, Cosmos DB, a policy
service) without touching the loop.
"""

from __future__ import annotations

from core.contracts import PolicyRule, Violation, Verdict
from core.llm import DAY_CLAIM, MONTH_CLAIM

DEFAULT_RULES: tuple[PolicyRule, ...] = (
    PolicyRule(
        rule_id="returns",
        statement=(
            "Unopened items may be returned within 30 days. Opened items "
            "require manager review for refund eligibility."
        ),
        keywords=("return", "refund", "exchange", "opened"),
        facts={"return_window_days": 30, "opened_requires_review": True},
    ),
    PolicyRule(
        rule_id="warranty",
        statement="Acme Widget includes a 12-month limited warranty.",
        keywords=("warranty", "guarantee", "coverage"),
        facts={"warranty_months": 12},
    ),
    PolicyRule(
        rule_id="shipping",
        statement="Standard shipping is 3-5 business days.",
        keywords=("shipping", "delivery", "track"),
        facts={"shipping_days_min": 3, "shipping_days_max": 5},
    ),
)


class PolicyStore:
    """Holds the criteria as data and answers a draft with cited violations."""

    def __init__(self, rules: list[PolicyRule] | None = None) -> None:
        self._rules = list(rules if rules is not None else DEFAULT_RULES)

    def rules(self) -> list[PolicyRule]:
        return list(self._rules)

    def select(self, draft: str) -> list[PolicyRule]:
        """The rows the draft actually touches - the critic's evidence set."""

        text = draft.lower()
        selected = [
            rule for rule in self._rules if any(k in text for k in rule.keywords)
        ]
        return selected

    def evidence(self, draft: str) -> list[dict]:
        """What the critic is given. Rows only, no opinion about the draft."""

        return [
            {"rule": r.rule_id, "statement": r.statement, "facts": r.facts}
            for r in self.select(draft)
        ]

    def check(self, draft: str) -> Verdict:
        """Deterministic policy check. The fallback path, and the tests' signal."""

        return self.check_rules(draft, self.select(draft))

    def check_rules(self, draft: str, rules: list[PolicyRule]) -> Verdict:
        """Check a draft against an explicit rule set.

        The critic's evidence may arrive as rows rather than a live store
        handle (that is how it crosses a service boundary in a deployed
        system), so the checker accepts rules directly.
        """

        violations: list[Violation] = []
        for rule in rules:
            violations.extend(self._check_rule(draft, rule))
        score = 1.0 if not violations else max(0.0, 1.0 - 0.25 * len(violations))
        return Verdict(passed=not violations, violations=violations, score=score)

    def _check_rule(self, draft: str, rule: PolicyRule) -> list[Violation]:
        text = draft.lower()
        out: list[Violation] = []

        if rule.rule_id == "returns":
            expected = rule.facts.get("return_window_days")
            for days in [int(n) for n in DAY_CLAIM.findall(draft)]:
                if expected is not None and days != expected:
                    out.append(
                        Violation(
                            rule="returns",
                            detail=(
                                f"return window stated as {days} days; "
                                f"policy is {expected}"
                            ),
                        )
                    )
            if rule.facts.get("opened_requires_review") and (
                "opened" in text or "used" in text
            ):
                if "review" not in text:
                    out.append(
                        Violation(
                            rule="returns",
                            detail=(
                                "refund offered on an opened item without manager review"
                            ),
                        )
                    )

        if rule.rule_id == "warranty":
            expected = rule.facts.get("warranty_months")
            for months in [int(n) for n in MONTH_CLAIM.findall(draft)]:
                if expected is not None and months != expected:
                    out.append(
                        Violation(
                            rule="warranty",
                            detail=(
                                f"warranty stated as {months} months; "
                                f"policy is {expected}"
                            ),
                        )
                    )

        return out


def rules_from_evidence(rows: list[dict]) -> list[PolicyRule]:
    """Rebuild rules from the evidence rows a critic was handed."""

    return [
        PolicyRule(
            rule_id=str(row.get("rule", "unknown")),
            statement=str(row.get("statement", "")),
            facts=dict(row.get("facts", {})),
        )
        for row in rows
    ]


def verdict_from_dict(data: dict) -> Verdict:
    """Parse a model critic's JSON verdict into the shared contract."""

    violations = [
        Violation(rule=str(v.get("rule", "unknown")), detail=str(v.get("detail", "")))
        for v in data.get("violations", [])
        if isinstance(v, dict)
    ]
    passed = bool(data.get("passed", not violations))
    score = float(data.get("score", 1.0 if passed else max(0.0, 1.0 - 0.25 * len(violations))))
    return Verdict(passed=passed and not violations, violations=violations, score=score)
