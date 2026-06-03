# Career Jarvis

An AI-powered job-fit evaluator. Built with Claude (Anthropic).

Paste any job description into the CLI — Career Jarvis scores it against your CV with reasoning, surfaces concrete matches and gaps, and tells you whether to apply, apply with caveats, or skip.

I built this to help me cut through the noise of the European tech job market during my own job hunt. It's been a useful tool _and_ an excuse to build something real with the Anthropic API end to end.

## Example output

```
============================================================
  🟢  FIT SCORE: 82/100  —  GOOD_FIT
============================================================

Reasoning:
  Strong technical match on Python, RAG, and LLM pipeline experience. Remote
  role with English-only requirement removes the usual German-language filter.
  Agent framework specifics are newer ground but adjacent.

What matches:
  ✓ Hands-on RAG and LLM work from master's thesis
  ✓ Python is primary working language
  ✓ Production API and backend experience at Infosys
  ✓ Comfortable using AI tools in dev workflow

Gaps & risks:
  ✗ Less direct experience with n8n / agent frameworks
  ✗ No prior startup-style role on CV

Recommendation: Apply, but address the gaps in your cover letter.
```

## How it works

1. Your CV lives in `config/cv.md` as markdown — the agent's persistent memory of you.
2. You feed in a job description (paste in the CLI, or pass a file with `--file`).
3. The agent calls Claude (Haiku for speed and cost) with a careful system prompt that includes calibration guidance — penalize hard filters (language, years of experience), reward genuine technical alignment.
4. Claude returns a structured JSON verdict that the CLI renders as a readable report.

## Architecture

```
career-jarvis/
├── config/
│   └── cv.md              # Your CV in markdown — the agent's context
├── src/
│   ├── config.py          # Loads API key and settings safely
│   ├── scorer.py          # The Claude call — system prompt, JSON parsing
│   └── main.py            # CLI entry point
├── data/                  # Local-only — scored jobs, digests, SQLite
├── .env                   # API key (gitignored)
└── .gitignore
```

Design choices worth noting:

- **JSON-mode output, no framework wrappers.** The orchestration is hand-rolled. Simpler to reason about and debug, and the system prompt enforces a strict JSON schema rather than relying on a framework's parsing layer.
- **Calibration in the prompt, not the model.** Hard filters (language barriers, years of experience) are explicit in the system prompt rather than buried in model behavior — easier to tune.
- **Haiku for screening, Sonnet for important steps.** Cost-aware model routing means dozens of jobs can be scored for cents per day.

## Setup

Requires Python 3.10+ and an Anthropic API key.

```bash
git clone https://github.com/Aalu-77/career-jarvis.git
cd career-jarvis
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install anthropic python-dotenv pyyaml
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

Add your CV to `config/cv.md` in markdown format.

## Usage

Score a job description interactively:

```bash
python -m src.main
# Paste the JD, then type END on a new line and press Enter
```

Or from a file:

```bash
python -m src.main --file path/to/jd.txt
```

## Roadmap

- [x] CLI job-fit scoring with structured output
- [ ] Tailored cover letter drafting using CV as context
- [ ] SQLite storage for scored jobs (avoid duplicates, track applications)
- [ ] RSS-based job ingestion (Indeed, Stepstone)
- [ ] Daily markdown digest with top-N ranked jobs
- [ ] Email delivery via SMTP, scheduled via Task Scheduler / cron

## Why

Job hunting in Europe in 2026 is a slog. Recruiters get more applications than ever, candidates get less feedback than ever, and most "AI job search tools" are paid SaaS wrappers that don't tell you anything about _your_ fit.

This is the version I wanted: a small, transparent, local tool that uses a real LLM, gives me honest signals, and lives entirely on my own machine.

## License

MIT.
