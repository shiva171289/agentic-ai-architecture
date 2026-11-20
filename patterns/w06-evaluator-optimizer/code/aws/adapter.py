# AWS adapter stub.
#
# Step Functions state machine around the loop:
#   Draft state    -> Bedrock invoke (generator)
#   Critique state -> Lambda reads the policy row (DynamoDB), then a second
#                     Bedrock invoke returns the JSON verdict
#   Choice state   -> verdict.passed == true -> Ship
#                     verdict.passed == false and rewrites < cap -> Rewrite
#                     rewrites == cap -> Ship with the recorded violation
#   Ship state     -> emit the verdict to CloudWatch Omni as an evaluation
#                     score next to the trace
#
# The step cap is a state-machine constant, not a prompt instruction.
raise NotImplementedError("AWS Step Functions evaluator-optimizer loop")
