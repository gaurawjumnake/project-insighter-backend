
TOKEN_THRESHOLD  = 6000      # compress data section if it exceeds this

# ── Output schemas ────────────────────────────────────────────
PROJECT_SCHEMA = {
    "project_name": "",
    "health_score": 0,
    "summary": "",
    "delivery_insights": [],
    "financial_insights": [],
    "ai_insights": [],
    "engineering_insights": [],
    "timeline_insights": [],
    "governance_insights": [],
    "risks": [{"type": "", "severity": "low|medium|high", "message": ""}],
    "opportunities": [{"type": "", "impact": "low|medium|high", "message": ""}],
    "recommendations": []
}

ACCOUNT_SCHEMA = {
    "account_name": "",
    "overall_health_score": 0,
    "summary": "",
    "portfolio_insights": [],
    "financial_insights": [],
    "delivery_insights": [],
    "ai_insights": [],
    "governance_insights": [],
    "risks": [{"type": "", "severity": "low|medium|high", "message": ""}],
    "opportunities": [{"type": "", "impact": "low|medium|high", "message": ""}],
    "recommendations": []
}

PE_SCHEMA = {
    "pe_name": "",
    "portfolio_summary": "",
    "portfolio_insights": [],
    "strategic_gaps": [{"gap_type": "", "description": "", "impact": "low|medium|high"}],
    "capability_alignment": [{"gap": "", "relevant_capability": "", "solution_approach": ""}],
    "opportunities": [{"type": "", "impact": "low|medium|high", "description": ""}],
    "risks": [{"type": "", "severity": "low|medium|high", "description": ""}],
    "strategic_recommendations": [],
    "leadership_pitch": []
}

ANY_DOCUMENT_SCHEMA = {"mode":"markdown"}

SCHEMAS = {
    "project":        PROJECT_SCHEMA,
    "account":        ACCOUNT_SCHEMA,
    "private_equity": PE_SCHEMA,
    "any_document":   ANY_DOCUMENT_SCHEMA
}