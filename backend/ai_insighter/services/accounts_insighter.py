from backend.ai_insighter.engine.pipeline import InsightsPipeline
from backend.ai_insighter.engine.config import SCHEMAS
from backend.ai_insighter.services.prompts import PromptsTemplates
from typing import Any, Optional
import json
pipeline = InsightsPipeline()

def analyse(
    account_data: dict,
    project_insights: list,
    delivery_unit_data: Optional[dict] = None,
) -> dict:
    """
    Args:
        account_data:       Account metadata + revenue from Supabase.
        project_insights:   List of pre-generated project insight dicts
                            pulled from Supabase. Already generated —
                            never re-analysed here.
        delivery_unit_data: Optional delivery unit metrics dict.

    Returns:
        Structured account insight dict matching ACCOUNT_SCHEMA.
    """

    delivery_str = (
        json.dumps(delivery_unit_data, default=str)
        if delivery_unit_data
        else "Not available"
    )

    # Project insights are already compact summaries — inject directly
    insights_str = json.dumps(project_insights, indent=2, default=str)

    # Build a prompt template with {data} for account_data (compressible)
    # and the other two sections already resolved
    prompt_template = PromptsTemplates.ACCOUNTS_PROMPT.replace(
        "{delivery_unit_data}", delivery_str
    ).replace(
        "{project_insights_list}", insights_str
    )
    # {account_data} becomes {data} — pipeline replaces {data} with
    # compressed or raw account_data
    prompt_template = prompt_template.replace("{account_data}", "{data}")

    return pipeline.run(
        data            = account_data,
        prompt_template = prompt_template,
        output_format   = SCHEMAS["account"],
    )

 
# # - Dry Run ----------------------------------------------------------
# if __name__ == "__main__":
#     account_data = {
#         "account_id":   "acct_456",
#         "account_name": "Acme Corp",
#         "industry":     "Financial Services",
#         "revenue": [
#             {"month": "2024-01", "current_revenue": 180000, "expected_revenue": 200000},
#             {"month": "2024-02", "current_revenue": 172000, "expected_revenue": 200000},
#         ],
#         "ai_revenue":    24000,
#         "ai_hours_total": 310,
#     }
 
#     # Pre-generated project insights pulled from Supabase
#     project_insights = [
#         {
#             "project_id":   "proj_123",
#             "project_name": "Alpha Modernisation",
#             "health_score": 62,
#             "summary":      "Delayed delivery, margin pressure in Feb.",
#             "risks": [
#                 {"type": "delivery", "severity": "high",
#                  "message": "API integration blocked for 2 weeks"}
#             ],
#             "opportunities": [],
#             "ai_insights":   ["Low AI utilisation — 16 hours total"],
#             "engineering_insights": ["Code coverage at 44% — high risk"],
#         },
#         {
#             "project_id":   "proj_124",
#             "project_name": "Beta Analytics",
#             "health_score": 78,
#             "summary":      "On track, good AI utilisation.",
#             "risks": [
#                 {"type": "governance", "severity": "low",
#                  "message": "WSR submissions inconsistent"}
#             ],
#             "opportunities": [
#                 {"type": "ai_scaling", "impact": "medium",
#                  "message": "AI assist usage can be expanded"}
#             ],
#             "ai_insights":   ["Strong AI direct usage — 85 hours"],
#             "engineering_insights": ["Coverage at 72% — good"],
#         },
#         {
#             "project_id":   "proj_125",
#             "project_name": "Gamma Migration",
#             "health_score": 55,
#             "summary":      "Timeline overrun risk, blocked on infra access.",
#             "risks": [
#                 {"type": "delivery", "severity": "high",
#                  "message": "Infra access blocked — same pattern as Alpha"}
#             ],
#             "opportunities": [],
#             "ai_insights":   ["AI usage minimal — 8 hours"],
#             "engineering_insights": ["Coverage at 48% — high risk"],
#         },
#     ]
 
#     result = analyse(
#         account_data    = account_data,
#         project_insights = project_insights,
#     )
 
#     import json
#     print(json.dumps(result, indent=2))