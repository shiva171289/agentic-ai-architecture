"""Shared contracts for the evaluator-optimizer sample.

The loop's interfaces are small on purpose: a policy store that holds the
criteria as data, a verdict the critic must produce, and a run record that
keeps every attempt so the loop is inspectable after the fact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class PolicyRule:
    """One named criterion, with the values the critic can check.

    Facts are data, not prose: ``{"return_window_days": 30}`` can be checked,
    "follow the returns policy" cannot.
    """

    rule_id: str
    statement: str
    keywords: tuple[str, ...] = ()
    facts: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Violation:
    """A specific, cited failure of one rule. The rewrite is bounded to these."""

    rule: str
    detail: str


@dataclass
class Verdict:
    """The critic's output. Structured, loggable, and cheap to store."""

    passed: bool
    violations: list[Violation] = field(default_factory=list)
    score: float = 1.0

    def as_telemetry(self) -> dict:
        """The form emitted next to the trace by the online eval hook."""

        return {
            "passed": self.passed,
            "score": self.score,
            "violations": [v.rule for v in self.violations],
        }


@dataclass
class Attempt:
    """One generate-then-critique round."""

    kind: str  # "draft" | "rewrite"
    text: str
    verdict: Verdict


@dataclass
class Run:
    """Full record of one evaluator-optimizer run."""

    final_text: str
    attempts: list[Attempt] = field(default_factory=list)
    rewrites: int = 0

    @property
    def verdict(self) -> Verdict:
        return self.attempts[-1].verdict

    @property
    def initial_verdict(self) -> Verdict:
        return self.attempts[0].verdict


VerdictHook = Callable[[dict], None]
