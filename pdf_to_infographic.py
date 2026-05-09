"""
PDF → NotebookLM Infographic generator

Flow:
  1. Upload the PDF to a new NotebookLM notebook as a source.
  2. Trigger infographic generation (AI-generated, server-side).
  3. Poll until ready, then download the PNG.

Prerequisites:
  pip install notebooklm-py

Authentication:
  Run once: notebooklm login
"""

import argparse
import asyncio
from pathlib import Path

from notebooklm import NotebookLMClient
from notebooklm.rpc.types import InfographicDetail, InfographicOrientation, InfographicStyle


async def main(
    pdf_path: Path,
    output: Path,
    orientation: InfographicOrientation,
    detail: InfographicDetail,
    style: InfographicStyle,
    instructions: str | None,
):
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    async with await NotebookLMClient.from_storage() as client:
        # ── 1. Create notebook ────────────────────────────────────────────────
        title = f"PDF: {pdf_path.stem}"
        print(f"[notebooklm] Creating notebook '{title}' ...")
        notebook = await client.notebooks.create(title=title)
        notebook_id = notebook.id
        print(f"[notebooklm] Notebook ID: {notebook_id}")

        # ── 2. Upload PDF ─────────────────────────────────────────────────────
        print(f"[notebooklm] Uploading '{pdf_path.name}' ...")
        source = await client.sources.add_file(
            notebook_id,
            file_path=pdf_path,
            wait=True,
            wait_timeout=600.0,
        )
        print(f"[notebooklm] Source ready — ID: {source.id}")

        # ── 3. Generate infographic ───────────────────────────────────────────
        print(f"[notebooklm] Requesting infographic "
              f"(style={style.name}, orientation={orientation.name}, detail={detail.name}) ...")
        status = await client.artifacts.generate_infographic(
            notebook_id,
            source_ids=[source.id],
            orientation=orientation,
            detail_level=detail,
            style=style,
            instructions=instructions,
        )
        print(f"[notebooklm] Generation started — task ID: {status.task_id}")

        # ── 4. Wait for completion ────────────────────────────────────────────
        print("[notebooklm] Waiting for infographic to be ready (may take 5-10 min) ...")
        final = await client.artifacts.wait_for_completion(
            notebook_id,
            task_id=status.task_id,
            initial_interval=5.0,
            max_interval=30.0,
            timeout=900.0,
        )
        print(f"[notebooklm] Done — artifact status: {final.status}")

        # ── 5. Download PNG ───────────────────────────────────────────────────
        output.parent.mkdir(parents=True, exist_ok=True)
        saved = await client.artifacts.download_infographic(
            notebook_id,
            output_path=str(output),
        )
        print(f"\nInfographic saved to: {saved}")


# ── CLI ───────────────────────────────────────────────────────────────────────

ORIENTATION_MAP = {o.name.lower(): o for o in InfographicOrientation}
DETAIL_MAP      = {d.name.lower(): d for d in InfographicDetail}
STYLE_MAP       = {s.name.lower(): s for s in InfographicStyle}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload a PDF to NotebookLM and generate an infographic."
    )
    parser.add_argument("pdf", type=Path, help="Path to the PDF file.")
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help="Output PNG path (default: <pdf-stem>_infographic.png).",
    )
    parser.add_argument(
        "--orientation", choices=list(ORIENTATION_MAP), default="landscape",
        help="Infographic orientation (default: landscape).",
    )
    parser.add_argument(
        "--detail", choices=list(DETAIL_MAP), default="standard",
        help="Level of detail (default: standard).",
    )
    parser.add_argument(
        "--style", choices=list(STYLE_MAP), default="auto_select",
        help="Visual style (default: auto_select).",
    )
    parser.add_argument(
        "--instructions", "-i", default=None,
        help="Optional custom instructions for the infographic.",
    )
    args = parser.parse_args()

    output = args.output or args.pdf.with_name(f"{args.pdf.stem}_infographic.png")

    asyncio.run(main(
        pdf_path=args.pdf,
        output=output,
        orientation=ORIENTATION_MAP[args.orientation],
        detail=DETAIL_MAP[args.detail],
        style=STYLE_MAP[args.style],
        instructions=args.instructions,
    ))
