from backend.ai_insighter.engine.pipeline import InsightsPipeline
from backend.ai_insighter.engine.config import SCHEMAS
from backend.ai_insighter.services.prompts import PromptsTemplates
from typing import Any, Optional
import json

pipeline = InsightsPipeline()


def _to_str(value: Any) -> str:
    return value if isinstance(value, str) else json.dumps(value, indent=2, default=str)


def _normalize_project_insights(project_insights: list) -> tuple[list, list[str]]:
    normalized_project_insights = []
    project_names: list[str] = []
    for project in project_insights:
        if isinstance(project, dict):
            project_name = project.get("project_name") or project.get("project_id") or "unknown_project"
            project_names.append(str(project_name))
            project_copy = dict(project)
            project_copy["project_name"] = project_name
            normalized_project_insights.append(project_copy)
        else:
            normalized_project_insights.append(project)
    return normalized_project_insights, project_names


def _run_account_layer(
    account_data: dict,
    prompt_template: str,
    schema_key: str,
) -> dict:
    return pipeline.run(
        data=account_data,
        prompt_template=prompt_template,
        output_format=SCHEMAS[schema_key],
    )


def _append_project_name_enforcement(prompt_template: str, project_names: list[str]) -> str:
    return prompt_template + (
        "\n\n# PROJECT NAME ENFORCEMENT\n"
        "Use only the exact project names from the project insights list.\n"
        f"Allowed project names: {json.dumps(project_names, default=str)}\n"
        "Never use placeholders such as Project A, Project B, Project C, or Project D.\n"
        "If a project name is unavailable, use the project_id from input.\n"
    )


def analyse_operational_intelligence(
    account_data: dict,
    project_insights: list,
    delivery_unit_data: Optional[dict] = None,
) -> dict:
    delivery_str = json.dumps(delivery_unit_data, default=str) if delivery_unit_data else "Not available"
    normalized_project_insights, project_names = _normalize_project_insights(project_insights)

    prompt_template = PromptsTemplates.ACCOUNT_OPERATIONAL_PROMPT.replace(
        "{delivery_unit_data}", delivery_str
    ).replace(
        "{project_insights_list}", _to_str(normalized_project_insights)
    ).replace(
        "{account_data}", "{data}"
    )

    prompt_template = _append_project_name_enforcement(prompt_template, project_names)
    return _run_account_layer(account_data, prompt_template, "account_operational")


def analyse_capability_proof_intelligence(
    account_data: dict,
    project_insights: list,
    operational_layer: dict,
) -> dict:
    normalized_project_insights, project_names = _normalize_project_insights(project_insights)

    prompt_template = PromptsTemplates.ACCOUNT_CAPABILITY_PROOF_PROMPT.replace(
        "{project_insights_list}", _to_str(normalized_project_insights)
    ).replace(
        "{operational_layer}", _to_str(operational_layer)
    ).replace(
        "{account_data}", "{data}"
    )

    prompt_template = _append_project_name_enforcement(prompt_template, project_names)
    return _run_account_layer(account_data, prompt_template, "account_capability_proof")


def analyse_strategic_commercial_intelligence(
    account_data: dict,
    project_insights: list,
    operational_layer: dict,
    capability_proof_layer: dict,
) -> dict:
    normalized_project_insights, project_names = _normalize_project_insights(project_insights)

    prompt_template = PromptsTemplates.ACCOUNT_STRATEGIC_COMMERCIAL_PROMPT.replace(
        "{project_insights_list}", _to_str(normalized_project_insights)
    ).replace(
        "{operational_layer}", _to_str(operational_layer)
    ).replace(
        "{capability_proof_layer}", _to_str(capability_proof_layer)
    ).replace(
        "{account_data}", "{data}"
    )

    prompt_template = _append_project_name_enforcement(prompt_template, project_names)
    return _run_account_layer(account_data, prompt_template, "account_strategic_commercial")


def analyse_executive_synthesis_intelligence(
    account_data: dict,
    project_insights: list,
    operational_layer: dict,
    capability_proof_layer: dict,
    strategic_commercial_layer: dict,
) -> dict:
    normalized_project_insights, project_names = _normalize_project_insights(project_insights)

    prompt_template = PromptsTemplates.ACCOUNT_EXECUTIVE_SYNTHESIS_PROMPT.replace(
        "{project_insights_list}", _to_str(normalized_project_insights)
    ).replace(
        "{operational_layer}", _to_str(operational_layer)
    ).replace(
        "{capability_proof_layer}", _to_str(capability_proof_layer)
    ).replace(
        "{strategic_commercial_layer}", _to_str(strategic_commercial_layer)
    ).replace(
        "{account_data}", "{data}"
    )

    prompt_template = _append_project_name_enforcement(prompt_template, project_names)
    return _run_account_layer(account_data, prompt_template, "account_executive_synthesis")


def run_full_account_intelligence(
    account_data: dict,
    project_insights: list,
    delivery_unit_data: Optional[dict] = None,
) -> dict:
    operational_layer = analyse_operational_intelligence(
        account_data=account_data,
        project_insights=project_insights,
        delivery_unit_data=delivery_unit_data,
    )
    capability_proof_layer = analyse_capability_proof_intelligence(
        account_data=account_data,
        project_insights=project_insights,
        operational_layer=operational_layer,
    )
    strategic_commercial_layer = analyse_strategic_commercial_intelligence(
        account_data=account_data,
        project_insights=project_insights,
        operational_layer=operational_layer,
        capability_proof_layer=capability_proof_layer,
    )
    executive_synthesis_layer = analyse_executive_synthesis_intelligence(
        account_data=account_data,
        project_insights=project_insights,
        operational_layer=operational_layer,
        capability_proof_layer=capability_proof_layer,
        strategic_commercial_layer=strategic_commercial_layer,
    )

    combined = {}
    if isinstance(operational_layer, dict):
        combined.update(operational_layer)
    if isinstance(capability_proof_layer, dict):
        combined.update(capability_proof_layer)
    if isinstance(strategic_commercial_layer, dict):
        combined.update(strategic_commercial_layer)
    if isinstance(executive_synthesis_layer, dict):
        combined.update(executive_synthesis_layer)

    combined["account_id"] = account_data.get("account_id")
    combined["account_name"] = account_data.get("account_name")
    return combined


def analyse(
    account_data: dict,
    project_insights: list,
    delivery_unit_data: Optional[dict] = None,
) -> dict:
    """
    Backward-compatible account entrypoint.
    Now runs layered account intelligence and returns one merged object.
    """
    return run_full_account_intelligence(
        account_data=account_data,
        project_insights=project_insights,
        delivery_unit_data=delivery_unit_data,
    )
