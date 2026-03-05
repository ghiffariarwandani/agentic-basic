from pydantic import BaseModel


class InsightRequest(BaseModel):
    prompt_text: str


class StructuredContext(BaseModel):
    product_name: str
    requested_feature: str
    target_user_segment: str
    target_region: str
    research_keywords: list[str]
    desired_outcomes: list[str]
    operating_constraints: list[str]


class KeywordSchema(BaseModel):
    keyword: str
    title: str
    url: str
    published_at: str
    source: str
    summary: str
    relevance_reason: str


class InsightItem(BaseModel):
    action: str
    reason: str
    priority: str
    evidence_feedback_ids: list[str]
    evidence_trend_urls: list[str]


class InsightResult(BaseModel):
    summary: str
    now: list[InsightItem]
    next: list[InsightItem]
    later: list[InsightItem]
