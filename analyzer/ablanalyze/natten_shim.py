"""Pure-PyTorch 1-D neighborhood attention with the NATTEN 0.14 call signatures All-In-One expects.

NATTEN 0.14 (which All-In-One was written against) does not build on Apple Silicon with a current
PyTorch, and NATTEN 0.21 renamed everything. All-In-One only uses the 1-D ops, so this module
re-implements them exactly (same clamped windows, same relative-position-bias indexing) and installs
them into `natten.functional` before All-In-One is imported.
"""

from __future__ import annotations

import torch

_INDEX_CACHE: dict[tuple, tuple[torch.Tensor, torch.Tensor]] = {}


def _window_start(i: int, length: int, kernel: int, radius: int, dilation: int) -> int:
    if dilation <= 1:
        start = max(i - radius, 0)
        if i + radius >= length:
            start += length - i - radius - 1
        return start
    ni = i - radius * dilation
    if ni < 0:
        return i % dilation
    if i + radius * dilation >= length:
        imodd = i % dilation
        a = (length // dilation) * dilation
        b = length - a
        if imodd < b:
            return length - b + imodd - 2 * radius * dilation
        return a + imodd - kernel * dilation
    return ni


def _bias_start(i: int, length: int, kernel: int, radius: int, dilation: int) -> int:
    if dilation <= 1:
        start = radius
        if i < radius:
            start += radius - i
        if i + radius >= length:
            start += length - i - 1 - radius
        return start
    if i - radius * dilation < 0:
        return kernel - 1 - (i // dilation)
    if i + radius * dilation >= length:
        return (length - i - 1) // dilation
    return radius


def _indices(length: int, kernel: int, dilation: int, device) -> tuple[torch.Tensor, torch.Tensor]:
    key = (length, kernel, dilation, str(device))
    if key not in _INDEX_CACHE:
        radius = kernel // 2
        kernel = min(kernel, length)
        neighbours = torch.empty((length, kernel), dtype=torch.long)
        bias = torch.empty((length, kernel), dtype=torch.long)
        for i in range(length):
            start = _window_start(i, length, kernel, radius, dilation)
            pb = _bias_start(i, length, kernel, radius, dilation)
            for j in range(kernel):
                neighbours[i, j] = min(max(start + j * dilation, 0), length - 1)
                bias[i, j] = pb + j
        _INDEX_CACHE[key] = (neighbours.to(device), bias.to(device))
    return _INDEX_CACHE[key]


def natten1dqkrpb(query: torch.Tensor, key: torch.Tensor, rpb: torch.Tensor, kernel_size: int, dilation: int) -> torch.Tensor:
    """query, key: [B, heads, L, D]; rpb: [heads, 2*kernel-1] -> scores [B, heads, L, kernel]."""
    b, h, length, d = query.shape
    neighbours, bias = _indices(length, kernel_size, dilation, query.device)
    gathered = key[:, :, neighbours]  # [B, H, L, K, D]
    scores = torch.einsum("bhld,bhlkd->bhlk", query, gathered)
    if rpb is not None:
        bias_index = bias.clamp(0, rpb.shape[-1] - 1)
        scores = scores + rpb[:, bias_index].unsqueeze(0)  # [1, H, L, K]
    return scores


def natten1dav(attn: torch.Tensor, value: torch.Tensor, kernel_size: int, dilation: int) -> torch.Tensor:
    """attn: [B, heads, L, kernel]; value: [B, heads, L, D] -> [B, heads, L, D]."""
    length = value.shape[2]
    neighbours, _ = _indices(length, kernel_size, dilation, value.device)
    gathered = value[:, :, neighbours]  # [B, H, L, K, D]
    return torch.einsum("bhlk,bhlkd->bhld", attn, gathered)


def _indices_2d(height: int, width: int, kernel_size: int, dilation: int, device) -> tuple[torch.Tensor, torch.Tensor]:
    """Flat neighbour indices [H, W, K*K] into an H*W grid, and bias indices into a (2k-1)^2 table."""
    key = ("2d", height, width, kernel_size, dilation, str(device))
    if key not in _INDEX_CACHE:
        nh, bh = _indices(height, kernel_size, dilation, "cpu")
        nw, bw = _indices(width, kernel_size, dilation, "cpu")
        kh, kw = nh.shape[1], nw.shape[1]
        table = 2 * kernel_size - 1
        flat = nh[:, None, :, None] * width + nw[None, :, None, :]  # [H, W, kh, kw]
        bias = bh[:, None, :, None] * table + bw[None, :, None, :]
        _INDEX_CACHE[key] = (flat.reshape(height, width, kh * kw).to(device), bias.reshape(height, width, kh * kw).to(device))
    return _INDEX_CACHE[key]


def natten2dqkrpb(query: torch.Tensor, key: torch.Tensor, rpb: torch.Tensor, kernel_size: int, dilation: int) -> torch.Tensor:
    """query, key: [B, heads, H, W, D]; rpb: [heads, 2k-1, 2k-1] -> scores [B, heads, H, W, K*K]."""
    b, h, height, width, d = query.shape
    neighbours, bias = _indices_2d(height, width, kernel_size, dilation, query.device)
    flat_key = key.reshape(b, h, height * width, d)
    gathered = flat_key[:, :, neighbours]  # [B, H, Hh, Ww, K2, D]
    scores = torch.einsum("bhijd,bhijkd->bhijk", query, gathered)
    if rpb is not None:
        table = rpb.reshape(h, -1)
        scores = scores + table[:, bias.clamp(0, table.shape[-1] - 1)].unsqueeze(0)
    return scores


def natten2dav(attn: torch.Tensor, value: torch.Tensor, kernel_size: int, dilation: int) -> torch.Tensor:
    b, h, height, width, d = value.shape
    neighbours, _ = _indices_2d(height, width, kernel_size, dilation, value.device)
    gathered = value.reshape(b, h, height * width, d)[:, :, neighbours]
    return torch.einsum("bhijk,bhijkd->bhijd", attn, gathered)


def install() -> None:
    import natten.functional as functional

    for name, fn in (("natten1dqkrpb", natten1dqkrpb), ("natten1dav", natten1dav), ("natten2dqkrpb", natten2dqkrpb), ("natten2dav", natten2dav)):
        if not hasattr(functional, name):
            setattr(functional, name, fn)
