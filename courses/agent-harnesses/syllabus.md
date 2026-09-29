# Agent Harness Engineering

66 scheduled hands-on hours over 10 weeks. Day 0 contains setup, review and administration outside the regular calendar. Weekdays: 1 hour. Saturday: up to 2 hours. Sunday: off.

## Day 0

Prepare only the tools needed for your first lab, then begin Day 1 with a working FakeModel loop. All setup, review and course-administration material lives here. Later-use checklists are references for their stated milestones, not prerequisites to complete now.

- I can run Python and pytest in my course workspace.
- My repository ignores credentials, virtual environments, generated task workspaces and private runtime traces.
- Fake model responses are the default; the first lab makes no paid requests.
- I know the A$250 course ceiling and the development/final-task separation rule.

### Local repository and Python

Create agent-harness-lab with harness/, tests/, fixtures/, evals/, docs/, reports/, and scripts/. Create or reuse a Python virtual environment and install pytest. Run a minimal import/JSON smoke test. Ignore credentials, environments, generated workspaces, and private runtime traces. Python and pytest are sufficient for Day 1. Install and pin provider/MCP SDKs from this setup reference before the lessons that actually use them.

### Execution-runtime readiness

Before the execution-boundary module, prepare a local container runtime supporting Apple silicon. Follow its official installation instructions and confirm one harmless container starts, record its version and how to stop it. The Day 1 FakeModel loop does not require a container. The actual mounts, permissions, network and resource boundaries are implemented in the course. If installation blocks, save the exact blocker and resolve it before live-code lessons; never replace isolation with an unlabelled host subprocess.

### Study, evaluation, and spending conventions

Read the course outcome, 8 development / 16 final split rule, and budget convention. Create a ledger with A$175 API, A$50 CPU/storage, A$25 contingency within this course’s A$250 allowance. Set fake responses as the default mode. Put report/evidence templates in docs/ without filling future result fields. Sundays are off; weekdays and Saturdays retain their existing time caps.

### Setup and optional integrations

Use this page for environment, SDK, and container readiness before their first use. Record installed versions and reproducible setup commands. A provider API key is only needed for the later bounded live smoke run; keep fake responses as the default.

Harbor is an optional integration. Its installation is not required for the private-task study. If you choose it, reserve up to one separate setup hour here and complete it before the optional comparison; skip the extension if setup remains blocked. The core lesson time is for implementation and measurement.

### Study rhythm and completion policy

Whenever blocked or planning the next session.

Use 5 minutes retrieval, 10 minutes focused source study, 35 minutes building, 10 minutes checking. Stop at the timebox; a failed prerequisite stays open and shifts later dates. No mandatory catch-up day or Sunday work is added. Record the smallest reproducer and next action. Spending caps and final-set separation apply throughout; never mark a result complete solely because time was spent.

### Optional self-assessments and execution gates

Use these questions after the associated implementation milestone. They are reference material, not prerequisites to understand on Day 0. For each response, award 0 for incorrect, 1 for the key idea, or 2 for the idea plus a concrete consequence. A useful target is 5/6; use the answer to identify the next small repair.

The technical execution gates remain mandatory within their implementation lessons: demonstrate the execution boundary before live code; reconcile uncertain side effects and preserve budgets before resume; and validate policy activation, matched resources, frozen manifests, and affordability before final paid evaluation.

### Report, demonstration, and release templates

Populate these templates incrementally from completed work. Leave future-result fields empty. Writing and presentation are reference guidance rather than standalone lesson days.

Report (2–4 pages): question; harness design; the two context conditions; task suite; limits and metrics; audited main results; failure analysis; limitations. Every numerical claim links to an authoritative table or trace and the frozen manifest. A neutral or negative result is a valid outcome.

README reproduction path: prerequisites; exact pinned dependency and model versions; setup commands; credential variable names without values; a bounded fake-client or development smoke command; expected output paths and success criteria. Document the full 96-attempt study command separately with its exposure estimate. A smoke run does not reproduce the full statistical result.

Evidence index columns: claim; frozen code/configuration; command; smallest supporting trace or table; limitation. Suggested rows: termination, execution boundary, resume reconciliation, MCP parity, context policies, attempt accounting, cost, uncertainty. Separate development, final, and optional external results.

Demonstration checklist: use existing clean development fixtures for success, restart, and bounded failure; show run ID, decisive event, terminal status, and outcome evidence; label fake responses. A terminal transcript is sufficient.

Release checklist: verify links and scope, remove credentials and unintended private traces, record a release commit, state the 16-task/two-condition/three-attempt design and actual outcome, and keep follow-up work separate. Publish only under your chosen visibility and license.

Contribution checklist: consult the project contribution guide; reduce the problem to a minimal reproducible case; include expected and observed behavior, versions, and a focused regression test. Drafting is sufficient for the course; sending an issue or pull request is optional.

### Optional official video

A broader discussion from Anthropic after you have a working loop. Optional; no invented timestamps and no requirement to watch the full talk within a one-hour lesson.

### After events, replay, and development evaluation — optional self-assessment

After events, replay, and development evaluation. These questions are for that milestone, not initial setup.

Questions: (1) Why is a path-prefix check insufficient for symlinks? (2) What must an event include to identify one tool attempt? (3) Why must execution replay start from a clean fixture with a new run ID?

Answer guide: (1) A path that appears inside the root can resolve through a symlink outside it; enforce the supported resolved boundary, including parent paths for writes. (2) Stable run/action identifiers, ordering, arguments, outcomes, and timing/usage fields connect the attempt to evidence. (3) Execution replay is a new execution and may perform the approved local effects again; a fresh fixture prevents duplication in the original workspace and a new ID preserves provenance. Read-only log playback merely displays recorded observations.

### After persistence and context policies — optional self-assessment

After persistence and context policies. These questions are for that milestone, not initial setup.

Questions: (1) Why can an atomic checkpoint still leave an uncertain write? (2) What should a third file hash mean during before/after reconciliation? (3) Which context and accounting constraints must both policies share?

Answer guide: (1) Checkpoint persistence and the workspace mutation are separate operations, so a crash can occur between them. (2) A hash matching neither before nor intended after indicates conflict or uncertainty; stop for reconciliation rather than overwriting it blindly. (3) Keep model revision, task/constraints, valid call/result pairs, context ceiling, tools, time, and total-token/cost limits matched; charge summarizer calls and latency to the compaction condition.

### Before the frozen final experiment — optional self-assessment

Before the frozen final experiment. These questions are for that milestone, not initial setup.

Questions: (1) Why must the pilot activate both policies? (2) Why are timeouts and budget stops retained? (3) Does MCP compatibility establish tool authorization?

Answer guide: (1) Without activation, the trial does not exercise the intended difference in memory policy. (2) They are outcomes under the declared budget; excluding them creates a favorable, selected denominator. (3) No. MCP describes capability interaction; trusted host code must still enforce permissions independently of model output.

## Study calendar

### Week 1

- Monday (1h): Build the First Bounded Agent Loop
- Tuesday (1h): Validate Typed Tool Call Arguments
- Wednesday (1h): Connect Tool Results To Messages
- Thursday (1h): Verify Every Loop Stopping Condition
- Friday (1h): Build Confined Workspace Read Tools
- Saturday (2h): Add Writes And Structured Traces + Outline Tasks And Build Fixtures
- Sunday: off.

### Week 2

- Monday (1h): Run Three Fixtures End To End
- Tuesday (1h): Isolate Task Processes And Credentials
- Wednesday (1h): Enforce Paths And Tool Authorization
- Thursday (1h): Bound Process Time And Output
- Friday (1h): Verify The Execution Boundary Matrix
- Saturday (2h): Record Events With Stable Identifiers + Replay Mock Runs And Inspect Traces
- Sunday: off.

### Week 3

- Monday (1h): Complete Eight Development Task Fixtures
- Tuesday (1h): Run And Summarize Development Results
- Wednesday (1h): Build Clean Workspace Outcome Evaluation
- Thursday (1h): Implement the Provider Message Adapter
- Friday (1h): Enforce Budgets and Verify the Live Adapter
- Saturday (2h): Integrate and Inspect the Baseline Harness + Compare Two Systems Under Declared Limits
- Sunday: off.

### Week 4

- Monday (1h): Implement Bounded Repository File Listing
- Tuesday (1h): Combine Search With Selected File Reads
- Wednesday (1h): Compare One Context Selection Policy
- Thursday (1h): Explain Lost Evidence And Outcomes
- Friday (1h): Define Durable Agent Run State
- Saturday (2h): Persist Checkpoints Around Tool Actions + Resume And Reconcile Uncertain Actions
- Sunday: off.

### Week 5

- Monday (1h): Interrupt And Verify Mutation Handling
- Tuesday (1h): Define The Compacted Context Record
- Wednesday (1h): Implement Evidence Preserving Context Compaction
- Thursday (1h): Run The Bounded Recent History Baseline
- Friday (1h): Inspect Compaction Information Loss Cases
- Saturday (2h): Trace The Official MCP Tool Interface + Expose One Existing Workspace Tool
- Sunday: off.

### Week 6

- Monday (1h): Compare Direct And Protocol Invocations
- Tuesday (1h): Verify Protocol And Permission Boundaries
- Wednesday (1h): Author Final Tasks 01–04
- Thursday (1h): Author Final Tasks 05–08
- Friday (1h): Author Final Tasks 09–12
- Saturday (2h): Finish the Last Four Final Task Fixtures + Verify Reference And Broken Controls
- Sunday: off.

### Week 7

- Monday (1h): Build the Frozen Task Manifest
- Tuesday (1h): Validate Task and Grader Invariants
- Wednesday (1h): Inject Model Timeout And Rate Limits
- Thursday (1h): Exercise Malformed Calls And Tool Crashes
- Friday (1h): Recover From Stale Summaries And Restarts
- Saturday (2h): Verify The Complete Recovery Failure Matrix + Predeclare The Matched Harness Hypothesis
- Sunday: off.

### Week 8

- Monday (1h): Freeze Metrics Splits And Cost Estimates
- Tuesday (1h): Pilot Both Policies At Context Ceiling
- Wednesday (1h): Implement the Experiment Manifest Loader
- Thursday (1h): Verify Evaluation Manifest And Trial Accounting
- Friday (1h): Launch The First Matched Trial Round
- Saturday (2h): Launch The Second Matched Trial Round + Complete Trials and Verify Outcome Accounting
- Sunday: off.

### Week 9

- Monday (1h): Group Private Suite Failures And Costs
- Tuesday (1h): Inspect Representative Private Task Failure Traces
- Wednesday (1h): Run The Optional Frozen External Pilot
- Thursday (1h): Validate Evaluation Result Tables
- Friday (1h): Audit Outcome Graders Against Saved Evidence
- Saturday (2h): Reconcile Run Budgets And Actual Charges + Calculate Uncertainty Across Paired Task Results
- Sunday: off.

### Week 10

- Monday (1h): Generate Claims From Audited Evidence
- Tuesday (1h): Test Reproduction From a Clean Environment
- Wednesday (1h): Build a Minimal Upstream Regression Case
- Sunday: off.

## Project standards


Use a capable pinned pretrained API model for harness research. Keep your raw loop small enough to explain. The core state consists of the task, model/tool messages, selected context, run metadata, tool outcomes, budget state, and terminal result. SDKs may handle transport; your code should own control flow and evaluation.

The task environment is disposable and isolated from your personal working files. A container is one execution boundary, not a universal security guarantee. Keep secrets, evaluator logic, expected answers, and final outcome checks outside agent-writable paths. A host-owned grader must not import agent-modified modules into the host; run candidate code inside the bounded grading environment and inspect inert outputs from the host. Tools enforce authorization in code; a prompt saying “be safe” is not enforcement. Scope the course to benign coding/data tasks. Reconcile uncertain side effects after a crash; exactly-once execution cannot be assumed simply because a log exists.

For the private suite, author 24 small tasks in categories such as bug fixing, adding a tested feature, repairing a data-processing script, and changing an experiment configuration. Write outcome checks before agent runs. For every task, require a known-correct reference solution to pass and the original broken or no-op state to fail. Check external tasks with their provided oracle/no-op controls where available; otherwise document the equivalent validation. Split task families where practical so the final set is not a renamed copy of development tasks. You will know the authored tasks, so call this a held-out development split, not a blind independent benchmark. Do not use final outcomes to tune prompts or policies.

Main experiment: 16 final tasks × 2 conditions × 3 trials = 96 attempted trials. A trial that times out, hits its cost cap, or cannot recover is a failure under that budget. Use the same model revision, tools, task snapshots, and limits; the changed variable is context policy. Both policies preserve the original task/constraints and valid tool-call/result pairs under the same context ceiling. Charge summarizer calls, tokens, and latency to the compaction condition. Report how often the policy activates; if the development pilot never reaches the ceiling, redesign development tasks or choose another measured intervention before freezing. Report success counts/rates, all-trials-success where useful, median/p90 time, tokens/cost per task, and failure categories. Do not convert three tries into an inflated single-try success figure.

Label infrastructure failures separately from task failures, while including both in overall end-to-end completion. Use paired per-task comparisons and, if giving intervals, resample tasks rather than treating all repeated trials as independent tasks. Sixteen tasks is small; the result is a pilot, not a broad reliability claim. Describe model stochasticity and infrastructure noise. If the API does not expose deterministic seeds, say so and use repeated trials without pretending they are seed-controlled.

The external 10-task subset is optional and helps expose integration problems and unfamiliar task distributions. Its optional installation/setup budget is one scheduled hour; if it fails, finish the private study and document the infrastructure limitation. Pin the benchmark version actually used; do not call a subset score an official Terminal-Bench or SWE-bench result. Public benchmark contamination cannot be ruled out. Only one run per condition means this external comparison is descriptive. If infrastructure fails for a task, report it; do not silently replace it after seeing results.

MCP demonstrates interoperability. It does not supply an agent loop, memory policy, authorization design, or evaluation methodology. Multi-agent systems, vector databases, and automatic harness evolution are optional experiments after the single-agent baseline is trustworthy. [H3–H8]


Pre-request budget reservations include all enabled billable work and remain reserved when usage is uncertain. The global study dispatcher reserves against shared remaining funds before launching each request, so concurrent trials cannot each spend the same apparent balance. Start with concurrency one; use transactional reservation updates before adding parallel execution.


## Assessment


Every substantive experiment note should contain the question, falsifiable prediction, baseline, changed variable, data/task IDs, exact commit/configuration, hardware/dtype, correctness criteria, result, cost, confounds, and next experiment. Save machine-readable results alongside the note.

| Criterion | Weight |
|---|---:|
| Correctness and reliable failure handling | 30% |
| Fair evaluation and measurement | 25% |
| Mechanistic explanation | 20% |
| Reproducibility and documentation | 15% |
| Useful independent extension or contribution | 10% |

Correctness is a gate. An honestly rejected hypothesis can earn full experiment marks.

Prepare one report of about 2–4 pages, or equivalent Markdown, for this course. Include a clear result, a limitation, raw evidence and a command that reproduces a smaller version. Use the Day 0 assessment and portfolio checklists after the relevant practical work. Technical reproduction remains part of the hands-on sequence where scheduled.


## Extended reading catalog

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
