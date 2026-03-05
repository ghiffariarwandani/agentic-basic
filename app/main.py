from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.modules.insight.schema import InsightRequest
from app.modules.insight.tasks import run_insight_task

app = FastAPI(title=settings.app_name)


@app.post("/")
def submit_insight_request(insight_request: InsightRequest):
    if len(insight_request.prompt_text) == 0:
        return {"message": "No prompt text provided!"}

    run_insight_task.delay(insight_request.prompt_text)
    return {"message": "Processing!"}


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
