"""
Entrypoint for Meeting Maestro.
Implements a simple sequential orchestration: Transcribe -> Summarize -> Extract Actions -> Verify -> Save to Memory
"""
import os
import time
import logging
from agents.transcriber_agent import TranscriberAgent
from agents.summarizer_agent import SummarizerAgent
from agents.action_agent import ActionAgent
from agents.verifier_agent import VerifierAgent
from memory.memory_bank import MemoryBank
from observability.metrics_logger import MetricsLogger
from utils.io_utils import load_meeting_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("meeting-maestro")

def run_meeting_pipeline(meeting_input_path, meeting_id=None):
    metrics = MetricsLogger()
    memory = MemoryBank(db_path="memory.db")
    meeting_id = meeting_id or f"mtg-{int(time.time())}"

    # 1) Load audio/text (here we use text for reproducibility; transcriber supports audio in extension)
    meeting_text = load_meeting_text(meeting_input_path)
    metrics.inc("meetings_received")

    # 2) Transcription (wraps speech-to-text; here identity)
    t_agent = TranscriberAgent()
    start = time.time()
    transcript = t_agent.run(meeting_text)
    metrics.timing("transcription_time", time.time() - start)

    # 3) Summarization
    s_agent = SummarizerAgent()
    start = time.time()
    summary = s_agent.run(transcript, max_length=400)
    metrics.timing("summary_time", time.time() - start)

    # 4) Action extraction
    a_agent = ActionAgent()
    start = time.time()
    actions = a_agent.run(transcript)
    metrics.timing("action_extraction_time", time.time() - start)

    # 5) Verification (parallel check — simplified synchronous here)
    v_agent = VerifierAgent()
    issues = v_agent.run(summary)
    metrics.inc("verifications", 1)

    # 6) Save to memory
    memory.insert_meeting(meeting_id, transcript, summary, actions, issues)
    metrics.inc("meetings_saved")

    # 7) Return package
    result = {
        "meeting_id": meeting_id,
        "transcript": transcript,
        "summary": summary,
        "actions": actions,
        "issues": issues,
        "metrics": metrics.snapshot()
    }

    logger.info("Pipeline complete for %s", meeting_id)
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="examples/sample_meeting.txt")
    args = parser.parse_args()
    out = run_meeting_pipeline(args.input)
    import json
    print(json.dumps(out, indent=2))
