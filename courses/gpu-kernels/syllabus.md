# GPU Kernels & Optimization

53 scheduled hands-on hours over 8 weeks. Day 0 contains setup, review and administration outside the regular calendar. Weekdays: 1 hour. Saturday: up to 2 hours. Sunday: off.

## Day 0

One setup and course-operations page, with start-now tasks and clearly marked later-use references. Do not attempt future experiments or finish every checklist before Day1. First technical lab runs locally with Python; rent GPUs only before the actual CUDA/Triton or Pallas work.

- I can run a Python script on my M1 Max.
- I have a working folder or repository for the local first lab.
- I know which NVIDIA and H100 readiness checkpoints will be needed later.
- I know the A$450 kernel allowance is part of the combined A$1,000 ceiling.
- I understand that later reviews and release checklists are references to use when their results exist.

### Start here:local tools and fixture

At the beginning. Set a sustainable schedule, create the repository, and prepare the local Python/PyTorch fixture when needed. If Python already works, you can begin Day1 immediately. Keep the A$450 kernel ceiling inside the A$1,000 combined ceiling.

### Before the first NVIDIA lab

Immediately before 1-3. Choose and record a compatible image, verify CUDA/Triton and `nvcc`/compiler/Ninja for the CUDA extension, run the smoke, export evidence and stop billing when finished. Do not rent hardware merely to read this section.

### Before the first Pallas GPU lab

Immediately before 11-3. Use the official current-compatible H100/Mosaic path. Execute the minimal actual-device smoke before porting the row kernel. Source study11-2 can happen locally first.

### Clean-environment recipe

After13-4, before 14-4. Rebuild only the environment and existing benchmark needed for the reproduction experiment. Later experiment artifacts are prerequisites, not Day0 deliverables.

### Measurement and understanding checklists

At the corresponding technical milestones. Use on demand to diagnose a real evidence gap. No numbered review days, no mandatory rerun of already sound results, and no claims of having future measurements during setup.

### When something blocks progress

As needed. Save the smallest reproducer and use the next study slot. Shift dependent lessons rather than filling Sundays or scheduling fixed filler days.

### Report, release and contribution guide

After substantive technical artifacts exist. Use the report template and release checklist when ready. Retain honest limits and negative results. Publishing is the learner’s choice. These are common references, not fake Day0 accomplishments.

## Study calendar

### Week 1

- Monday (1h): Model GPU Indexing and Memory Traffic Locally
- Tuesday (1h): Build Reliable GPU Timing Utilities
- Wednesday (1h): Profile and Explain Dominant Operations
- Thursday (1h): Write CUDA Vector Addition Indexing
- Friday (1h): Validate CUDA Boundaries and Timing
- Saturday (2h): Implement Triton Vector Addition Masks + Compare Both Vector Addition Implementations
- Sunday: off.

### Week 2

- Monday (1h): Derive Stable Row Softmax
- Tuesday (1h): Implement Triton Softmax Reductions
- Wednesday (1h): Handle Softmax Tails and Extremes
- Thursday (1h): Benchmark Softmax Against Both Baselines
- Friday (1h): Specify RMSNorm Precision and Shapes
- Saturday (2h): Implement Triton RMSNorm Forward + Validate RMSNorm Across Row Shapes
- Sunday: off.

### Week 3

- Monday (1h): Measure RMSNorm Wins and Losses
- Tuesday (1h): Derive Tiled Matrix Multiplication
- Wednesday (1h): Implement Triton Matmul Tile Loop
- Thursday (1h): Support Matmul Boundaries and Strides
- Friday (1h): Validate Tensor Core Matmul Precision
- Saturday (2h): Freeze Matmul Tuning and Baselines + Measure Tile Reuse and Occupancy
- Sunday: off.

### Week 4

- Monday (1h): Fuse One Matmul Output Epilogue
- Tuesday (1h): Explain Matmul Performance Tradeoffs Clearly
- Wednesday (1h): Derive Online Softmax State Updates
- Thursday (1h): Verify Online Softmax Tile Merges
- Friday (1h): Implement Blockwise Causal Attention Reference
- Saturday (2h): Validate Attention Recurrence and Memory + Specify Restricted Triton Attention Forward
- Sunday: off.

### Week 5

- Monday (1h): Implement Attention Tiles and Online State
- Tuesday (1h): Validate Attention Causality and Tails
- Wednesday (1h): Benchmark Restricted Attention Forward Correctness
- Thursday (1h): Derive RMSNorm Input and Weight Gradients
- Friday (1h): Implement RMSNorm Input Gradient Kernel
- Saturday (2h): Implement RMSNorm Weight Gradient Reduction + Validate Actual GPU Gradient Dtypes
- Sunday: off.

### Week 6

- Monday (1h): Register the Custom Triton Operator
- Tuesday (1h): Connect Autograd and Unsupported Cases
- Wednesday (1h): Integrate RMSNorm Into the Decoder
- Thursday (1h): Profile Integration and Amdahl Limits
- Friday (1h): Map Pallas Refs Grids and Memory
- Saturday (2h): Port One Row Kernel to Pallas + Validate the Pallas GPU Kernel
- Sunday: off.

### Week 7

- Monday (1h): Benchmark Pallas Against Jitted JAX
- Tuesday (1h): Trace Hopper Pipelined Matmul Stages
- Wednesday (1h): Study Modern Attention Hardware Tradeoffs
- Thursday (1h): Freeze End To End Decoder Measurements
- Friday (1h): Measure Decoder Prefill and Transfers
- Saturday (2h): Measure Cached Decode Across Lengths + Report Whole Model Gains and Regressions
- Sunday: off.

### Week 8

- Monday (1h): Inspect One Optional Kernel DSL
- Tuesday (1h): Reproduce the Main Kernel Result
- Wednesday (1h): Build a Minimal Reproducer and Focused Fix
- Thursday (1h): Verify the Regression or Support Boundary
- Sunday: off.

## Project standards


Specify exactly which shapes, strides, dtypes, masks, and gradients each operator supports. Test zeros, repeated values, extreme finite logits, random seeds, tile boundaries, and non-power-of-two tails. Test non-contiguous inputs only if supported; otherwise reject them or fall back. Define all-masked-row behavior explicitly if the interface permits such inputs.

Use FP32 references and small FP64 CPU derivative checks where appropriate. Mixed-precision tolerances depend on the operation, reduction length, and accumulation dtype; there is no universal BF16 threshold. Validate actual GPU gradients against a reference at supported dtypes. Check memory/race behavior with supported tooling when necessary and record any environment restriction.

Freeze a shape matrix before tuning, for example row widths 127/128/129/768/1024/4096, several row counts, GEMM dimensions on both sides of a tile boundary, and attention lengths 63/64/65/256/1024. Separate supported correctness tests from performance shapes. Keep a few shapes untouched until the final performance run.

Compare custom code against both eager and compiled framework code. For attention and matmul, also compare against SDPA and optimized library matmul. Set dropout, causal convention, TF32/matmul precision, layout, and dtype consistently. A speedup only against an avoidably poor reference is insufficient.

Warm up compilation and autotuning, use resident inputs, synchronize correctly, and time repeated runs. Report median and variability across at least three independent timing batches. Keep cold compile/setup costs separate. JAX needs `block_until_ready()`; CUDA work needs appropriate events/synchronization. Record thermal/shared-machine noise. Never benchmark competing candidates concurrently on one GPU.

The required FlashAttention lab is a restricted forward implementation explaining IO avoidance and online normalization. Production features, general backward, every mask type, and every head dimension are not required. The differentiable integration requirement is satisfied by RMSNorm. If the broad attention kernel exceeds its timebox, narrow to a restricted Triton forward, such as one head dimension and bounded lengths. If that still does not work, extend the schedule instead of claiming GPU completion.

A useful systems report explains where the kernel wins, where it loses, and whether it affects model throughput. No fixed speedup percentage is a graduation requirement. Correct negative results count.



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

### GPU kernels and optimization

- **K1 — [GPU MODE lecture materials](https://github.com/gpu-mode/lectures).** Select profiling, CUDA execution, GPU memory, reductions, Triton, and FlashAttention topics. Skip unrelated lectures until needed.
- **K2 — [CUDA C++ Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html).** Use memory access, timing, occupancy, and precision sections while interpreting your own profiles.
- **K3 — [Official Triton tutorials](https://triton-lang.org/main/getting-started/tutorials/index.html).** Work through vector addition, fused softmax, matrix multiplication, normalization, and fused attention in that order, implementing before comparing with reference code.
- **K4 — [FlashAttention](https://arxiv.org/abs/2205.14135) and [FlashAttention-2](https://arxiv.org/abs/2307.08691).** Derive IO savings and online softmax; implement the restricted forward exercise. The [official repository](https://github.com/Dao-AILab/flash-attention) provides current hardware constraints.
- **K5 — [PyTorch custom Triton integration](https://docs.pytorch.org/tutorials/recipes/torch_compile_user_defined_triton_kernel_tutorial.html).** Study `torch.library.triton_op`, composition with compile, and autograd registration. Use the guidance matching your pinned version.
- **K6 — [Pallas GPU quickstart](https://docs.jax.dev/en/latest/pallas/gpu/quickstart.html), [Pallas overview](https://docs.jax.dev/en/latest/pallas/index.html), and [Hopper pipelined matmul](https://docs.jax.dev/en/latest/pallas/gpu/pipelining.html#example-matmul-kernel-on-hopper-gpus).** Use actual H100 execution and the documented Mosaic GPU programming model.
- **K7 — [FlashAttention-4](https://arxiv.org/abs/2603.05451), [author engineering article](https://www.together.ai/blog/flashattention-4), and [CuTe DSL quickstart](https://docs.nvidia.com/cutlass/latest/media/docs/pythonDSL/quick_start.html).** Read hardware bottleneck shifts and a code example. [FlexAttention with FA4](https://pytorch.org/blog/flexattention-flashattention-4-fast-and-flexible/) is optional because the integration's compatible versions can be fast-moving.
- **K8 — [Helion](https://pytorch.org/projects/helion/) and [KernelBench](https://github.com/ScalingIntelligence/KernelBench).** Optional continuation: compare a higher-level kernel DSL, or let your agent propose kernels in a correctness-gated isolated worker. Keep evaluator/reference code outside the candidate's writable area and recompute baselines on your hardware.

### Learning evidence and operating references

- **P1 — [Retrieval practice experiment](https://pubmed.ncbi.nlm.nih.gov/16507066/).** Supports closed-book retrieval for later retention.
- **P2 — [Spacing research](https://www.yorku.ca/ncepeda/publications/CPVWR2006.html).** Supports distributed revisits; exact useful spacing depends on the retention goal.
- **P3 — [Active learning in undergraduate STEM](https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/).** Supports active problem-solving over a lecture-only approach; not direct validation of this exact self-study plan.
- **P4 — [How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245).** A 2026 randomized coding-skill study; interpret its immediate assessment and participant/task setting carefully. It motivates preserving independent reasoning, not a claim that all AI assistance harms learning.
- **C1 — [PyTorch MPS](https://developer.apple.com/metal/pytorch/).** Local Apple GPU setup.
- **C2 — [JAX installation](https://docs.jax.dev/en/latest/installation.html).** Official platform support and GPU installation paths.
- **C3 — [Pallas quickstart](https://docs.jax.dev/en/latest/pallas/quickstart.html).** Backend support and current GPU path; check alongside K6.
- **C4 — [Runpod prices](https://www.runpod.io/pricing) and [Pod lifecycle](https://docs.runpod.io/pods/manage-pods).** Recheck rates, storage, and stop/terminate semantics before spending. Alternative: [Modal pricing](https://modal.com/pricing).
