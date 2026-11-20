# Azure adapter stub.
#
# Durable Functions orchestrator (deterministic, replay-safe):
#   draft_activity     -> Foundry model call (generator)
#   critique_activity  -> reads the policy row (Cosmos DB / AI Search), then a
#                         second Foundry model call returns the JSON verdict
#   loop               -> bounded for-loop over iterations; the verdict and the
#                         iteration count are part of the orchestrator history,
#                         so a host restart resumes at the same decision
#   emit               -> verdict as a custom event / metric in Application
#                         Insights, correlated by operation id
#
# The cap is a constant in the orchestrator code, not a prompt instruction.
raise NotImplementedError("Azure Durable Functions evaluator-optimizer loop")
