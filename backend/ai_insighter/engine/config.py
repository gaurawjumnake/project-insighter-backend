
TOKEN_THRESHOLD  = 6000      # compress data section if it exceeds this

# ── Output schemas ────────────────────────────────────────────
PROJECT_SCHEMA = {
    "project_name": "",
    "health_score": 0,
    "summary": "",
    # Operational insights
    "delivery_insights":    [],
    "financial_insights":   [],
    "ai_insights":          [],
    "engineering_insights": [],
    "timeline_insights":    [],
    "governance_insights":  [],
    # Tech positioning — NEW
    "tech_stack_insights": [
        {
            "technology":  "",
            "domain":      "frontend|backend|cloud|data|ai_ml|devops|qa|security|other",
            "status":      "strong|moderate|lagging",
            "observation": "",
            "source":      "structured|inferred from SOW|inferred from WSR"
        }
    ],
    # Capability gaps — NEW
    "capability_gaps": [
        {
            "gap":      "",
            "domain":   "",
            "impact":   "high|medium|low",
            "evidence": "",
            "suggestion": ""
        }
    ],
    # Commercial pitch signals — NEW
    "pitch_signals": [
        {
            "opportunity":       "",
            "rationale":         "",
            "expected_outcome":  "",
            "priority":          "high|medium|low"
        }
    ],
    "risks": [
        {
            "type":     "delivery|financial|engineering|ai|governance|technology",
            "severity": "low|medium|high",
            "message":  ""
        }
    ],
    "opportunities": [
        {
            "type":    "ai_adoption|optimization|expansion|quality_improvement|modernization",
            "impact":  "low|medium|high",
            "message": ""
        }
    ],
    "recommendations": []
}

ACCOUNT_SCHEMA = {
    "account_name": "",
    "overall_health_score": 0,
    "summary": "",
    # Existing pattern-level insights
    "portfolio_insights":  [],
    "financial_insights":  [],
    "delivery_insights":   [],
    "ai_insights":         [],
    "governance_insights": [],
    # NEW — named project risk attribution
    "project_risk_attribution": [
        {
            "risk":                 "",
            "affected_projects":    [],     # list of project names
            "severity":             "high|medium|low",
            "account_level_impact": ""
        }
    ],
    # NEW — cross-project success replication
    "replication_opportunities": [
        {
            "practice":          "",        # what is working
            "source_project":    "",        # where it works well
            "target_projects":   [],        # where it should be applied
            "expected_benefit":  "",
            "effort":            "high|medium|low"
        }
    ],
    # NEW — prioritised account improvement roadmap
    "account_improvement_plan": [
        {
            "improvement":       "",
            "affected_projects": [],        # project names impacted
            "priority":          "high|medium|low",
            "rationale":         "",
            "expected_outcome":  ""
        }
    ],
    "risks": [
        {
            "type":     "delivery|financial|ai|governance|concentration|technology",
            "severity": "low|medium|high",
            "message":  ""
        }
    ],
    "opportunities": [
        {
            "type":    "ai_scaling|revenue_expansion|optimization|cross_project_reuse",
            "impact":  "low|medium|high",
            "message": ""
        }
    ],
    "recommendations": []
}

PE_SCHEMA = {

    "pe_name": "",

    "portfolio_summary": "",

    # Existing portfolio-level insights

    "portfolio_insights": [],

    # Existing gap analysis

    "strategic_gaps": [

        {

            "gap_type":    "technology|ai|delivery|revenue|governance",

            "description": "",

            "impact":      "low|medium|high",

            "affected_accounts": []         # account names as evidence

        }

    ],

    # Existing capability mapping

    "capability_alignment": [

        {

            "gap":                  "",

            "relevant_capability":  "",

            "solution_approach":    "",

            "affected_accounts":    []      # who benefits

        }

    ],

    # NEW — cross-account success replication

    "cross_account_replication": [

        {

            "success":          "",         # what worked

            "source_account":   "",         # proof point — account where it worked

            "evidence":         "",         # specific metric or outcome

            "target_accounts":  [],         # accounts that have the same gap

            "capability_used":  "",         # company capability that enabled it

            "pitch":            "",         # 1-2 line consulting pitch

            "impact":           "high|medium|low"

        }

    ],

    "opportunities": [

        {

            "type":        "portfolio_transformation|ai_scaling|modernization|optimization",

            "impact":      "low|medium|high",

            "description": "",

            "accounts_affected": []

        }

    ],

    "risks": [

        {

            "type":        "portfolio|financial|execution|concentration",

            "severity":    "low|medium|high",

            "description": "",

            "accounts_affected": []

        }

    ],

    "strategic_recommendations": [],

    # Updated — each pitch point now has evidence and target audience

    "leadership_pitch": [

        {

            "point":               "",      # 1-2 line outcome-driven pitch

            "supporting_evidence": "",      # specific account data or metric

            "target_audience":     "pe_leadership|portfolio_ceo|cto"

        }

    ]

}
 

ANY_DOCUMENT_SCHEMA = {"mode":"markdown"}

SCHEMAS = {
    "project":        PROJECT_SCHEMA,
    "account":        ACCOUNT_SCHEMA,
    "private_equity": PE_SCHEMA,
    "any_document":   ANY_DOCUMENT_SCHEMA
}