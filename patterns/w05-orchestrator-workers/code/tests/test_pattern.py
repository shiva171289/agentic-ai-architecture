from core.contracts import Task, WorkerResult, WorkerRegistry
from core.llm import MockLLM
from core.pattern import DEFAULT_MAX_WORKERS, make_plan, run_orchestrator
from core.workers import LookupWorker, default_registry


def _llm() -> MockLLM:
    return MockLLM()


# --- plan / decomposition -------------------------------------------------


def test_multi_part_request_produces_two_workers():
    reg = default_registry(_llm())
    plan = make_plan(_llm(), "Where is my order and what is the return window?", reg)
    assert sorted(plan.kinds()) == ["order_lookup", "policy_lookup"]


def test_single_part_request_delegates_at_most_one_worker():
    reg = default_registry(_llm())
    plan = make_plan(_llm(), "How do I reset my widget?", reg)
    assert plan.kinds() == ["policy_lookup"]


def test_plan_is_deterministic():
    reg = default_registry(_llm())
    q = "Where is order ORD-1001 and the warranty?"
    assert make_plan(_llm(), q, reg).kinds() == make_plan(_llm(), q, reg).kinds()


def test_fan_out_is_capped():
    reg = default_registry(_llm())
    plan = make_plan(
        _llm(), "order and return and warranty and refund", reg, max_workers=1
    )
    assert len(plan.tasks) <= 1
    assert len(plan.tasks) <= DEFAULT_MAX_WORKERS


def test_unknown_kind_is_dropped():
    reg = default_registry(_llm())

    class BadPlanner(MockLLM):
        def complete(self, system, user):
            from core.llm import PLAN_MARKER, LLMResponse

            if PLAN_MARKER in system:
                return LLMResponse(
                    text='{"tasks": [{"kind": "telepathy", "instruction": "x"}]}'
                )
            return super().complete(system, user)

    plan = make_plan(BadPlanner(), "anything", reg)
    assert plan.tasks == []


# --- worker registry / selection -----------------------------------------


def test_registry_selects_by_capability():
    reg = default_registry(_llm())
    assert reg.knows("order_lookup")
    worker = reg.select("order_lookup")
    assert worker.kind == "order_lookup"


def test_registry_rejects_unknown():
    reg = default_registry(_llm())
    try:
        reg.select("nope")
    except KeyError:
        return
    raise AssertionError("expected KeyError for unknown worker kind")


def test_worker_returns_attributable_result():
    reg = default_registry(_llm())
    result = reg.select("order_lookup").run(Task("order_lookup", "status"))
    assert result.ok
    assert "ORD-1001" in result.detail
    assert result.as_context().startswith("order_lookup:")


# --- merge / verify / end to end -----------------------------------------


def test_merge_includes_each_worker_result():
    orch = run_orchestrator(
        _llm(), "Where is my order and what is the return window?"
    )
    context = "\n".join(r.as_context() for r in orch.results)
    assert "order_lookup:" in context
    assert "policy_lookup:" in context


def test_orchestration_verifier_passes_for_full_fan_out():
    orch = run_orchestrator(
        _llm(), "Where is my order and what is the return window?"
    )
    assert orch.complete
    assert orch.problems == []


def test_verifier_flags_failed_worker():
    reg = default_registry(_llm())

    def flaky(task: Task, r: WorkerRegistry) -> WorkerResult:
        if task.kind == "order_lookup":
            return WorkerResult(kind=task.kind, ok=False, detail="timeout")
        return r.select(task.kind).run(task)

    orch = run_orchestrator(
        _llm(),
        "Where is my order and what is the return window?",
        registry=reg,
        runner=flaky,
    )
    assert not orch.complete
    assert "order_lookup" in orch.problems


def test_end_to_end_answer_grounded_in_context():
    orch = run_orchestrator(_llm(), "Where is order ORD-1001?")
    assert "Acme policy and order" in orch.answer
    assert "ORD-1001" in orch.answer


def test_replay_reuses_plan_via_checkpoint():
    llm = _llm()
    first = run_orchestrator(llm, "Where is order ORD-1001 and the warranty?")
    second = run_orchestrator(
        llm,
        "Where is order ORD-1001 and the warranty?",
        checkpoint=first.checkpoint,
    )
    assert second.plan.kinds() == first.plan.kinds()
    assert second.complete


def test_no_hard_coded_worker_in_planner_prompt():
    # The planner prompt must not name a specific worker implementation.
    from core.pattern import PLAN_PROTOCOL

    assert "LookupWorker" not in PLAN_PROTOCOL
    assert "class " not in PLAN_PROTOCOL
