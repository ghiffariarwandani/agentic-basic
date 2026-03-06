from datetime import datetime

from fpdf import FPDF
from markdown import markdown

from app.celery import celery_app
from app.modules.insight.methods import (
    generate_insight,
    get_feedback,
    parse_prompt_to_context,
    research_keyword,
    synthesize_insights,
)


def run_insight(prompt_text: str):
    structured = parse_prompt_to_context(prompt_text)
    feedback = get_feedback()
    trends = []

    for keyword in structured.research_keywords:
        result = research_keyword(keyword)
        trends.append(result)

    synthesized_insight = synthesize_insights(structured, feedback, trends)
    research_result = generate_insight(prompt_text, synthesized_insight)

    now = datetime.now()
    result = markdown(text=research_result, output_format="html")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.write_html(result)
    pdf.output(f"research-{now}.pdf")


@celery_app.task(name="insight_task")
def run_insight_task(prompt_text: str):
    if not prompt_text:
        return {"error": "Prompt text is required."}

    insight_result = run_insight(prompt_text)
    return insight_result
