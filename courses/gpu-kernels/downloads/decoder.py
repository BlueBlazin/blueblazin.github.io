"""A tiny, untrained PyTorch decoder for the GPU Kernels course.

This is a deterministic benchmark and correctness fixture, not a trained language
model. No tokenizer, dataset, model download, or architecture-course work is
required. Install PyTorch in your course environment, then run:

    python decoder.py --device cpu --seed 0
    python decoder.py --device cuda --seed 0

Public API:
    model = create_fixture(device="cpu", seed=0)
    logits = model(input_ids)  # [batch, new_tokens, vocab_size]
    logits, cache = model(input_ids, use_cache=True)
    next_logits, cache = model(next_ids, cache=cache, use_cache=True)

``input_ids`` must be torch.long with shape [batch, new_tokens]. When passing a
cache, pass ONLY new tokens, not the complete prefix. Reset a sequence by passing
cache=None. The cache is a tuple of LayerKV(key, value), one entry per layer;
each tensor has shape [batch, heads, cached_tokens, head_dim]. The cache is an
explicit return value, never hidden mutable state. Use torch.no_grad() or
torch.inference_mode() for inference: cache tensors are not detached for you.

The model uses learned absolute positions, pre-RMSNorm residual blocks, causal
multi-head attention, and a GELU MLP. The exported rmsnorm_reference and
causal_attention_reference helpers use FP32 arithmetic for ordinary inputs and
preserve FP64 for derivative checks. Cache concatenation allocates memory: this is a reference implementation,
not an optimized serving engine. It intentionally contains no custom GPU kernels.

For the RMSNorm exercise, replace RMSNorm.forward or pass a norm_factory taking
(width, eps) and returning a compatible nn.Module. Preserve the reference module
for parity checks and copy its weights into the candidate before comparing.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Callable, NamedTuple

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class DecoderConfig:
    vocab_size: int = 128
    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    mlp_ratio: int = 4
    max_seq_len: int = 256
    rms_eps: float = 1e-5

    def __post_init__(self) -> None:
        for name in (
            "vocab_size", "d_model", "n_heads", "n_layers", "mlp_ratio", "max_seq_len"
        ):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")
        if self.d_model % self.n_heads:
            raise ValueError("d_model must be divisible by n_heads")
        if self.rms_eps <= 0:
            raise ValueError("rms_eps must be positive")


class LayerKV(NamedTuple):
    key: Tensor
    value: Tensor


KVCache = tuple[LayerKV, ...]
NormFactory = Callable[[int, float], nn.Module]


def rmsnorm_reference(x: Tensor, weight: Tensor, eps: float = 1e-5) -> Tensor:
    """RMSNorm over the last dimension; return the same shape and dtype as x.

    x has shape [..., width], weight has shape [width], and both are floating
    tensors on one device. Reduction and multiplication use FP32, or FP64 when
    either input is FP64. The latter supports torch.autograd.gradcheck without
    silently truncating its small perturbations. eps is added to mean(x**2).
    """
    if x.ndim < 1 or x.shape[-1] == 0 or weight.ndim != 1:
        raise ValueError("expected x[..., width] and weight[width], with width > 0")
    if weight.shape[0] != x.shape[-1]:
        raise ValueError("weight length must equal x's last dimension")
    if x.device != weight.device or not (x.is_floating_point() and weight.is_floating_point()):
        raise ValueError("x and weight must be floating tensors on the same device")
    if eps <= 0:
        raise ValueError("eps must be positive")
    dtype = torch.float64 if torch.float64 in (x.dtype, weight.dtype) else torch.float32
    values = x.to(dtype)
    inv_rms = torch.rsqrt(values.square().mean(dim=-1, keepdim=True) + eps)
    return (values * inv_rms * weight.to(dtype)).to(x.dtype)


def causal_attention_reference(
    q: Tensor, k: Tensor, v: Tensor, query_offset: int = 0
) -> Tensor:
    """Dense causal attention returning [B, H, Tq, D] in q's dtype.

    q is [B, H, Tq, D]; k and v are [B, H, Tk, D]. Batch, heads, head dimension,
    device, and floating dtype must agree. This is ordinary multi-head attention
    (including H=1), with no GQA broadcasting. All dimensions must be positive.

    Query i may attend to key j exactly when j <= query_offset + i. Use offset=0
    for a full sequence; for cached decode use the previous cache length, with
    both previous and newly projected keys/values already concatenated in k/v.
    Scores, softmax, and the probability/value product use FP32 unless inputs
    are FP64, in which case FP64 is preserved for numerical derivative checks.
    No dropout or implicit cache mutation is performed.
    """
    if any(t.ndim != 4 for t in (q, k, v)):
        raise ValueError("q, k, and v must be rank-4 tensors [B, H, tokens, D]")
    if any(d <= 0 for t in (q, k, v) for d in t.shape):
        raise ValueError("all q/k/v dimensions must be positive")
    if k.shape != v.shape or q.shape[:2] != k.shape[:2] or q.shape[-1] != k.shape[-1]:
        raise ValueError("expected q[B,H,Tq,D] and k/v[B,H,Tk,D]; GQA is not supported")
    if any(t.device != q.device or t.dtype != q.dtype for t in (k, v)) or not q.is_floating_point():
        raise ValueError("q, k, and v must share a floating dtype and device")
    if not isinstance(query_offset, int) or query_offset < 0:
        raise ValueError("query_offset must be a nonnegative integer")
    dtype = torch.float64 if q.dtype == torch.float64 else torch.float32
    query_positions = query_offset + torch.arange(q.shape[2], device=q.device)
    key_positions = torch.arange(k.shape[2], device=q.device)
    allowed = key_positions[None, :] <= query_positions[:, None]
    scores = (q.to(dtype) @ k.to(dtype).transpose(-2, -1)) / math.sqrt(q.shape[-1])
    scores = scores.masked_fill(~allowed[None, None, :, :], float("-inf"))
    probabilities = torch.softmax(scores, dim=-1)
    return (probabilities @ v.to(dtype)).to(q.dtype)


class RMSNorm(nn.Module):
    """Replaceable RMSNorm module using the exported reference function."""

    def __init__(self, width: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(width))
        self.eps = eps

    def forward(self, x: Tensor) -> Tensor:
        return rmsnorm_reference(x, self.weight, self.eps)


class CausalAttention(nn.Module):
    def __init__(self, config: DecoderConfig) -> None:
        super().__init__()
        self.n_heads = config.n_heads
        self.head_dim = config.d_model // config.n_heads
        self.qkv = nn.Linear(config.d_model, 3 * config.d_model, bias=False)
        self.output = nn.Linear(config.d_model, config.d_model, bias=False)

    def forward(self, x: Tensor, past: LayerKV | None) -> tuple[Tensor, LayerKV]:
        batch, length, width = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        q, k, v = (
            t.reshape(batch, length, self.n_heads, self.head_dim).transpose(1, 2)
            for t in (q, k, v)
        )
        offset = 0 if past is None else past.key.shape[2]
        if past is not None:
            k = torch.cat((past.key, k), dim=2)
            v = torch.cat((past.value, v), dim=2)

        attended = causal_attention_reference(q, k, v, query_offset=offset)
        attended = attended.transpose(1, 2).contiguous().reshape(batch, length, width)
        return self.output(attended), LayerKV(k, v)


class DecoderBlock(nn.Module):
    def __init__(self, config: DecoderConfig, norm_factory: NormFactory) -> None:
        super().__init__()
        self.attn_norm = norm_factory(config.d_model, config.rms_eps)
        self.attention = CausalAttention(config)
        self.mlp_norm = norm_factory(config.d_model, config.rms_eps)
        self.mlp = nn.Sequential(
            nn.Linear(config.d_model, config.d_model * config.mlp_ratio, bias=False),
            nn.GELU(),
            nn.Linear(config.d_model * config.mlp_ratio, config.d_model, bias=False),
        )

    def forward(self, x: Tensor, past: LayerKV | None) -> tuple[Tensor, LayerKV]:
        attended, updated = self.attention(self.attn_norm(x), past)
        x = x + attended
        x = x + self.mlp(self.mlp_norm(x))
        return x, updated


class TinyDecoder(nn.Module):
    def __init__(
        self, config: DecoderConfig | None = None, norm_factory: NormFactory = RMSNorm
    ) -> None:
        super().__init__()
        self.config = config if config is not None else DecoderConfig()
        config = self.config
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embedding = nn.Embedding(config.max_seq_len, config.d_model)
        self.blocks = nn.ModuleList(
            DecoderBlock(config, norm_factory) for _ in range(config.n_layers)
        )
        self.final_norm = norm_factory(config.d_model, config.rms_eps)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

    def forward(
        self, input_ids: Tensor, cache: KVCache | None = None, use_cache: bool = False
    ) -> Tensor | tuple[Tensor, KVCache]:
        """Return new-token logits, optionally paired with the updated cache.

        A supplied cache is consumed even when use_cache=False; that flag controls
        only whether the updated cache is returned. A cached prefix must describe
        these same batch rows, in the same order, under the same model weights.
        """
        if input_ids.ndim != 2 or input_ids.dtype != torch.long:
            raise ValueError("input_ids must be torch.long with shape [batch, tokens]")
        batch, length = input_ids.shape
        if batch == 0 or length == 0:
            raise ValueError("input_ids must contain at least one batch row and token")
        if input_ids.device != self.token_embedding.weight.device:
            raise ValueError("input_ids and model must be on the same device")
        offset = self._validate_cache(cache, batch, input_ids.device)
        if offset + length > self.config.max_seq_len:
            raise ValueError("prefix plus new tokens exceeds config.max_seq_len")
        positions = torch.arange(offset, offset + length, device=input_ids.device)
        x = self.token_embedding(input_ids) + self.position_embedding(positions)[None, :, :]
        updated = []
        for index, block in enumerate(self.blocks):
            x, layer_cache = block(x, None if cache is None else cache[index])
            if use_cache:
                updated.append(layer_cache)
        logits = self.lm_head(self.final_norm(x))
        return (logits, tuple(updated)) if use_cache else logits

    def _validate_cache(
        self, cache: KVCache | None, batch: int, device: torch.device
    ) -> int:
        if cache is None:
            return 0
        if not isinstance(cache, tuple) or len(cache) != self.config.n_layers:
            raise ValueError("cache must be a tuple with one LayerKV per layer")
        offset = None
        head_dim = self.config.d_model // self.config.n_heads
        for entry in cache:
            if not isinstance(entry, LayerKV) or entry.key.ndim != 4:
                raise ValueError("each cache entry must be LayerKV with rank-4 tensors")
            if offset is None:
                offset = entry.key.shape[2]
            expected = (batch, self.config.n_heads, offset, head_dim)
            if tuple(entry.key.shape) != expected or tuple(entry.value.shape) != expected:
                raise ValueError(f"cache tensors must all have shape {expected}")
            if entry.key.device != device or entry.value.device != device:
                raise ValueError("cache and input_ids must be on the same device")
            if entry.key.dtype != entry.value.dtype or not entry.key.is_floating_point():
                raise ValueError("cache keys and values must have the same floating dtype")
        return int(offset)


def create_fixture(
    device: str | torch.device = "cpu",
    seed: int = 0,
    config: DecoderConfig | None = None,
    norm_factory: NormFactory = RMSNorm,
) -> TinyDecoder:
    """Build reproducible CPU-initialized weights, move them, and return eval mode.

    CPU initialization makes a given seed independent of the selected device and
    leaves the caller's CPU RNG state unchanged. This does not promise bitwise
    identical arithmetic across different devices or PyTorch versions.
    """
    with torch.random.fork_rng(devices=[]):
        torch.random.default_generator.manual_seed(seed)
        model = TinyDecoder(config, norm_factory=norm_factory)
        for module in model.modules():
            if isinstance(module, (nn.Linear, nn.Embedding)):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
    return model.to(device).eval()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA was requested but is unavailable in this PyTorch environment")

    model = create_fixture(device=args.device, seed=args.seed)
    generator = torch.Generator(device="cpu").manual_seed(args.seed + 1)
    input_ids = torch.randint(model.config.vocab_size, (2, 32), generator=generator).to(args.device)
    with torch.inference_mode():
        full = model(input_ids)
        cache = None
        pieces = []
        for token in input_ids.split(1, dim=1):
            logits, cache = model(token, cache=cache, use_cache=True)
            pieces.append(logits)
        incremental = torch.cat(pieces, dim=1)
        torch.testing.assert_close(incremental, full, atol=2e-5, rtol=1e-4)

        chunk_cache = None
        chunk_outputs = []
        for chunk in input_ids.split((7, 9, 16), dim=1):
            logits, chunk_cache = model(chunk, cache=chunk_cache, use_cache=True)
            chunk_outputs.append(logits)
        chunked = torch.cat(chunk_outputs, dim=1)
        torch.testing.assert_close(chunked, full, atol=2e-5, rtol=1e-4)

    print(f"device={args.device} seed={args.seed} parameters={sum(p.numel() for p in model.parameters()):,}")
    print(f"input_ids={tuple(input_ids.shape)} logits={tuple(full.shape)}")
    print(f"cache_layers={len(cache)} key/value_shape={tuple(cache[0].key.shape)}")
    print(f"single-token cache parity: PASS (max_abs_error={(incremental - full).abs().max().item():.3g})")
    print(f"chunked cache parity: PASS (max_abs_error={(chunked - full).abs().max().item():.3g})")
    print("Untrained reference fixture; parity is a correctness check, not a speed or quality score.")


if __name__ == "__main__":
    main()
