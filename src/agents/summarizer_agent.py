"""
SummarizerAgent:
Uses an LLM (OpenAI by default) to produce a concise meeting summary.
If OPENAI_API_KEY is not set, uses a deterministic fallback summarizer.
"""
import os
import logging
logger = logging.getLogger("summarizer")

OPENAI_ENABLED = bool(os.environ.get("OPENAI_API_KEY"))

if OPENAI_ENABLED:
    import openai

class SummarizerAgent:
    def __init__(self, model="gpt-4o" if OPENAI_ENABLED else None):
        self.model = model

    def run(self, transcript, max_length=300):
        if OPENAI_ENABLED:
            prompt = (
                "You are a helpful assistant. Produce a concise meeting summary (3-6 bullets)."
                f"\n\nMeeting transcript:\n{transcript}\n\nSummary:"
            )
            resp = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role":"user","content":prompt}],
                max_tokens= max_length//2
            )
            summary = resp.choices[0].message.content.strip()
            logger.info("LLM summarization completed")
            return summary
        else:
            # Simple heuristic summarizer fallback
            lines = [l.strip() for l in transcript.splitlines() if l.strip()]
            top = lines[:6]
            bullets = "\n".join(f"- {s[:200]}" for s in top)
            logger.info("Fallback summarizer used")
            return bullets
