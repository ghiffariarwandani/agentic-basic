import csv
from pathlib import Path

from app.utils.openai import oa_client

from .schema import StructuredContext

csv_path = Path("app/__mock__/feedback.csv")


def parse_prompt_to_context(prompt_text: str) -> StructuredContext:
    context = oa_client.chat.completions.parse(
        model="google/gemini-3-flash-preview",
        messages=[
            {
                "role": "system",
                "content": (
                    "Return JSON only. No markdown, no explanation, no extra keys. "
                    "Use exactly these keys: "
                    "product_name, requested_feature, target_user_segment, target_region, "
                    "competitor_names, research_keywords, desired_outcomes, operating_constraints."
                ),
            },
            {"role": "user", "content": f"Prompt text: {prompt_text}"},
        ],
        response_format=StructuredContext,
    )

    parsed = context.choices[0].message.parsed.model_dump()
    return StructuredContext(**parsed)


def get_feedback():
    feedback_list = []

    with csv_path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        for row in rows:
            data = {
                "pain_point": row["pain_point"],
                "feature_request": row["feature_request"],
                "sentiment": row["sentiment"],
                "rating_1_5": row["rating_1_5"],
                "priority_hint": row["priority_hint"],
                "feedback_id": row["feedback_id"],
            }
            feedback_list.append(data)

    return feedback_list


def research_keywords():
    trends = []
    return trends


def synthesize_insights():
    insights = []
    return insights


def generate_insight():
    insight = {}
    return insight
