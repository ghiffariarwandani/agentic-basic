# Agentic Insight Engine

Assignment project based on **FastAPI + Celery** to generate event insights from user prompts.

## Project About

Agentic Insight Engine is a learning project to:
- receive user prompts about product/event ticketing problems,
- parse prompts into structured context,
- collect signals from dummy feedback and external trends,
- prioritize insights into **Now / Next / Later**,
- generate an easy-to-read insight report.

Current scope:
- Market: Indonesia
- Focus: B2C event ticketing/discovery
- Output: insight report with **Now / Next / Later** priorities

## Disclaimer

- AI is used for **discussion, guidance, dummy data generation, and README writing**.

## Tech Stack

- Python 3.14+
- FastAPI
- Celery
- Redis
- OpenRouter (via OpenAI SDK)
- Tavily
- Pydantic + Pydantic Settings
- Markdown + FPDF2 (report rendering)
- Uvicorn + Watchfiles
- Ruff (linting)

## Simple Process (5 Steps)

1. Intake prompt dari user (`POST /`)
2. Parse prompt ke context terstruktur
3. Collect signals:
   - dummy customer feedback (`app/__mock__/feedback.csv`)
   - trend signals year to now (Tavily)
4. Synthesize insights dari semua sinyal
5. Generate report actionable (Now / Next / Later)

## API Overview

- Endpoint: `POST /`
- Body:

```json
{
  "prompt_text": "Users struggle at checkout because fees are not transparent. Prioritize improvements."
}
```

- Response:

```json
{
  "message": "Processing!"
}
```

## Run Locally

Prerequisite:
- Python + `uv`
- Redis
- environment keys: `OPENROUTER_API_KEY`, `TAVILY_API_KEY`

Run:

```bash
uv sync
make dev
```

In another terminal:

```bash
make celery
```

If Redis is not running yet:

```bash
docker run --rm -p 6379:6379 redis:7
```

## Core Structure

```text
app/main.py                    # FastAPI endpoint
app/celery.py                  # Celery worker config
app/modules/insight/tasks.py   # Workflow orchestration
app/modules/insight/methods.py # Parse + collect + synthesize logic
app/__mock__/feedback.csv      # Dummy feedback context
```
