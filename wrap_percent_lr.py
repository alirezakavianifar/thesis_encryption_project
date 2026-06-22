from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(r"e:\projects\thesis_project_v2\thesis_latex_source")

# Matches "99.60\%", "۹۹.۴۸٪", "30.19%" (should be rare), optional surrounding spaces.
PERCENT_TOKEN_RE = re.compile(
    r"(?P<tok>(?:[0-9۰-۹]+(?:[.,/][0-9۰-۹]+)?)\s*(?:\\%|%|٪))"
)

LR_SPAN_RE = re.compile(r"\\lr\{[^{}]*\}")


def spans_lr(line: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in LR_SPAN_RE.finditer(line)]


def inside_any(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= pos < b for a, b in spans)


def wrap_line(line: str) -> tuple[str, int]:
    # Skip verbatim / listings content lines: handled outside via state.
    lr_spans = spans_lr(line)
    out = []
    last = 0
    n = 0
    for m in PERCENT_TOKEN_RE.finditer(line):
        s, e = m.span("tok")
        if inside_any(s, lr_spans):
            continue
        out.append(line[last:s])
        out.append(r"\lr{" + m.group("tok").strip() + "}")
        last = e
        n += 1
    if n == 0:
        return line, 0
    out.append(line[last:])
    return "".join(out), n


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    changed = 0
    out_lines: list[str] = []
    in_verbatim = False

    for line in text:
        if r"\begin{verbatim}" in line or r"\begin{lstlisting}" in line:
            in_verbatim = True
            out_lines.append(line)
            continue
        if r"\end{verbatim}" in line or r"\end{lstlisting}" in line:
            in_verbatim = False
            out_lines.append(line)
            continue

        if in_verbatim:
            out_lines.append(line)
            continue

        new_line, n = wrap_line(line)
        changed += n
        out_lines.append(new_line)

    if changed:
        path.write_text("".join(out_lines), encoding="utf-8")
    return changed


def main() -> None:
    total = 0
    files = sorted(ROOT.glob("*.tex"))
    for p in files:
        # Don't touch preamble: could contain percent in macro definitions/comments.
        if p.name == "preamble.tex":
            continue
        total += process_file(p)
    print(f"Wrapped {total} percent tokens with \\\\lr{{...}}")


if __name__ == "__main__":
    main()

