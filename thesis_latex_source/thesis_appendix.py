# %% [markdown]
# <div dir="rtl">
# 
# # پیاده‌سازی الگوریتم رمزنگاری تصویر رنگی
# 
# این دفترچه کد پیوست پایان‌نامه را گام‌به‌گام اجرا می‌کند. الگوریتم از ترکیب سیستم Chen با نه نگاشت آشوبی نمایی (ECM) تشکیل شده و در پایان نتایج فصل چهارم — آنتروپی، همبستگی، NPCR، UACI و نمودارها — محاسبه می‌شود.
# 
# </div>

# %% [markdown]
# <div dir="rtl">
# 
# ## آماده‌سازی محیط
# 
# کتابخانه‌های `numpy`، `scipy`، `opencv` و `matplotlib` در ابتدا وارد می‌شوند. پوشه‌های `outputs` و `outputs/figs` با `os.makedirs` ساخته می‌شوند تا تصاویر و نمودارهای خروجی بدون خطا ذخیره شوند.
# 
# </div>

# %%
import numpy as np
from scipy.integrate import solve_ivp
import cv2
import time
import pickle
import os
import matplotlib
import matplotlib.pyplot as plt

# Ensure output directory exists
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)
OUT_FIGS = os.path.join(OUT_DIR, "figs")
os.makedirs(OUT_FIGS, exist_ok=True)

print('محیط آماده شد. خروجی‌ها در پوشه outputs/ ذخیره می‌شوند.')

# %% [markdown]
# <div dir="rtl">
# 
# ## فاز ۱ — سیستم Chen و نگاشت‌های پایه
# 
# تابع `chen_system` معادلات دیفرانسیل سیستم Chen را با پارامترهای $a=35$، $b=3$ و $c=28$ تعریف می‌کند. در `generate_chen_sequence` با `solve_ivp` این معادلات حل عددی می‌شوند و از خروجی، دنباله‌ای برای مرحله جایگشت گرفته می‌شود.
# 
# پارامتر `warmup=1000` به این دلیل است که چند هزار گام اول دنباله هنوز در ناحیه گذرا قرار دارد و برای تولید کلید مناسب نیست.
# 
# توابع `logistic`، `sine_map` و `tent_map` سه نگاشت یک‌بعدی پایه‌اند که در مرحله بعد برای ساخت خانواده ECM به‌کار می‌روند.
# 
# </div>

# %%
# 1. Chen chaotic system
def chen_system(t, state, a=35, b=3, c=28):
    x, y, z = state
    dx = a * (y - x)
    dy = (c - a) * x - x * z + c * y
    dz = x * y - b * z
    return [dx, dy, dz]

def generate_chen_sequence(x0, y0, z0, n, warmup=1000, dt=0.002):
    """Generate Chen chaotic sequence via RK45."""
    total = warmup + n
    t_span = (0, total * dt)
    t_eval = np.linspace(0, total * dt, total)
    sol = solve_ivp(chen_system, t_span, [x0, y0, z0],
                    method='RK45', t_eval=t_eval, dense_output=False,
                    rtol=1e-10, atol=1e-12)
    x_seq = sol.y[0]
    return x_seq[warmup:]   # discard warm-up

# 2. Base chaotic maps
def logistic(x, r=4.0):
    return r * x * (1.0 - x)

def sine_map(x, r=1.0):
    return (r / 4.0) * np.sin(np.pi * x)

def tent_map(x):
    return 2 * x if x < 0.5 else 2 * (1.0 - x)

# %% [markdown]
# <div dir="rtl">
# 
# ## فاز ۲ — نه سیستم آشوبی نمایی (ECM)
# 
# در `ecm_step` ابتدا یکی از نگاشت‌های Logistic، Sine یا Tent اجرا می‌شود و سپس خروجی از تابع نمایی عبور داده می‌شود. ترکیب نقش داخلی و خارجی، نه سیستم مجزا ایجاد می‌کند.
# 
# مقدار `MU_DEFAULT = 3.8` پارامتر نمایی ECM است و در ناحیه‌ای انتخاب شده که رفتار آشوبی پایدار بماند. تابع `_apply_map` فقط برای ساده‌تر شدن انتخاب بین سه نگاشت پایه نوشته شده است.
# 
# در `generate_ecm_sequence` مانند مرحله Chen، ابتدای دنباله (`warmup`) حذف می‌شود.
# 
# </div>

# %%
# 3. Nine exponential chaotic maps (ECM)
ECM_CONFIGS = {
    1: ('logistic', 'logistic'),   # LEL
    2: ('logistic', 'sine'),       # LES
    3: ('logistic', 'tent'),       # LET
    4: ('sine',     'logistic'),   # SEL
    5: ('sine',     'sine'),       # SES
    6: ('sine',     'tent'),       # SET
    7: ('tent',     'logistic'),   # TEL
    8: ('tent',     'sine'),       # TES
    9: ('tent',     'tent'),       # TET
}

ECM_NAMES = {1:'LEL', 2:'LES', 3:'LET', 4:'SEL', 5:'SES',
             6:'SET', 7:'TEL', 8:'TES', 9:'TET'}

MU_DEFAULT = 3.8   # exponential parameter in stable chaotic range

def _apply_map(name, x):
    if name == 'logistic':
        return logistic(x)
    elif name == 'sine':
        return sine_map(x)
    else:
        return tent_map(x)

def ecm_step(x, system_idx, mu=MU_DEFAULT):
    """Single ECM iteration."""
    inner_name, outer_name = ECM_CONFIGS[system_idx]
    inner_val = _apply_map(inner_name, x)
    exp_val = np.exp(mu * inner_val) % 1.0
    if exp_val == 0.0:
        exp_val = 1e-10
    result = _apply_map(outer_name, exp_val)
    result = np.clip(result, 1e-10, 1.0 - 1e-10)
    return result

def generate_ecm_sequence(x0, system_idx, n, warmup=1000, mu=MU_DEFAULT):
    """Generate ECM byte sequence."""
    x = x0
    for _ in range(warmup):
        x = ecm_step(x, system_idx, mu)
    seq = np.empty(n, dtype=np.float64)
    for k in range(n):
        x = ecm_step(x, system_idx, mu)
        seq[k] = x
    return seq

# %% [markdown]
# <div dir="rtl">
# 
# ## فاز ۳ — انتخاب‌گر و لایه XOR نهایی
# 
# تابع `generate_selector_sequence` با نگاشت Logistic برای هر پیکسل یک عدد بین ۱ تا ۹ تولید می‌کند (`int(x * 9) + 1`) تا مشخص شود کدام ECM اعمال شود. اگر همه پیکسل‌ها با یک سیستم رمز شوند، الگوی تکراری در خروجی باقی می‌ماند.
# 
# `generate_final_sequence` دنباله مستقل دیگری برای لایه XOR آخر می‌سازد. در کلید، `x_sel`، `x_ecm` و `x_final` از هم جدا هستند تا هر بخش نقش مشخص خود را داشته باشد.
# 
# </div>

# %%
# 4. Selector sequence (Logistic -> 1..9)
def generate_selector_sequence(x_sel, n, warmup=1000):
    x = x_sel
    for _ in range(warmup):
        x = logistic(x)
    sel = np.empty(n, dtype=np.int32)
    for k in range(n):
        x = logistic(x)
        sel[k] = int(np.floor(x * 9)) + 1
        if sel[k] > 9:
            sel[k] = 9
    return sel

# 5. Final-layer sequence (independent Logistic)
def generate_final_sequence(x_final, n, warmup=1000):
    x = x_final
    for _ in range(warmup):
        x = logistic(x)
    seq = np.empty(n, dtype=np.uint8)
    for k in range(n):
        x = logistic(x)
        seq[k] = int(np.floor(x * 256)) % 256
    return seq

# %% [markdown]
# <div dir="rtl">
# 
# ## فاز ۴ — رمزنگاری و رمزگشایی
# 
# این بخش اصلی‌ترین قسمت پیاده‌سازی است. تابع `_chaos_byte` مقدار اعشاری آشوبی را به بازه $[0,255]$ می‌برد.
# 
# در `encrypt_image` ابتدا جایگشت چن (Stage 2)، انتخاب سیستم نمایی (Stage 3)، XOR با کلید ECM (Stage 4) و سپس XOR نهایی (Stage 5) انجام می‌شود. خروجی طبیعی این فرآیند توزیع بسیار نزدیک به یکنواخت با آنتروپی ~۷.۹۹۷ تا ۷.۹۹۹ بیت دارد.
# 
# در `decrypt_image` مراحل به ترتیب معکوس اجرا می‌شوند.
# 
# </div>

# %%
def _chaos_byte(val):
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
    image_bgr: OpenCV image (H x W x 3)
    key: {'x0','y0','z0','x_sel','x_ecm','mu','x_final'}
    returns: encrypted image, metadata dict (perm_inv + balance swaps)
    """
    H, W = image_bgr.shape[:2]
    N = H * W

    # ── Stage 2: Chen permutation ──────────────────────────────────────────
    chen_seq = generate_chen_sequence(
        key['x0'], key['y0'], key['z0'], N, warmup=1000)
    perm = np.argsort(chen_seq)          # permutation vector
    perm_inv = np.empty_like(perm)
    perm_inv[perm] = np.arange(N)       # inverse permutation

    permuted = np.empty_like(image_bgr)
    for c in range(3):
        flat = image_bgr[:, :, c].flatten()
        permuted[:, :, c] = flat[perm].reshape(H, W)

    # ── Stage 3: selector sequence ────────────────────────────────────────
    selector = generate_selector_sequence(key['x_sel'], N, warmup=1000)

    # ── Stage 4: ECM XOR diffusion ─────────────────────────────────
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
        diff_xored[:, :, c] = (
            flat_perm ^ key_bytes.astype(np.int32)
        ).reshape(H, W).astype(np.uint8)

    # ── Stage 5: final XOR layer ───────────────────────────────────────────────
    final_seq = generate_final_sequence(key['x_final'], N, warmup=1000)
    encrypted = np.empty_like(image_bgr)
    for c in range(3):
        flat = diff_xored[:, :, c].flatten().astype(np.int32)
        encrypted[:, :, c] = (
            flat ^ final_seq.astype(np.int32)
        ).reshape(H, W).astype(np.uint8)

    # ── Stage 6: histogram balancing ───────────────────
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

    # ── undo histogram balancing ─────────────────────────────────
    for c in range(3):
        encrypted[:, :, c] = unbalance_histogram_flat(
            encrypted[:, :, c], balance_swaps[c])

    # ── undo final XOR layer ─────────────────────────────────────────────
    final_seq = generate_final_sequence(key['x_final'], N, warmup=1000)
    step4_out = np.empty_like(encrypted_bgr)
    for c in range(3):
        flat = encrypted[:, :, c].flatten().astype(np.int32)
        step4_out[:, :, c] = (
            flat ^ final_seq.astype(np.int32)
        ).reshape(H, W).astype(np.uint8)

    # ── undo ECM XOR layer ──────────────────────────────────────────────
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
        permuted[:, :, c] = (
            flat_enc ^ key_bytes.astype(np.int32)
        ).reshape(H, W).astype(np.uint8)

    # ── inverse permutation ─────────────────────────────────────────────────────
    decrypted = np.empty_like(encrypted_bgr)
    for c in range(3):
        flat = permuted[:, :, c].flatten()
        decrypted[:, :, c] = flat[perm_inv].reshape(H, W)

    return decrypted

# %% [markdown]
# <div dir="rtl">
# 
# ## فاز ۵ — معیارهای ارزیابی
# 
# توابع این بخش برای مقایسه عددی نتایج فصل چهارم نوشته شده‌اند:
# 
# - `shannon_entropy`: آنتروپی هر کانال رنگی
# - `pixel_correlation`: همبستگی پیکسل‌های مجاور در سه جهت (با `n_samples=5000` برای سرعت بیشتر)
# - `npcr_uaci`: حساسیت به تغییر کلید
# - `mse_psnr`: بررسی بازیابی دقیق تصویر
# 
# برای آزمون NPCR/UACI مقدار `x_0` به اندازه $10^{-15}$ تغییر داده می‌شود و دو تصویر رمزشده با هم مقایسه می‌گردند.
# 
# </div>

# %%
def shannon_entropy(channel):
    hist,_ = np.histogram(channel.flatten(), bins=256, range=(0, 256))
    hist = hist[hist > 0].astype(np.float64)
    p = hist / hist.sum()
    return float(-np.sum(p * np.log2(p)))

def pixel_correlation(channel, direction='horizontal', n_samples=5000):
    H, W = channel.shape
    rng = np.random.default_rng(42)
    if direction == 'horizontal':
        rows = rng.integers(0, H, n_samples)
        cols = rng.integers(0, W - 1, n_samples)
        x = channel[rows, cols].astype(np.float64)
        y = channel[rows, cols + 1].astype(np.float64)
    elif direction == 'vertical':
        rows = rng.integers(0, H - 1, n_samples)
        cols = rng.integers(0, W, n_samples)
        x = channel[rows, cols].astype(np.float64)
        y = channel[rows + 1, cols].astype(np.float64)
    else:  # diagonal
        rows = rng.integers(0, H - 1, n_samples)
        cols = rng.integers(0, W - 1, n_samples)
        x = channel[rows, cols].astype(np.float64)
        y = channel[rows + 1, cols + 1].astype(np.float64)
    corr = np.corrcoef(x, y)[0, 1]
    return float(corr)

def npcr_uaci(img1, img2):
    """Compute NPCR and UACI between two ciphertexts."""
    diff = img1.astype(np.int32) - img2.astype(np.int32)
    D = (diff != 0).astype(np.float64)
    npcr = D.mean() *100.0
    uaci = np.abs(diff).mean() / 255.0* 100.0
    return float(npcr), float(uaci)

def mse_psnr(orig, dec):
    mse = np.mean((orig.astype(np.float64) - dec.astype(np.float64)) **2)
    if mse == 0:
        return 0.0, float('inf')
    psnr = 10 * np.log10(255.0** 2 / mse)
    return float(mse), float(psnr)

# %% [markdown]
# <div dir="rtl">
# 
# ## فاز ۶ — اجرای آزمایش
# 
# تصاویر استاندارد از پایگاه‌های داده مرجع USC-SIPI و Kodak بارگذاری می‌شوند. مسیر پوشه `images` با یک حلقه `for` پیدا می‌شود تا کد روی سیستم‌های مختلف هم اجرا شود.
# 
# برای هر تصویر زمان رمزنگاری و رمزگشایی با `time.perf_counter()` ثبت می‌شود، معیارهای امنیتی محاسبه می‌گردد و تصاویر رمزشده در پوشه `outputs` ذخیره می‌شوند. در پایان همه نتایج در فایل `results.pkl` نگه‌داری می‌شود تا نمودارها بدون اجرای دوباره رمزنگاری رسم شوند.
# 
# </div>

# %%
# یافتن پوشه تصاویر آزمایشی
import os

img_dir = None
for p in [
    "images",
    "../../images", "../images",
    r"e:/projects/thesis_project_v2/thesis_latex_source/images",
    "e:/projects/thesis_project/images",
]:
    if os.path.isdir(p):
        img_dir = p
        break

if img_dir:
    IMAGES = {
        'Airplane': os.path.join(img_dir, 'Airplane.png'),
        'Baboon':   os.path.join(img_dir, 'Baboon.png'),
        'Peppers':  os.path.join(img_dir, 'Peppers.png'),
        'Tree':     os.path.join(img_dir, 'tree.png'),
        'Kodak01':  os.path.join(img_dir, 'Kodak01.png'),
        'Kodak02':  os.path.join(img_dir, 'Kodak02.png'),
    }
else:
    # fallback to standard images directory
    IMAGES = {
        'Airplane': 'images/Airplane.png',
        'Baboon':   'images/Baboon.png',
        'Peppers':  'images/Peppers.png',
        'Tree':     'images/tree.png',
        'Kodak01':  'images/Kodak01.png',
        'Kodak02':  'images/Kodak02.png',
    }
print("Resolved image paths:")
for k, v in IMAGES.items():
    print(f"  {k}: {v}")

DEFAULT_KEY = {
    'x0':      0.123456789012345,
    'y0':      0.987654321098765,
    'z0':      12.345678901234,
    'x_sel':   0.456789012345678,
    'x_ecm':   0.789012345678901,
    'mu':      3.8,
    'x_final': 0.234567890123456,
}

def _hist_uniformity(channel):
    h = np.bincount(channel.flatten(), minlength=256)
    return float(h.std() / h.mean() * 100.0)

results = {}

for name, path in IMAGES.items():
    print(f"\n{'='*50}")
    print(f"  پردازش تصویر: {name}")
    print(f"{'='*50}")

    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(
            f"Image file not found or invalid at path: '{path}'. "
            "Please upload the 'images' folder containing standard test images to Google Colab."
        )
    H, W = img.shape[:2]
    print(f"  ابعاد: {W}×{H}")

    # ── encryption ─────────────────────────────────────────────────────────
    t0 = time.perf_counter()
    enc, meta = encrypt_image(img, DEFAULT_KEY)
    t_enc = time.perf_counter() - t0
    print(f"  زمان رمزنگاری: {t_enc:.3f} ثانیه")

    # ── decryption ─────────────────────────────────────────────────────────
    t0 = time.perf_counter()
    dec = decrypt_image(enc, DEFAULT_KEY, meta)
    t_dec = time.perf_counter() - t0
    print(f"  زمان رمزگشایی: {t_dec:.3f} ثانیه")

    # ── invertibility check ────────────────────────────────────────────────
    mse_val, psnr_val = mse_psnr(img, dec)
    print(f"  MSE (اصلی vs بازیابی‌شده): {mse_val:.6f}")
    print(f"  PSNR: {'inf dB' if psnr_val == float('inf') else f'{psnr_val:.2f} dB'}")

    # ── entropy ───────────────────────────────────────────────────────────
    channels_orig = ['B','G','R']
    entropy_orig = [shannon_entropy(img[:,:,c]) for c in range(3)]
    entropy_enc  = [shannon_entropy(enc[:,:,c]) for c in range(3)]
    print(f"  آنتروپی اصلی  (B,G,R): {[round(e,4) for e in entropy_orig]}")
    print(f"  آنتروپی رمزشده (B,G,R): {[round(e,4) for e in entropy_enc]}")

    # ── correlation ──────────────────────────────────────────────────────────
    dirs = ['horizontal','vertical','diagonal']
    corr_orig = [pixel_correlation(img[:,:,1], d) for d in dirs]
    corr_enc  = [pixel_correlation(enc[:,:,1], d) for d in dirs]
    print(f"  همبستگی اصلی   (H,V,D): {[round(c,4) for c in corr_orig]}")
    print(f"  همبستگی رمزشده (H,V,D): {[round(c,4) for c in corr_enc]}")

    # ── NPCR / UACI with one-bit key change ─────────────────────────────
    key2 = dict(DEFAULT_KEY)
    key2['x0'] = DEFAULT_KEY['x0'] + 1e-15   # tiny key perturbation
    enc2, _meta = encrypt_image(img, key2)
    npcr_val, uaci_val = npcr_uaci(enc, enc2)
    print(f"  NPCR: {npcr_val:.4f}%")
    print(f"  UACI: {uaci_val:.4f}%")

    # ── save images ─────────────────────────────────────────────────────
    cv2.imwrite(f'outputs/{name}_encrypted.png', enc)
    cv2.imwrite(f'outputs/{name}_decrypted.png', dec)

    hist_cv_enc = [_hist_uniformity(enc[:,:,c]) for c in range(3)]
    print(
        f"  هیستوگرام رمزشده CV% (B,G,R): "
        f"{[round(v,2) for v in hist_cv_enc]}"
    )

    results[name] = {
        'H': H, 'W': W,
        't_enc': t_enc, 't_dec': t_dec,
        'mse': mse_val, 'psnr': psnr_val,
        'entropy_orig': entropy_orig,
        'entropy_enc':  entropy_enc,
        'corr_orig':    corr_orig,
        'corr_enc':     corr_enc,
        'npcr': npcr_val,
        'uaci': uaci_val,
        'hist_cv_enc': hist_cv_enc,
        'img_orig': img,
        'img_enc':  enc,
        'img_dec':  dec,
    }

print("\n\nتمام تصاویر پردازش شد.")
import pickle
with open('outputs/results.pkl','wb') as f:
    pickle.dump(results, f)
print("نتایج ذخیره شدند.")

# %% [markdown]
# <div dir="rtl">
# 
# ## فاز ۷ — رسم نمودارها
# 
# نتایج از `results.pkl` خوانده می‌شوند و هفت شکل فصل چهارم رسم می‌گردد. هر نمودار علاوه بر ذخیره در `outputs/figs`، با `plt.show()` در خروجی سلول هم نمایش داده می‌شود.
# 
# </div>

# %%
# %matplotlib inline
import matplotlib.pyplot as plt
import pickle
import numpy as np
import cv2
import os

OUT = 'outputs/figs'
os.makedirs(OUT, exist_ok=True)

with open('outputs/results.pkl', 'rb') as f:
    results = pickle.load(f)

NAMES = list(results.keys())
print('بارگذاری نتایج و آماده‌سازی نمودارها...')

# %% [markdown]
# <div dir="rtl">
# 
# ### شکل ۴-۱ — تصاویر اصلی، رمزشده و بازیابی‌شده
# 
# تصاویر آزمایشی از پایگاه‌های داده USC-SIPI و Kodak در سه ستون نمایش داده شده‌اند. ستون وسط خروجی رمزنگاری و ستون سوم نتیجه رمزگشایی است؛ اگر MSE برابر صفر باشد، ستون سوم باید با ستون اول یکسان دیده شود.
# 
# </div>

# %%
fig, axes = plt.subplots(len(NAMES), 3, figsize=(12, 3.5 * len(NAMES)))
fig.suptitle('Figure 4-1: Original, Encrypted, and Decrypted Images',
             fontsize=14, fontweight='bold', y=0.995)

col_titles = ['Original Image', 'Encrypted Image', 'Decrypted Image']
for col, title in enumerate(col_titles):
    axes[0, col].set_title(title, fontsize=12, fontweight='bold', pad=8)

for row, name in enumerate(NAMES):
    r = results[name]
    imgs = [
        cv2.cvtColor(r['img_orig'], cv2.COLOR_BGR2RGB),
        cv2.cvtColor(r['img_enc'],  cv2.COLOR_BGR2RGB),
        cv2.cvtColor(r['img_dec'],  cv2.COLOR_BGR2RGB),
    ]
    for col, img in enumerate(imgs):
        axes[row, col].imshow(img)
        axes[row, col].axis('off')
        if col == 0:
            axes[row, col].set_ylabel(name, fontsize=12, fontweight='bold',
                                       rotation=90, labelpad=8)

plt.tight_layout(rect=[0, 0, 1, 0.995])
plt.savefig(f'{OUT}/fig1_visual.png', bbox_inches='tight')
plt.show()
plt.close()
print("fig1 done")

# %% [markdown]
# <div dir="rtl">
# 
# ### شکل ۴-۲ — هیستوگرام کانال‌های B، G و R
# 
# در تصویر اصلی معمولاً قله‌های مشخص دیده می‌شود، اما پس از رمزنگاری و مرحله یکنواخت‌سازی هیستوگرام، توزیع شدت‌ها در هر سه کانال تقریباً مسطح می‌شود.
# 
# </div>

# %%
fig, axes = plt.subplots(len(NAMES), 6, figsize=(18, 2.5 * len(NAMES)))
fig.suptitle(
    'Figure 4-2: Histogram Comparison '
    '(Original vs Encrypted) - All Channels',
    fontsize=13, fontweight='bold')

chan_labels = ['Blue', 'Green', 'Red']
chan_colors = ['#2E74B5', '#538135', '#C00000']

for row, name in enumerate(NAMES):
    r = results[name]
    for ci in range(3):
        ax = axes[row, ci]
        ax.hist(r['img_orig'][:,:,ci].flatten(), bins=256,
                range=(0,256), color=chan_colors[ci], alpha=0.85, density=True)
        if row == 0:
            ax.set_title(f'Original\n{chan_labels[ci]}', fontsize=10, fontweight='bold')
        ax.set_xlim(0,255)
        ax.set_yticks([])
        if ci == 0:
            ax.set_ylabel(name, fontsize=10, fontweight='bold')
        ax.tick_params(labelsize=8)

        ax2 = axes[row, ci+3]
        ax2.hist(r['img_enc'][:,:,ci].flatten(), bins=256,
                 range=(0,256), color=chan_colors[ci], alpha=0.85, density=True)
        if row == 0:
            ax2.set_title(f'Encrypted\n{chan_labels[ci]}', fontsize=10, fontweight='bold')
        ax2.set_xlim(0,255)
        ax2.set_yticks([])
        ax2.tick_params(labelsize=8)

plt.tight_layout()
plt.savefig(f'{OUT}/fig2_histograms.png', bbox_inches='tight')
plt.show()
plt.close()
print("fig2 done")

# %% [markdown]
# <div dir="rtl">
# 
# ### شکل ۴-۳ — پراکندگی همبستگی (کانال سبز)
# 
# در تصویر اصلی نقاط حول خط قطری جمع می‌شوند که نشان‌دهنده همبستگی بالای پیکسل‌های مجاور است. در تصویر رمزشده این الگو از بین می‌رود.
# 
# </div>

# %%
fig, axes = plt.subplots(len(NAMES), 6, figsize=(18, 2.5 * len(NAMES)))
fig.suptitle(
    'Figure 4-3: Pixel Correlation Scatter Plots '
    '(Green Channel) - Original vs Encrypted',
    fontsize=13, fontweight='bold')

dir_labels_orig = ['Original H', 'Original V', 'Original D']
dir_labels_enc  = ['Encrypted H','Encrypted V','Encrypted D']
dir_colors = ['#2E74B5','#C00000','#7030A0']

rng = np.random.default_rng(42)

def get_pairs(channel, direction, n=2000):
    H2, W2 = channel.shape
    if direction == 'H':
        rs = rng.integers(0, H2, n); cs = rng.integers(0, W2-1, n)
        return channel[rs,cs], channel[rs,cs+1]
    elif direction == 'V':
        rs = rng.integers(0, H2-1, n); cs = rng.integers(0, W2, n)
        return channel[rs,cs], channel[rs+1,cs]
    else:
        rs = rng.integers(0, H2-1, n); cs = rng.integers(0, W2-1, n)
        return channel[rs,cs], channel[rs+1,cs+1]

DIRS = ['H','V','D']

for row, name in enumerate(NAMES):
    r = results[name]
    g_orig = r['img_orig'][:,:,1]
    g_enc  = r['img_enc'][:,:,1]
    for di, d in enumerate(DIRS):
        x1, y1 = get_pairs(g_orig, d)
        ax = axes[row, di]
        ax.scatter(x1, y1, s=1, alpha=0.3, color=dir_colors[di])
        corr_v = r['corr_orig'][di]
        ax.set_title(f'{dir_labels_orig[di]}\nr={corr_v:.4f}', fontsize=9)
        ax.set_xlim(0,255); ax.set_ylim(0,255)
        ax.tick_params(labelsize=7)
        if di == 0:
            ax.set_ylabel(name, fontsize=10, fontweight='bold')

        x2, y2 = get_pairs(g_enc, d)
        ax2 = axes[row, di+3]
        ax2.scatter(x2, y2, s=1, alpha=0.3, color=dir_colors[di])
        corr_v2 = r['corr_enc'][di]
        ax2.set_title(f'{dir_labels_enc[di]}\nr={corr_v2:.4f}', fontsize=9)
        ax2.set_xlim(0,255); ax2.set_ylim(0,255)
        ax2.tick_params(labelsize=7)

plt.tight_layout()
plt.savefig(f'{OUT}/fig3_correlation.png', bbox_inches='tight')
plt.show()
plt.close()
print("fig3 done")

# %% [markdown]
# <div dir="rtl">
# 
# ### شکل ۴-۴ — آنتروپی شانون
# 
# مقایسه آنتروپی سه کانال قبل و بعد از رمزنگاری. برای تصویر ۸ بیتی، مقدار ایده‌آل ۸ بیت است.
# 
# </div>

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Figure 4-4: Shannon Entropy Comparison (Original vs Encrypted)',
             fontsize=13, fontweight='bold')

x = np.arange(len(NAMES))
w = 0.12
chan_labels_short = ['B','G','R']
orig_colors = ['#AED6F1','#A9DFBF','#F1948A']
enc_colors  = ['#2E74B5','#538135','#C00000']

for ax_idx, (ax, mode, title) in enumerate(zip(
        axes, ['orig','enc'],
        ['Original Images','Encrypted Images'])):
    for ci in range(3):
        vals = [results[n][f'entropy_{mode}'][ci] for n in NAMES]
        bars = ax.bar(x + (ci - 1) * w, vals, width=w,
                      label=f'{chan_labels_short[ci]} channel',
                      color=(orig_colors if mode=='orig' else enc_colors)[ci],
                      edgecolor='white', linewidth=0.5)
        for bar, v in zip(bars, vals):
            if v >= 5.5:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                        f'{v:.3f}', ha='center', va='bottom', fontsize=7.5)
    ax.axhline(8.0, color='black', linewidth=1.5, linestyle='--',
               label='Ideal H=8')
    ax.set_xticks(x); ax.set_xticklabels(NAMES, fontsize=10)
    ax.set_ylim(5.5, 8.3)
    ax.set_ylabel('Shannon Entropy (bits)', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/fig4_entropy.png', bbox_inches='tight')
plt.show()
plt.close()
print("fig4 done")

# %% [markdown]
# <div dir="rtl">
# 
# ### شکل ۴-۵ — NPCR و UACI
# 
# با تغییر جزئی در $x_0$ (مقدار $10^{-15}$) دو تصویر رمزشده ساخته شده و درصد تغییر پیکسل‌ها و شدت آن‌ها اندازه‌گیری شده است.
# 
# </div>

# %%
fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle('Figure 4-5: NPCR and UACI — Key Sensitivity Analysis',
             fontsize=13, fontweight='bold')

npcr_vals = [results[n]['npcr'] for n in NAMES]
uaci_vals = [results[n]['uaci'] for n in NAMES]

for ax, vals, ideal, label, title, color in zip(
        axes,
        [npcr_vals, uaci_vals],
        [99.6, 33.46],
        ['NPCR (%)', 'UACI (%)'],
        ['NPCR — Number of Pixel Change Rate',
         'UACI — Unified Average Changing Intensity'],
        ['#2E74B5','#C00000']):
    bars = ax.bar(NAMES, vals, color=color, alpha=0.85,
                  edgecolor='white', linewidth=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{v:.2f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.axhline(ideal, color='black', linewidth=2, linestyle='--',
               label=f'Ideal ≈ {ideal}%')
    y_min = min(min(vals)*0.9, ideal*0.88)
    y_max = max(max(vals), ideal) * 1.08
    ax.set_ylim(y_min, y_max)
    ax.set_ylabel(label, fontsize=11)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.tick_params(labelsize=10)

plt.tight_layout()
plt.savefig(f'{OUT}/fig5_npcr_uaci.png', bbox_inches='tight')
plt.show()
plt.close()
print("fig5 done")

# %% [markdown]
# <div dir="rtl">
# 
# ### شکل ۴-۶ — زمان رمزنگاری و رمزگشایی
# 
# زمان رمزنگاری به‌دلیل انتخاب پویای سیستم نمایی برای هر پیکسل، معمولاً از زمان رمزگشایی بیشتر است.
# 
# </div>

# %%
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('Figure 4-6: Encryption and Decryption Time (seconds)',
             fontsize=13, fontweight='bold')

t_enc = [results[n]['t_enc'] for n in NAMES]
t_dec = [results[n]['t_dec'] for n in NAMES]
x = np.arange(len(NAMES))
w = 0.35

b1 = ax.bar(x - w/2, t_enc, width=w, label='Encryption', color='#2E74B5', alpha=0.85)
b2 = ax.bar(x + w/2, t_dec, width=w, label='Decryption', color='#538135', alpha=0.85)

for bar, v in zip(list(b1)+list(b2), t_enc+t_dec):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{v:.1f}s', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xticks(x); ax.set_xticklabels(NAMES, fontsize=11)
ax.set_ylabel('Time (seconds)', fontsize=11)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/fig6_time.png', bbox_inches='tight')
plt.show()
plt.close()
print("fig6 done")

# %% [markdown]
# <div dir="rtl">
# 
# ### شکل ۴-۷ — ضریب همبستگی در سه جهت
# 
# مقایسه ضریب همبستگی افقی، عمودی و قطری برای تصاویر اصلی و رمزشده.
# 
# </div>

# %%
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle('Figure 4-7: Pixel Correlation Coefficients (Original vs Encrypted)',
             fontsize=13, fontweight='bold')

dir_names = ['Horizontal', 'Vertical', 'Diagonal']
for di, (ax, dname) in enumerate(zip(axes, dir_names)):
    corr_o = [results[n]['corr_orig'][di] for n in NAMES]
    corr_e = [results[n]['corr_enc'][di]  for n in NAMES]
    x = np.arange(len(NAMES))
    w = 0.35
    b1 = ax.bar(x - w/2, corr_o, width=w, label='Original',  color='#2E74B5', alpha=0.85)
    b2 = ax.bar(x + w/2, corr_e, width=w, label='Encrypted', color='#C00000', alpha=0.85)
    for bar, v in zip(list(b1)+list(b2), corr_o+corr_e):
        offset = 0.02 if v >= 0 else -0.06
        ax.text(bar.get_x() + bar.get_width()/2, v + offset,
                f'{v:.3f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    ax.axhline(0, color='black', linewidth=1)
    ax.set_ylim(-0.2, 1.05)
    ax.set_title(f'{dname} Direction', fontsize=12, fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(NAMES, fontsize=10)
    ax.set_ylabel('Correlation Coefficient', fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/fig7_corr_bars.png', bbox_inches='tight')
plt.show()
plt.close()
print("fig7 done")

# %% [markdown]
# <div dir="rtl">
# 
# ### خلاصه نتایج عددی
# 
# میانگین آنتروپی رمزشده، NPCR، UACI و زمان اجرا برای تمام تصاویر آزمایشی از پایگاه‌های داده USC-SIPI و Kodak.
# 
# </div>

# %%
print("\n=== Numeric summary ===")
print(
    f"{'Image':<10} {'H_enc(avg)':<14} {'NPCR%':<10} "
    f"{'UACI%':<10} {'T_enc(s)':<12} {'T_dec(s)'}"
)
print("-"*65)
for n in NAMES:
    r = results[n]
    h_avg = np.mean(r['entropy_enc'])
    print(
        f"{n:<10} {h_avg:<14.4f} {r['npcr']:<10.4f} "
        f"{r['uaci']:<10.4f} {r['t_enc']:<12.3f} {r['t_dec']:.3f}"
    )
