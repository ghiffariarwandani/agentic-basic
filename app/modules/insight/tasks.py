from app.celery import celery_app
from app.modules.insight.methods import get_feedback, parse_prompt_to_context, research_keyword, synthesize_insights


def run_insight(prompt_text: str):
    structured = parse_prompt_to_context(prompt_text)
    feedback = get_feedback()
    trends = []

    for keyword in structured.research_keywords:
        result = research_keyword(keyword)
        trends.append(result)

    synthesized_insight = synthesize_insights(structured, feedback, trends)

    print("Synthesized Insight:", synthesized_insight)  # Debug print

    return {"message": f"This is an insight task for prompt {feedback} {trends}"}


@celery_app.task(name="insight_task")
def run_insight_task(prompt_text: str):
    if not prompt_text:
        return {"error": "Prompt text is required."}

    insight_result = run_insight(prompt_text)
    return insight_result
