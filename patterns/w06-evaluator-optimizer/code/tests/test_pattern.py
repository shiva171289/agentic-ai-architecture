from core.llm import CRITIQUE_MARKER, LLM, LLMResponse, MockLLM
from core.pattern import evaluate, run_evaluator_optimizer
from core.policy import PolicyStore


def _run(**kwargs):
    return run_evaluator_optimizer(
        MockLLM(),
        "What is the return window?",
        context="Unopened items may be returned within 30 days.",
        **kwargs,
    )


# --- the first draft is checked -------------------------------------------


def test_first_draft_fails_the_policy_check():
    run = run_evaluator_optimizer(MockLLM(), "return window?", max_rewrites=0)
    assert not run.initial_verdict.passed
    # Two cited violations: the wrong window, and the unreviewed opened-item refund.
    assert {v.rule for v in run.initial_verdict.violations} == {"returns"}
    assert len(run.initial_verdict.violations) == 2


def test_violation_cites_the_policy_value():
    run = run_evaluator_optimizer(MockLLM(), "return window?", max_rewrites=0)
    detail = run.initial_verdict.violations[0].detail
    assert "90" in detail and "30" in detail


# --- the loop rewrites, once ---------------------------------------------


def test_loop_rewrites_once_and_then_passes():
    run = _run()
    assert run.rewrites == 1
    assert run.verdict.passed
    assert len(run.attempts) == 2
    assert [a.kind for a in run.attempts] == ["draft", "rewrite"]


def test_rewrite_corrects_the_cited_values():
    run = _run()
    assert "30 day" in run.final_text
    assert "90 day" not in run.final_text
    assert "manager review" in run.final_text.lower()


def test_rewrite_is_bounded_to_the_cited_violation():
    # The rewrite keeps the draft's intent; it does not rewrite the message.
    run = _run()
    assert "return your Acme Widget" in run.final_text


def test_cap_ships_the_unchecked_draft():
    run = _run(max_rewrites=0)
    assert run.rewrites == 0
    assert len(run.attempts) == 1
    assert not run.verdict.passed
    assert run.final_text == run.attempts[0].text


def test_compliant_first_draft_needs_no_rewrite():
    llm = MockLLM(
        first_draft=(
            "Unopened items may be returned within 30 days. "
            "Opened items need manager review."
        )
    )
    run = run_evaluator_optimizer(llm, "return window?")
    assert run.verdict.passed
    assert run.rewrites == 0


# --- the critic is grounded in the store ----------------------------------


def test_critic_without_a_policy_store_cannot_catch_the_violation():
    # The documented failure mode: a critic with no external signal agrees
    # with the draft. Keep this test - it is the pattern's whole risk.
    run = run_evaluator_optimizer(MockLLM(), "return window?", store=PolicyStore(rules=[]))
    assert run.verdict.passed
    assert run.rewrites == 0


def test_critic_receives_policy_evidence():
    class RecordingLLM(MockLLM):
        def __init__(self):
            super().__init__()
            self.critique_payload: dict = {}

        def complete(self, system, user):
            if CRITIQUE_MARKER in system:
                import json

                self.critique_payload = json.loads(user)
            return super().complete(system, user)

    llm = RecordingLLM()
    evaluate(llm, "return within 90 days", PolicyStore())
    assert llm.critique_payload["policy"], "critic must be handed policy rows"
    facts = llm.critique_payload["policy"][0]["facts"]
    assert facts["return_window_days"] == 30


def test_unparseable_verdict_falls_back_to_the_policy_check():
    class BadCritic(MockLLM):
        def complete(self, system, user):
            if CRITIQUE_MARKER in system:
                return LLMResponse(text="I think it is fine!")
            return super().complete(system, user)

    verdict = evaluate(BadCritic(), "return within 90 days", PolicyStore())
    assert not verdict.passed
    assert verdict.violations


# --- telemetry ------------------------------------------------------------


def test_each_attempt_emits_a_verdict_score():
    scores: list[dict] = []
    _run(on_verdict=scores.append)
    assert len(scores) == 2
    assert scores[0]["score"] < 1.0
    assert scores[0]["passed"] is False
    assert scores[1]["passed"] is True
    assert scores[1]["score"] == 1.0


def test_verdict_telemetry_shape():
    run = _run()
    payload = run.verdict.as_telemetry()
    assert set(payload) == {"passed", "score", "violations"}
    assert 0.0 <= payload["score"] <= 1.0
