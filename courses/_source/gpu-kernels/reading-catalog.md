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
