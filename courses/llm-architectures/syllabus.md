# LLM Architectures

57 scheduled hands-on hours over 9 weeks. Day 0 contains setup, review and administration outside the regular calendar. Weekdays: 1 hour. Saturday: up to 2 hours. Sunday: off.

## Day 0

Do only the readiness work you need, then start Day1 by implementing stable next-token loss. Setup, review questions and portfolio instructions are collected here so they do not interrupt the technical sequence. The later-use sections are reference checklists, not work to complete before learning.

- Create or reuse an isolated Python environment; verify NumPy and PyTorch on CPU. Prepare JAX CPU in the same environment only if versions are compatible, otherwise document a separate environment.
- Create or reuse model/, tests/, data/, notes/, experiments/, results/ and reports/. Keep model downloads, generated datasets, checkpoints and credentials out of Git.
- Run fixed 2×3 and 3×2 matrix multiplication and an autograd smoke calculation; reuse existing evidence if it already passes.
- Read the one-page study rhythm, budget cap and save-at-the-hour policy. Install no GPU stack and rent no hardware to begin.

### Environment and repository

Create or reuse isolated CPU environments and the course directories. Record versions and keep downloaded models, generated data and credentials outside committed code. Skip this section if the existing environment already passes.

### Optional tensor and diagnostic refresher

Use the relocated intro-2 tensor checks or1-1 diagnostic only when a prerequisite feels rusty. These are optional readiness tools, not compulsory prerequisite reports.

### Optional concept checkpoints

Preview the checkpoint list only; skip questions whose material has not been learned. Use an individual question when its mechanism has been implemented; the final defense belongs after the experiments. No new scheduled review days.

### When a check fails

Read the four-step stop/save/debug/continue policy; do not manufacture a blocker. As needed inside the current session; save a minimal failure and pause dependent work rather than scheduling Sunday catch-up.

### Architecture comparison template

Preview the implemented/code-traced/paper-only legend; leave evidence cells blank. Use after the architecture tracing lessons to consolidate the existing comparisons.

### Reproducible input and environment template

Create the empty manifest and environment convention, not a fake final checkpoint inventory. Record artifacts as they are produced; use the clean-run instructions when the executable smoke command exists.

### Portfolio cards, report, explanation and release guide

Preview the expected evidence and save the templates. Final reports, recordings and release tags cannot be completed before the project exists. Fill from completed code and measurements; required truthfulness/correctness standards remain visible.

### Reviewer experience checklist

Read what a reviewer should be able to run; no fresh final clone exists yet. After the executable reproduction command exists, use this checklist as a reference; it is not another mandatory class day.

## Study calendar

### Week 1

- Monday (1h): Implement Stable Next-Token Loss
- Tuesday (1h): Implement And Check Causal Attention
- Wednesday (1h): Assemble Your First GPT Block
- Thursday (1h): Finish The Tiny GPT Model
- Friday (1h): Implement A Verified Training Step
- Saturday (2h): Overfit And Sample Tiny Sequences + Save And Resume Model Training
- Sunday: off.

### Week 2

- Monday (1h): Replace Normalization And Feedforward Layers
- Tuesday (1h): Derive And Implement Rotary Positions
- Wednesday (1h): Implement Grouped Query Attention Heads
- Thursday (1h): Validate The Modern Dense Decoder
- Friday (1h): Practice Functional JAX State Handling
- Saturday (2h): Apply JAX Transformations To Primitives + Port Shared Decoder Layer Primitives
- Sunday: off.

### Week 3

- Monday (1h): Verify Cross Framework Primitive Gradients
- Tuesday (1h): Assemble The Functional JAX Decoder
- Wednesday (1h): Match Parameter Layouts Across Frameworks
- Thursday (1h): Implement The Functional Training Step
- Friday (1h): Validate Full Model Numerical Parity
- Saturday (2h): Design And Implement KV Cache + Verify Cached And Full Prefix Logits
- Sunday: off.

### Week 4

- Monday (1h): Freeze Data And Run Training Pilots
- Tuesday (1h): Measure Completed Training Work
- Wednesday (1h): Derive And Implement Low Rank Updates
- Thursday (1h): Check Initialization And Merge Behavior
- Friday (1h): Load The Small Pretrained Decoder
- Saturday (2h): Integrate And Validate LoRA Adapters + Generate And Check Structured Data
- Sunday: off.

### Week 5

- Monday (1h): Prepare Masked SFT And Baseline
- Tuesday (1h): Run The Bounded Fine Tuning Experiment
- Wednesday (1h): Evaluate Structured Task Improvement Honestly
- Thursday (1h): Specify Sparse Expert Routing Shapes
- Friday (1h): Implement The Explicit MoE Forward
- Saturday (2h): Build A Dense Masked Reference + Inspect Routing And Validate Sparse Experts
- Sunday: off.

### Week 6

- Monday (1h): Trace MLA Projection Tensor Dimensions
- Tuesday (1h): Follow Latent And Positional Cache State
- Wednesday (1h): Compare MLA And GQA Memory
- Thursday (1h): Explain Compression And MLA Differences
- Friday (1h): Read The Hybrid Attention Structure
- Saturday (2h): Trace A Single Recurrent Update + Compare State And Cache Scaling
- Sunday: off.

### Week 7

- Monday (1h): Explain The Hybrid Design Tradeoffs
- Tuesday (1h): Map Gemma Components Against Your Decoder
- Wednesday (1h): Map DeepSeek Components Against Your Decoder
- Thursday (1h): Survey Post Training And Multimodal Interfaces
- Friday (1h): Specify A Matched Attention Comparison
- Saturday (2h): Validate Attention And Cache Accounting + Measure Prefill And Decode Separately
- Sunday: off.

### Week 8

- Monday (1h): Interpret The GQA Versus MHA Study
- Tuesday (1h): Build a Controlled Training Experiment
- Wednesday (1h): Run And Inspect The Baseline
- Thursday (1h): Run The Matched Training Ablation
- Friday (1h): Compare Curves And State Limitations
- Saturday (2h): Automate Tiny Training and Numerical Parity + Test Reproduction Failure Handling
- Sunday: off.

### Week 9

- Monday (1h): Prepare a Small Upstream Contribution
- Sunday: off.

## Project standards


Use a tiny configuration for debugging: 2 layers, width 128, a small number of heads, sequence length 32–128. For the main learning run, consider 30–60 million parameters and sequence length 256–512 only if the pilot supports them; a smaller model and token allowance are valid when needed to finish both comparison arms within the available time and budget. Use a fixed tokenizer and a modest, documented TinyStories subset. The parameter count includes embeddings; calculate it rather than trusting a nickname. A 100–300M-token training allowance is a starting ceiling, not a guarantee of useful language quality. A 5–10-minute GPU pilot determines actual tokens/second, peak memory, and the affordable run length. [A12]

Use a deterministic document split before packing/tokenization, with EOS boundaries and a documented cross-document attention policy. For these small labs, keep examples separate or mask boundaries to avoid accidental cross-document leakage. Never split overlapping chunks of the same document across train and validation. Record licenses and model/data revisions. TinyStories is a teaching distribution, not evidence of general coding or reasoning ability.

Must-pass tests:

- Changing token t+1 cannot affect outputs through position t.
- A very small repeated training batch can be strongly overfit with dropout disabled; choose a realistic threshold for that batch, such as cross-entropy below 0.2, and diagnose failures.
- Shared PyTorch/JAX parameters produce matching tiny-model outputs, loss, and gradients. Start FP32 CPU checks around `atol=1e-5, rtol=1e-4`; justify operation-specific changes rather than blindly loosening tolerances. Account for layout, epsilon, precision, and random-number differences.
- Cache-based next-token logits match full-prefix recomputation, including nonzero position offsets. Do not compare sampled text as the primary equality test.
- Resume includes optimizer, schedule, RNG, and data position, not only model weights. Compare resumed and uninterrupted trajectories under the same supported deterministic setup.
- LoRA keeps the base frozen, excludes prompt tokens from the intended SFT loss, and evaluates task correctness separately from syntax validity.

For GQA cache accounting, use `2 × B × L × T × n_kv_heads × head_dim × bytes_per_element`. The factor two is K and V. For standard dense attention scores, memory is proportional to `B × n_query_heads × T × T`. Distinguish model weights, optimizer state, activations, and KV state when explaining memory. Derive an architecture-specific formula for MLA or a recurrent model rather than reusing GQA's formula.

JAX requirements are substantive: a complete functional decoder, explicit parameter/optimizer/RNG state, a jitted train step, shared-weight parity, and a short training run. You need not duplicate every expensive experiment in both frameworks. The scheduled exercises cover `grad`, `vmap` and `jit`. `lax.scan` is an optional control-flow extension after the required work passes; using Flax later is also optional, not a prerequisite for this course.



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

### Architectures and training

- **A1 — [Stanford CS336 Spring 2026](https://cs336.stanford.edu/).** Use lectures on resource accounting, architectures, kernels, inference, data, and post-training. Adapt selected work from [A1 basics](https://github.com/stanford-cs336/assignment1-basics) and [A2 systems](https://github.com/stanford-cs336/assignment2-systems). Do not attempt all five full assignments alongside this curriculum. Pin handout/repository versions; some linked READMEs retain earlier-year labels.
- **A2 — [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783).** Read architecture/training sections and map components to your implementation. It is a baseline for architectural literacy, not a full-scale reproduction target.
- **A3 — [RoFormer](https://arxiv.org/abs/2104.09864) and [GQA](https://arxiv.org/abs/2305.13245).** Focus on rotary-position identities and query/KV grouping. Derive shapes before code.
- **A4 — [JAX documentation](https://docs.jax.dev/en/latest/).** Focus on arrays, pytrees, random keys, transformations, jit/control flow, benchmarking, and autodiff. The [Training Cookbook](https://docs.jax.dev/en/latest/the-training-cookbook.html) is a reference when organizing a training loop.
- **A5 — [LoRA](https://arxiv.org/abs/2106.09685).** Implement the low-rank update and merge behavior. [DPO](https://arxiv.org/abs/2305.18290) and [DeepSeekMath/GRPO](https://arxiv.org/abs/2402.03300) are optional method readings after SFT works.
- **A6 — [SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M).** Practical pretrained dense model for the small SFT lab. Use its model card, exact tokenizer, architecture configuration, license, and revision. A larger model is optional after a memory/time pilot.
- **A7 — [DeepSeekMoE](https://arxiv.org/abs/2401.06066).** Read routing, shared experts, and specialization. Your required toy top-2 layer is intentionally simpler; document that distinction.
- **A8 — [DeepSeek-V2](https://arxiv.org/abs/2405.04434) and [DeepSeek-V3](https://arxiv.org/abs/2412.19437).** Study MLA/cache structure, expert routing, and training-system interactions selectively. Do not imply that a low-rank KV projection alone reproduces the entire design.
- **A9 — [Gated Delta Networks](https://arxiv.org/abs/2412.06464), [Qwen3.5-0.8B-Base](https://huggingface.co/Qwen/Qwen3.5-0.8B-Base), and [Mamba-2](https://arxiv.org/abs/2405.21060).** Trace hybrid recurrent/global-attention trade-offs. For current SSM work, add [Mamba-3](https://arxiv.org/abs/2603.15569) as an optional 2026 reading. Neither SSM is an additional required implementation.
- **A10 — [Gemma 4 official model card](https://ai.google.dev/gemma/docs/core/model_card_4).** Read the linked architecture/report sections relevant to dense/MoE variants, local/global attention and cache choices. Multimodal encoders are survey-only in this text-focused course.
- **A11 — [DeepSeek-V4 technical report](https://arxiv.org/abs/2606.19348).** Current 2026 reading on compressed sparse attention (CSA) and heavily compressed attention (HCA) and associated architecture/training choices. Optional contrasting 2026 direction: [Attention Residuals](https://arxiv.org/abs/2603.15031), concerning information aggregation across depth. Treat published claims as claims; distinguish them from your own measurements.
- **A12 — [TinyStories dataset](https://huggingface.co/datasets/roneneldan/TinyStories) and [paper](https://arxiv.org/abs/2305.07759).** Small-model learning distribution; use a fixed, licensed subset and report the resulting limits.
- **A13 — [nanoGPT](https://github.com/karpathy/nanoGPT) and [nanochat](https://github.com/karpathy/nanochat).** Read concise training/inference code after your unaided attempt. Nanochat is a useful contemporary end-to-end project; its published speedrun uses an 8×H100 node and is not the budget or hardware assumption here. An optional small reproduction must be sized from measured throughput.

### Learning evidence and operating references

- **P1 — [Retrieval practice experiment](https://pubmed.ncbi.nlm.nih.gov/16507066/).** Supports closed-book retrieval for later retention.
- **P2 — [Spacing research](https://www.yorku.ca/ncepeda/publications/CPVWR2006.html).** Supports distributed revisits; exact useful spacing depends on the retention goal.
- **P3 — [Active learning in undergraduate STEM](https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/).** Supports active problem-solving over a lecture-only approach; not direct validation of this exact self-study plan.
- **P4 — [How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245).** A 2026 randomized coding-skill study; interpret its immediate assessment and participant/task setting carefully. It motivates preserving independent reasoning, not a claim that all AI assistance harms learning.
- **C1 — [PyTorch MPS](https://developer.apple.com/metal/pytorch/).** Local Apple GPU setup.
- **C4 — [Runpod prices](https://www.runpod.io/pricing) and [Pod lifecycle](https://docs.runpod.io/pods/manage-pods).** Recheck rates, storage, and stop/terminate semantics before spending. Alternative: [Modal pricing](https://modal.com/pricing).
