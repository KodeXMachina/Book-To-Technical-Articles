#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

try:
    import fitz
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyMuPDF is required: python -m pip install pymupdf") from exc


def clean_slug(value: str, max_len: int = 40) -> str:
    value = re.sub(r"\s+", "_", value.strip())
    value = re.sub(r"[^\w\u4e00-\u9fff-]", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:max_len]


def nearby_caption(page: fitz.Page, rect: fitz.Rect, max_words: int = 8) -> str:
    candidates = [
        fitz.Rect(rect.x0, rect.y1, rect.x1, rect.y1 + 70),
        fitz.Rect(rect.x0, max(0, rect.y0 - 60), rect.x1, rect.y0),
    ]
    for area in candidates:
        text = page.get_text("text", clip=area).strip()
        if text:
            return clean_slug(" ".join(text.replace("\n", " ").split()[:max_words]))
    return ""


def pix_hash(pix: fitz.Pixmap) -> str:
    return hashlib.sha256(pix.samples).hexdigest()


def render_clip(page: fitz.Page, rect: fitz.Rect, dpi: int, max_dim: int) -> fitz.Pixmap:
    zoom = dpi / 72.0
    max_pixel = max(rect.width, rect.height) * zoom
    if max_pixel > max_dim:
        zoom = max_dim / max(rect.width, rect.height)
    return page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=rect, alpha=False)


def extract(pdf: Path, out_dir: Path, dpi: int, max_dim: int, dedupe: str) -> list[dict[str, object]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    manifest: list[dict[str, object]] = []
    seen_xrefs: set[int] = set()
    seen_hashes: set[str] = set()
    kept = 0

    for page_no, page in enumerate(doc, start=1):
        for image_no, image in enumerate(page.get_images(full=True), start=1):
            xref = int(image[0])
            if dedupe == "xref" and xref in seen_xrefs:
                manifest.append({"page": page_no, "xref": xref, "status": "duplicate_xref"})
                continue
            rects = page.get_image_rects(xref)
            if not rects:
                manifest.append({"page": page_no, "xref": xref, "status": "no_rect"})
                continue
            rect = rects[0]
            pix = render_clip(page, rect, dpi=dpi, max_dim=max_dim)
            digest = pix_hash(pix)
            if dedupe == "hash" and digest in seen_hashes:
                manifest.append({"page": page_no, "xref": xref, "sha256": digest, "status": "duplicate_hash"})
                continue
            seen_xrefs.add(xref)
            seen_hashes.add(digest)
            kept += 1
            caption = nearby_caption(page, rect)
            suffix = f"_{caption}" if caption else f"_p{page_no:04d}_img{image_no:02d}"
            filename = f"{kept:03d}{suffix}.png"
            target = out_dir / filename
            pix.save(target)
            manifest.append({
                "page": page_no,
                "image_index": image_no,
                "xref": xref,
                "status": "kept",
                "file": str(target),
                "width": pix.width,
                "height": pix.height,
                "sha256": digest,
                "bbox": [round(rect.x0, 2), round(rect.y0, 2), round(rect.x1, 2), round(rect.y1, 2)],
                "caption_slug": caption,
            })
    return manifest


def markdown_report(manifest: list[dict[str, object]], out_dir: Path) -> str:
    kept = [item for item in manifest if item.get("status") == "kept"]
    lines = ["# Extracted PDF Images", "", f"Kept images: {len(kept)}", ""]
    for item in kept:
        file = Path(str(item["file"]))
        rel = file.relative_to(out_dir.parent) if file.is_relative_to(out_dir.parent) else file
        lines.append(f"- P{item['page']} `{rel}` {item['width']}x{item['height']} bbox={item['bbox']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract PDF images by rendering placed image rectangles with a white background.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("outdir", nargs="?", type=Path, help="Output directory; default: <pdf-dir>/images")
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--max-dim", type=int, default=2000)
    parser.add_argument("--dedupe", choices=["hash", "xref", "none"], default="hash")
    parser.add_argument("--manifest", type=Path, help="Manifest JSON path; default: <outdir>/image_manifest.json")
    parser.add_argument("--markdown-report", type=Path, help="Optional Markdown report path.")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    out_dir = (args.outdir or (pdf.parent / "images")).resolve()
    dedupe = "" if args.dedupe == "none" else args.dedupe
    manifest = extract(pdf, out_dir, dpi=args.dpi, max_dim=args.max_dim, dedupe=dedupe)
    manifest_path = args.manifest or (out_dir / "image_manifest.json")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.markdown_report:
        args.markdown_report.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_report.write_text(markdown_report(manifest, out_dir), encoding="utf-8")
    print(json.dumps({"kept": sum(1 for item in manifest if item.get("status") == "kept"), "manifest": str(manifest_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
