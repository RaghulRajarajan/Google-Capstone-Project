# Meeting Maestro — Capstone (Enterprise Agents)

## Overview
Meeting Maestro is a multi-agent pipeline that converts meeting transcripts into concise minutes, extracts action items and owners, verifies summary quality, and stores results in long-term memory.

## Features demonstrated
- Multi-agent sequencing (Transcriber → Summarizer → ActionExtractor → Verifier)
- Tools (Calendar mock, Search mock, Code execution utility)
- Sessions & Memory (MemoryBank using SQLite)
- Observability (metrics & logging)
- Agent evaluation (simple summary overlap & action precision/recall)

## Quickstart (local)
1. Install:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 2. (Optional) Set `OPENAI_API_KEY` for LLM-powered summarization:
export OPENAI_API_KEY="sk-..."

## 3. Run:
python src/agent_main.py --input examples/sample_meeting.txt