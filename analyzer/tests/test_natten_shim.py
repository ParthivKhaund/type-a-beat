import torch

from ablanalyze.natten_shim import _bias_start, _window_start, natten1dav, natten1dqkrpb, natten2dav, natten2dqkrpb


def test_interior_window_is_centred_and_edges_are_clamped():
    assert _window_start(5, 20, 7, 3, 1) == 2
    assert _window_start(0, 20, 7, 3, 1) == 0
    assert _window_start(19, 20, 7, 3, 1) == 13


def test_bias_index_puts_the_query_at_the_centre_of_the_table():
    kernel, radius = 7, 3
    assert _bias_start(5, 20, kernel, radius, 1) + radius == 2 * radius  # centre of a 2k-1 table
    assert _bias_start(0, 20, kernel, radius, 1) == 2 * radius


def test_dilated_windows_stay_on_the_same_residue():
    starts = [_window_start(i, 40, 5, 2, 3) for i in range(40)]
    assert all((s - i) % 3 == 0 for i, s in enumerate(starts))
    assert all(0 <= s and s + 4 * 3 < 40 for s in starts)


def test_qk_then_av_matches_a_brute_force_reference():
    torch.manual_seed(0)
    b, h, length, d, k = 1, 2, 11, 4, 5
    q, kk, v = torch.randn(b, h, length, d), torch.randn(b, h, length, d), torch.randn(b, h, length, d)
    rpb = torch.randn(h, 2 * k - 1)
    scores = natten1dqkrpb(q, kk, rpb, k, 1)
    out = natten1dav(torch.softmax(scores, -1), v, k, 1)
    radius = k // 2
    for i in range(length):
        start = min(max(i - radius, 0), length - k)
        idx = list(range(start, start + k))
        ref_scores = torch.stack([(q[0, :, i] * kk[0, :, j]).sum(-1) + rpb[:, (j - i) + (k - 1)] for j in idx], dim=-1)
        assert torch.allclose(scores[0, :, i], ref_scores, atol=1e-5)
        probs = torch.softmax(ref_scores, -1)
        ref_out = sum(probs[:, n, None] * v[0, :, j] for n, j in enumerate(idx))
        assert torch.allclose(out[0, :, i], ref_out, atol=1e-5)


def test_2d_qk_then_av_matches_a_brute_force_reference():
    torch.manual_seed(1)
    b, h, hh, ww, d, k = 1, 2, 9, 7, 3, 3
    q, kk, v = torch.randn(b, h, hh, ww, d), torch.randn(b, h, hh, ww, d), torch.randn(b, h, hh, ww, d)
    rpb = torch.randn(h, 2 * k - 1, 2 * k - 1)
    scores = natten2dqkrpb(q, kk, rpb, k, 1)
    out = natten2dav(torch.softmax(scores, -1), v, k, 1)
    r = k // 2
    for i in range(hh):
        for j in range(ww):
            si, sj = min(max(i - r, 0), hh - k), min(max(j - r, 0), ww - k)
            cells = [(a, c) for a in range(si, si + k) for c in range(sj, sj + k)]
            ref = torch.stack([(q[0, :, i, j] * kk[0, :, a, c]).sum(-1) + rpb[:, a - i + k - 1, c - j + k - 1] for a, c in cells], dim=-1)
            assert torch.allclose(scores[0, :, i, j], ref, atol=1e-5)
            probs = torch.softmax(ref, -1)
            ref_out = sum(probs[:, n, None] * v[0, :, a, c] for n, (a, c) in enumerate(cells))
            assert torch.allclose(out[0, :, i, j], ref_out, atol=1e-5)
