import json
from backend.ai_insighter.engine.pipeline import InsightsPipeline
from backend.ai_insighter.engine.config import SCHEMAS
from backend.ai_insighter.services.prompts import PromptsTemplates
from typing import Any, Optional

pipeline = InsightsPipeline()

def analyse(
    company_capabilities: dict,
    account_insights: list,
    pe_research_document: dict | str,
) -> dict:
    """
    Args:
        company_capabilities:  Your company's capability dict — this is
                                the compressible payload (can be large).
        account_insights:      List of pre-generated account insight dicts
                                pulled from Supabase.
        pe_research_document:  PE overview — investment thesis, sector
                                focus, financial priorities. Dict or string.

    Returns:
        Structured PE insight dict matching PE_SCHEMA.
    """
    pe_doc_str = (
        json.dumps(pe_research_document, default=str)
        if not isinstance(pe_research_document, str)
        else pe_research_document
    )

    insights_str = json.dumps(account_insights, indent=2, default=str)

    prompt_template = PromptsTemplates.PE_PROMPT.replace(
        "{pe_research_document}", pe_doc_str
    ).replace(
        "{account_insights_list}", insights_str
    )
    
    return pipeline.run(
        data            = company_capabilities,
        prompt_template = prompt_template,
        output_format   = SCHEMAS["private_equity"],
    )


# # - Dry Run ----------------------------------------------------------
# if __name__ == "__main__":
#     company_capabilities = {
#         "technical_strengths": [
#             "Cloud-native architecture", "Microservices", "DevSecOps"
#         ],
#         "ai_capabilities": [
#             "LLM integration", "MLOps pipelines", "AI-assisted QA"
#         ],
#         "delivery_strengths": [
#             "Agile delivery", "Nearshore teams", "Platform engineering"
#         ],
#         "domain_expertise": [
#             "Financial services", "Healthcare", "Retail"
#         ],
#         "qa_practice": "Automated testing frameworks, coverage enforcement, shift-left QA"
#     }

#     pe_research_document = {
#         "pe_name":          "Apex Capital Partners",
#         "investment_thesis": "Technology-led transformation of mid-market B2B companies",
#         "sector_focus":     ["FinTech", "HealthTech", "EnterpriseOps"],
#         "growth_strategy":  "AI adoption, platform modernisation, scalable delivery",
#         "financial_priorities": "EBITDA improvement, revenue growth 20% YoY",
#         "technology_direction": "Cloud migration, AI integration, legacy decommission"
#     }

#     # Pre-generated account insights pulled from Supabase
#     account_insights = [
#         {
#             "account_id":           "acct_456",
#             "account_name":         "Acme Corp",
#             "overall_health_score": 65,
#             "summary":              "Two high-risk projects, infra blockers recurring.",
#             "ai_insights":          ["Low AI adoption across most projects"],
#             "financial_insights":   ["Revenue shortfall of 14% vs expected"],
#             "risks": [
#                 {"type": "delivery", "severity": "high",
#                  "message": "Infra access blocking multiple projects"}
#             ],
#         },
#         {
#             "account_id":           "acct_789",
#             "account_name":         "BetaCo",
#             "overall_health_score": 72,
#             "summary":              "Stable delivery but low AI ROI.",
#             "ai_insights":          ["High AI hours but no measurable revenue impact"],
#             "financial_insights":   ["On-target revenue, margin thinning"],
#             "risks": [
#                 {"type": "ai", "severity": "medium",
#                  "message": "AI investment not translating to outcomes"}
#             ],
#         },
#         {
#             "account_id":           "acct_101",
#             "account_name":         "GammaTech",
#             "overall_health_score": 48,
#             "summary":              "Critical delivery risk, legacy stack blocking modernisation.",
#             "ai_insights":          ["No AI adoption"],
#             "financial_insights":   ["Significant shortfall, cost overruns"],
#             "risks": [
#                 {"type": "execution", "severity": "high",
#                  "message": "Legacy stack causing repeated delivery failures"}
#             ],
#         },
#     ]

#     result = analyse(
#         company_capabilities  = company_capabilities,
#         account_insights      = account_insights,
#         pe_research_document  = pe_research_document,
#     )

#     print(json.dumps(result, indent=2))