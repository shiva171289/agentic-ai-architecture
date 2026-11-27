# Azure adapter stub.
#
#   Runtime   -> Microsoft Foundry Agent Service hosts the agent (threads,
#                tool calls); Durable Functions owns the loop when the
#                trajectory must survive a host restart
#   Model     -> Foundry model deployments return typed function-call blocks;
#                the loop executes them and returns typed tool results
#   Tool      -> order tool reads through a managed identity with scoped read;
#                Foundry Toolboxes group tools behind one MCP endpoint with a
#                policy that centrally sets the approved tool types
#   Gate      -> argument validation against the tool schema, plus the tool
#                policy, before execution
#   Stop rule -> max steps + token budget + wall-clock, owned by our code
#   Trace     -> trajectory emitted to Application Insights; multi-turn
#                evaluation scores the whole conversation, not one answer
raise NotImplementedError("Azure ReAct loop runtime")
