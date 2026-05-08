# Prompt: CrewAI Workflow Design

**For:** Designing multi-agent AI workflows  
**Used by:** @ai-arch agent

---

## 🎯 OBJECTIVE

Design CrewAI crews that are:
- Task-focused with clear roles
- Observable and debuggable
- Token-efficient (GPT-4o budget awareness)
- Error-resilient with retry logic
- Scalable to new doc types

---

## 📋 CHECKLIST BEFORE GENERATING CODE

- [ ] Document type specified (SOW, WSR, Code Review, etc.)
- [ ] Expected output format defined (JSON schema)
- [ ] Agent roles identified (minimum 2, max 4 per crew)
- [ ] Tools listed (S3 reader, validator, formatter, etc.)
- [ ] Error scenarios anticipated (parsing fail, LLM timeout, invalid output)
- [ ] Context requirements stated (which fields needed from DB)
- [ ] Token budget estimated for the flow
- [ ] Existing doc processor patterns reviewed

---

## 🏗️ CREW STRUCTURE TEMPLATE

```python
# File: backend/doc_insighter/core/ai_agent.py

from crewai import Agent, Task, Crew, Tool
from crewai.process import Process
from typing import Any, Dict
import json
import logging

logger = logging.getLogger(__name__)

class {DocType}DocumentCrew:
    """
    Crew for {doctype_description} document analysis.
    
    Process:
    1. Extract text/tables from document
    2. Identify key metrics and KPIs
    3. Flag risks and issues
    4. Format structured output
    
    Expected Input: S3 path to {doctype} document
    Expected Output: JSON with kpis, risks, confidence scores
    """
    
    def __init__(self, llm_client=None):
        """Initialize crew with shared LLM client."""
        self.llm = llm_client or get_llm_client()
        self.tools = self._setup_tools()
        self.agents = self._setup_agents()
        self.crew = self._setup_crew()
    
    def _setup_tools(self) -> list[Tool]:
        """Define tools available to agents."""
        
        # Tool 1: Read from S3
        def read_s3_document(s3_path: str) -> str:
            """Read and return document content from S3."""
            from backend.utitlites.s3_storage import S3Client
            s3 = S3Client()
            return s3.download_file(s3_path)
        
        s3_tool = Tool(
            name="read_s3_document",
            func=read_s3_document,
            description="Read document content from S3 by path (e.g., s3://bucket/file.pdf)"
        )
        
        # Tool 2: Validate JSON output
        def validate_json_schema(json_str: str, schema: dict) -> bool:
            """Validate JSON against schema."""
            try:
                import jsonschema
                obj = json.loads(json_str)
                jsonschema.validate(obj, schema)
                return True
            except Exception as e:
                logger.error(f"Schema validation failed: {e}")
                return False
        
        validation_tool = Tool(
            name="validate_output_schema",
            func=validate_json_schema,
            description="Validate JSON output against expected schema"
        )
        
        return [s3_tool, validation_tool]
    
    def _setup_agents(self) -> dict[str, Agent]:
        """Define agents with roles and responsibilities."""
        
        # Agent 1: Extractor
        extractor = Agent(
            role="Document Extractor",
            goal="Extract key information from {doctype} documents accurately",
            backstory="Expert document analyst with 15+ years in {domain}. "
                     "Focused on precision and completeness.",
            tools=[self.tools[0]],  # S3 reader
            verbose=True,
            max_iter=3,  # Prevent infinite loops
            temperature=0.2  # Low temp for factual extraction
        )
        
        # Agent 2: Analyzer
        analyzer = Agent(
            role="KPI Analyzer",
            goal="Identify critical KPIs and metrics from extracted information",
            backstory="Data analyst with expertise in {domain} metrics. "
                     "Skilled at spotting anomalies and trends.",
            tools=[self.tools[1]],  # Validation
            verbose=True,
            max_iter=3,
            temperature=0.3
        )
        
        # Agent 3: Risk Officer (optional, for high-stakes docs)
        risk_officer = Agent(
            role="Risk Assessment Officer",
            goal="Identify risks, issues, and red flags in the document",
            backstory="Risk management professional. "
                     "Experienced in {domain} risk patterns.",
            verbose=True,
            max_iter=2,
            temperature=0.2
        )
        
        return {
            "extractor": extractor,
            "analyzer": analyzer,
            "risk_officer": risk_officer
        }
    
    def _setup_crew(self) -> Crew:
        """Define task workflow and crew."""
        
        # Task 1: Extract information
        extract_task = Task(
            description="""
            Extract all key information from the {doctype} document at: {doc_path}
            
            Focus on:
            - Timeline/dates
            - Budget/cost figures
            - Resource requirements
            - Deliverables
            - Team composition
            
            Return as structured JSON:
            {
                "timeline": "string",
                "budget_usd": "float",
                "resources": "list of string",
                "deliverables": "list of string",
                "team": "list of string"
            }
            """,
            expected_output="Extracted JSON with all key fields populated",
            agent=self.agents["extractor"],
            output_file="extracted_content.json"
        )
        
        # Task 2: Analyze KPIs
        analyze_task = Task(
            description="""
            Analyze the extracted information and identify key KPIs.
            
            For each KPI:
            - Assign a confidence score (0-1)
            - Flag if value is unexpected/concerning
            - Compare to industry benchmarks if applicable
            
            Return as JSON:
            {
                "kpis": [
                    {
                        "name": "Budget Utilization",
                        "value": "float",
                        "unit": "string",
                        "confidence": 0.95,
                        "status": "normal|warning|critical"
                    }
                ]
            }
            """,
            expected_output="KPI analysis with confidence scores and status flags",
            agent=self.agents["analyzer"],
            context=[extract_task],  # Depends on extraction
            output_file="kpi_analysis.json"
        )
        
        # Task 3: Risk assessment
        risk_task = Task(
            description="""
            Review extracted information and identify risks.
            
            Assess:
            - Timeline compression
            - Budget constraints
            - Resource gaps
            - Technical risks
            - Dependency issues
            
            Return as JSON:
            {
                "risks": [
                    {
                        "title": "string",
                        "severity": "low|medium|high|critical",
                        "description": "string",
                        "mitigation": "string"
                    }
                ]
            }
            """,
            expected_output="Risk assessment with severity and mitigation steps",
            agent=self.agents["risk_officer"],
            context=[extract_task, analyze_task]
        )
        
        # Crew orchestration
        crew = Crew(
            agents=[
                self.agents["extractor"],
                self.agents["analyzer"],
                self.agents["risk_officer"]
            ],
            tasks=[extract_task, analyze_task, risk_task],
            process=Process.sequential,  # Task 1 → Task 2 → Task 3
            verbose=True
        )
        
        return crew
    
    def run(self, doc_path: str, context: dict = None) -> Dict[str, Any]:
        """
        Execute the crew workflow.
        
        Args:
            doc_path: S3 path (e.g., s3://bucket/document.pdf)
            context: Additional context {account_id, project_id, etc.}
        
        Returns:
            {
                "status": "success|failure",
                "extracted": {...},
                "kpis": [...],
                "risks": [...],
                "confidence": float,
                "error": "string if failed"
            }
        """
        try:
            logger.info(f"Starting {DocType} crew", extra={"doc_path": doc_path})
            
            # Execute crew with input variables
            result = self.crew.kickoff(
                inputs={"doc_path": doc_path, "context": context}
            )
            
            logger.info(f"Crew completed successfully", extra={"doc_path": doc_path})
            
            # Parse and validate output
            output = json.loads(result.raw)
            
            return {
                "status": "success",
                "data": output,
                "confidence": self._calculate_confidence(output)
            }
        
        except Exception as e:
            logger.error(f"Crew execution failed", extra={
                "doc_path": doc_path,
                "error": str(e)
            })
            
            return {
                "status": "failure",
                "error": str(e),
                "data": None,
                "confidence": 0.0
            }
    
    def _calculate_confidence(self, output: dict) -> float:
        """Calculate overall confidence from task outputs."""
        if "kpis" in output:
            confidences = [kpi.get("confidence", 0) for kpi in output["kpis"]]
            return sum(confidences) / len(confidences) if confidences else 0.5
        return 0.5
```

---

## 🔧 ERROR HANDLING STRATEGY

```python
class CrewExecutionException(Exception):
    """Base exception for crew failures."""
    pass

try:
    crew = {DocType}DocumentCrew()
    result = crew.run(doc_path="s3://bucket/doc.pdf")
    
    if result["status"] == "failure":
        # Retry logic
        if "timeout" in result["error"]:
            # Exponential backoff
            time.sleep(2 ** attempt)
            result = crew.run(doc_path)
        elif "parsing" in result["error"]:
            # Fall back to simpler extraction
            result = fallback_extraction(doc_path)
        else:
            raise CrewExecutionException(result["error"])

except CrewExecutionException as e:
    logger.critical(f"Crew failed permanently", exc_info=e)
    # Store partial result + error for manual review
    db.store_extraction_failure(doc_path, str(e))
```

---

## 🧪 TESTING REQUIREMENTS

```python
def test_crew_extraction_happy_path():
    """Test crew with valid SOW document."""
    crew = SOWDocumentCrew()
    result = crew.run(doc_path="s3://test-bucket/valid_sow.pdf")
    
    assert result["status"] == "success"
    assert "extracted" in result["data"]
    assert result["confidence"] > 0.8

def test_crew_handles_missing_document():
    """Test crew gracefully fails for missing document."""
    crew = SOWDocumentCrew()
    result = crew.run(doc_path="s3://test-bucket/nonexistent.pdf")
    
    assert result["status"] == "failure"
    assert "error" in result

def test_crew_output_schema():
    """Test crew output matches expected schema."""
    crew = SOWDocumentCrew()
    result = crew.run(doc_path="s3://test-bucket/valid_sow.pdf")
    
    if result["status"] == "success":
        assert "kpis" in result["data"]
        assert "risks" in result["data"]
        # Validate against JSON schema
        jsonschema.validate(result["data"], SOW_OUTPUT_SCHEMA)
```

---

## ✅ ACCEPTANCE CRITERIA

- [ ] Crew has 2-4 agents with distinct roles
- [ ] Each task has clear expected_output and dependencies
- [ ] Error handling includes retry logic and fallbacks
- [ ] Output format is JSON with validation
- [ ] Crew tested with real documents + edge cases
- [ ] Token budget estimated and logged
- [ ] All tool definitions include docstrings
- [ ] Confidence scores calculated from agent outputs
- [ ] Verbose logging enabled for debugging
- [ ] Async/await pattern used for long-running crews

---

**Last Updated:** 2026-05-07
