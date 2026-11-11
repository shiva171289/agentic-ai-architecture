# LinkedIn — w02 prompt-chaining

## Post A — Pattern

**Hook:** Before you route models or add agents, try a **two-step prompt chain**.

Classify intent → retrieve → answer with an intent-specific system prompt.

You get per-intent eval sets and clearer failures (mis-route) without variable agent loops.

Acme w02: billing vs product prompts on one corpus.

Code on GitHub — link in comments.

## Post B — Opinion

**Hot take:** If you cannot name your intents, chaining will not save you.

Start with 3–5 intents max. Measure mis-route rate before adding w03 routing.

Blog: /blog/w02-prompt-chaining/
