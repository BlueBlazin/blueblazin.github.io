### Agent harnesses

- **H1 — [ReAct](https://arxiv.org/abs/2210.03629).** Read the interleaving of actions and observations; implement the control loop without depending on access to a model's private reasoning.
- **H2 — [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).** Read workflows versus agents, simple patterns, and tool design before introducing orchestration machinery.
- **H3 — [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) and [SWE-agent paper](https://arxiv.org/abs/2405.15793).** Trace the minimal loop and study how the interface affects coding behavior. Use an existing baseline instead of inventing an implausibly weak comparator.
- **H4 — [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).** January 2026 engineering reference for tasks, trials, outcomes, graders, and meaningful success metrics.
- **H5 — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).** Read persistence, task progress, and working across context windows. Adapt these ideas to a small demonstrable resume experiment.
- **H6 — [MCP specification](https://modelcontextprotocol.io/specification/latest) and [Python SDK](https://github.com/modelcontextprotocol/python-sdk).** Pin the version used. Learn one local transport/tool interaction, rather than building a protocol stack.
- **H7 — [Harbor documentation](https://docs.harborframework.com/) and [Terminal-Bench](https://www.tbench.ai/).** Use a fixed compatible subset and the benchmark version recorded in your run manifest. Harbor is evaluation infrastructure, not your agent's reasoning architecture.
- **H8 — [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227).** July 2026 paper, revised August, motivating matched inference budgets and genuinely held-out evaluation. Optional contrast: [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850). Compare their claims and evaluation designs rather than accepting a headline improvement.


- **H9 — [Official Anthropic Python SDK](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python) and [handling tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).** Pin the SDK version actually used. Implement one request/response adapter, preserve tool-result identifiers and required content blocks, and make timeout/retry behavior explicit before paid tests. Equivalent provider adapters must satisfy the same protocol and budget checks.
- **H10 — [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/) and [Docker security](https://docs.docker.com/engine/security/).** Inspect the effective memory/CPU limits, mounts, credentials, and network boundary; process separation alone is not filesystem isolation. Scope the course to controlled disposable workloads.

### Learning evidence and operating references

- **P1 — [Retrieval practice experiment](https://pubmed.ncbi.nlm.nih.gov/16507066/).** Supports closed-book retrieval for later retention.
- **P2 — [Spacing research](https://www.yorku.ca/ncepeda/publications/CPVWR2006.html).** Supports distributed revisits; exact useful spacing depends on the retention goal.
- **P3 — [Active learning in undergraduate STEM](https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/).** Supports active problem-solving over a lecture-only approach; not direct validation of this exact self-study plan.
- **P4 — [How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245).** A 2026 randomized coding-skill study; interpret its immediate assessment and participant/task setting carefully. It motivates preserving independent reasoning, not a claim that all AI assistance harms learning.
- **C5 — [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing).** Pin the chosen model, record actual usage, and check current availability and rates.
