# Python Task Reporter

A small, runnable Python command-line tool for AI-adjacent workflows. It reads JSON input, calls a **mock API**, and writes useful JSON and Markdown reports. It works offline and does not need an API key.

## Requirements
- Python 3.10 or newer
- Git (for publishing the repository)

## Run it

```bash
python main.py
```

Or provide your own files:

```bash
python main.py --input sample_input.json --output-dir output
```

The script creates:
- `output/report.json` — structured results for other tools to consume
- `output/report.md` — a readable report

## Example input

`sample_input.json` contains a list of tasks:

```json
[
  {"id": 1, "task": "Summarize customer feedback about a mobile app"}
]
```

## How it works
1. Reads and validates JSON input.
2. Processes each task through `mock_api()` (a local mock API; no network or secret key needed).
3. Writes JSON and Markdown output files.
4. Reports input errors with a clear message.

## Environment setup (optional but recommended)

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Running Tests


To verify all components:

```bash
python -m unittest tests/test_main.py
```

## Evidence for the skill check
- Python source: `main.py`
- Sample data: `sample_input.json` and `data/benchmark_tasks.json`
- Dependency list: `requirements.txt`
- Unit tests: `tests/test_main.py`
- Mock API: `mock_api()` in `main.py`
- Output files: generated under `output/` after running the command

## Before submitting
Run the tool yourself, inspect the output, and customize the sample tasks or add a small feature you understand. Then publish the files to a **public GitHub repository** from your own account so the commit history is yours.
