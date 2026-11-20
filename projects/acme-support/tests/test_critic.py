from core.critic import (
    MAX_REWRITES,
    answer_with_critic,
    check_policy,
    critique,
    rule_facts,
)
from core.llm import MockLLM
from core.support import load_policies

FLAWED = (
    "You can return your Acme Widget within 90 days for a full refund, "
    "even if you have opened it."
)
COMPLIANT = (
    "Unopened items may be returned within 30 days. "
    "Opened items need manager review for a refund."
)


def _policies() -> list[dict]:
    return load_policies()


def _fixed(draft: str):
    return lambda: draft


# --- the deterministic check (the critic's tool) --------------------------


def test_check_flags_wrong_return_window():
    verdict = check_policy(FLAWED, _policies())
    assert not verdict.passed
    assert any("90" in v.detail and "30" in v.detail for v in verdict.violations)


def test_check_flags_unreviewed_opened_item_refund():
    verdict = check_policy(FLAWED, _policies())
    assert any("review" in v.detail for v in verdict.violations)


def test_check_passes_a_compliant_draft():
    verdict = check_policy(COMPLIANT, _policies())
    assert verdict.passed
    assert verdict.violations == []
    assert verdict.score == 1.0


def test_policy_facts_are_data_not_prose():
    facts = rule_facts(_policies())
    assert facts["return_window_days"] == 30
    assert facts["warranty_months"] == 12


# --- the critic is grounded -----------------------------------------------


def test_critique_is_handed_policy_rows():
    seen: dict = {}

    class Recording(MockLLM):
        def complete(self, system, user):
            if "TASK:CRITIQUE" in system:
                import json

                seen.update(json.loads(user))
            return super().complete(system, user)

    critique(Recording(), FLAWED, _policies())
    assert seen["policies"], "critic must receive the policy rows"
    assert seen["policies"][0]["facts"]["return_window_days"] == 30


def test_critic_without_policies_cannot_catch_the_violation():
    # Documented failure mode: no external signal -> the critic agrees.
    verdict = critique(MockLLM(), FLAWED, policies=[])
    assert verdict.passed


def test_unparseable_verdict_falls_back_to_the_check():
    class BadCritic(MockLLM):
        def complete(self, system, user):
            if "TASK:CRITIQUE" in system:
                from core.llm import LLMResponse

                return LLMResponse(text="looks fine to me")
            return super().complete(system, user)

    verdict = critique(BadCritic(), FLAWED, _policies())
    assert not verdict.passed


# --- the loop -------------------------------------------------------------


def test_loop_rewrites_once_then_passes():
    result = answer_with_critic(MockLLM(), "return?", draft_fn=_fixed(FLAWED))
    assert result.rewrites == 1
    assert result.verdict.passed
    assert "30 day" in result.answer
    assert "90 day" not in result.answer
    assert "manager review" in result.answer.lower()


def test_loop_is_capped_by_max_rewrites():
    result = answer_with_critic(
        MockLLM(), "return?", draft_fn=_fixed(FLAWED), max_rewrites=0
    )
    assert result.rewrites == 0
    assert not result.verdict.passed
    assert result.answer == FLAWED
    assert MAX_REWRITES == 1


def test_compliant_draft_ships_without_a_rewrite():
    result = answer_with_critic(MockLLM(), "return?", draft_fn=_fixed(COMPLIANT))
    assert result.rewrites == 0
    assert result.answer == COMPLIANT
    assert result.verdict.passed


def test_every_attempt_emits_a_verdict():
    seen: list[dict] = []
    answer_with_critic(
        MockLLM(), "return?", draft_fn=_fixed(FLAWED), on_verdict=seen.append
    )
    assert len(seen) == 2
    assert seen[0]["passed"] is False
    assert seen[0]["score"] < 1.0
    assert seen[1]["passed"] is True


def test_default_draft_path_runs_the_w05_orchestrator():
    # No policy numbers in the reply, so the critic passes it unchanged.
    result = answer_with_critic(MockLLM(), "How do I reset my Acme Widget?")
    assert result.verdict.passed
    assert result.rewrites == 0
    assert result.answer
