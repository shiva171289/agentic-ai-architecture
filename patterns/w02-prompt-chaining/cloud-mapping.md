# Cloud mapping — Prompt chaining

## Cloud-agnostic core

`classify → retrieve → complete` with intent-specific system prompts.

## AWS

| Component | Service | Notes |
|-----------|---------|-------|
| Chain orchestration | Step Functions Express or Lambda sequence | One state per chain step |
| Classify step | Bedrock InvokeModel (small model) | Optional; Acme uses rules first |
| Answer step | Bedrock InvokeModel | Separate prompt templates per intent |

## Azure

| Component | Service | Notes |
|-----------|---------|-------|
| Chain orchestration | Durable Functions or Logic Apps | Sequential activities |
| Prompt templates | Prompt Flow / Foundry prompts | Version per intent |
| Answer step | Foundry chat deployment | Pin deployment per intent if needed |

## Comparison

Both clouds favor **explicit orchestration** for chains instead of hiding steps inside one chat call — easier audit and cost attribution per step.
