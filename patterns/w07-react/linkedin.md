# LinkedIn — w07 react

## Post A — Pattern

ReAct hands control flow to the model. Every pattern so far (w01–w06) fixed the path before the request ran — the chain, the routes, the worker list, the critic's criteria. Here the model decides the next action itself.

- First pattern where action selection happens at runtime. The model picks the tool from the request, not from code.
- Acme case: if the request already carries the order number and delivery date, skip `get_order_status`. The agent decides.
- You control three things: a curated read-only tool set, pre-execution checks (allowlist, argument schema, intent), and the stop rule (`MAX_STEPS = 4` plus token and wall-clock budgets). ReAct has no built-in terminator.
- Use the provider's typed tool contract (a `tool_use` block executed by your code, returned as a typed `tool_result`), not parsed "Thought / Action / Observation" prose.
- The loop is where prompt injection becomes action: customer text can steer the next tool call. Google's inline semantic check cuts AgentDojo attack success from 48.7% to 0.9%. Keep writes out of the loop.

Diagram: reason → decide → (tool call gated by a pre-execution check) → observe → bounded loop → reply.

Full write-up in the first comment.

## Post B — Opinion

Most customer requests still do not need a free-running agent loop.

- AWS: Amazon Bedrock + AgentCore, the tool a Lambda under an STS-scoped read-only identity. Azure: Foundry Agent Service + a Foundry Toolbox behind one MCP endpoint, the tool an Azure Functions app under an Entra ID managed identity.
- If the path is known and short, use a fixed chain (w02): cheaper, testable, deterministic. Anthropic's own material ranks agents last, after five workflow patterns.

And no corpus source specifies a safe stop-rule number for a customer-facing loop — that control is yours to set.

When does a loop add real value without adding risk or cost?

/blog/w07-react/

## Comment starters

1. Where have you seen a ReAct loop reduce friction without introducing instability?
2. How do you enforce pre-execution checks without blocking legitimate edge cases?
3. Is a 4-step limit realistic for customer support, or are we underestimating path complexity?
