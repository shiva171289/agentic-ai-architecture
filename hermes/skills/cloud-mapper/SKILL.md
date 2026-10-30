---
name: cloud-mapper
description: AWS and Azure mapping for weekly pattern. Tier 1 model.
---

# CloudMapper

Apply `_shared/ground-rules.md`.

## Inputs

- Approved `adr.md`
- [docs/roadmap/03-multi-cloud-aws-azure.md](../../../docs/roadmap/03-multi-cloud-aws-azure.md)

## Tasks

Write `cloud-mapping.md` from [templates/cloud-mapping.md](../../templates/cloud-mapping.md):

- Cloud-agnostic summary
- AWS services + reference diagram notes
- Azure services + reference diagram notes
- Comparison table
- Indicative cost per 1,000 runs (order of magnitude)
- Lock-in and portability notes
- Flag deprecated/rename if docs differ

## Output

Commit to `drafts/{week}` branch.
