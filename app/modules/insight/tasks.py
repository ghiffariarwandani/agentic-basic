from app.celery import celery_app
from app.modules.insight.methods import get_feedback, parse_prompt_to_context


def run_insight(prompt_text: str):
    structured = parse_prompt_to_context(prompt_text)
    feedback = get_feedback()

    return {"message": f"This is an insight task for prompt: {structured} {feedback}"}


@celery_app.task(name="insight_task")
def run_insight_task(prompt_text: str):
    insight_result = run_insight(prompt_text)
    return insight_result
