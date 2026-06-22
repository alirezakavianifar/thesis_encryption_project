"""Patch code.ipynb with histogram flattening (stage 6)."""
import json
from pathlib import Path

NB = Path(r"e:\projects\thesis_project_v2\code.ipynb")

NEW_ENCRYPT_CELL = r'''def _chaos_byte(val):
    """Map chaotic state in [0,1) to an unbiased 8-bit key."""
    return int(np.floor(val * 256.0)) % 256


def generate_balance_chaos(key: dict, n: int, channel: int, warmup=1000):
    """Independent chaotic sequence for histogram balancing (per channel)."""
    x = (key['x_final'] + (channel + 1) * 0.137) % 1.0
    if x <= 0.0:
        x = 1e-10
    for _ in range(warmup):
        x = logistic(x)
    seq = np.empty(n, dtype=np.float64)
    for k in range(n):
        x = logistic(x)
        seq[k] = x
    return seq


def _uniform_target_counts(n: int):
    base, rem = divmod(n, 256)
    counts = np.full(256, base, dtype=np.int32)
    counts[:rem] += 1
    return counts


def balance_histogram_flat(flat_uint8, chaos):
    """Force an exactly uniform histogram via chaos-ordered surplus swaps."""
    flat = flat_uint8.reshape(-1).astype(np.uint8).copy()
    n = flat.size
    target = _uniform_target_counts(n)
    hist = np.bincount(flat, minlength=256)
    diff = target - hist

    surplus_idx = []
    for v in range(256):
        if diff[v] < 0:
            idxs = np.where(flat == v)[0]
            order = np.argsort(chaos[idxs], kind='mergesort')
            surplus_idx.append(idxs[order[: (-diff[v])]])

    need_vals = []
    for v in range(256):
        if diff[v] > 0:
            need_vals.extend([v] * diff[v])
    need_vals = np.asarray(need_vals, dtype=np.uint8)

    swaps = []
    if surplus_idx:
        surplus_idx = np.concatenate(surplus_idx)
        order = np.argsort(chaos[surplus_idx], kind='mergesort')
        surplus_idx = surplus_idx[order]
        need_vals = need_vals[order]
        for idx, new_val in zip(surplus_idx, need_vals):
            old_val = int(flat[idx])
            flat[idx] = new_val
            swaps.append((int(idx), old_val))

    return flat.reshape(flat_uint8.shape), swaps


def unbalance_histogram_flat(flat_uint8, swaps):
    flat = flat_uint8.reshape(-1).astype(np.uint8).copy()
    for idx, old_val in reversed(swaps):
        flat[idx] = old_val
    return flat.reshape(flat_uint8.shape)


def encrypt_image(image_bgr, key: dict):
    """
    image_bgr: تصویر OpenCV (H×W×3)
    key: {'x0','y0','z0','x_sel','x_ecm','mu','x_final'}
    returns: encrypted image, metadata dict (perm_inv + balance swaps)
    """
    H, W = image_bgr.shape[:2]
    N = H * W

    # ── مرحله ۲: جایگشت با Chen ──────────────────────────────────────────
    chen_seq = generate_chen_sequence(
        key['x0'], key['y0'], key['z0'], N, warmup=1000)
    perm = np.argsort(chen_seq)          # بردار جایگشت
    perm_inv = np.empty_like(perm)
    perm_inv[perm] = np.arange(N)       # جایگشت معکوس

    permuted = np.empty_like(image_bgr)
    for c in range(3):
        flat = image_bgr[:, :, c].flatten()
        permuted[:, :, c] = flat[perm].reshape(H, W)

    # ── مرحله ۳: دنباله انتخاب‌گر ────────────────────────────────────────
    selector = generate_selector_sequence(key['x_sel'], N, warmup=1000)

    # ── مرحله ۴: XOR با سیستم‌های نمایی ─────────────────────────────────
    ecm_states = {i: key['x_ecm'] for i in range(1, 10)}
    for i in range(1, 10):
        x = ecm_states[i]
        for _ in range(1000):
            x = ecm_step(x, i, key['mu'])
        ecm_states[i] = x

    diff_xored = np.empty_like(image_bgr)
    for c in range(3):
        flat_perm = permuted[:, :, c].flatten().astype(np.int32)
        key_bytes = np.empty(N, dtype=np.uint8)
        ecm_st = dict(ecm_states)
        for k in range(N):
            sys_idx = selector[k]
            ecm_st[sys_idx] = ecm_step(ecm_st[sys_idx], sys_idx, key['mu'])
            key_bytes[k] = _chaos_byte(ecm_st[sys_idx])
        diff_xored[:, :, c] = (flat_perm ^ key_bytes.astype(np.int32)).reshape(H, W).astype(np.uint8)

    # ── مرحله ۵: XOR نهایی ───────────────────────────────────────────────
    final_seq = generate_final_sequence(key['x_final'], N, warmup=1000)
    encrypted = np.empty_like(image_bgr)
    for c in range(3):
        flat = diff_xored[:, :, c].flatten().astype(np.int32)
        encrypted[:, :, c] = (flat ^ final_seq.astype(np.int32)).reshape(H, W).astype(np.uint8)

    # ── مرحله ۶: یکنواخت‌سازی هیستوگرام (کاملاً مسطح) ───────────────────
    balance_swaps = []
    for c in range(3):
        chaos_bal = generate_balance_chaos(key, N, c, warmup=1000)
        enc_ch, swaps = balance_histogram_flat(encrypted[:, :, c], chaos_bal)
        encrypted[:, :, c] = enc_ch
        balance_swaps.append(swaps)

    meta = {'perm_inv': perm_inv, 'balance_swaps': balance_swaps}
    return encrypted, meta


def decrypt_image(encrypted_bgr, key: dict, meta):
    H, W = encrypted_bgr.shape[:2]
    N = H * W
    perm_inv = meta['perm_inv']
    balance_swaps = meta['balance_swaps']

    encrypted = encrypted_bgr.copy()

    # ── خنثی‌سازی یکنواخت‌سازی هیستوگرام ─────────────────────────────────
    for c in range(3):
        encrypted[:, :, c] = unbalance_histogram_flat(
            encrypted[:, :, c], balance_swaps[c])

    # ── خنثی‌سازی لایه نهایی ─────────────────────────────────────────────
    final_seq = generate_final_sequence(key['x_final'], N, warmup=1000)
    step4_out = np.empty_like(encrypted_bgr)
    for c in range(3):
        flat = encrypted[:, :, c].flatten().astype(np.int32)
        step4_out[:, :, c] = (flat ^ final_seq.astype(np.int32)).reshape(H, W).astype(np.uint8)

    # ── خنثی‌سازی XOR نمایی ──────────────────────────────────────────────
    selector = generate_selector_sequence(key['x_sel'], N, warmup=1000)
    ecm_states = {i: key['x_ecm'] for i in range(1, 10)}
    for i in range(1, 10):
        x = ecm_states[i]
        for _ in range(1000):
            x = ecm_step(x, i, key['mu'])
        ecm_states[i] = x

    permuted = np.empty_like(encrypted_bgr)
    for c in range(3):
        flat_enc = step4_out[:, :, c].flatten().astype(np.int32)
        key_bytes = np.empty(N, dtype=np.uint8)
        ecm_st = dict(ecm_states)
        for k in range(N):
            sys_idx = selector[k]
            ecm_st[sys_idx] = ecm_step(ecm_st[sys_idx], sys_idx, key['mu'])
            key_bytes[k] = _chaos_byte(ecm_st[sys_idx])
        permuted[:, :, c] = (flat_enc ^ key_bytes.astype(np.int32)).reshape(H, W).astype(np.uint8)

    # ── جایگشت معکوس ─────────────────────────────────────────────────────
    decrypted = np.empty_like(encrypted_bgr)
    for c in range(3):
        flat = permuted[:, :, c].flatten()
        decrypted[:, :, c] = flat[perm_inv].reshape(H, W)

    return decrypted
'''

nb = json.loads(NB.read_text(encoding="utf-8"))

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell.get("source", []))
    if "def encrypt_image(image_bgr, key: dict):" in src and "def decrypt_image" in src:
        cell["source"] = [line + "\n" for line in NEW_ENCRYPT_CELL.split("\n")]
        if cell["source"] and cell["source"][-1] == "\n":
            cell["source"].pop()
        print("patched encrypt/decrypt cell")
    if "enc, perm_inv = encrypt_image(img, DEFAULT_KEY)" in src:
        src = src.replace(
            "enc, perm_inv = encrypt_image(img, DEFAULT_KEY)",
            "enc, meta = encrypt_image(img, DEFAULT_KEY)",
        )
        src = src.replace(
            "dec = decrypt_image(enc, DEFAULT_KEY, perm_inv)",
            "dec = decrypt_image(enc, DEFAULT_KEY, meta)",
        )
        if "hist_cv" not in src:
            src += (
                "\n\ndef _hist_uniformity(channel):\n"
                "    h = np.bincount(channel.flatten(), minlength=256)\n"
                "    return float(h.std() / h.mean() * 100.0)\n"
            )
        if "H_hist_cv" not in src:
            src = src.replace(
                "    results[name] = {",
                "    hist_cv_enc = [_hist_uniformity(enc[:,:,c]) for c in range(3)]\n"
                "    print(f\"  هیستوگرام رمزشده CV% (B,G,R): {[round(v,2) for v in hist_cv_enc]}\")\n\n"
                "    results[name] = {",
            )
            src = src.replace(
                "        'uaci': uaci_val,\n",
                "        'uaci': uaci_val,\n"
                "        'hist_cv_enc': hist_cv_enc,\n",
            )
        cell["source"] = [line + "\n" for line in src.split("\n")]
        if cell["source"] and cell["source"][-1] == "\n":
            cell["source"].pop()
        print("patched main execution cell")

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("done")
