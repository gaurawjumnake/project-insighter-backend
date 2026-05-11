import json
from backend.ai_insighter.engine.pipeline import InsightsPipeline
from backend.ai_insighter.engine.config import SCHEMAS
from backend.ai_insighter.services.prompts import PromptsTemplates
from typing import Any, Optional

pipeline = InsightsPipeline(True)

class DocumentInsightService:
 
    def __init__(self, ):
        pass
 
    def analyse(
        self,
        document_text: str,
        file_name: str = "uploaded_document",
        context_hint: str = "No additional context provided.",
    ) -> dict:

        prompt_template = PromptsTemplates.ANY_DOCUMENT_PROMPT.replace(
            "{file_name}", file_name
        ).replace(
            "{context_hint}", context_hint
        )
        # {data} left for pipeline to resolve after token routing
 
        return pipeline.run(
            data            = {"content": document_text},
            prompt_template = prompt_template,
            output_format   = SCHEMAS["any_document"],
            output_mode     = "markdown",
        )
 
 
# # Dry Run -----------------------------------------------------------
# if __name__ == "__main__":
#     document_text = """
#     Q1 2024 Strategic Review — Acme Corp
 
#     Acme Corp has seen a 14% shortfall against Q1 revenue targets driven by
#     delays in the Alpha Modernisation project. The API integration milestone,
#     originally planned for February, remains incomplete as of March 15th.
 
#     The sales team has identified two expansion opportunities: a data analytics
#     platform for the finance division and a potential AI copilot rollout across
#     their operations team. Budget discussions are scheduled for Q2.
 
#     Engineering concerns have been raised — test coverage across delivered
#     modules is averaging 46%, below the agreed 70% threshold in the SOW.
#     The client has not formally escalated this but informal signals suggest
#     dissatisfaction is growing.
 
#     Competitor activity: TechRivals Inc has approached Acme Corp's CTO with
#     a proposal for managed AI services at a 20% lower price point.
#     """
#     service = DocumentInsightService()
#     result = service.analyse(
#         document_text = document_text,
#         file_name     = "acme_corp_q1_strategic_review.pdf",
#         context_hint  = "Strategic review related to the Acme Corp account.",
#     )
 
#     print(result)