# LinkedIn post pillars

Use these templates while the weekly blog matures. Ground every **NewsLens** post in [content/source-corpus/latest.md](source-corpus/latest.md). Agents draft; **you** post manually ([00-ground-rules.md](../docs/roadmap/00-ground-rules.md)).

## Mix (Week 1–4)

1. **70%** Pattern or Opinion (from `patterns/wNN/linkedin.md` or ADR bullets).
2. **30%** NewsLens (from Telegram `news today` LinkedIn angle lines).

Cap NewsLens at **two posts per week**.

---

## Pillar A — Pattern

**Purpose:** Teach one architecture pattern from the Acme spine.

**Structure:**

1. Hook (one sentence, ≤12 words).
2. Three bullets (tradeoffs or steps).
3. CTA: code + ADR on GitHub (link in first comment).

**Example hook:** Most enterprise agents should start as augmented LLMs—not multi-agent graphs.

---

## Pillar B — Opinion

**Purpose:** State a thesis senior architects can disagree with.

**Structure:**

1. Thesis (one sentence).
2. Two contrasts (what fails loud vs quiet).
3. Question to comments.
4. First comment: blog URL when live.

**Example thesis:** Add autonomy only after four weeks of augmented-LLM metrics per task.

---

## Pillar C — NewsLens

**Purpose:** Comment on vendor news with an architecture lens—not a link dump.

**Structure:**

1. Name the vendor release (from corpus URL).
2. One tradeoff for enterprise (evals, tools, cost, sovereignty).
3. One sentence how it maps to Acme (optional).
4. Source URL in post or first comment.

**Rules:**

1. Cite one allowlisted URL only.
2. Do not repost the same thesis as Post A/B for that week.
3. Keep body ≤50 words before the URL.

**Example:** Google ADK posts agent lifecycle tooling. I still gate production on eval baselines before new SDK surface area. `<corpus URL>`

---

## Related

- [content/voice-guide.md](voice-guide.md)
- [docs/roadmap/02-content-strategy.md](../docs/roadmap/02-content-strategy.md)
- [hermes/skills/daily-ai-brief/SKILL.md](../hermes/skills/daily-ai-brief/SKILL.md)
