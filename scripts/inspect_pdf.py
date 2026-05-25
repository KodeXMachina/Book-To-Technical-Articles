#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

try:
    import fitz
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyMuPDF is required: python -m pip install pymupdf") from exc


def inspect_pdf(pdf: Path, sample_pages: int = 5) -> dict[str, object]:
    doc = fitz.open(pdf)
    fonts: Counter[str] = Counter()
    image_pages: list[dict[str, int]] = []
    low_text_pages: list[int] = []
    page_samples: list[dict[str, object]] = []

    for index, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if len(text.strip()) < 40:
            low_text_pages.append(index)
        image_count = len(page.get_images(full=True))
        if image_count:
            image_pages.append({"page": index, "images": image_count})
        blocks = page.get_text("dict").get("blocks", [])
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font = span.get("font", "")
                    size = round(float(span.get("size", 0)), 1)
                    if font:
                        fonts[f"{font} {size}"] += 1
        if len(page_samples) < sample_pages:
            page_samples.append({
                "page": index,
                "chars": len(text),
                "text_prefix": re.sub(r"\s+", " ", text.strip())[:240],
                "images": image_count,
            })

    toc = doc.get_toc(simple=True)
    metadata = doc.metadata or {}
    return {
        "pdf": str(pdf),
        "pages": doc.page_count,
        "metadata": metadata,
        "outline_entries": len(toc),
        "outline_sample": toc[:40],
        "top_fonts": fonts.most_common(25),
        "image_page_count": len(image_pages),
        "image_refs": sum(item["images"] for item in image_pages),
        "image_pages_sample": image_pages[:80],
        "low_text_page_count": len(low_text_pages),
        "low_text_pages_sample": low_text_pages[:80],
        "needs_ocr_likely": len(low_text_pages) > max(3, doc.page_count * 0.5),
        "page_samples": page_samples,
    }


def to_markdown(result: dict[str, object]) -> str:
    lines = [
        "# PDF Inspection Report",
        "",
        f"- PDF: `{result['pdf']}`",
        f"- Pages: {result['pages']}",
        f"- Outline entries: {result['outline_entries']}",
        f"- Image refs: {result['image_refs']} across {result['image_page_count']} pages",
        f"- Low-text pages: {result['low_text_page_count']}",
        f"- OCR likely: {result['needs_ocr_likely']}",
        "",
        "## Metadata",
        "",
    ]
    for key, value in (result.get("metadata") or {}).items():
        if value:
            lines.append(f"- {key}: {value}")
    lines.extend(["", "## Top Fonts", ""])
    for font, count in result["top_fonts"]:
        lines.append(f"- `{font}`: {count}")
    lines.extend(["", "## Page Samples", ""])
    for item in result["page_samples"]:
        lines.append(f"- P{item['page']}: chars={item['chars']}, images={item['images']}, text=`{item['text_prefix']}`")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a PDF before converting it into book materials.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--sample-pages", type=int, default=5)
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--output", type=Path, help="Optional output report path.")
    args = parser.parse_args()
    result = inspect_pdf(args.pdf.resolve(), sample_pages=args.sample_pages)
    output = to_markdown(result) if args.markdown else json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
