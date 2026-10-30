# LinkedIn — w01 augmented-llm

## Post A — Pattern

**Hook:** Most enterprise “agents” should ship as augmented LLMs first—one retrieval + one generation + guarded tools.

**Body:**

Before you add ReAct loops or multi-agent drama, ask:

• Can retrieval + a strict prompt answer 80% of cases?  
• Do you have a golden eval set **today**?  
• Are tools scoped least-privilege (not “MCP everything”)?

Pattern (Acme Manufacturing-style support):

1. Retrieve approved docs  
2. Compose prompt with context boundaries  
3. Single model call  
4. Optional ticket tool behind policy  

AWS: Bedrock + Knowledge Bases  
Azure: Foundry models + AI Search  

Diagram in carousel 👇

Code + ADR on GitHub (link in comments).

---

## Post B — Opinion

**Thesis:** Adding autonomy before measurement is how AI prototypes die in production.

**Body:**

Augmented LLMs fail loudly when retrieval is bad—that’s fixable.

Autonomous agents fail **quietly** when tool graphs grow—hard to regression-test.

My rule: prove augmented baseline latency, cost, and quality **per task** for 4 weeks. Only then escalate pattern complexity.

Agree/disagree: what metric triggered your last jump from RAG chat to “real agent”?

**First comment:** Full write-up: `<blog URL after deploy>`

---

## Comment starters

1. What eval size do you require before enabling write tools?
2. Bedrock Knowledge Bases vs bring-your-own OpenSearch—what did you pick and why?
3. When did a single LLM call stop being enough for your use case?
