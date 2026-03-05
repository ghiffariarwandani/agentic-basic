# Agentic Insight Engine

Project assignment berbasis **FastAPI + Celery** untuk menghasilkan insight event dari prompt user.

Scope saat ini:
- Market: Indonesia
- Fokus: B2C event ticketing/discovery
- Output: insight report dengan prioritas **Now / Next / Later**

## Simple Process (5 Steps)

1. Intake prompt dari user (`POST /`)
2. Parse prompt ke context terstruktur
3. Collect signals:
   - dummy customer feedback (`app/__mock__/feedback.csv`)
   - trend signals 30 hari (Tavily)
4. Synthesize insights dari semua sinyal
5. Generate report actionable (Now / Next / Later)

## API Singkat

- Endpoint: `POST /`
- Body:

```json
{
  "prompt_text": "User kesulitan checkout karena fee tidak transparan. Beri prioritas improvement."
}
```

- Response:

```json
{
  "message": "Processing!"
}
```

## Run Local

Prerequisite:
- Python + `uv`
- Redis
- env key: `OPENROUTER_API_KEY`, `APIFY_TOKEN`, `TAVILY_API_KEY`

Run:

```bash
uv sync
make dev
```

Terminal lain:

```bash
make celery
```

Jika Redis belum jalan:

```bash
docker run --rm -p 6379:6379 redis:7
```

## Struktur Inti

```text
app/main.py                    # FastAPI endpoint
app/celery.py                  # Celery worker config
app/modules/insight/tasks.py   # Orkestrasi workflow
app/modules/insight/methods.py # Logic parse + collect + synthesize
app/__mock__/feedback.csv      # Dummy feedback context
```
