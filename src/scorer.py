import json
from anthropic import Anthropic
from . import config

client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a sharp, honest career advisor helping a software engineer evaluate job opportunities in Europe (especially Germany).

You will be given:
1. The candidate's CV.
2. A job description.

Your task: produce an honest, calibrated fit assessment. Be direct. Don't be encouraging by default — the candidate needs accurate signals to spend their time well.

Return your assessment as STRICT JSON with this exact schema (no extra text, no markdown fences):

{
  "fit_score": <integer 0-100>,
  "verdict": "<one of: STRONG_FIT, GOOD_FIT, STRETCH, WEAK_FIT, NO_FIT>",
  "matches": [<list of 2-5 specific things the candidate genuinely matches>],
  "gaps": [<list of 1-4 specific things missing or weak>],
  "language_barrier": <true if German is required at B2+ and candidate is below B2, else false>,
  "reasoning": "<2-3 sentences explaining the score in plain language>",
  "recommendation": "<one of: APPLY, APPLY_WITH_CAVEATS, SKIP, RESEARCH_MORE>"
}

Scoring guidance:
- 80-100: Strong match. Most requirements met. Apply.
- 60-79: Good match with manageable gaps. Worth applying.
- 40-59: Stretch. Apply only if highly motivated and willing to address gaps in cover letter.
- 20-39: Weak. Better roles likely exist; don't burn time unless you love this one.
- 0-19: Mismatch. Skip.

Hard filters that lower the score significantly:
- "Several years" / "3+ years" experience required when candidate has <2 years industry work
- German required at C1/B2+ when candidate's German is A2
- Location requirement that doesn't match candidate's situation
- Security clearance or citizenship requirements the candidate can't meet

Strengths to weight positively:
- AI/LLM/RAG/GenAI roles (candidate has direct hands-on experience)
- Python-centric roles
- Remote or English-first roles
- Early-career or graduate roles in engineering/AI
"""

def score_job(job_description: str, cv: str| None = None)->dict:
    if cv is None:
        cv = config.load_cv()

    user_message = f"""## Candidate CV
{cv}

---

## Job Description
{job_description}

---
Now evaluate the fit and respond with the JSON only."""
    
    response = client.messages.create(
        model=config.MODEL_FAST,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    # Extract the text and parse the JSON
    raw_text = response.content[0].text.strip()

    # Sometimes models wrap JSON in ```json fences even when told not to — strip them
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1]) if len(lines) > 2 else raw_text

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Claude returned invalid JSON. Raw response:\n{raw_text}\nError: {e}"
        )

    return result
