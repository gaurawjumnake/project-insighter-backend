from backend.ai_insighter.engine.pipeline import InsightsPipeline
from backend.ai_insighter.engine.config import SCHEMAS
from backend.ai_insighter.services.prompts import PromptsTemplates

pipeline = InsightsPipeline(True)

def analyse(project_data: dict) -> dict:
    return pipeline.run(
        data            = project_data,
        prompt_template = PromptsTemplates.PROJECT_PROMPT,
        output_format   = SCHEMAS["project"],
    )

# # - DRY Run -------------------------------------------------------
# if __name__ == "__main__":
#     data = {
#         "project_id":   "proj_123",
#         "project_name": "Alpha Modernisation",
#         "account_id":   "acct_456",
#         "status":       "active",
#         "from_date":    "2024-01-01",
#         "to_date":      "2024-06-30",
#         "revenue": [
#             {"month": "2024-01", "mrr": 45000, "margin": 0.31},
#             {"month": "2024-02", "mrr": 43000, "margin": 0.28},
#         ],
#         "documents": [
#             {
#                 "doc_type": "wsr",
#                 "period":   "2024-W10",
#                 "extracted_content": (
#                     "API integration delayed by 2 weeks. Team blocked on "
#                     "environment access. Status marked as on-track by PM."
#                 ),
#             },
#             {
#                 "doc_type": "sow",
#                 "extracted_content": "Deliver Phase 1 by March 2024.",
#             },
#         ],
#         "ai_direct_hours":  12,
#         "ai_assist_hours":  4,
#         "code_coverage_pct": 44,
#     }

#     result = analyse(data)
#     import json
#     print(json.dumps(result, indent=2))