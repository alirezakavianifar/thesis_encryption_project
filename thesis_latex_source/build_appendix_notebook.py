#!/usr/bin/env python3
"""Build thesis_appendix.ipynb from appendix_code.py with Persian RTL markdown."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APPENDIX_PY = ROOT / "appendix_code.py"
NOTEBOOK_PATH = ROOT / "thesis_appendix.ipynb"


def rtl(text: str) -> str:
    return f'<div dir="rtl">\n\n{text.strip()}\n\n</div>'


def md_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [rtl(text)],
    }


def code_cell(source: str) -> dict:
    lines = source.strip("\n").splitlines()
    return {
        "cell_type": "code",
        "metadata": {},
        "source": [ln + "\n" for ln in lines] + ([] if not lines else []),
        "outputs": [],
        "execution_count": None,
    }


def slice_code(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    if end is None:
        return text[i:]
    j = text.index(end, i + len(start))
    return text[i:j]


def persianize_experiment(code: str) -> str:
    code = code.replace(
        """for p in [
    "../../images", "images", "../images",
    "e:/projects/thesis_project/images",
]:""",
        """for p in [
    "images",
    "../../images", "../images",
    r"e:/projects/thesis_project_v2/thesis_latex_source/images",
    "e:/projects/thesis_project/images",
]:""",
    )
    subs = {
        "# Locate images directory (relative or absolute paths)": "# یافتن پوشه تصاویر آزمایشی",
        'print(f"  Processing image: {name}")': 'print(f"  پردازش تصویر: {name}")',
        'print(f"  Size: {W}x{H}")': 'print(f"  ابعاد: {W}×{H}")',
        'print(f"  Encryption time: {t_enc:.3f} s")': 'print(f"  زمان رمزنگاری: {t_enc:.3f} ثانیه")',
        'print(f"  Decryption time: {t_dec:.3f} s")': 'print(f"  زمان رمزگشایی: {t_dec:.3f} ثانیه")',
        'print(f"  MSE (original vs recovered): {mse_val:.6f}")': 'print(f"  MSE (اصلی vs بازیابی‌شده): {mse_val:.6f}")',
        'print(f"  Entropy original  (B,G,R): {[round(e,4) for e in entropy_orig]}")': 'print(f"  آنتروپی اصلی  (B,G,R): {[round(e,4) for e in entropy_orig]}")',
        'print(f"  Entropy encrypted (B,G,R): {[round(e,4) for e in entropy_enc]}")': 'print(f"  آنتروپی رمزشده (B,G,R): {[round(e,4) for e in entropy_enc]}")',
        'print(f"  Correlation original (H,V,D): {[round(c,4) for c in corr_orig]}")': 'print(f"  همبستگی اصلی   (H,V,D): {[round(c,4) for c in corr_orig]}")',
        'print(f"  Correlation encrypted (H,V,D): {[round(c,4) for c in corr_enc]}")': 'print(f"  همبستگی رمزشده (H,V,D): {[round(c,4) for c in corr_enc]}")',
        'print("\\n\\nAll images processed.")': 'print("\\n\\nتمام تصاویر پردازش شد.")',
        'print("Results saved.")': 'print("نتایج ذخیره شدند.")',
        'f"  Encrypted histogram CV% (B,G,R): "': 'f"  هیستوگرام رمزشده CV% (B,G,R): "',
    }
    for old, new in subs.items():
        code = code.replace(old, new)
    return code


def inline_fig(code: str) -> str:
    return code.replace("plt.close()", "plt.show()\nplt.close()")


FIGURE_NOTES = {
    "fig1": (
        "### شکل ۴-۱ — تصاویر اصلی، رمزشده و بازیابی‌شده\n\n"
        "تصاویر آزمایشی از پایگاه‌های داده USC-SIPI و Kodak در سه ستون نمایش داده شده‌اند. "
        "ستون وسط خروجی رمزنگاری و ستون سوم نتیجه رمزگشایی است؛ "
        "اگر MSE برابر صفر باشد، ستون سوم باید با ستون اول یکسان دیده شود."
    ),
    "fig2": (
        "### شکل ۴-۲ — هیستوگرام کانال‌های B، G و R\n\n"
        "در تصویر اصلی معمولاً قله‌های مشخص دیده می‌شود، "
        "اما پس از رمزنگاری و مرحله یکنواخت‌سازی هیستوگرام، "
        "توزیع شدت‌ها در هر سه کانال تقریباً مسطح می‌شود."
    ),
    "fig3": (
        "### شکل ۴-۳ — پراکندگی همبستگی (کانال سبز)\n\n"
        "در تصویر اصلی نقاط حول خط قطری جمع می‌شوند که نشان‌دهنده همبستگی بالای پیکسل‌های مجاور است. "
        "در تصویر رمزشده این الگو از بین می‌رود."
    ),
    "fig4": (
        "### شکل ۴-۴ — آنتروپی شانون\n\n"
        "مقایسه آنتروپی سه کانال قبل و بعد از رمزنگاری. "
        "برای تصویر ۸ بیتی، مقدار ایده‌آل ۸ بیت است."
    ),
    "fig5": (
        "### شکل ۴-۵ — NPCR و UACI\n\n"
        "با تغییر جزئی در $x_0$ (مقدار $10^{-15}$) دو تصویر رمزشده ساخته شده "
        "و درصد تغییر پیکسل‌ها و شدت آن‌ها اندازه‌گیری شده است."
    ),
    "fig6": (
        "### شکل ۴-۶ — زمان رمزنگاری و رمزگشایی\n\n"
        "زمان رمزنگاری به‌دلیل انتخاب پویای سیستم نمایی برای هر پیکسل، "
        "معمولاً از زمان رمزگشایی بیشتر است."
    ),
    "fig7": (
        "### شکل ۴-۷ — ضریب همبستگی در سه جهت\n\n"
        "مقایسه ضریب همبستگی افقی، عمودی و قطری برای تصاویر اصلی و رمزشده."
    ),
    "summary": (
        "### خلاصه نتایج عددی\n\n"
        "میانگین آنتروپی رمزشده، NPCR، UACI و زمان اجرا برای تمام تصاویر آزمایشی از پایگاه‌های داده USC-SIPI و Kodak."
    ),
}

SETUP_NOTE = """## آماده‌سازی محیط

کتابخانه‌های `numpy`، `scipy`، `opencv` و `matplotlib` در ابتدا وارد می‌شوند. پوشه‌های `outputs` و `outputs/figs` با `os.makedirs` ساخته می‌شوند تا تصاویر و نمودارهای خروجی بدون خطا ذخیره شوند."""

SECTION_NOTES = {
    "# 1. Chen chaotic system": """## فاز ۱ — سیستم Chen و نگاشت‌های پایه

تابع `chen_system` معادلات دیفرانسیل سیستم Chen را با پارامترهای $a=35$، $b=3$ و $c=28$ تعریف می‌کند. در `generate_chen_sequence` با `solve_ivp` این معادلات حل عددی می‌شوند و از خروجی، دنباله‌ای برای مرحله جایگشت گرفته می‌شود.

پارامتر `warmup=1000` به این دلیل است که چند هزار گام اول دنباله هنوز در ناحیه گذرا قرار دارد و برای تولید کلید مناسب نیست.

توابع `logistic`، `sine_map` و `tent_map` سه نگاشت یک‌بعدی پایه‌اند که در مرحله بعد برای ساخت خانواده ECM به‌کار می‌روند.""",
    "# 3. Nine exponential chaotic maps (ECM)": """## فاز ۲ — نه سیستم آشوبی نمایی (ECM)

در `ecm_step` ابتدا یکی از نگاشت‌های Logistic، Sine یا Tent اجرا می‌شود و سپس خروجی از تابع نمایی عبور داده می‌شود. ترکیب نقش داخلی و خارجی، نه سیستم مجزا ایجاد می‌کند.

مقدار `MU_DEFAULT = 3.8` پارامتر نمایی ECM است و در ناحیه‌ای انتخاب شده که رفتار آشوبی پایدار بماند. تابع `_apply_map` فقط برای ساده‌تر شدن انتخاب بین سه نگاشت پایه نوشته شده است.

در `generate_ecm_sequence` مانند مرحله Chen، ابتدای دنباله (`warmup`) حذف می‌شود.""",
    "# 4. Selector sequence (Logistic -> 1..9)": """## فاز ۳ — انتخاب‌گر و لایه XOR نهایی

تابع `generate_selector_sequence` با نگاشت Logistic برای هر پیکسل یک عدد بین ۱ تا ۹ تولید می‌کند (`int(x * 9) + 1`) تا مشخص شود کدام ECM اعمال شود. اگر همه پیکسل‌ها با یک سیستم رمز شوند، الگوی تکراری در خروجی باقی می‌ماند.

`generate_final_sequence` دنباله مستقل دیگری برای لایه XOR آخر می‌سازد. در کلید، `x_sel`، `x_ecm` و `x_final` از هم جدا هستند تا هر بخش نقش مشخص خود را داشته باشد.""",
    "def _chaos_byte": """## فاز ۴ — رمزنگاری، رمزگشایی و یکنواخت‌سازی هیستوگرام

این بخش اصلی‌ترین قسمت پیاده‌سازی است. تابع `_chaos_byte` مقدار اعشاری آشوبی را به بازه $[0,255]$ می‌برد.

در `encrypt_image` ابتدا جایگشت و XOR انجام می‌شود، سپس `balance_histogram_flat` هیستوگرام را یکنواخت می‌کند. این مرحله برای کاهش نشت آماری در توزیع شدت‌ها ضروری است، اما جابه‌جایی‌های انجام‌شده باید در `meta` ذخیره شوند.

در `decrypt_image` تابع `unbalance_histogram_flat` همان جابه‌جایی‌ها را معکوس می‌کند و سپس مراحل قبلی به ترتیب معکوس اجرا می‌شوند.""",
    "def shannon_entropy": """## فاز ۵ — معیارهای ارزیابی

توابع این بخش برای مقایسه عددی نتایج فصل چهارم نوشته شده‌اند:

- `shannon_entropy`: آنتروپی هر کانال رنگی
- `pixel_correlation`: همبستگی پیکسل‌های مجاور در سه جهت (با `n_samples=5000` برای سرعت بیشتر)
- `npcr_uaci`: حساسیت به تغییر کلید
- `mse_psnr`: بررسی بازیابی دقیق تصویر

برای آزمون NPCR/UACI مقدار `x_0` به اندازه $10^{-15}$ تغییر داده می‌شود و دو تصویر رمزشده با هم مقایسه می‌گردند.""",
}

EXPERIMENT_NOTE = """## فاز ۶ — اجرای آزمایش

تصاویر استاندارد از پایگاه‌های داده مرجع USC-SIPI و Kodak بارگذاری می‌شوند. مسیر پوشه `images` با یک حلقه `for` پیدا می‌شود تا کد روی سیستم‌های مختلف هم اجرا شود.

برای هر تصویر زمان رمزنگاری و رمزگشایی با `time.perf_counter()` ثبت می‌شود، معیارهای امنیتی محاسبه می‌گردد و تصاویر رمزشده در پوشه `outputs` ذخیره می‌شوند. در پایان همه نتایج در فایل `results.pkl` نگه‌داری می‌شود تا نمودارها بدون اجرای دوباره رمزنگاری رسم شوند."""

PLOT_NOTE = """## فاز ۷ — رسم نمودارها

نتایج از `results.pkl` خوانده می‌شوند و هفت شکل فصل چهارم رسم می‌گردد. هر نمودار علاوه بر ذخیره در `outputs/figs`، با `plt.show()` در خروجی سلول هم نمایش داده می‌شود."""


def build_notebook() -> dict:
    raw = APPENDIX_PY.read_text(encoding="utf-8")
    cells: list[dict] = []

    cells.append(md_cell(
        "# پیاده‌سازی الگوریتم رمزنگاری تصویر رنگی\n\n"
        "این دفترچه کد پیوست پایان‌نامه را گام‌به‌گام اجرا می‌کند. "
        "الگوریتم از ترکیب سیستم Chen با نه نگاشت آشوبی نمایی (ECM) تشکیل شده "
        "و در پایان نتایج فصل چهارم — آنتروپی، همبستگی، NPCR، UACI و نمودارها — محاسبه می‌شود."
    ))
    cells.append(md_cell(SETUP_NOTE))

    setup = slice_code(raw, "import numpy", "# 1. Chen chaotic system")
    setup = "import numpy" + setup[ len("import numpy") : ]  # keep from import
    setup = setup.replace(
        "print(\"Environment initialized. Outputs will be saved to './outputs/'\")",
        "print('محیط آماده شد. خروجی‌ها در پوشه outputs/ ذخیره می‌شوند.')",
    )
    cells.append(code_cell(setup))

    sections = [
        (
            SECTION_NOTES["# 1. Chen chaotic system"],
            "# 1. Chen chaotic system",
            "# 3. Nine exponential chaotic maps (ECM)",
        ),
        (
            SECTION_NOTES["# 3. Nine exponential chaotic maps (ECM)"],
            "# 3. Nine exponential chaotic maps (ECM)",
            "# 4. Selector sequence (Logistic -> 1..9)",
        ),
        (
            SECTION_NOTES["# 4. Selector sequence (Logistic -> 1..9)"],
            "# 4. Selector sequence (Logistic -> 1..9)",
            "def _chaos_byte",
        ),
        (
            SECTION_NOTES["def _chaos_byte"],
            "def _chaos_byte",
            "def shannon_entropy",
        ),
        (
            SECTION_NOTES["def shannon_entropy"],
            "def shannon_entropy",
            "# Locate images directory",
        ),
    ]
    for md, start, end in sections:
        cells.append(md_cell(md))
        cells.append(code_cell(slice_code(raw, start, end)))

    cells.append(md_cell(EXPERIMENT_NOTE))
    exp = persianize_experiment(slice_code(raw, "# Locate images directory", "import matplotlib.pyplot as plt"))
    cells.append(code_cell(exp))

    cells.append(md_cell(PLOT_NOTE))
    plot_load = """%matplotlib inline
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
"""
    cells.append(code_cell(plot_load))

    plot_body = slice_code(raw, "fig, axes = plt.subplots(len(NAMES), 3", None)
    fig_markers = [
        ("fig1", 'fig, axes = plt.subplots(len(NAMES), 3', 'print("fig1 done")'),
        ("fig2", 'fig, axes = plt.subplots(len(NAMES), 6', 'print("fig2 done")'),
        ("fig3", 'fig, axes = plt.subplots(len(NAMES), 6', 'print("fig3 done")'),
        ("fig4", 'fig, axes = plt.subplots(1, 2', 'print("fig4 done")'),
        ("fig5", 'fig, axes = plt.subplots(1, 2', 'print("fig5 done")'),
        ("fig6", 'fig, ax = plt.subplots', 'print("fig6 done")'),
        ("fig7", 'fig, axes = plt.subplots(1, 3', 'print("fig7 done")'),
        ("summary", 'print("\\n=== Numeric summary ===")', None),
    ]
    cursor = 0
    for key, start, end in fig_markers:
        cells.append(md_cell(FIGURE_NOTES[key]))
        i = plot_body.index(start, cursor)
        if end is None:
            chunk = plot_body[i:]
        else:
            j = plot_body.index(end, i) + len(end)
            chunk = plot_body[i:j]
            cursor = j
        cells.append(code_cell(inline_fig(chunk)))

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def main() -> None:
    nb = build_notebook()
    NOTEBOOK_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Wrote {NOTEBOOK_PATH} ({len(nb['cells'])} cells)")


if __name__ == "__main__":
    main()
