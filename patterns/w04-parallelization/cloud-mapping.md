# Cloud mapping — Parallelization

## AWS

- Lambda **parallel** invocations (Knowledge Base + DynamoDB order) → merge in orchestrator Step Function **Parallel state**.

## Azure

- Durable Functions **fan-out/fan-in** or asyncio in one Function app for I/O-bound calls.
