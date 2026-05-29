import json
from typing import Any

from backend.ai_insighter.engine.pipeline import InsightsPipeline
from backend.ai_insighter.engine.config import SCHEMAS
from backend.ai_insighter.services.prompts import PromptsTemplates

pipeline = InsightsPipeline()


def _to_str(value: Any) -> str:
    return value if isinstance(value, str) else json.dumps(value, indent=2, default=str)


def _schema(schema_key: str) -> dict:
    schema = SCHEMAS.get(schema_key)
    if schema is None:
        raise ValueError(
            f"Schema '{schema_key}' not found in SCHEMAS. "
            "Please add it in backend/ai_insighter/engine/config.py."
        )
    return schema


def _run_prompt(
    company_capabilities: dict,
    prompt_template: str,
    schema_key: str,
) -> dict:
    return pipeline.run(
        data=company_capabilities,
        prompt_template=prompt_template,
        output_format=_schema(schema_key),
    )


def analyse_portfolio_intelligence(
    company_capabilities: dict,
    account_insights: list,
    pe_research_document: Any,
) -> dict:
    prompt_template = PromptsTemplates.PE_PORTFOLIO_PROMPT.replace(
        "{pe_research_document}", _to_str(pe_research_document)
    ).replace(
        "{account_insights_list}", _to_str(account_insights)
    )

    return _run_prompt(
        company_capabilities=company_capabilities,
        prompt_template=prompt_template,
        schema_key="pe_portfolio",
    )


def extract_proof_points(
    company_capabilities: dict,
    account_insights: list,
    pe_research_document: Any,
) -> dict:
    prompt_template = PromptsTemplates.PE_PROOF_POINT_PROMPT.replace(
        "{pe_research_document}", _to_str(pe_research_document)
    ).replace(
        "{account_insights_list}", _to_str(account_insights)
    )

    return _run_prompt(
        company_capabilities=company_capabilities,
        prompt_template=prompt_template,
        schema_key="pe_proof_point",
    )


def detect_buying_signals(
    company_capabilities: dict,
    account_insights: list,
    pe_research_document: Any,
) -> dict:
    prompt_template = PromptsTemplates.PE_BUYING_SIGNAL_PROMPT.replace(
        "{pe_research_document}", _to_str(pe_research_document)
    ).replace(
        "{account_insights_list}", _to_str(account_insights)
    )

    return _run_prompt(
        company_capabilities=company_capabilities,
        prompt_template=prompt_template,
        schema_key="pe_buying_signal",
    )


def generate_whitespace_opportunities(
    company_capabilities: dict,
    portfolio_insights: dict,
    proof_points: dict,
    buying_signals: dict,
) -> dict:
    prompt_template = PromptsTemplates.PE_WHITESPACE_PROMPT.replace(
        "{portfolio_insights}", _to_str(portfolio_insights)
    ).replace(
        "{proof_points}", _to_str(proof_points)
    ).replace(
        "{buying_signals}", _to_str(buying_signals)
    )

    return _run_prompt(
        company_capabilities=company_capabilities,
        prompt_template=prompt_template,
        schema_key="pe_whitespace",
    )


def generate_executive_strategy(
    company_capabilities: dict,
    portfolio_insights: dict,
    whitespace_opportunities: dict,
    proof_points: dict,
    buying_signals: dict,
) -> dict:
    prompt_template = PromptsTemplates.PE_EXECUTIVE_STRATEGY_PROMPT.replace(
        "{portfolio_insights}", _to_str(portfolio_insights)
    ).replace(
        "{whitespace_opportunities}", _to_str(whitespace_opportunities)
    ).replace(
        "{proof_points}", _to_str(proof_points)
    ).replace(
        "{buying_signals}", _to_str(buying_signals)
    )

    return _run_prompt(
        company_capabilities=company_capabilities,
        prompt_template=prompt_template,
        schema_key="pe_executive_strategy",
    )


def run_full_pe_strategy(
    company_capabilities: dict,
    account_insights: list,
    pe_research_document: Any,
) -> dict:
    portfolio_insights = analyse_portfolio_intelligence(
        company_capabilities=company_capabilities,
        account_insights=account_insights,
        pe_research_document=pe_research_document,
    )
    proof_points = extract_proof_points(
        company_capabilities=company_capabilities,
        account_insights=account_insights,
        pe_research_document=pe_research_document,
    )
    buying_signals = detect_buying_signals(
        company_capabilities=company_capabilities,
        account_insights=account_insights,
        pe_research_document=pe_research_document,
    )
    whitespace_opportunities = generate_whitespace_opportunities(
        company_capabilities=company_capabilities,
        portfolio_insights=portfolio_insights,
        proof_points=proof_points,
        buying_signals=buying_signals,
    )
    executive_strategy = generate_executive_strategy(
        company_capabilities=company_capabilities,
        portfolio_insights=portfolio_insights,
        whitespace_opportunities=whitespace_opportunities,
        proof_points=proof_points,
        buying_signals=buying_signals,
    )

    return {
        "portfolio_insights": portfolio_insights,
        "proof_points": proof_points,
        "buying_signals": buying_signals,
        "whitespace_opportunities": whitespace_opportunities,
        "executive_strategy": executive_strategy,
    }


def analyse(
    company_capabilities: dict,
    account_insights: list,
    pe_research_document: Any,
) -> dict:
    """
    Backward-compatible PE analysis wrapper.
    Uses the original prompt/schema for existing callers.
    """
    prompt_template = PromptsTemplates.PE_PROMPT.replace(
        "{pe_research_document}", _to_str(pe_research_document)
    ).replace(
        "{account_insights_list}", _to_str(account_insights)
    )

    return _run_prompt(
        company_capabilities=company_capabilities,
        prompt_template=prompt_template,
        schema_key="private_equity",
    )
