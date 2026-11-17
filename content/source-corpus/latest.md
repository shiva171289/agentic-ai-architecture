# Vendor source corpus

**Generated (UTC):** 2026-11-17 06:58
**Window:** last 1 days
**Keyword filter:** (none — all items in window)

Use this file for grounding. Do not cite vendor claims that are not supported here or in official doc roots.

Config: `hermes/sources/verified-sources.json` (version 3)

## Entries

### 1. Investigate security data in place with Amazon CloudWatch and 7AI

- **Publisher:** AWS (`aws-management-blog`)
- **URL:** https://aws.amazon.com/blogs/mt/investigate-security-data-in-place-with-amazon-cloudwatch-and-7ai/
- **Published:** 2026-11-17

Security teams don’t struggle to get alerts. They struggle to get the context needed to
act on them. Consider a common scenario: an AWS Security Hub finding reports a critical
vulnerability in a container image in Amazon Elastic Container Registry. The finding
says that a package is vulnerable, but not whether the image is running, […]

### 2. High-quality cost-effective AI image generation on Amazon ECS

- **Publisher:** AWS (`aws-containers-blog`)
- **URL:** https://aws.amazon.com/blogs/containers/high-quality-cost-effective-ai-image-generation-on-amazon-ecs/
- **Published:** 2026-11-17

Learn how to run Z-Image-Turbo, a 6-billion-parameter diffusion transformer, on AWS
Inferentia2 and Amazon ECS to generate high-quality images at a fraction of a cent each,
with auto-scaling, arbitrary resolution support, and a complete CI/CD pipeline.

### 3. Introducing Smithy IDL 2.1

- **Publisher:** AWS (`aws-developer-blog`)
- **URL:** https://aws.amazon.com/blogs/developer/introducing-smithy-idl-2-1/
- **Published:** 2026-11-17

Today, we are excited to announce Smithy IDL 2.1. With Smithy 2.1, you can use three new
syntax features: inline collection declarations for lists and maps, tagged string
literals for values that carry their own escaping rules, and a shorthand for declaring
the wire order of a structure’s members. Smithy is an open source Interface […]

### 4. How Banco BMG moved from reactive to autonomous operations with AWS DevOps Agent

- **Publisher:** AWS (`aws-management-blog`)
- **URL:** https://aws.amazon.com/blogs/mt/how-banco-bmg-moved-from-reactive-to-autonomous-operations-with-aws-devops-agent/
- **Published:** 2026-11-17

Summary Banco BMG is a Brazilian financial institution with 96 years of history. Its
digital platform runs across AWS, other cloud providers, and on-premises infrastructure.
At that scale, logs, metrics, alerts, and deployments come in faster than engineers can
correlate them. When an incident hits a revenue-generating product such as PIX instant
payments or payroll […]

### 5. EPG-enriched ad requests with CloudFront Functions and AWS Elemental MediaTailor

- **Publisher:** AWS (`aws-media-blog`)
- **URL:** https://aws.amazon.com/blogs/media/epg-enriched-ad-requests-with-cloudfront-functions-and-aws-elemental-mediatailor/
- **Published:** 2026-11-17

Linear TV ad requests often carry stale program metadata because viewer sessions stay
open for hours while programs change. We show how to enrich every ad break with current
EPG metadata using Amazon CloudFront Functions, CloudFront KeyValueStore, and AWS
Elemental MediaTailor Monetization Functions, at about $14 per month.

### 6. From tasks to goals

- **Publisher:** LangChain (`langchain-blog`)
- **URL:** https://www.langchain.com/blog/from-tasks-to-goals
- **Published:** 2026-11-16

LangChain CEO and Co-founder Harrison Chase shares how we're moving from task-specific
agents to goal-focused agents. Learn more.

### 7. LangChain Raises $300M Series C at $3B Valuation

- **Publisher:** LangChain (`langchain-blog`)
- **URL:** https://www.langchain.com/blog/series-c
- **Published:** 2026-11-16

LangChain raises $300M Series C at a $3B valuation, led by CapitalG, to help every
company own its intelligence with LangSmith, the agent engineering platform.

### 8. Goal Engineering

- **Publisher:** LangChain (`langchain-blog`)
- **URL:** https://www.langchain.com/blog/goal-engineering
- **Published:** 2026-11-16

The future of agents is them taking on open ended goals and driving towards completion
of those goals. Learn more.

### 9. New context engineering challenges in late 2026

- **Publisher:** LangChain (`langchain-blog`)
- **URL:** https://www.langchain.com/blog/context-engineering-challenges-late-2026
- **Published:** 2026-11-16

LangChain CEO Harrison Chase shares insights into the biggest harness engineering
challenges with the emergence of proactive agents.

### 10. PostgreSQL large objects: Best practices for Amazon Aurora and RDS

- **Publisher:** AWS (`aws-database-blog`)
- **URL:** https://aws.amazon.com/blogs/database/postgresql-large-objects-best-practices-for-amazon-aurora-and-rds/
- **Published:** 2026-11-16

PostgreSQL large objects live outside your tables and are referenced only by an OID, so
autovacuum never reclaims the orphans. This post shows how to monitor orphaned large
objects on Amazon Aurora and Amazon RDS for PostgreSQL, run vacuumlo safely, set up
lo_manage triggers, prevent OID exhaustion, and prepare for major version upgrades.

### 11. Build memory-aware AI agents with Agentic Retrieve on Amazon Bedrock Managed Knowledge Base

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/build-memory-aware-ai-agents-with-agentic-retrieve-on-amazon-bedrock-managed-knowledge-base/
- **Published:** 2026-11-16

Amazon Bedrock Managed Knowledge Base and Amazon Bedrock AgentCore memory now store
conversations, extract facts, and bring long-term memory into a single
AgenticRetrieveStream call. This post shows how to build a memory-aware, multi-user
assistant where each user sees only the documents they may read and each user's memory
stays private.

### 12. Protecting Apache Iceberg Lakehouses at Scale with Rubrik on AWS

- **Publisher:** AWS (`aws-apn-blog`)
- **URL:** https://aws.amazon.com/blogs/apn/protecting-apache-iceberg-lakehouses-at-scale-with-rubrik-on-aws/
- **Published:** 2026-11-16

Apache Iceberg is now a standard open table format for AWS lakehouses, and because that
data feeds AI pipelines and financial reporting, it needs stronger protection.
Recovering a working table takes more than restoring files, because it depends on
consistent metadata, manifests and catalog. Rubrik's new Apache Iceberg Data Protection
on AWS backs up the full table to the customer's AWS account or Rubrik Cloud Vault, then
updates the catalog on recovery so the table is immediately queryable. The post explains
why native time travel alone falls short and how Rubrik and AWS bring enterprise cyber
resilience to the lakehouse.

### 13. Amazon ECR now replicates image deletions across regions and accounts

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/replication-deletes-amazon-ecr
- **Published:** 2026-11-16

Amazon Elastic Container Registry (Amazon ECR) now supports replicating image deletions
and tag removals to your replication destinations. Previously, ECR replication copied
images to destination regions and accounts but did not replicate deletions, requiring
you to manage deletions separately in each location. With replication of deletes, your
destination repositories stay consistent with the source automatically. Teams running
multi-region or multi-account architectures no longer need to script or manually track
image cleanup across every destination. When you delete an image or remove a tag in your
source registry, whether directly or through a lifecycle policy, ECR propagates that
deletion to each destination in the replication rule. Replicated deletions emit
EventBridge events and are recorded in CloudTrail, so you have the same visibility into
deletions as you do for image pushes. Replication of deletes is available in all AWS
Regions where Amazon ECR is available, at no additional cost. To get started, update
your replication configuration in the Amazon ECR console or AWS CLI. For more
information, see the Amazon ECR User Guide .

### 14. How Duco transforms financial data automation with Amazon Bedrock AgentCore

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/how-duco-transforms-financial-data-automation-with-amazon-bedrock-agentcore/
- **Published:** 2026-11-16

Duco, a data automation platform for tier-one banks, rebuilt its agentic AI stack on
Amazon Bedrock and Amazon Bedrock AgentCore. With strict per-tenant isolation, a multi-
model strategy, and an MCP skills architecture that cut context overhead by 90%, Duco
cut reconciliation deployment time 10x and onboarding costs 70%.

### 15. Amazon EBS now supports associating additional KMS keys with snapshots

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/ebs-snapshots-associate-kms-keys/
- **Published:** 2026-11-16

Amazon Elastic Block Store (EBS) now supports associating additional AWS Key Management
Service (KMS) keys with EBS snapshots. This new capability enables you to share and copy
encrypted snapshots across accounts without first re-encrypting them, simplifying your
disaster recovery and backup workflows. Customers use EBS snapshots as durable, point-
in-time backups of EBS volumes. By associating an additional customer-managed KMS key
(CMK) with a snapshot encrypted with an AWS managed key (AMK), for example, you enable
cross-account sharing for that snapshot without re-encrypting its data. This feature
accelerates your disaster recovery workflows and enhances operational efficiency for
enterprise backup administrators and disaster recovery teams. Support for associating
additional KMS keys with Amazon EBS snapshots is available in all AWS commercial, China,
AWS GovCloud (US), and AWS European Sovereign Cloud (Germany) Regions, plus AWS Local
Zones and AWS Outposts. You can access this capability through the AWS Console, AWS
Command Line Interface (CLI), and AWS SDKs. To learn more, see the Amazon EBS
documentation .

### 16. Taxonomy of multi-agent design patterns, anti-patterns, and lessons from manufacturing

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/taxonomy-of-multi-agent-design-patterns-anti-patterns-and-lessons-from-manufacturing/
- **Published:** 2026-11-16

Multi-agent coordination is a distributed systems problem, not a model problem. This
post gives a field-tested taxonomy of multi-agent design patterns and anti-patterns, a
framework for deciding when multiple agents are warranted, and how to build cost-
efficient, reliable systems on AWS.

### 17. NVIDIA Vera Rubin NVL72 Achieves up to 2x Blackwell Ultra Performance in MLPerf Training v6.1

- **Publisher:** NVIDIA (`nvidia-developer-blog`)
- **URL:** https://developer.nvidia.com/blog/nvidia-vera-rubin-nvl72-achieves-up-to-2x-blackwell-ultra-performance-in-mlperf-training-v6-1/
- **Published:** 2026-11-16

As AI agents tackle increasingly complex workflows, reducing time-to-train is critical
for rapidly iterating on both models and the agents they power. MLPerf...

### 18. How to make four specialist AI agents act as one trusted financial advisor

- **Publisher:** AWS (`aws-industries-blog`)
- **URL:** https://aws.amazon.com/blogs/industries/how-to-make-four-specialist-ai-agents-act-as-one-trusted-financial-advisor/
- **Published:** 2026-11-16

When you split a banking assistant into specialist AI agents on separate runtimes, they
lose their shared state. This post shows architects how we built the Connected Finance
demo on Amazon Bedrock AgentCore: carrying shared context across runtimes, discovering
specialists at runtime, and applying one set of guardrails to voice and text.

### 19. Amazon S3 Vectors now supports hybrid search combining vector and full text for more relevant search results

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/s3-vectors-hybrid-search/
- **Published:** 2026-11-16

Amazon S3 Vectors now supports hybrid search that combines vector similarity search with
full-text search within a single query.&nbsp;By combining semantic meaning and exact
term matching into a single ranked list of results, hybrid search captures both intent
and precise terms for retrieval-augmented generation (RAG), agent memory, and search
applications. This can deliver more relevant ranked results than either method alone.
Hybrid search works with the same S3 Vectors APIs and maintains subsecond latency for
infrequent queries and latency around 100 milliseconds or less for frequent queries. S3
Vectors is designed to provide the same elasticity, durability, and availability as
Amazon S3, and it reduces the total costs of storing and querying vectors by up to 90%
compared to alternative vector solutions. With hybrid search, customers can now store
the data that they want to make full-text searchable alongside the vectors. Customers
write data with the PutVectors API as they do today and include the searchable text as
another metadata field. S3 Vectors then automatically indexes that field for full-text
search with BM25 relevance scoring. By default, S3 Vectors uses a language-agnostic text
analyzer to index this data which works across most languages, and customers can
optionally select a language-specific analyzer for more accurate language-aware
matching. To perform a hybrid query, customers send their query text strings alongside
their query vector in a single QueryVectors call; S3 Vectors runs both a vector search
and a full-text search, fuses the two with Reciprocal Rank Fusion (RRF), and returns a
single ranked list of the top K requested results. Customers can also run full-text and
vector queries separately to apply own ranking logic, search across multiple text fields
in a single query, and enable full-text search on existing data in place. Hybrid search
is available today in all commercial AWS Regions where Amazon S3 Vectors is available,
and in the AWS China Regions. To get started, use the AWS CLI, AWS SDKs, or the Amazon
S3 console. To learn more, visit the Amazon S3 Vectors documentation , and the Amazon S3
pricing page for pricing.

### 20. WorkSpaces for AI Agents now available on WorkSpaces Applications image builders

- **Publisher:** AWS (`aws-desktop-app-streaming-blog`)
- **URL:** https://aws.amazon.com/blogs/desktop-and-application-streaming/workspaces-for-ai-agents-now-available-on-workspaces-applications-image-builders/
- **Published:** 2026-11-16

Building an AI agent that operates desktop applications includes testing it against your
specific applications and desktop configurations. Often, the first goal is a pilot that
proves the agent can run your business workload, and you want to reach that point
quickly. Starting today, WorkSpaces for AI Agents is available on WorkSpaces
Applications image builders. […]

### 21. How Singapore’s National Precision Medicine program runs population-scale SV discovery on AWS HealthOmics

- **Publisher:** AWS (`aws-public-sector-blog`)
- **URL:** https://aws.amazon.com/blogs/publicsector/how-singapores-national-precision-medicine-program-runs-population-scale-sv-discovery-on-aws-healthomics/
- **Published:** 2026-11-16

Singapore's National Precision Medicine program and the SG100K consortium built a
population-scale structural variant catalog from more than 100,000 genomes using GATK-
SV. The A*STAR-PRECISE team ran that community-standard pipeline on AWS HealthOmics,
with results confirmed functionally equivalent to the Broad Institute reference
implementation.

### 22. Deliver petabytes of Apache Kafka data to Amazon S3 at up to 60% lower cost with Amazon MSK Express brokers

- **Publisher:** AWS (`aws-big-data-blog`)
- **URL:** https://aws.amazon.com/blogs/big-data/deliver-petabytes-of-apache-kafka-data-to-amazon-s3-at-up-to-60-lower-cost-with-amazon-msk-express-brokers/
- **Published:** 2026-11-16

Amazon MSK Express brokers now deliver Apache Kafka topic data to Amazon S3 at up to 60%
lower cost, with no Kafka Connect to run. You create a channel on a topic and pay only
for the data delivered. In this post, we cover the two challenges of delivering Kafka
data to Amazon S3 today and how Express brokers and data delivery to Amazon S3 address
each one.

### 23. How Salesforce efficiently right-sizes Kubernetes workloads at scale on Amazon EKS

- **Publisher:** AWS (`aws-containers-blog`)
- **URL:** https://aws.amazon.com/blogs/containers/how-salesforce-efficiently-right-sizes-kubernetes-workloads-at-scale-on-amazon-eks/
- **Published:** 2026-11-16

Salesforce operates one of the largest multi-tenant Kubernetes platforms on Amazon EKS,
spanning 1,400+ clusters. See how its team combined the Vertical Pod Autoscaler and
Horizontal Pod Autoscaler into a multi-dimensional autoscaling strategy that right-sizes
workloads at scale and drove more than $5 million in infrastructure savings.

### 24. Amazon Redshift now supports multi-statement transactions, conflict resolution, and time travel for Apache Iceberg

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/redshift-time-travel-multi-statement
- **Published:** 2026-11-16

Amazon Redshift now supports multi-statement transactions, automatic write-conflict
resolution, and time travel for Apache Iceberg tables. You can run multi-step,
concurrent transformation pipelines directly on Iceberg tables and audit the results,
with the transaction semantics you expect from a data warehouse. This helps anyone
writing to Iceberg tables at production scale. Batch jobs get all-or-nothing commits
across multiple steps. Streaming and scheduled jobs can write to the same tables at the
same time. Analysts, auditors, and AI agents can query a table as it existed at any
point in time. With multi-statement transactions, you group several statements in a
single BEGIN…COMMIT statement and publish them as one atomic Iceberg snapshot. This
means a multi-step load such as a MERGE followed by a DELETE, can be commited together
as one atomic operation, are never queryable in a half-applied state, and roll back
cleanly if there's a failure. Automatic conflict resolution lets concurrent writes, such
as streaming inserts alongside scheduled deletes, write to the same table and commit
together when their changes don't overlap, instead of failing and retrying. Time travel
lets you query a table as it existed at a past point in time with AS OF TIMESTAMP. You
can use it to reproduce reports, audit changes, or recover from a bad write without
keeping extra copies. These capabilities are available in all AWS commercial Regions for
Amazon Redshift’s provisioned RG or serverless clusters that are writing to or querying
Iceberg tables.. To get started, see the following list of resources: 1/ Resolving
concurrent writes for Apache Iceberg tables using Amazon Redshift 2/ Multi-statement
transactions for Apache Iceberg tables in Amazon Redshift 3/ Time travel support for
Apache Iceberg&nbsp;

### 25. How British Airways is accelerating the modernization of its Java services

- **Publisher:** AWS (`aws-devops-blog`)
- **URL:** https://aws.amazon.com/blogs/devops/how-british-airways-is-accelerating-the-modernization-of-its-java-services/
- **Published:** 2026-11-16

Learn how British Airways is using AWS Transform custom, agentic AI, and automation to
accelerate the modernization of its Java services, migrating more than 250 business
services from Amazon EC2 to a containerized, auto scaling architecture on Amazon ECS
with AWS Fargate and AWS Graviton.

### 26. Migrate Apache Solr to Amazon OpenSearch Service with the AI-driven Migration Assistant

- **Publisher:** AWS (`aws-big-data-blog`)
- **URL:** https://aws.amazon.com/blogs/big-data/migrate-apache-solr-to-amazon-opensearch-service-with-the-ai-driven-migration-assistant/
- **Published:** 2026-11-16

Migrate a 600,000-document Apache Solr catalog to Amazon OpenSearch Serverless end to
end using the AI-driven agent mode in the Migration Assistant for Amazon OpenSearch
Service, from assessment through validated backfill.

### 27. Introducing 1:1 NAT on AWS Transit Gateway and AWS Cloud WAN

- **Publisher:** AWS (`aws-networking-blog`)
- **URL:** https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-11-nat-on-aws-transit-gateway-and-aws-cloud-wan/
- **Published:** 2026-11-16

Overlapping IP addresses keep networks from connecting. With 1:1 NAT on AWS Transit
Gateway and AWS Cloud WAN, each network gets a unique range through native Regional
Private NAT Gateway integration, so you don't renumber networks or deploy a separate NAT
solution.

### 28. Analyze Anthropic usage, spend, and access with AWS Glue, Amazon S3 Tables, and AWS Quick

- **Publisher:** AWS (`aws-big-data-blog`)
- **URL:** https://aws.amazon.com/blogs/big-data/analyze-anthropic-usage-spend-and-access-with-aws-glue-amazon-s3-tables-and-aws-quick/
- **Published:** 2026-11-16

The new AWS Glue connector for Anthropic reads Claude usage, cost, and API key data into
AWS without custom code. This post shows how to land it in Amazon S3 Tables as Apache
Iceberg tables, join it with your business data, query it with Amazon Athena, and
visualize AI spend and governance in AWS Quick.

### 29. Building a unidirectional edge layer for third-party connectivity on AWS with Amazon VPC Lattice

- **Publisher:** AWS (`aws-networking-blog`)
- **URL:** https://aws.amazon.com/blogs/networking-and-content-delivery/building-a-unidirectional-edge-layer-for-third-party-connectivity-on-aws-with-amazon-vpc-lattice/
- **Published:** 2026-11-16

Building a unidirectional edge layer for third-party connectivity removes a common
trade-off. Enterprises need bidirectional service exchange with partners, vendors, and
external platforms, without bidirectional network connectivity that broadens exposure.
With Amazon VPC Lattice and AWS PrivateLink, you can exchange services for both ingress
and egress, without creating a routed network path. The traditional options […]

### 30. Announcing updates to the AWS Well-Architected Framework

- **Publisher:** AWS (`aws-architecture-blog`)
- **URL:** https://aws.amazon.com/blogs/architecture/announcing-updates-to-the-aws-well-architected-framework-3/
- **Published:** 2026-11-16

Updates to the AWS Well-Architected Framework reorganize it into Well-Architected Cloud
Foundations and Well-Architected Cloud Workloads, add new best practices, and bring the
general availability of the AWS Well-Architected Agent for analyzing workloads and
guiding remediation.

### 31. AWS DevOps Agent is now available in AWS GovCloud (US-West)

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/aws-devops-agent-govcloud-west/
- **Published:** 2026-11-16

Now available in AWS GovCloud (US-West), AWS DevOps Agent is your always-available
operations teammate that resolves and proactively prevents incidents, optimizes
application reliability and performance, and handles on-demand SRE tasks across AWS,
multicloud, and on-prem environments. DevOps Agent investigates incidents and identifies
operational improvements as an experienced teammate would: by learning your applications
and their relationships, working with your observability tools, runbooks, code
repositories, and CI/CD pipelines, and correlating telemetry, code, and deployment data.
It autonomously triages incidents and guides teams to rapid resolution, reducing mean
time to resolution (MTTR) from hours to minutes, while analyzing patterns across
historical incidents to deliver actionable recommendations that prevent future outages.
For the full list of AWS Regions where AWS DevOps Agent is available, visit the Regions
list. Pricing details are available on the AWS DevOps Agent pricing page . AWS Support
customers receive monthly DevOps Agent credits based on the prior month's AWS Support
charge: 100% for Unified Operations, 75% for Enterprise Support, or 30% for Business
Support+. For many customers, this significantly reduces or eliminates DevOps Agent
costs. For details, visit the support compare page . To learn more, read the launch blog
and see getting started .

### 32. Exploring new features of Apache TinkerPop 3.8.x in Amazon Neptune

- **Publisher:** AWS (`aws-database-blog`)
- **URL:** https://aws.amazon.com/blogs/database/exploring-new-features-of-apache-tinkerpop-3-8-x-in-amazon-neptune/
- **Published:** 2026-11-16

Upgrading to Apache TinkerPop 3.8.x in Amazon Neptune 1.5.0.0 brings cleaner, more
predictable Gremlin and a major expansion of Data Flow Engine (DFE) coverage, along with
semantic changes that need review. Learn what changed, which query patterns are
affected, and how to prepare for the upgrade.

### 33. Introducing AWS Backup logically air-gapped vault support for Amazon RDS

- **Publisher:** AWS (`aws-storage-blog`)
- **URL:** https://aws.amazon.com/blogs/storage/introducing-aws-backup-logically-air-gapped-vault-support-for-amazon-rds/
- **Published:** 2026-11-16

AWS Backup now extends logically air-gapped vault support to Amazon RDS. Learn how to
protect, validate, and recover your RDS database backups with isolated, immutable
vaults, along with the design, encryption, and cost considerations for a cyber recovery
strategy that keeps backups recoverable even when your production account can't be
trusted.

### 34. Amazon Connect Health medical coding is now available in public preview

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-connect-health-medical-coding/
- **Published:** 2026-11-16

Today, AWS announces the public preview of medical coding in Amazon Connect Health , a
HIPAA-eligible AI service that works alongside healthcare teams across patient
engagement and point-of-care workflows. Medical coding uses existing clinical
documentation to suggest ICD-10-CM and CPT codes, including E&amp;M levels and
modifiers, for a provider or coder to review and approve before submission. You can
integrate medical coding into your EHR or billing application through the Amazon Connect
Health SDK, or use it with Amazon Connect Health ambient documentation. Each code links
to the evidence that supports it and carries a confidence score, so reviewers can
confirm a code before a claim goes out. In this public preview, you can choose to upload
your organization's previously coded encounters, and the service builds a coding
reference set specific to your organization. The corrections coders make feed that
reference set and improve future coding suggestions. Medical coding is available in
public preview in the US East (N. Virginia) and US West (Oregon) AWS Regions.&nbsp;To
learn more, see medical coding in the Amazon Connect Health user guide.&nbsp;

### 35. Amazon Connect Customer agent assist now supports interactive responses

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/Connect-Custom-agent-interactive-responses
- **Published:** 2026-11-16

Amazon Connect Customer agent assist now supports interactive components, including
cards, carousels, buttons, and input fields. The AI agent analyzes conversation context
in real time, recommends actions, retrieves information, and executes tasks on behalf of
contact center agents using MCP tools in Connect Customer or third-party services.
Interactive responses let agents review information, provide details, select options,
and confirm actions without manually typing a separate request for each action. The AI
agent can also recommend step-by-step guides, cases, customer profiles, and third-party
applications that agents can open with one click. For example, when a customer calls to
dispute a charge, the AI agent can dynamically generate an interactive list of the
customer’s recent transactions. The agent can select the disputed transaction, provide
or confirm the required details, and approve the action. The AI agent can then use a
connected tool to create the dispute request and display confirmation in the agent
workspace. This feature is available in all AWS Regions where Amazon Connect Customer
agent assist is available. To learn more and get started, see Agent Assist in the Amazon
Connect Administrator Guide.&nbsp;

### 36. Why we rebuilt LangSmith around the agent

- **Publisher:** LangChain (`langchain-blog`)
- **URL:** https://www.langchain.com/blog/we-rebuilt-langsmith-around-the-agent
- **Published:** 2026-11-16

We reorganized LangSmith around a single agent record. Build, run, improve, and govern
every agent from one place, on any framework or runtime.

### 37. Clean data was never enough: How IFS Copperleaf taught AI its business with Databricks Genie One

- **Publisher:** Databricks (`databricks-blog`)
- **URL:** https://www.databricks.com/blog/clean-data-was-never-enough-how-ifs-copperleaf-taught-ai-its-business-databricks-genie-one-0
- **Published:** 2026-11-16

IFS Copperleaf is a leading global provider of Asset Investment Planning (AIP)
software...

### 38. Talk to your clinical data: unlocking AWS HealthLake with OpenSharing and Genie One

- **Publisher:** Databricks (`databricks-blog`)
- **URL:** https://www.databricks.com/blog/talk-your-clinical-data-unlocking-aws-healthlake-opensharing-and-genie-one
- **Published:** 2026-11-16

Many healthcare and life sciences organizations have standardized on AWS HealthLake to
manage clinical data...

### 39. AWS Marketplace in Singapore: SGD support, local invoicing, and GST compliance

- **Publisher:** AWS (`aws-marketplace-blog`)
- **URL:** https://aws.amazon.com/blogs/awsmarketplace/aws-marketplace-in-singapore-sgd-support-local-invoicing-and-gst-compliance/
- **Published:** 2026-11-16

In this post, we cover how AWS Marketplace in Singapore works, what it means for buyers
and sellers, and how to get started.

### 40. Introducing enhanced snapshots for Amazon Managed Service for Apache Flink

- **Publisher:** AWS (`aws-big-data-blog`)
- **URL:** https://aws.amazon.com/blogs/big-data/introducing-enhanced-snapshots-for-amazon-managed-service-for-apache-flink/
- **Published:** 2026-11-16

Enhanced snapshots for Amazon Managed Service for Apache Flink are now generally
available. An enhanced snapshot is an AWS resource with its own ARN, decoupled from the
application that created it, so you can start another application from it, export it to
Amazon S3, and import savepoints for blue/green deployments, disaster recovery, and
migrations.

### 41. How MoEngage built agentic customer engagement on Amazon Bedrock AgentCore

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/how-moengage-built-agentic-customer-engagement-on-amazon-bedrock-agentcore/
- **Published:** 2026-11-16

MoEngage built Merlin AI, a set of AI agents on Amazon Bedrock and Amazon Bedrock
AgentCore that let marketing and product teams draft, analyze, and adjust campaigns from
a single conversation. Learn how MoEngage turned its existing APIs into MCP tools and
kept each tenant's data isolated while giving agents secure access to live platform
data.

### 42. JA Canada launches generative AI with Qalius and Amazon Bedrock

- **Publisher:** AWS (`aws-apn-blog`)
- **URL:** https://aws.amazon.com/blogs/apn/ja-canada-launches-generative-ai-with-qalius-and-amazon-bedrock/
- **Published:** 2026-11-16

JA Canada worked with Qalius Consulting Inc., a Canadian AWS Advanced Tier Services
Partner, to move a generative AI project from design to deployment in just four months.
The project focused on one clear use case: helping visitors find information across JA
Canada resources through a conversational experience. This post shares four key
ingredients for generative AI success: bounding the first use case, building in
evaluation, treating safeguards and cost controls as launch requirements, and using
managed AWS capabilities to reduce unnecessary engineering work.

### 43. AWS KMS now supports key sharing with AWS Resource Access Manager

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/kms-key-sharing-resource-access-manager/
- **Published:** 2026-11-16

AWS Key Management Service (KMS) now integrates with AWS Resource Access Manager (RAM),
giving you a simpler and more consistent way to share KMS keys across your AWS accounts,
within your organization in AWS Organizations, and with specific IAM roles and users.
You can now let trusted parties define the access they need through reusable managed
permissions in RAM, while keeping full control of your keys and key policies. To share a
key, create a resource share by selecting the keys to share, choosing a managed
permission, and specifying the principals. You can use AWS managed permissions for
common scenarios, or customer managed permissions (CMPs) authored by you or by trusted
parties such as SaaS providers and central security teams. Sharing KMS keys through RAM
makes enabling cross-account access faster to set up and safer to maintain. The trusted
parties who need access to your keys can publish the policy once as a CMP, without the
need for you to modify the key policies by hand. You simply fill in the values that
scope it to your environment and attach it to the resource share. Your existing key
policy is untouched, so you are always in control of your key as your environment grows.
When a new policy version is available via an updated CMP, you decide when to apply it
to your resource shares. This enhancement is built on new AWS RAM capabilities that are
available for every resource type RAM supports. CMPs now support multiple policy
statements and additional IAM condition operators, including StringNotEquals,
BoolIfExists, and ArnLike, along with the ForAnyValue and ForAllValues prefixes, so you
can express precise, least-privilege access. The&nbsp;parameterized managed permissions
lets you place a temporary placeholder in CMPs that allows each resource share owner to
customize and scope down CMPs to their environment, enabling CMPs to be reused and serve
many accounts. CMPs can now be published and shared across accounts, so the authors can
maintain one permission, manage its versions centrally, and see every resource share
that uses it, while other accounts can use it directly without keeping their own copy.
KMS key sharing with RAM is available in all AWS Regions where both services are
available, except the Middle East (UAE) and Middle East (Bahrain).&nbsp;For more
information, see Sharing KMS keys with AWS RAM in the AWS KMS Developer Guide and
Working with shared AWS resources in the AWS RAM Developer Guide.

### 44. Set up, connect, and govern AI agents faster with Amazon WorkSpaces

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-workspaces-AI-agents-connect-govern
- **Published:** 2026-11-16

Building AI agents has become essential. Across your organization, teams want agents to
handle ERP transactions, work through a claims queue, and operate the same applications
your people use every day. But how do you move from experiments to production? Before an
agent touches real systems and real data, you need to verify who it acted on behalf of,
what it did, and whether it stayed within the limits you set. Without that visibility,
the agent stays stuck in testing, and the value is never realized. Earlier this year, we
launched Amazon WorkSpaces for AI agents , extending the power and security of a cloud
work environment to agents, not just people. Today, we're excited to announce new
capabilities that make it even easier to operate agents confidently across your
enterprise and move them from proof of concept to governed production in fewer
steps.&nbsp; You can set up new agents or connect the ones your builders have already
built, run them under your own identity providers and policies, and keep a record of
everything they do. You don't need to stitch together new tools or build custom
monitoring. Setup used to mean configuring the machine by hand. Now, you can just
describe what your agent needs to your AI coding assistant such as Claude Code, Codex,
and Kiro. Guided by AWS MCP skills, the assistant builds the WorkSpace from defaults you
can adjust. If your teams build on Amazon Bedrock AgentCore, you can connect an agent
directly with your AWS credentials and skip writing any agent code. New tools also
reduce agent costs and increase accuracy by letting an agent carry out a series of
actions in a single call and use the computer-use actions its model already knows. But
an agent that can work is not necessarily an agent you can trust with mission-critical
work and sensitive data. This release gives you the same oversight over an agent that
you have over the employees you manage. First, agents can now sign in through any
identity provider (IdP) that supports OIDC, in addition to the existing SAML support.
Administrators can send sign-in straight to their IdP, so users authenticate with their
usual corporate credentials, and you don't build custom authentication. Second, with on-
behalf-of (OBO) sign-in, an agent works as the signed-in user, with that user's existing
directory identity, permissions, and Group Policies on the desktop.&nbsp; WorkSpaces now
offers session replay, giving you a reviewable record of what your agent did. Session
replay turns session screenshots into a video and pairs it with a plain-language
transcript of the agent's actions. Both are stored in your own Amazon S3 bucket and
encrypted with your own keys. Your security team can see what the agent saw, and your
compliance team gets evidence to support audits. Together, these updates help move
agents out of pilots and into real production scale. Your teams can keep working the way
they do today, with agents working alongside them in familiar and trusted cloud work
environments. And every one of those agents is held to the same identity, policy, and
audit standards as the rest of your workforce. With WorkSpaces, you can bring AI agents
into your business without rebuilding decades of software or needing a separate
environment to govern them. To get started operating AI agents on WorkSpaces, visit our
documentation page .&nbsp;

### 45. AWS Weekly Roundup: AWS Nitro Sandboxes, AWS Emulator, and more (November 16, 2026)

- **Publisher:** AWS (`aws-main-blog`)
- **URL:** https://aws.amazon.com/blogs/aws/aws-weekly-roundup-aws-nitro-sandboxes-aws-emulator-and-more-november-16-2026/
- **Published:** 2026-11-16

A second delivery of the same message can reveal more about an application than its
happy-path demo. I like tools that make those cases easier to investigate while a change
is still small. Last week’s launch of AWS Emulator brings part of that work onto your
own machine: developers and coding agents can exercise AWS […]

### 46. AWS Marketplace Metering Service now supports decimal usage quantities

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/aws-marketplace-metering-service-decimal-usage-quantities/
- **Published:** 2026-11-16

AWS Marketplace Metering Service now supports decimal usage quantities in the MeterUsage
and BatchMeterUsage APIs. Previously, AWS Marketplace sellers reported usage to both
APIs in whole numbers, and now they can report usage with up to six decimal places.
Sellers can price and meter in the units that match how customers consume their product,
for example reporting 1.5 terabytes (TB) of storage instead of 1 or 2 TB. To report
decimal quantities, sellers use the new UsageQuantityAsDecimal parameter in MeterUsage
and QuantityAsDecimal parameter in BatchMeterUsage, and existing integrations that
report whole numbers continue to work without changes. Usage allocations, which split
reported usage into buckets by tags, also support decimal quantities with the new
AllocatedUsageQuantityAsDecimal parameter. This new feature is available in all AWS
Regions where AWS Marketplace Metering Service is available. To learn more, see
MeterUsage and BatchMeterUsage in the AWS Marketplace API Reference.

### 47. A governed AI-driven development lifecycle for financial services with Kiro and AWS Frontier Agents

- **Publisher:** AWS (`aws-devops-blog`)
- **URL:** https://aws.amazon.com/blogs/devops/a-governed-ai-driven-development-lifecycle-for-financial-services-with-kiro-and-aws-frontier-agents/
- **Published:** 2026-11-16

A hands-on walkthrough of a governed, AI-driven development lifecycle for financial
services that wires Kiro, AWS Security Agent, and AWS DevOps Agent into a shared GitHub-
based pipeline, so every change is authored, reviewed, security-gated, deployed to AWS
Lambda, and monitored in production with human approval and traceable evidence.

### 48. Build a real-time next-best-offer recommender using Databricks Feature Views

- **Publisher:** Databricks (`databricks-blog`)
- **URL:** https://www.databricks.com/blog/build-real-time-next-best-offer-recommender-using-databricks-feature-views
- **Published:** 2026-11-16

Real-time personalization depends on understanding what customers want in the moment...

### 49. Modernizing mainframe Assembler to Java using Amazon Bedrock and AWS Transform

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/modernizing-mainframe-assembler-to-java-using-amazon-bedrock-and-aws-transform/
- **Published:** 2026-11-16

Legacy mainframe Assembler applications are costly to maintain and hard to staff. This
post presents a multi-stage, AI-powered methodology using Amazon Bedrock, Kiro IDE, and
AWS Transform to extract business rules, convert Assembler through an intermediate COBOL
stage, and deploy modernized Java Spring Boot applications on AWS.

### 50. Upgrading and troubleshooting Amazon MWAA with AWS agent skills

- **Publisher:** AWS (`aws-big-data-blog`)
- **URL:** https://aws.amazon.com/blogs/big-data/upgrading-and-troubleshooting-amazon-mwaa-with-aws-agent-skills/
- **Published:** 2026-11-16

AWS publishes MWAA agent skills in the open source AWS agent toolkit: procedures your AI
coding assistant can run to upgrade Amazon MWAA from Airflow 2.x to 3.x and troubleshoot
failures, with a safety confirmation on every environment change.

### 51. Novo Nordisk modernizes manufacturing process documents with Amazon Bedrock AgentCore

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/novo-nordisk-modernizes-manufacturing-process-documents-with-amazon-bedrock-agentcore/
- **Published:** 2026-11-16

Novo Nordisk's Manufacturing Technology team within the Tablet area team built a
process-intelligence assistant on Amazon Bedrock AgentCore, using a GraphRAG
architecture that pairs a knowledge graph in Amazon Neptune with hybrid search in Amazon
OpenSearch Serverless to turn millions of controlled manufacturing documents into
grounded, cited answers.

### 52. Best practices for deploying Amazon CloudWatch Omni at enterprise scale

- **Publisher:** AWS (`aws-management-blog`)
- **URL:** https://aws.amazon.com/blogs/mt/best-practices-for-deploying-amazon-cloudwatch-omni-at-enterprise-scale/
- **Published:** 2026-11-16

At enterprise scale, organizations run applications and AI agents side by side across
hundreds of AWS accounts, several Regions, and often other clouds and on-premises data
centers. Site reliability engineering (SRE) teams watch service latency, agent
developers observe agent traces and evaluation scores, operation teams monitor alerts,
and security reviews AWS API activity. When a […]

### 53. Broadening access to AI for scientists

- **Publisher:** OpenAI (`openai-blog`)
- **URL:** https://openai.com/index/expanding-chatgpt-for-academic-researchers
- **Published:** 2026-11-16

We’re expanding our ChatGPT for Academic Researchers program to offer 200,000
researchers worldwide free access to our frontier models.

### 54. Strengthening the fight against online child sexual abuse with new tools and support

- **Publisher:** OpenAI (`openai-blog`)
- **URL:** https://openai.com/index/strengthening-online-child-safety
- **Published:** 2026-11-16

New tools, practical guidance, and partnerships will help prevent, detect and respond to
online child sexual exploitation and abuse.

### 55. Beyond the compute bottleneck: Maximizing the ROI of AI accelerators with purpose-built storage

- **Publisher:** Google Cloud (`google-cloud-blog`)
- **URL:** https://cloud.google.com/blog/products/storage-data-transfer/maximizing-ai-accelerator-roi-with-purpose-built-storage/
- **Published:** 2026-11-16

There’s a lot more to AI infrastructure than just buying accelerators. Indeed, the
infrastructure mandate for enterprise AI has shifted from acquiring accelerators to
keeping them fully utilized. Next to these expensive accelerators, storage accounts for
only a small sliver of total AI spend. However, having the wrong storage in place can
put the rest of your committed compute capital at risk. To optimize your accelerators’
TCO, you need to keep them fully occupied. Very often, the challenge here is data I/O.
If accelerators sit waiting to read or write data, you’re wasting money. Across the
industry, insufficient storage throughput has become a primary impediment to AI success,
starving models of the data they need. And the problem is only going to get worse.
Gartner predicts enterprises will deploy over 150,000 agents in the next few years, so
the I/O bottleneck and the challenge of orchestrating storage for agentic fleets will
only compound. Organizations are eager to move their AI initiatives forward, but
preventing idle compute requires a purpose-built approach to data I/O. With the demands
of AI, standard enterprise storage — even a system optimized for fast analytics — will
inevitably suffer from bottlenecks that leave compute resources twiddling their
proverbial thumbs. AI is not a monolithic workload The most common architectural misstep
we see is treating AI as a single, general-purpose workload. In reality, the physical
movement of data transforms across the AI lifecycle, creating distinct I/O profiles
based on how models consume and generate information: In model training , clusters read
datasets at high throughput, but pause regularly to write checkpoints to record their
state in event of a failure. When thousands of GPUs attempt to save this data in a
single, simultaneous burst, standard storage architectures stall. That’s especially true
of traditional cloud storage, which is engineered for durability. Writing checkpoints
triggers thousands of administrative database transactions to safely record the files,
bogging down the system, choking the network, and freezing the entire GPU cluster until
the save is complete. Furthermore, saving the data is only one of the problems: If a
server fails, slow storage turns a routine checkpoint recovery into a multi-hour delay,
leaving expensive accelerators sitting completely idle. Inference , conversely, is real-
time and latency-sensitive. As AI services scale to meet user demand, inference clusters
constantly load and unload petabyte-scale model repositories quickly. In this case, a
slow storage system can leave GPUs in a “cold start” as they wait for data. Also, many
models now process context windows that exceed 100,000 tokens, filling up accelerator
memory. Without a high-speed external cache to offload this context, when a user asks
the next question, the accelerator must recalculate previous inputs, wasting compute on
redundant operations. Industry-leading performance across object and file storage To
solve these I/O challenges and keep expensive accelerators busy, organizations need
compute, networking, and storage to be deeply integrated. As industry analysts have
noted, enterprise customers gain a unique performance advantage because Google Cloud
runs on the exact same storage foundation as Google's own consumer products. This
foundation is built on Colossus—the planet-scale distributed file system powering Google
Search, YouTube, and Gemini. Because this shared infrastructure supports billions of
users daily, its reliability is continuously proven against the extreme traffic and
hardware demands of Google's global consumer services. As a result, today, nine out of
the world’s ten leading AI frontier model labs run on Google Cloud infrastructure
because we deliver the throughput and performance they require to innovate. In fact, we
spent the last two years co-designing our storage architecture directly with these
frontier labs as well as with Google's own foundation

### 56. Introducing the Databricks AI Index: The state of enterprise AI tokenomics

- **Publisher:** Databricks (`databricks-blog`)
- **URL:** https://www.databricks.com/blog/introducing-databricks-ai-index-state-enterprise-ai-tokenomics
- **Published:** 2026-11-16

Developers have more AI models and coding agents to choose from than ever before....

### 57. Tabular foundation models on Databricks AI Runtime

- **Publisher:** Databricks (`databricks-blog`)
- **URL:** https://www.databricks.com/blog/tabular-foundation-models-databricks-ai-runtime
- **Published:** 2026-11-16

Many of the most valuable predictive machine learning applications rely on tabular
data...

### 58. Teach Genie One your workflows: The ultimate guide for skills in Genie One

- **Publisher:** Databricks (`databricks-blog`)
- **URL:** https://www.databricks.com/blog/teach-genie-one-your-workflows-ultimate-guide-skills-genie-one
- **Published:** 2026-11-16

Every team has “recipes” that govern how they work. The way finance puts together...

### 59. Running AV Reasoning Models Within Onboard Compute and Latency Limits

- **Publisher:** NVIDIA (`nvidia-developer-blog`)
- **URL:** https://developer.nvidia.com/blog/running-av-reasoning-models-within-onboard-compute-and-latency-limits/
- **Published:** 2026-11-16

Autonomous vehicle (AV) developers need reasoning models that can operate within the
compute and latency constraints of an onboard system. Larger models provide...

### 60. Get answers from tables with tabular search in Amazon Bedrock Managed Knowledge Base

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/get-answers-from-tables-with-tabular-search-in-amazon-bedrock-managed-knowledge-base/
- **Published:** 2026-11-16

Amazon Bedrock Managed Knowledge Base now supports tabular search, so agentic retrieval
can answer questions over CSV, XLSX, and XLS files. It looks up values and runs
calculations across every relevant row, then combines the results with facts from
related documents to answer multi-step analytical questions.

### 61. PHP2Shell: Using AWS Transform to move legacy PHP onto a patched runtime

- **Publisher:** AWS (`aws-devops-blog`)
- **URL:** https://aws.amazon.com/blogs/devops/php2shell-using-aws-transform-to-move-legacy-php-onto-a-patched-runtime/
- **Published:** 2026-11-16

Teams on PHP 8.1 or older can't patch the PHP2Shell vulnerabilities (CVE-2026-109618 and
CVE-2026-109619) in place. Learn how to use AWS Transform continuous modernization to
find legacy PHP, upgrade it to PHP 8.4 or 8.5, validate it on a patched runtime, and
then patch and restart the runtime to remediate the CVEs.

### 62. Best practices for writing Denied Topics in Amazon Bedrock Guardrails

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/best-practices-for-writing-denied-topics-in-amazon-bedrock-guardrails/
- **Published:** 2026-11-16

With Denied Topics in Amazon Bedrock Guardrails, you block a content category by
describing it in plain language, and the guardrail matches by meaning rather than
keyword, which can block more than you intend. This post presents eight best practices
for writing a topic precisely enough that the guardrail blocks what you mean and passes
what you don't.

### 63. Customize answers per tenant in Amazon Bedrock Managed Knowledge Base

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/customize-answers-per-tenant-in-amazon-bedrock-managed-knowledge-base/
- **Published:** 2026-11-16

Retrieval instructions in Amazon Bedrock Managed Knowledge Base set the voice, format,
retrieval guidance, and answer policy for each tenant on shared knowledge bases. This
post shows how to give each tenant its own answers, keep tenant data apart with metadata
filters, scope access with IAM tags, and roll out changes one tenant at a time.

### 64. Use prompt caching with open-weight models on Amazon Bedrock

- **Publisher:** AWS (`aws-ml-blog`)
- **URL:** https://aws.amazon.com/blogs/machine-learning/use-prompt-caching-with-open-weight-models-on-amazon-bedrock/
- **Published:** 2026-11-16

Many generative AI applications resend the same long context on every request. Prompt
caching lets open-weight models on Amazon Bedrock reuse it to reduce input cost and
latency. This post shows implicit and explicit caching through the Chat Completions API
and applies caching to an OpenCode coding agent session.

### 65. ​​​AWS observability maturity assessment: from guesswork to a blueprint​​

- **Publisher:** AWS (`aws-management-blog`)
- **URL:** https://aws.amazon.com/blogs/mt/aws-observability-maturity-assessment-from-guesswork-to-a-blueprint/
- **Published:** 2026-11-16

Introduction ​​Most teams know they should have good observability. Few can answer the
two questions that matter: How good is our observability posture today, and what should
we fix first? Without an objective way to measure, prioritization defaults to intuition,
tribal knowledge, and the most recent escalation. The service that paged someone last
night gets […]

### 66. NVIDIA Vera Rubin NVL72 Leads Agentic Inference Performance on MLPerf Endpoints v1.0

- **Publisher:** NVIDIA (`nvidia-developer-blog`)
- **URL:** https://developer.nvidia.com/blog/nvidia-vera-rubin-nvl72-leads-agentic-inference-performance-on-mlperf-endpoints-v1-0/
- **Published:** 2026-11-16

Agentic workloads are demanding more from inference systems. AI agents carry growing
conversation histories across turns and generate a mix of reasoning, tool...

### 67. Import AI 481: AI sub-contractors; a wet lab for AI; and subterfuge during development

- **Publisher:** Import AI (Substack) (`import-ai`)
- **URL:** https://importai.substack.com/p/import-ai-481-ai-sub-contractors
- **Published:** 2026-11-16

Plus: CucumberVision!

### 68. GTIG AI Threat Tracker: Agentic Threat Activity Crosses a Significant Threshold

- **Publisher:** Google Cloud (`google-cloud-blog`)
- **URL:** https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold/
- **Published:** 2026-11-16

Written by: Aurora Blum, Kelli Vanderlee, Jess Xia, David Mainor Executive Summary As
threat actors increasingly move beyond basic prompting to deploying autonomous multi-
agent frameworks , automated vulnerability exploitation pipelines, and alternative
monetization schemes like LLMJacking , the adversarial AI landscape has reached a
critical inflection point. In this update, Google Threat Intelligence Group (GTIG) and
Mandiant examine how adversaries across the cyber crime, espionage, and information
operations spectrum are operationalizing generative AI to compress attack timelines,
scale operations, and execute multi-stage intrusions at machine speed. Key trends over
the last quarter include: Shift to Autonomous Workflows and Multi-Agent Frameworks:
Adversary tradecraft has continued to transition beyond manual prompting to deploying
autonomous multi-agent offensive frameworks—such as ARTEX , CAIRN, CyberStrikeAI, and
PentAGI—to execute multi-stage intrusions at greater operational velocity. Automated
Vulnerability Research and Exploitation: Threat actors are increasingly leveraging LLMs
and agentic frameworks to fully automate the reverse engineering of patches via
differential analysis, allowing them to rapidly weaponize n-day vulnerabilities and
scale exploitation pipelines against internet-facing servers without human intervention.
Monetization and Infrastructure Abuse : Financially motivated threat actors continue to
profit from LLMJacking by stealing LLM credentials and cloud resources from compromised
enterprise environments and reselling access to high-performance AI models through
underground proxy services (e.g., LLM Mixers). LLM Integration in Information Operations
(IO): State-sponsored groups, commercial Influence-as-a-Service (IaaS) vendors, and
inauthentic political monetization networks now routinely use LLMs in their operations
to produce synthetic media at scale, create localized personas, and automate cross-
platform distribution. Targeted Espionage and Supply Chain Evolution: Cyber espionage
groups are leveraging LLMs for target research, automated data analysis, and novel
supply chain attack vectors—such as manipulating autonomous coding assistant
configurations to drop backdoors during local execution. Grounded in telemetry from
frontline Mandiant incident response engagements, global threat actor tracking, and live
platform defenses, this report details how state-sponsored espionage groups, financially
motivated cyber criminals, and IO threat actors are operationalizing LLMs in the wild.
At Google, we are committed to developing AI boldly and responsibly. Our multifaceted
defense strategy integrates proactive model-level safeguards, specialized threat
intelligence, and targeted containment protocols to protect our customers and
infrastructure. We continuously harden our models against misuse, mitigate malicious
activity through proactive disruption of bad actor projects and accounts, and use our
autonomous Google AI Threat Defense architecture and BeyondZero to operationalize
security, continuous monitoring, and responding at machine speed across enterprise
environments. Multi-Agent Frameworks in Cyber Intrusions While previous milestones
documented in our quarterly research highlighted nascent adversary interest in agentic
capabilities, GTIG and Mandiant have now observed multiple threat actors abusing open
source, agentic penetration-testing (pentesting) frameworks to automate discrete phases
and specific operational tasks during live intrusions. Threat actor adoption of these
frameworks represents a paradigm shift towards intrusions occurring at machine speed,
with the automated chaining of complex attack paths scaling operations significantly.
While the mechanics of the intrusions remain the same, such as using compromised
credentials and targeting unpatched systems, the speed and scale at which frameworks can
exploit these known weaknesses introduces a new defensive challenge. Figure 1: Multi-
agen

### 69. Science at the Frontier: How scientists use ChatGPT

- **Publisher:** OpenAI (`openai-blog`)
- **URL:** https://openai.com/index/science-at-the-frontier
- **Published:** 2026-11-16

Explore how more than 1,800 scientists use ChatGPT in research. See findings on daily
workflows, reported productivity, and expectations for discovery.

### 70. How Revolut raises ambition without lowering the bar

- **Publisher:** OpenAI (`openai-blog`)
- **URL:** https://openai.com/business/customer-stories/revolut
- **Published:** 2026-11-16

Discover how Revolut uses OpenAI models and Codex to cut coding time by 30–60%, scale
financial crime investigations, and innovate without compromising security.

### 71. LVMH’s Media Division announces strategic partnership with OpenAI

- **Publisher:** OpenAI (`openai-blog`)
- **URL:** https://openai.com/index/lvmh-media-division-partnership
- **Published:** 2026-11-16

LVMH’s Media Division and OpenAI announce a partnership to support journalism with AI
and make its publications more accessible through ChatGPT.

### 72. Google is a Leader in the 2026 Gartner® Magic Quadrant™ for Cloud Operational Database Management Systems

- **Publisher:** Google Cloud (`google-cloud-blog`)
- **URL:** https://cloud.google.com/blog/products/databases/2026-gartner-mq-cloud-operational-databases-management-systems/
- **Published:** 2026-11-16

Google has been recognized as a Leader and positioned furthest in vision in the 2026
Gartner® Magic Quadrant™ for Cloud Operational Database Management Systems (Cloud
ODBMS). This recognition comes as we cross into the era of agentic AI. Leading
enterprises are in their journey of deploying autonomous agents to transform core
business functions. At the center is data, the fuel for AI. In our view, this
recognition from Gartner — particularly our placement furthest for Completeness of
Vision — builds on the August 2026 Gartner® report, AI Vendor Race: Google Is the
Company to Beat in Data Platforms for AI . Together, we believe this validates our long-
standing belief that the future of operational data is unified, open, and inseparable
from the AI layer. In our opinion, this is the blueprint for what we call the Agentic
Data Cloud. Powering a true System of Action through the Agentic Data Cloud requires
operational data to be unified, open, and inseparable from the AI tier. We deliver on
this across our operational databases by converging transaction processing and analytics
in a single engine, while leveraging Google's full-stack AI advantage to integrate
Google DeepMind models and vector indexing directly into the core engine over our AI
Hypercomputer. Furthermore, we define openness not just through 100% PostgreSQL
compatibility and open Apache Iceberg formats, but by providing borderless access to
data across other clouds and environments without requiring complete data replication.
This eliminates operational friction and costly data movement, providing the low-
latency, planet-scale foundation needed to power trusted autonomous agents with
confidence . The Agentic Data Cloud is engineered from the ground up to minimize the
complexity and hidden costs of the agentic era. Let's review the core benefits
enterprises realize when operating on Google Cloud operational databases, along with our
latest innovations to help you thrive in the agentic era. Performance across critical
capabilities and use cases Our operational database portfolio, anchored by Spanner and
AlloyDB, integrates AI natively within the database engine. In AlloyDB, auto vector
embeddings and auto vector indexing automatically generate, maintain, and self-tune
vector data using simple SQL commands, eliminating complex ETL pipelines. Furthermore,
built-in support for Google DeepMind models such as TimesFM enables zero-shot time-
series forecasting directly in SQL. With Spanner, organizations can combine full-text,
vector, and graph capabilities in a single database to power complex multi-model agentic
workflows and context-aware applications with enterprise-grade availability. In the
companion 2026 Gartner® Critical Capabilities for Cloud Operational Database Management
Systems report , Google’s operational database portfolio was evaluated as Google
(Spanner) and Google (AlloyDB) for the following use cases. Highest-placed use cases:
Agentic AI Operations use case : Google was ranked first among all evaluated vendors,
with Google (Spanner) ranking #1 and Google (AlloyDB) ranking #2. Capabilities such as
natively built AI functions provide developers the ability to bring the power of
foundational models within operational databases. OLTP Transactions use case : Google
(Spanner) placed #2 among all evaluated vendors. Spanner's horizontal scalability with
full interoperability between various modalities and no-compromise strong consistency
enables differentiated experiences. In addition, Google (Spanner) placed among the 3
highest-scoring vendors across all 4 evaluated use cases in the report, which we believe
demonstrates the breadth of workloads it supports across transactional, analytical,
NoSQL, and agentic AI scenarios. Agentic Data Cloud for a million-agent world Your
organization's ability to take advantage of AI depends directly on your enterprise data
strategy. Autonomous agents require a modern data foundation that pairs high-performance
transactional proc

### 73. How ISVs are unlocking European workloads using Google Cloud Dedicated technology

- **Publisher:** Google Cloud (`google-cloud-blog`)
- **URL:** https://cloud.google.com/blog/products/identity-security/how-isvs-are-unlocking-european-workloads-on-google-cloud-dedicated/
- **Published:** 2026-11-16

Across Europe, organizations handling sensitive workloads in regulated sectors — such as
financial services, healthcare, critical infrastructure, and the public sector — are
trying to modernize their infrastructure while adhering to strict local data governance
standards, including SecNumCloud in France and BSI C3A in Germany. To help organizations
accomplish this, Google Cloud Dedicated provides the architectural, security, and API
consistency of Google Cloud in locally governed environments managed by independent
domestic operators. But infrastructure is only the starting point. Organizations also
need to transform the software ecosystem they rely on every day. To meet regional
sovereignty requirements, organizations acquire and run these software solutions through
trusted local entities — such as S3NS in France (a joint venture majority-owned and
managed by Thales) and a newly formed German entity that will also be owned and managed
by Thales, currently in preview. These local entities operate dedicated infrastructure
stacks, help maintain operational custody, and handle customer data within independent
jurisdictional boundaries. Today, we are highlighting the expanding independent software
vendor (ISV) ecosystem validated on Google Cloud Dedicated, enabling French and German
organizations to run their critical enterprise software in environments designed to
support their sovereign and regulatory needs. The local partner model: Cloud capability
under domestic custody Deploying in a sovereign boundary should not require an
organization to sacrifice software choice or rewrite its enterprise applications.Because
Google Cloud Dedicated provides architectural and API consistency with Google Cloud,
validated enterprise software runs directly inside these partner-operated environments
without custom re-platforming. This model provides European enterprises with three
concrete advantages: Localized operational custody : Infrastructure operations, software
quarantine procedures, and day-to-day administrative access are under the direct
management of local European partners operating with specialized remote technical
escalations governed by strict, partner-supervised escorted access controls. Broad
software choice : Regulated institutions can deploy industry-standard tools for identity
governance, cyber resilience, simulation, and data streaming natively in their sovereign
perimeter. Streamlined compliance : Organizations fulfill national frameworks like
SecNumCloud and BSI guidelines while preserving familiar CI/CD pipelines, APIs, and
developer workflows. Software choice is the true bottleneck for sovereign migrations
When highly regulated European institutions consider moving to a sovereign cloud, the
infrastructure itself is rarely the primary roadblock. The real bottleneck is
software.Historically, pursuing strict sovereignty meant accepting compromises:
Rewriting applications from scratch or maintaining custom, brittle tooling because
mainstream enterprise platforms were unavailable. Forcing security, engineering, and
data teams to abandon the industry-standard tools they use daily in favor of untested
niche alternatives. Sidelining high-impact initiatives like real-time fraud scoring,
automated DevSecOps, and modern identity governance simply because the required ISVs
could not legally or technically operate in the environment. Because Google Cloud
Dedicated maintains architectural and API consistency with Google Cloud, leading global
and European software providers can deploy their proven platforms directly inside
national, domestic operator-managed boundaries. Regulated organizations retain the
software, automated pipelines, and operational standards they rely on — without
sacrificing compliance or operational custody. Validated ISVs on Google Cloud Dedicated
Deploying enterprise software on Google Cloud Dedicated and S3NS isn't just about
hosting an application locally; it’s about pairing proven software engines with soverei

### 74. Inside the new Google Cloud Data Boundary experience

- **Publisher:** Google Cloud (`google-cloud-blog`)
- **URL:** https://cloud.google.com/blog/products/identity-security/inside-the-new-data-boundary-experience/
- **Published:** 2026-11-16

Digital sovereignty is evolving from a standard compliance requirement into a powerful
strategic advantage for regulated industries worldwide. From European frameworks
designed to meet sovereign standards (DORA, EHDS, GDPR) to FedRAMP/ILs/ITARs in the
U.S., or expanding mandates across Asia-Pacific and the Middle East, organizations can
build deeper global trust through clear governance over data locality, encryption keys
and system access. Historically, achieving that level of control meant accepting an
impossible tradeoff: rely on rigid legacy architectures that lacked access to frontier
AI innovation, or stitch together brittle, manual guardrails that slowed developer
velocity. Google Cloud Data Boundary helps remove that compromise. Built directly onto
Google Cloud’s global commercial infrastructure, Data Boundary delivers software-
defined, AI-assisted governance. This allows organizations to move at commercial speed
with verifiable sovereign controls built in from day one. Today, we’re announcing a new
and updated experience in Data Boundary. Google Cloud Data Boundary combines technical
controls across residency, access, and encryption with ongoing monitoring and
operational assurance. What’s new in Data Boundary Data Boundary streamlines how
security, data and AI teams configure, test and scale governance across their cloud
footprint. Below are the key highlights for the new experience: End-to-end visibility
into sovereign controls: Browse and deploy pre-configured regional and industry
frameworks with clear visibility into mapped technical controls, severities and
remediation steps. Flexible hierarchy-wide enforcement: Apply preventative guardrails
across organizations, complex nested folders and projects — on both net-new and existing
workloads — to block out-of-policy API calls and configuration drift. Dry run posture
validation: Dry run any framework in monitor mode across live existing workloads to
identify drift and violations before enabling active enforcement. Compliance
customization: Frameworks and controls customization according to your organization's
needs. Use Gemini in Google Cloud to customize controls and generate remediation logic
to help reduce manual compliance toil. Accelerated compliance with machine-readable
evidence: Continuously monitor posture, record immutable exception justifications, run
scheduled audits and export machine-readable audit evidence to help fast-track
certification workflows. Turn compliance and digital sovereignty into a business
accelerator In an era of evolving global regulations and rapid AI transformation,
compliance and sovereignty should accelerate your innovation, not hold you back. Google
Cloud Data Boundary helps you deploy frontier AI, scale globally across commercial
regions, and meet stringent regulatory requirements — with greater control and
visibility over your data, your keys and your operations. Here are six steps to get
started with Data Boundary today: You can access the Data Boundary directly from your
Google Cloud console . Navigate to the Compliance tab in your Google Cloud console, and
select Frameworks to begin with. Select existing or configure your own compliance :
Browse 40+ public sector, industry and sovereign AI control packages, or customize
guardrails to match your specific organizational policies. Select your regions :
Designate precise geographic boundaries and data residency restrictions across 29 global
commercial regions. Evaluate workloads in dry-run mode : E nforce controls at either the
folder or the project level. If you already have an active BigQuery or Gemini project
running, you can turn on dry run mode to evaluate how controls behave across existing
resources without disrupting live workloads. Monitor against drifts and violations :
Continuously track posture in real time to automatically detect non-compliant API calls
and configuration drift without disrupting engineering velocity. On-demand audits,
scanning and compliance evidenc

### 75. AWS Secrets Manager adds managed external secrets support for Auth0, Okta, and Palo Alto Networks

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/secrets-manager-managed-external-secrets-auth0-okta-palo-alto/
- **Published:** 2026-11-16

AWS Secrets Manager now supports managed external secrets for Auth0, Okta, and Palo Alto
Networks. Long-lived credentials that are not rotated increase the risk of unauthorized
access if exposed. Rotating a third-party credential requires coordinated updates to the
external service and every application that uses it. You set a rotation schedule from
the AWS Management Console or API. Secrets Manager rotates the credential and stores the
current value without a custom rotation Lambda function. Secrets Manager offers self-
rotation and administrator-assisted rotation for Auth0 credentials. With self-rotation,
the target application replaces its own secret. With administrator-assisted rotation, a
separate Auth0 application with Management API permissions replaces the target
application's secret. For Okta, Secrets Manager offers administrator-assisted rotation
with a separate administrator JSON Web Token (JWT) key and validates the replacement
before deactivating the old secret. For Palo Alto Networks, Secrets Manager offers self-
rotation, in which the current API key authorizes its replacement. Applications that
already retrieve credentials from Secrets Manager receive the rotated value without a
code change or deployment. These integrations join existing managed external secrets
support for BigID, Cisco Security Platform, Confluent Cloud, Databricks, Datadog,
GitLab, Jenkins, MongoDB Atlas, Netskope, Paddle, Salesforce, Snowflake, SonarQube, and
Twilio. Auth0, Okta, and Palo Alto Networks managed external secrets are available in
all AWS Regions where AWS Secrets Manager managed external secrets is supported. To
learn more, visit the &nbsp; AWS Secrets Manager managed external secrets
documentation&nbsp; .

### 76. IAM Identity Center now supports VPC endpoints and network access controls

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/iam-identity-center-vpc-endpoints/
- **Published:** 2026-11-16

AWS IAM Identity Center now supports interface VPC endpoints powered by AWS PrivateLink
and network access controls, enabling you to keep IAM Identity Center traffic private
and restrict which networks can reach your&nbsp;IAM Identity Center services.
Previously, IAM Identity Center rejected traffic arriving through VPC endpoints,
requiring all sign-in and API traffic to use public endpoints. With this launch, you can
create interface VPC endpoints for&nbsp;AWS access portal and service APIs to route
traffic over the AWS private network. IAM Identity Center sign-in traffic flows through
the AWS Sign-in VPC endpoint. You can attach VPC endpoint policies to each endpoint to
scope which AWS organizations, accounts and resources are reachable through your private
connection. Network access controls add a second layer of enforcement at the IAM
Identity Center instance level. When enabled, you can require that all access arrive
through a VPC endpoint, allow specific IP address ranges or VPCs as trusted sources, and
exclude individual applications from enforcement to accommodate services that connect
from outside your VPC. SCIM provisioning traffic from your external identity provider
can be independently restricted to known IP address ranges. Network access controls are
configured through the IAM Identity Center API and are disabled by default. This
capability is available in all commercial AWS Regions and the AWS GovCloud (US) Regions
at no additional cost. To learn more, see Interface VPC endpoints in the IAM Identity
Center User Guide.&nbsp;For more information, visit the IAM Identity Center product page
.

### 77. Amazon SageMaker AI now supports KV cache-aware routing for real-time inference endpoints

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/sagemaker-kv-cache-routing/
- **Published:** 2026-11-16

Amazon SageMaker AI now supports KV cache-aware routing for real-time inference
endpoints, enabling you to reduce time to first token for LLM workloads with long or
repeated prompts. Serving engines such as vLLM store the computed key-value (KV) cache
for repeated prompt starts such as shared system prompts, documents, and conversation
history, to skip repeated work. Across several instances, a request that lands where the
cache is missing recomputes it. Under high load, instances also evict cached blocks to
free GPU memory, including shared prompts and earlier conversation turns. KV cache-aware
routing sends each request to the instance that holds the longest matching part of its
prompt in cache. The vLLM container reports the cache blocks it stores and evicts, and
SageMaker routes with that live view. If the lookup is slow or finds no match, the
endpoint falls back to load-aware routing, so the request is still served. Prefix-aware
routing suits stable shared prompts, short prompts, or moderate load. KV cache-aware
routing suits long prompts, high load, and limited GPU memory. Customers can now enable
this feature by setting `RoutingStrategy` to `KV_AWARE` on a production variant and
adding one environment variable so the container reports cache events. Customer can
invoke the endpoint with the same APIs and OpenAI-compatible payloads. It supports
single-model endpoints and inference components, including LoRA adapters, on GPU
instances. It requires the AWS vLLM Deep Learning Container version 0.33.0 or later with
at least two instances or inference component copies. Detailed observability metrics
show KV cache hit rate. There is no additional charge for KV cache-aware routing. KV
cache-aware routing is available today in all AWS Regions where Amazon SageMaker AI is
available. To get started, update to the latest AWS SDK or CLI. To learn more, visit the
Amazon SageMaker AI inference page and see the API documentation .

### 78. AWS Backup adds logically air-gapped vault support for Amazon RDS

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/aws-backup-air-gapped-vault-rds/
- **Published:** 2026-11-16

AWS Backup logically air-gapped vault now supports Amazon Relational Database Service
(Amazon RDS) DB instances. Logically air-gapped vaults are a type of AWS Backup vault
that stores immutable, isolated backups, which are locked by default with AWS Backup
Vault Lock in compliance mode. Secure sharing across accounts and AWS Organizations
enables direct restore, reducing recovery time from a data loss event. You can now
protect your Amazon RDS DB instances in logically air-gapped vaults. A logically air-
gapped vault stores immutable backups that are locked by default, and isolated with
encryption using AWS owned keys or customer-managed keys. This helps reduce the risk of
downtime, ensure business continuity, and meet compliance requirements. To get started,
use the AWS Backup console, AWS Command Line Interface (CLI), or AWS SDKs. Assign your
RDS DB instances to a backup plan and specify a logically air-gapped vault in the same
AWS Region as the copy destination. Share the vault for recovery or restore testing with
other accounts using AWS Resource Access Manager (RAM), or safeguard vault access during
account compromise using Multi-party approval . Once shared, you can initiate direct
restore jobs from that account. This support is available in most AWS Regions where both
logically air-gapped vault and Amazon RDS are available. For more information and
detailed regional availability, visit the AWS Backup documentation . To learn more about
logically air-gapped vaults for RDS, read the launch blog and visit the feature
documentation and pricing page .

### 79. AWS WAF advanced rate-based rules are now available in AWS GovCloud (US), Thailand, and Mexico

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/waf-advanced-rate-rules-available/
- **Published:** 2026-11-16

AWS WAF advanced rate-based rules are now available in the Asia Pacific (Thailand),
Mexico (Central), AWS GovCloud (US-East), and AWS GovCloud (US-West) Regions. Customers
in these Regions can now aggregate requests using custom keys and choose a 1 or 2 minute
evaluation window in addition to the existing 5 and 10 minute options, the same
capabilities already available in other AWS Regions. A rate-based rule counts requests
and applies an action, such as Block or CAPTCHA, when the request rate exceeds a limit
you set. Previously, rate-based rules in these Regions could aggregate requests only by
IP address and used a 5 or 10 minute evaluation window. Now you can aggregate by request
components such as HTTP headers, cookies, query strings, URI paths, HTTP methods, and
label namespaces, and combine up to five of them into a composite key. For example, you
can limit login attempts per IP address and User-Agent pair, or per session cookie,
which helps against attacks spread across many IP addresses. A shorter evaluation window
detects request floods sooner, and a longer window catches slower, sustained attacks.
You can configure these options in the AWS WAF console, the AWS CLI and SDKs, and AWS
CloudFormation. There is no additional charge for these capabilities, and standard AWS
WAF pricing applies. Advanced rate-based rules are now available in all commercial AWS
Regions where AWS WAF is available and in the AWS GovCloud (US) Regions. To learn more,
see Using rate-based rule statements in the AWS WAF Developer Guide.

### 80. AWS announces Networking Flexible Cost Allocation for Amazon VPC

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/networking-flexible-cost-allocation/
- **Published:** 2026-11-16

Amazon Virtual Private Cloud (VPC) now supports Networking Flexible Cost Allocation
(FCA), which splits shared networking costs by the resources that actually drive them,
so you can see what each team or application used. Until now, AWS Cost and Usage Report
(CUR), including CUR 2.0 in AWS Data Exports, showed networking usage as a single item,
and most customers split it across teams with custom scripts and manual estimates. FCA
splits this line item by the resources that generated it. It supports NAT gateway data
processing and data transfer, including traffic to the internet, and in-Region Amazon
Elastic Compute Cloud (Amazon EC2) and VPC peering data transfer. Today, when several
teams share a resource such as a NAT gateway, the account that owns it pays the full
cost and can't see which team or application drove it. To work around this, some
customers built custom scripts to analyze VPC Flow Logs, which takes ongoing engineering
effort. Others used fixed-percentage splits, which overcharge some teams and undercharge
others. FCA breaks down usage based on traffic sources, helping you accurately track
financial metrics based on applications and teams. To get started, attach a cost
allocation policy to a NAT gateway, VPC peering connection, or Amazon EC2 instance, then
select Networking flexible cost allocation under split cost allocation data in the AWS
Billing and Cost Management console. Allocated line items appear in your CUR within 24
hours. FCA changes only how costs are shown in your reports. Your bill and total charges
stay the same. FCA is available at no additional charge. It's supported in all AWS
commercial Regions except Middle East (Bahrain) and Middle East (UAE). It's also
available in the China Regions. It is not available in the AWS GovCloud (US) Regions. To
learn more, visit the Networking FCA product page .

### 81. AWS IAM Identity Center now supports ForceAuthn in SAML requests

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/iam-identity-center-reauth/
- **Published:** 2026-11-16

AWS IAM Identity Center now gives you the option to require workforce users to re-
authenticate with your external identity provider (IdP) each time their user interactive
session expires. By default, when a user's session expires, IAM Identity Center renews
it through the user's existing IdP session, and the user isn't prompted to sign in
again. For organizations with strict security or compliance requirements that mandate
explicit user verification at regular intervals, this automatic renewal may not meet
policy requirements. When you set user re-authentication to Required and a user's user
interactive session expires, IAM Identity Center prompts the user to re-authenticate
with your external IdP. This helps you enforce stronger sign-in controls for regulated
workloads. IAM Identity Center implements this by adding the SAML 2.0 ForceAuthn
attribute to the SAML request sent to your IdP. You can configure user re-authentication
for any IAM Identity Center instance (organization or account) that's connected to an
external IdP as its identity source. The setting applies only to service provider
initiated sign-ins, where users sign in through your AWS access portal URL. Changes to
the user re-authentication setting are logged in AWS CloudTrail, so you can audit when
it was turned on or off. User re-authentication is available in all AWS Regions where
IAM Identity Center is available at no additional cost. To learn more, see Require user
re-authentication in the AWS IAM Identity Center User Guide.

### 82. Our first phase of embedded assessments

- **Publisher:** OpenAI (`openai-blog`)
- **URL:** https://openai.com/index/our-first-phase-of-embedded-assessments
- **Published:** 2026-11-16

OpenAI begins embedded assessments with Apollo Research, METR, and Transluce, and
Goodfire to independently evaluate model alignment, safeguards, and monitoring systems.

### 83. AgentCore runtime instances are now available in six more AWS Regions

- **Publisher:** AWS (`aws-whats-new`)
- **URL:** https://aws.amazon.com/about-aws/whats-new/2026/11/agentcore-aws-regions/
- **Published:** 2026-11-16

Amazon Bedrock AgentCore runtime instances are now available in six additional AWS
Regions: US West (N. California), Canada (Central), Europe (London), Europe (Paris),
Europe (Stockholm), and Asia Pacific (Seoul). Runtime instances run your agents on
Amazon EC2 instances while AgentCore handles provisioning, patching, scaling, and
lifecycle management. By expanding to these AWS Regions, more teams can use runtime
instance capabilities such as GPU-accelerated, memory-optimized, or compute-optimized
instance types, and long-running agent sessions of up to 14 days. You can run your
agents closer to your users to reduce invocation latency, and keep agent instances,
storage volumes, and session data in the Region that your data residency requirements
call for. With this expansion, you can use runtime instances in the following AWS
Regions: US East (N. Virginia), US East (Ohio), US West (N. California), US West
(Oregon), Canada (Central), Europe (Frankfurt), Europe (Ireland), Europe (London),
Europe (Paris), Europe (Stockholm), Asia Pacific (Mumbai), Asia Pacific (Seoul), Asia
Pacific (Singapore), Asia Pacific (Sydney), and Asia Pacific (Tokyo). You are charged
for managing the provisioned compute, in addition to your Amazon EC2 costs. To get
started, see the following resources: Supported AWS Regions in the Amazon Bedrock
AgentCore Developer Guide AgentCore pricing Runtime instances and capacity providers in
the Amazon Bedrock AgentCore Developer Guide

### 84. Unlocking Stable On-Policy RL on TPU with Bitwise-Zero Train–Inference Mismatch

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/unlocking-stable-on-policy-rl-on-tpu-with-bitwise-zero-traininference-mismatch/
- **Published:** unknown-date

How we eliminated floating-point train–inference logprob drift for on-policy LLM
reinforcement learning across 64 Cloud TPU v5p chips using a generalizable four-part JAX
and Pallas recipe in Tunix.

### 85. TPU Model Design Considerations and Optimization Guide

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/tpu-model-design-considerations-and-optimization-guide/
- **Published:** unknown-date

The newly launched AI-Hypercomputer/tpu-codesign guide provides hardware-grounded design
rules to help developers maximize performance on TPUs for LLMs and Mixture-of-Experts
(MoE) workloads. Key principles include aligning reduction and output dimensions to 256
for systolic arrays, adopting LatentMoE to compress routed token traffic, and mapping
parallel axes directly onto physical links.

### 86. Securing Your Agents: A Hands-On Guide to Agent Anomaly Detection

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/securing-your-agents-a-hands-on-guide-to-agent-anomaly-detection/
- **Published:** unknown-date

This guide walks developers through setting up Agent Anomaly Detection on the Gemini
Enterprise Agent Platform to monitor AI agent telemetry and catch behavioral risks. It
demonstrates how to deploy a sample customer support agent, trigger out-of-scope
security findings, and configure proactive alerts using Cloud Monitoring and Security
Command Center.

### 87. Agents are sessions, not requests: size GKE node pools for AI agent sessions

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/agents-are-sessions-not-requests-size-gke-node-pools-for-ai-agent-sessions/
- **Published:** unknown-date

AI agent sessions remain active and idle for most of the workday, making traditional
one-Pod-per-session allocations inefficient for cluster resources. By using open-source
tools like Agent Substrate and AX on GKE, developers can park idle sessions in object
storage to release compute resources while maintaining session state. This approach
optimizes resource utilization and reduces Kubernetes node costs by up to 40%.

### 88. How Agent Anomaly Detection scores on benchmarks we didn't write

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/how-agent-anomaly-detection-scores-on-benchmarks-we-didnt-write/
- **Published:** unknown-date

Agent Anomaly Detection (AAD) provides asynchronous, low-latency monitoring for AI
agents by analyzing OpenTelemetry traces and logs to flag goal hijacks and tool misuse.
Tested across five public security benchmarks, AAD successfully caught 87% of harmful
instructions carried out by agents without adding runtime latency. Developers can
integrate AAD alongside semantic governance and strict tool limits as part of a defense-
in-depth strategy to secure agentic applications.

### 89. Catch Go bugs that fuzzing misses with Gemini and a constraint solver

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/catch-go-bugs-that-fuzzing-misses-with-gemini-and-a-constraint-solver/
- **Published:** unknown-date

How pairing Go's surviving compiler bounds-check traps with Gemini 4 Argon and the Z3
constraint solver catches latent out-of-bounds panics in Go code and uncovers a slice-
capacity blind spot in go test -fuzz.

### 90. A2UI 1.0: Build delightful, fast, reliable, agentic experiences

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/a2ui-10-build-delightful-fast-reliable-agentic-experiences/
- **Published:** unknown-date

A2UI 1.0 is an open protocol for generative UI that enables AI agents to render
interactive, native screens across web, mobile, and desktop applications. Developers can
leverage open-source renderer SDKs—including React, Angular, Lit, Flutter, SwiftUI, and
Jetpack Compose—alongside agent SDKs for Python, TypeScript, and Dart. The release
introduces bidirectional function calls, swappable inference formats, and secure data
binding to help teams seamlessly integrate generative UI into their product stacks.

### 91. On-Device Speech Recognition and Text-to-Speech in Google AI Edge Gallery

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/on-device-speech-recognition-and-text-to-speech-in-google-ai-edge-gallery/
- **Published:** unknown-date

Google AI Edge Gallery now supports on-device, offline Automatic Speech Recognition
(ASR) and Text-to-Speech (TTS) capabilities for building developer-friendly voice
applications. Developers can leverage ML Kit for optimized Android performance, or use
MediaPipe Tasks and LiteRT for cross-platform open-weight model integration. This local
pipeline seamlessly pairs lightweight speech models with on-device small language models
like Gemini Nano and Gemma 4 to enable real-time streaming transcription and low-latency
synthesis.

### 92. Announcing Long-Context Training on TPUs with MaxText Context Parallelism

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/announcing-long-context-training-on-tpus-with-maxtext-context-parallelism/
- **Published:** unknown-date

Google Cloud's MaxText framework now supports long-context training up to 14 million
tokens on Cloud TPUs by implementing four context-parallel strategies: All-gather, A2A,
P2P, and USP. Powered by the Tokamax Splash Attention kernel, these strategies
effectively manage attention compute and memory bottlenecks without materializing full
key-value sequences in high-bandwidth memory. Developers can adopt these capabilities in
MaxText v0.2.4 to achieve high Model FLOPs Utilization (MFU) across large-scale model
training workflows.

### 93. From prompt to app: Build with Google Maps in AI Studio

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/from-prompt-to-app-build-with-google-maps-in-ai-studio/
- **Published:** unknown-date

Developers can now build applications powered by Google Maps Platform directly within
Google AI Studio by prompting Gemini with real-world geospatial concepts. The
integration eliminates traditional configuration hurdles by providing one-click demo
keys that generate instantly without requiring Cloud Console redirects or credit cards.
This setup grants developers immediate access to core APIs—including Maps, Places, and
Routes—supported by daily sandbox quotas for seamless prototyping.

### 94. What is Pathways? Single-controller training for large models

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/what-is-pathways-single-controller-training-for-large-models/
- **Published:** unknown-date

Pathways is a single-controller distributed training system designed to coordinate
large-scale model training across multiple accelerator groups by representing
computations as a global dataflow graph. Unlike traditional SPMD models like DDP and
FSDP that rely on synchronous collectives, Pathways uses asynchronous dispatch and a
central scheduler to maximize hardware utilization and prevent deadlocks in complex
workloads. By decoupling model definition from physical hardware via virtual devices,
developers can efficiently scale complex training architectures and seamlessly handle
dynamic workloads like reinforcement learning post-training.

### 95. Agent Distraction

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/agent-distraction/
- **Published:** unknown-date

Analysis of over 913,000 coding agent sessions reveals that 13% expose agents to inline
TODO(b/...) comments. In 6% of encounters, agents act on these comments, with 83% being
entirely unprompted by the developer. These detours result in significant
overhead—adding 70% more steps, 77% more tokens, and 105% more wait time per
session—split between chasing closed tickets (41%) and unauthorized scope creep on open
bugs (57%). Higher-capability models show higher distraction rates, highlighting the
need for automated cleanup and linters to maintain agent-friendly codebases

### 96. Cost per task: Using cheap classifiers to route across Gemini models and thinking levels

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/cost-per-task-using-cheap-classifiers-to-route-across-gemini-models-and-thinking-levels/
- **Published:** unknown-date

Per-token API prices keep falling, yet engineering bills for autonomous coding agents
keep climbing....

### 97. DevFest is back!

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/devfest-is-back/
- **Published:** unknown-date

DevFest 2026 runs from October 1 to December 31, bringing together nearly a million
developers across more than 800 global events centered on the agentic AI era. Under the
theme "Build, Secure, Scale," participants gain hands-on experience with Google’s
developer stack—including Gemini, Google AI Studio, Google Antigravity, and Web
MCP—through live workshops and codelabs. The conference focuses on enabling developers
to prototype rapidly, ensure secure and private deployments, and leverage production-
ready infrastructure.

### 98. Build Generative UI Apps with A2UI & CopilotKit Agents

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/build-generative-ui-apps-with-a2ui-copilotkit-agents/
- **Published:** unknown-date

See Google A2Ui in action! Learn how to natively render agentic UIs across Langchain,
AWS Strands, Microsoft agents, and Google ADK using CopilotKit SDKs for A2UI.

### 99. Hill-Climbing Agent Quality with Agents CLI Evaluation

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/hill-climbing-agent-quality-with-agents-cli-evaluation/
- **Published:** unknown-date

This post walks through the Agents CLI evaluation loop for systematically improving
agent performance through continuous testing and grading. It demonstrates how to catch
prompt regressions, evaluate model backend swaps using side-by-side trace comparisons,
and automate evaluation passes. Developers will also learn how to integrate nightly
scheduled runs with threshold-based alerting to track quality over time.

### 100. Smaller apps and faster GPU inference with LiteRT in Google Play services

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/smaller-apps-and-faster-gpu-inference-with-litert-in-google-play-services/
- **Published:** unknown-date

LiteRT in Google Play services now offers GPU inference powered by ML Drift, delivering
about 1.4x faster performance alongside the new CompiledModel API. Switching from
bundled binaries reduces app size by approximately 8 MB while enabling seamless,
automatic runtime updates across billions of devices. Developers can easily adopt these
updates by updating their dependencies and utilizing the new Android Studio LiteRT skill
for automated migration.

### 101. Building Conversational Commerce with Multi-Agent Swarms on GCP: A Working Prototype

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/building-conversational-commerce-with-multi-agent-swarms-on-gcp-a-working-prototype/
- **Published:** unknown-date

This document provides a publication template and metadata structure for a technical
blog post focused on building Conversational User Interfaces (CUIs) using AI. It
outlines key developer focus areas, product stacks, and approval workflows required for
publishing technical content through Google Developer Studio. The framework helps
engineers organize their guides and solutions to effectively share AI-driven
conversational interface designs with the developer community.

### 102. Fast, reliable A2UI, with swappable inference formats

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/fast-reliable-a2ui/
- **Published:** unknown-date

A2UI now supports swappable inference formats, introducing A2UI Express which uses up to
3x fewer tokens and cuts latency by compiling compact Python-style syntax into standard
A2UI JSON via Agent SDKs. Developers can also use controlled generation with TypeSafe's
Jev system-decision models to render known-shape screens in under 300 ms while smaller
models stream text. These updates require no changes to frontend renderers or component
catalogs, offering flexible performance levers for generative UI development across
Python, TypeScript, and Dart.

### 103. Preview, edit, and collaborate on markdown (.md) files natively in Google Docs and Drive

- **Publisher:** Google Developers (`google-developers-blog`)
- **URL:** https://developers.googleblog.com/preview-edit-and-collaborate-on-markdown-md-files-natively-in-google-docs-and-drive/
- **Published:** unknown-date

Google Workspace now offers native support for Markdown (.md) files, allowing developers
and AI agents to seamlessly collaborate on documentation directly in Google Docs without
manual file conversions. This integration preserves native file fidelity for use with
Git repositories and developer tools while unlocking standard Docs features like line-
level commenting, rendered Drive previews, and tracked version history.

### 104. Announcements

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/announcements
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 105. Public Benefit Fund

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/public-benefit-fund
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 106. S1 Sec

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/s1-sec
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 107. Features

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/features
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 108. Roadshow Launch

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/roadshow-launch
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 109. Ai For Science Expands Foundations Research Institutions

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 110. Expanding Partnership Gsa

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/expanding-partnership-gsa
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 111. Partnerships

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/partnerships
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 112. Donating Agent Skills To The Agentic Ai Foundation

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 113. Product

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/product
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 114. Open Call Guest Investigators Life Sciences

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/open-call-guest-investigators-life-sciences
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 115. Christopher Stubbs Joins Long Term Benefit Trust

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/christopher-stubbs-joins-long-term-benefit-trust
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 116. An Update On Independent Evaluators

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/an-update-on-independent-evaluators
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 117. Policy

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/policy
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 118. 2026 Us Midterms

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/2026-us-midterms
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 119. Safeguards

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/safeguards
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 120. Singapore Office Opening

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/singapore-office-opening
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 121. Distillation Defenses

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/distillation-defenses
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 122. Anthropic Cyber Mission

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/anthropic-cyber-mission
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 123. Security

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/security
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 124. 2026 Usage Policy Update

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/2026-usage-policy-update
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 125. Genesis Mission Commitment

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/genesis-mission-commitment
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 126. Cyber Verification Program

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/cyber-verification-program
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 127. Claude Frontier Academy

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/claude-frontier-academy
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 128. Barclays Scales Claude

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/barclays-scales-claude
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 129. Accenture Embedded Evaluation

- **Publisher:** Anthropic (`anthropic-news`)
- **URL:** https://www.anthropic.com/news/accenture-embedded-evaluation
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 130. Rss

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/rss
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 131. Build With Studio

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/build-with-studio/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 132. Mistral Large 4 Oss

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-large-4-oss/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 133. Mistral Nvidia Ai For Industrial Engineering

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-nvidia-ai-for-industrial-engineering/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 134. Voxtral 3

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/voxtral-3/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 135. Timestral

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/timestral/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 136. Mistral Large 4

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-large-4/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 137. Hallo Deutschland

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/hallo-deutschland/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 138. Mistral X Mozilla

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-x-mozilla/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 139. Mistral X Cloudera

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-x-cloudera/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 140. Legacy Code Modernization

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/legacy-code-modernization/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 141. Mistral Makes Sovereign Open Weight Ai To Frontier

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 142. Mistral X Humain

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-x-humain/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 143. Agentic Search

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/agentic-search/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 144. Regional Inference Open Models New Compute

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/regional-inference-open-models-new-compute/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 145. Shieldstral

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/shieldstral/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 146. Manage Prompts And Skills In Studio

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/manage-prompts-and-skills-in-studio/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 147. Robostral Navigate

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/robostral-navigate/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 148. Leanstral 1 5

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/leanstral-1-5/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 149. More Control Over Connectors

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/more-control-over-connectors/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 150. Ocr 4

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/ocr-4/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 151. Ai Now Summit 2026

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/ai-now-summit-2026/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 152. Vibe Agent

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/vibe-agent/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 153. Search Toolkit

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/search-toolkit/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 154. Introducing Physics Ai At Mistral

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/introducing-physics-ai-at-mistral/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 155. Physics Ai Research

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/physics-ai-research/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 156. Accelerate Ai Native Industry

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/accelerate-ai-native-industry/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 157. Vibe Remote Agents Mistral Medium 3 5

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 158. Connectors

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/connectors/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 159. Workflows

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/workflows/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 160. Spaces

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/spaces/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 161. Voxtral Tts

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/voxtral-tts/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 162. Forge

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/forge/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 163. Mistral Small 4

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-small-4/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 164. Mistral Ai And Nvidia Partner To Accelerate Open Frontier Models

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-ai-and-nvidia-partner-to-accelerate-open-frontier-models/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 165. Leanstral

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/leanstral/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 166. Rails Testing On Autopilot Building An Agent That Writes What Developers Wont

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/rails-testing-on-autopilot-building-an-agent-that-writes-what-developers-wont/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 167. Voxtral Transcribe 2

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/voxtral-transcribe-2/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 168. Mistral Vibe 2 0

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/mistral-vibe-2-0/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

### 169. Debugging Memory Leak In Vllm

- **Publisher:** Mistral (`mistral-news`)
- **URL:** https://mistral.ai/news/debugging-memory-leak-in-vllm/
- **Published:** unknown-date

(HTML index entry — open URL for full text; do not invent body content.)

_Total entries: 169_