import csv
from pathlib import Path

from app.utils.openai import oa_client
from app.utils.tavily import tavily_client

from .prompts import OUTPUT_PROMPT, SYNTHESIZE_PROMPT
from .schema import InsightResult, KeywordSchema, StructuredContext

csv_path = Path("app/__mock__/feedback.csv")


def parse_prompt_to_context(prompt_text: str) -> StructuredContext:
    context = oa_client.chat.completions.parse(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": (
                    "Return JSON only. No markdown, no explanation, no extra keys. "
                    "Use exactly these keys: "
                    "product_name, requested_feature, target_user_segment, target_region, "
                    "research_keywords, desired_outcomes, operating_constraints."
                ),
            },
            {"role": "user", "content": f"Prompt text: {prompt_text}"},
        ],
        response_format=StructuredContext,
    )

    parsed = context.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Failed to parse context into schema.")
    return parsed


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
                "priority_hint": row["priority_hint"],
                "feedback_id": row["feedback_id"],
            }
            feedback_list.append(data)

    return feedback_list


def research_keyword(keyword: str):
    trends = tavily_client.search(
        query=keyword,
        search_depth="advanced",
        max_results=1,
        start_date="2026-01-01",
        end_date="2026-03-03",
        country="indonesia",
    )

    response = oa_client.chat.completions.parse(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": (
                    "Return valid JSON only. No markdown. "
                    "Use exactly this keys: keyword,title,url,published_at,source,summary,relevance_reason. "
                    "Do not add extra keys. If data missing, use empty string."
                ),
            },
            {"role": "user", "content": f"Search Results: {trends}"},
        ],
        response_format=KeywordSchema,
    )

    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Failed to parse keyword into schema.")
    return parsed


def synthesize_insights(context: StructuredContext, feedback: list[dict], trends: list[KeywordSchema]):
    synthesized = oa_client.chat.completions.parse(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": SYNTHESIZE_PROMPT,
            },
            {
                "role": "user",
                "content": f"Context: {context}, Feedback: {feedback}, Trends: {trends}",
            },
        ],
        response_format=InsightResult,
    )

    parsed = synthesized.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Failed to parse synthesized schema.")
    return parsed


def generate_insight(prompt_text: str, synthesized_insight: InsightResult):
    result = oa_client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": OUTPUT_PROMPT,
            },
            {
                "role": "user",
                "content": f"Context: {prompt_text}, Synthesized Insight: {synthesized_insight}",
            },
        ],
    )
    return result.choices[0].message.content
