from pydantic import BaseModel


class InsightRequest(BaseModel):
    prompt_text: str


class StructuredContext(BaseModel):
    product_name: str
    requested_feature: str
    target_user_segment: str
    target_region: str
    competitor_names: list[str]
    research_keywords: list[str]
    desired_outcomes: list[str]
    operating_constraints: list[str]
