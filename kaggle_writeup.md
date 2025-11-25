## Meeting Maestro — Multi-agent Meeting Summarizer & Action Manager

### Track
**Enterprise Agents**

### Problem
Post-meeting work (writing minutes, extracting action items, and following up) is time-consuming and often inconsistent. Teams waste time re-listening to meetings or losing track of decisions and action owners.

### Solution
Meeting Maestro automates the post-meeting workflow with a small multi-agent system:
1. **Transcriber Agent** — prepares a meeting transcript (supports text and placeholder for audio STT).
2. **Summarizer Agent** — creates concise meeting minutes using an LLM (fallback deterministic summarizer available).
3. **ActionExtractor Agent** — extracts action items and tentative owners.
4. **Verifier Agent** — performs lightweight checks to flag missing decisions or inconsistencies.
5. **Memory Bank** — stores meeting summaries and actions for long-term queries.

The pipeline is orchestrated sequentially; a parallel verification step runs to increase reliability. Tools (Calendar mock, Search mock) are packaged as explicit tool interfaces so agents can call external systems in later iterations.

### Architecture
The architecture is a simple pipeline orchestrator:
- `agent_main.py` orchestrates the flow per-meeting session.
- Agents implement a `run()` interface for modularity.
- Memory persisted in SQLite (`memory.db`) acts as a Memory Bank for long-term recall.
- Observability comprises a small in-memory metrics logger and structured logging.

### Key Concepts Demonstrated
- **Multi-agent system**: sequential agents plus a parallel verifier — clear division of responsibilities.
- **Tools**: Calendar and Search tools implemented as OpenAPI-style modules (easy to swap with real APIs).
- **Sessions & Memory**: session-level transcript + stored meeting record in `MemoryBank` for later retrieval.
- **Observability**: metrics (timings, counters) and logs collected for each pipeline run.
- **Agent evaluation**: `evaluator.py` computes a simple overlap score for summaries and precision/recall for action extraction.

### Implementation details
- Language: Python
- LLM: optional OpenAI (controlled by `OPENAI_API_KEY`) — fallback summarizer if not provided.
- Memory: SQLite for portability and ease of use.
- Tools: implemented as thin modules to highlight how tools are plugged into agents.

### How to reproduce
- Clone the repo and run `python src/agent_main.py` with the sample meeting.
- Set `OPENAI_API_KEY` as an env var if you want LLM-powered summarization.
- The project includes a simple evaluator to demonstrate agent evaluation on labeled examples.

### Results & Impact
- Automates minutes & action extraction — expected to reduce 2–4 hours of post-meeting work weekly for an active team.
- Memory enables querying past decisions, improving continuity for distributed teams.

### Bonus: Deployment & Gemini
- The codebase is containerizable (Dockerfile recommended) and can be deployed to Cloud Run or Agent Engine. To earn deployment bonus points, a Cloud Run deployment script and documentation are included in the repo (instructions in README).
- If you have access to Google Gemini, replace LLM calls with Gemini endpoints for effective model usage.

### Demo
- Run the pipeline on `examples/sample_meeting.txt` to see transcript → summary → extracted actions → memory saving.
