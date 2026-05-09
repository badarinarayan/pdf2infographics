# PDF to Infographic — via Google NotebookLM

Automatically turn any PDF into an AI-generated infographic using [Google NotebookLM](https://notebooklm.google.com/) and the [`notebooklm-py`](https://github.com/maxisoft/notebooklm-py) library.

> **This project was built with [Claude](https://claude.ai) (Anthropic's AI assistant) using [Claude Code](https://claude.ai/claude-code).**

---

## How it works

```
PDF file
   │
   ├─► notebooklm-py ──► Create NotebookLM notebook
   │                 ──► Upload PDF as source
   │                 ──► Trigger infographic generation (server-side AI)
   │                 ──► Poll until ready
   └─►                   Download infographic as PNG
```

1. A new NotebookLM notebook is created programmatically.
2. Your PDF is uploaded and processed as a source.
3. NotebookLM's AI generates a visual infographic summarising the content.
4. The finished PNG is downloaded to your local machine.

---

## Prerequisites

- Python 3.11+
- A Google account with access to [NotebookLM](https://notebooklm.google.com/)

### Install dependencies

```bash
pip install notebooklm-py
```

---

## Authentication

You need to log in with your Google account once so `notebooklm-py` can save your session:

```bash
notebooklm login
```

This opens a browser window. Sign in with your Google account and the session is saved locally at `~/.notebooklm/profiles/default/storage_state.json`.

To verify authentication is working:

```bash
notebooklm auth check
```

---

## Usage

### Basic

```bash
python pdf_to_infographic.py path/to/your.pdf
```

Output is saved as `your_infographic.png` in the same directory as the PDF.

### Custom output path

```bash
python pdf_to_infographic.py paper.pdf --output ~/Desktop/summary.png
```

### With style and layout options

```bash
python pdf_to_infographic.py paper.pdf --orientation portrait --detail detailed --style scientific
```

### With custom instructions

```bash
python pdf_to_infographic.py paper.pdf --instructions "Focus on the methodology and key results"
```

---

## Options

| Flag | Default | Description |
|---|---|---|
| `--output`, `-o` | `<pdf-stem>_infographic.png` | Output PNG path |
| `--orientation` | `landscape` | `landscape`, `portrait`, `square` |
| `--detail` | `standard` | `concise`, `standard`, `detailed` |
| `--style` | `auto_select` | See styles table below |
| `--instructions`, `-i` | _(none)_ | Custom generation instructions |

### Available styles

| Style | Description |
|---|---|
| `auto_select` | Let NotebookLM choose the best style |
| `professional` | Clean, business-ready layout |
| `sketch_note` | Hand-drawn sketchnote aesthetic |
| `bento_grid` | Modular bento-box grid layout |
| `editorial` | Magazine-style editorial design |
| `instructional` | Step-by-step instructional layout |
| `bricks` | Block/brick visual style |
| `clay` | Soft clay-render aesthetic |
| `anime` | Anime-inspired illustration style |
| `kawaii` | Cute kawaii style |
| `scientific` | Clean scientific/academic style |

---

## Timeouts

Infographic generation is server-side and depends on NotebookLM's load. Typical times:

| Step | Timeout |
|---|---|
| PDF source processing | 10 minutes |
| Infographic generation | 15 minutes |

If you consistently hit timeouts, try a smaller PDF or run during off-peak hours.

---

## Notes

- `notebooklm-py` uses **undocumented Google APIs** that may change without notice. If something breaks, check for a newer version: `pip install --upgrade notebooklm-py`
- Each run creates a **new notebook** in your NotebookLM account. You can delete old ones at [notebooklm.google.com](https://notebooklm.google.com/).
- The infographic is generated entirely by NotebookLM's AI — no local GPU or API key required.

---

## Built with

- [notebooklm-py](https://pypi.org/project/notebooklm-py/) — Python automation for Google NotebookLM
- [Claude](https://claude.ai) by [Anthropic](https://www.anthropic.com) — AI assistant that wrote this code
- [Claude Code](https://claude.ai/claude-code) — Agentic coding tool used to develop and iterate on the script

---

## License

BSD3-Clause
