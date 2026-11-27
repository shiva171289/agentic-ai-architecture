# AWS adapter stub.
#
# The loop is hosted; the stop rule and the checks stay in our code.
#
#   Runtime   -> Bedrock AgentCore (long agent sessions) hosts the loop, or a
#                Step Functions state machine owns it if the trajectory must
#                be replayable
#   Model     -> Amazon Bedrock invoke returns typed `tool_use` blocks; the
#                loop executes them and returns `tool_result` blocks. Do not
#                parse "Thought / Action / Observation" prose.
#   Tool      -> get_order_status reads order state through a read-only role
#                (no write scope in the loop)
#   Gate      -> before execution, allowlist the tool and validate arguments
#                against the tool schema; a proposed call is checked against
#                user intent (inline policy / Bedrock Guardrails)
#   Stop rule -> max steps + token budget + wall-clock, owned by our code
#   Trace     -> one trajectory per request (reason, call, observation)
#
# The tool surface stays small and the descriptions current: argument accuracy
# degrades as the surface grows.
raise NotImplementedError("AWS ReAct loop runtime")
