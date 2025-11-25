"""
ActionAgent:
Extracts action items (task, owner, deadline if present) from transcript.
This uses simple regex/heuristics; can be upgraded to LLM extraction.
"""
import re
import logging
logger = logging.getLogger("action_agent")

class ActionAgent:
    def __init__(self):
        pass

    def run(self, transcript):
        actions = []
        # naive heuristic: lines containing 'action', 'shall', 'will', 'to do', 'please'
        for line in transcript.splitlines():
            text = line.strip()
            if not text:
                continue
            if re.search(r'\b(action|will|please|todo|to do|shall|assign)\b', text, re.I):
                # attempt to parse owner by "—" or ":" or "by <name>"
                owner = None
                m = re.search(r'by (\w+)', text, re.I)
                if m:
                    owner = m.group(1)
                actions.append({"text": text, "owner": owner})
        logger.info("Extracted %d actions", len(actions))
        return actions
