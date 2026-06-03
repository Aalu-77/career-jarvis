"""Career Jarvis — CLI entry point.

Usage:
    python -m src.main          # interactive mode, paste a job description
    python -m src.main --file path/to/jd.txt   # score a JD from a file
"""

import argparse
import sys
from pathlib import Path

from .scorer import score_job


VERDICT_EMOJI = {
    "STRONG_FIT": "🟢",
    "GOOD_FIT": "🟢",
    "STRETCH": "🟡",
    "WEAK_FIT": "🟠",
    "NO_FIT": "🔴",
}

RECOMMENDATION_LABEL = {
    "APPLY": "Apply — go for it.",
    "APPLY_WITH_CAVEATS": "Apply, but address the gaps in your cover letter.",
    "RESEARCH_MORE": "Look into the company before deciding.",
    "SKIP": "Skip — better roles likely exist for your profile.",
}


def print_result(result: dict) -> None:
    """Render the scoring result as a readable terminal report."""
    score = result.get("fit_score", 0)
    verdict = result.get("verdict", "UNKNOWN")
    emoji = VERDICT_EMOJI.get(verdict, "⚪")

    print()
    print("=" * 60)
    print(f"  {emoji}  FIT SCORE: {score}/100  —  {verdict}")
    print("=" * 60)
    print()

    print("Reasoning:")
    print(f"  {result.get('reasoning', '(none)')}")
    print()

    print("What matches:")
    for m in result.get("matches", []):
        print(f"  ✓ {m}")
    print()

    print("Gaps & risks:")
    for g in result.get("gaps", []):
        print(f"  ✗ {g}")
    print()

    if result.get("language_barrier"):
        print("⚠️  German language requirement may be a hard filter.")
        print()

    rec = result.get("recommendation", "RESEARCH_MORE")
    print(f"Recommendation: {RECOMMENDATION_LABEL.get(rec, rec)}")
    print()


def read_job_description_interactive() -> str:
    """Read a multi-line job description from stdin."""
    print("Paste the job description below.")
    print("When done, press Enter on an empty line, then Ctrl+Z and Enter (Windows) to finish:")
    print("-" * 60)
    return sys.stdin.read().strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Career Jarvis — score jobs against your CV.")
    parser.add_argument("--file", type=Path, help="Path to a job description text file.")
    args = parser.parse_args()

    if args.file:
        if not args.file.exists():
            print(f"Error: file not found at {args.file}", file=sys.stderr)
            sys.exit(1)
        job_description = args.file.read_text(encoding="utf-8")
    else:
        job_description = read_job_description_interactive()

    if not job_description.strip():
        print("Error: no job description provided.", file=sys.stderr)
        sys.exit(1)

    print()
    print("Asking Claude...")
    result = score_job(job_description)
    print_result(result)


if __name__ == "__main__":
    main()