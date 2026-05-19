"""
Insights Pipeline
--------─
Entry point: InsightsPipeline.run(data, instructions, entity_type)

Flow:
  1. Token-count the payload
  2. Pre-summarise if over threshold  (single LLM call, no agent)
  3. Researcher  → structures the context
  4. Analyzer    → deep analysis, risks, recommendations
  5. Summarizer  → strict JSON output matching output schema

Interface:
    pipeline.run(
        data            = <dict>,   # raw data — compressed if over token limit
        prompt_template = <str>,    # analyst prompt with {data} placeholder
        output_format   = <dict>,   # exact JSON schema to produce
    ) -> dict
"""
import json
from typing import Any
import re
from backend.utitlites.llm_models import llm
from crewai import Agent, Crew, Task
from backend.ai_insighter.engine.config import TOKEN_THRESHOLD


def _count_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.encoding_for_model("gpt-4o")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4


def _extract_json(text: str) -> dict:
    """Pull the first valid JSON object out of any LLM response."""
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        return {"raw_output": text}


class InsightsPipeline:

    def __init__(self, verbose: bool = False):
        self.llm     = llm
        self.verbose = verbose

    # - Entry Point -------------------------------------------------------
    def run(
        self,
        data: dict,
        prompt_template: str,
        output_format: dict,
        output_mode: str = "json"
    ) -> Any:
        data_str = self._prepare_data(data)
        prompt   = prompt_template.replace("{data}", data_str)

        research_task      = self._research_task(prompt)
        analysis_task      = self._analysis_task(research_task)

        if output_mode == "markdown":
            final_task = self._markdown_task(analysis_task)
        else:
            final_task = self._summarization_task(output_format, analysis_task)

        crew = Crew(
            agents=[
                self._researcher(),
                self._analyzer(),
                self._summarizer(),
            ],
            tasks=[research_task, analysis_task, final_task],
            verbose=self.verbose,
        )

        result = crew.kickoff()

        if output_mode == "markdown":
            return str(result) 
        
        return _extract_json(str(result))

    # - Data preparation ---------------------------------------------------------

    def _prepare_data(self, data: dict) -> str:
        """
        Serialise data to string.
        If over threshold — compress data only with a single LLM call.
        Prompt template is never touched.
        """
        raw = json.dumps(data, default=str)

        if _count_tokens(raw) <= TOKEN_THRESHOLD:
            return raw

        compressed = self.llm.invoke( #type: ignore
            "Compress the following JSON into a concise structured summary. "
            "Preserve all key metrics, numbers, dates, risks, and entity identifiers. "
            "Remove verbose text but keep every fact.\n\n"
            f"{raw}"
        ).content 

        return compressed

    # - Agents -------------------------------------------------------------

    def _researcher(self) -> Agent:
        return Agent(
            role="Research Specialist",
            backstory=(
                "Expert at reading structured business data and extracting "
                "clean, faithful context for analysis. Never invents facts."
            ),
            goal=(
                "Read the data provided in the task. Identify all available "
                "fields, summarise key metrics and documents, and flag any "
                "missing or partial data for the Analyzer."
            ),
            llm=self.llm,
            verbose=self.verbose,
        )

    def _analyzer(self) -> Agent:
        return Agent(
            role="Analytics Specialist",
            backstory=(
                "Senior analyst with expertise in business performance, "
                "risk identification, and opportunity assessment. "
                "Findings are always specific and evidence-backed."
            ),
            goal=(
                "Perform deep analysis on the research brief using the "
                "instructions provided. Identify risks, trends, anomalies, "
                "and opportunities. Never make generic statements."
            ),
            llm=self.llm,
            verbose=self.verbose,
        )

    def _summarizer(self, output_mode: str = "json") -> Agent:
        if output_mode == "markdown":
            return Agent(
                role="Insights Synthesizer",
                backstory=(
                    "Expert at converting analytical findings into clean, "
                    "structured markdown reports for business leadership."
                ),
                goal=(
                    "Convert the analysis into a well-structured markdown report. "
                    "Skip sections with no real signal. "
                    "Return only the markdown — no preamble, no explanation."
                ),
                llm=self.llm,
                verbose=self.verbose,
            )
 
        return Agent(
            role="Insights Synthesizer",
            backstory=(
                "Expert at converting analytical findings into clean, "
                "structured JSON. Follows output schemas strictly."
            ),
            goal=(
                "Convert the analysis into valid JSON matching the required "
                "schema exactly. Return only the JSON — no markdown, "
                "no explanation, no code fences."
            ),
            llm=self.llm,
            verbose=self.verbose,
        )

    # - Tasks --------------------------------------------------------------

    def _research_task(self, prompt: str) -> Task:
        return Task(
            description=(
                f"{prompt}\n\n"
                "Your job at this stage:\n"
                "1. Parse all available fields — metadata, metrics, documents\n"
                "2. Summarise financial, operational, and document data\n"
                "3. Flag missing or partial data clearly\n"
                "4. Produce a clean, faithful research brief for the Analyzer\n"
                "Do not invent any facts not present in the data."
            ),
            expected_output=(
                "Structured research brief covering entity metadata, key metrics, "
                "document highlights, data gaps, and analysis focus areas."
            ),
            agent=self._researcher(),
        )

    def _analysis_task(self, research_task: Task) -> Task:
        return Task(
            description=(
                "Using the research brief and the original instructions, "
                "perform deep analysis.\n\n"
                "Rules:\n"
                "- Every insight must be specific and evidence-backed\n"
                "- Detect and explicitly call out contradictions\n"
                "- If data is missing, state the limitation — do not invent\n"
                "- Prefer: 'X indicates Y risk because Z'\n"
                "- Prioritise findings by business impact"
            ),
            expected_output=(
                "Prioritised analytical findings: risks, opportunities, "
                "performance signals, contradictions, and recommendations."
            ),
            agent=self._analyzer(),
            context=[research_task],
        )

    def _summarization_task(self, output_format: dict, analysis_task: Task) -> Task:
        schema_str = json.dumps(output_format, indent=2)
        return Task(
            description=(
                "Convert the analysis into valid JSON matching this schema exactly:\n\n"
                f"{schema_str}\n\n"
                "Rules:\n"
                "- Return only the JSON object — nothing else\n"
                "- No markdown, no code fences, no explanation outside JSON\n"
                "- Fill every field; use empty list [] if no data supports it\n"
                "- health_score values must be 0-100\n"
                "- severity / impact values: low | medium | high only"
            ),
            expected_output="A single valid JSON object matching the schema above.",
            agent=self._summarizer(),
            context=[analysis_task],
        )
    
    def _markdown_task(self, analysis_task: Task) -> Task:
        return Task(
            description=(
                "Convert the analysis into a structured markdown report "
                "following the output format in the original instructions.\n\n"
                "Rules:\n"
                "- Skip any section with no real signal\n"
                "- Every insight must be specific and decision-relevant\n"
                "- Return only the markdown — no preamble, no extra explanation"
            ),
            expected_output="A structured markdown report.",
            agent=self._summarizer("markdown"),
            context=[analysis_task],
        )