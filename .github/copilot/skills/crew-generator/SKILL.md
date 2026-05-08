# Skill: CrewAI Crew Generator

**Purpose:** Generate complete multi-agent CrewAI crew with agents, tasks, tools, and prompts  
**Agent:** @ai-arch  
**Duration:** 5-10 minutes

---

## QUERY PATTERN

```
@ai-arch Design {operation} crew for {document_type}
where operation = [extract, analyze, validate, summarize, generate-insights]
and document_type = [SOW, WSR, CodeReview, BestPractices, ...]

Examples:
- Design extraction crew for SOW documents
- Design risk analysis crew for WSR documents
- Design quality assessment crew for Code Review documents
```

---

## IMPLEMENTATION

### Step 1: Define Agents
Create 2-4 agents with:
- Distinct roles (Extractor, Analyzer, Validator)
- Specialized backstories (domain expertise)
- Tool assignments (S3 reader, JSON validator, etc.)
- Temperature settings (low=0.2 for factual, high=0.7 for creative)

**Generated Code Template:**
```python
extractor = Agent(
    role="Document Extractor",
    goal="Extract {specific metrics} with high precision",
    backstory="Expert in {domain} analysis with 15+ years experience",
    tools=[s3_reader_tool],
    temperature=0.2,  # Low for factual extraction
    verbose=True
)
```

### Step 2: Define Tasks
Create dependent tasks:
- Task 1: Extract information (primary task)
- Task 2: Analyze/validate (depends on Task 1)
- Task 3: Summarize/flag issues (depends on Tasks 1-2)

Each task includes:
- Clear description with context
- Expected output format (JSON schema)
- Agent assignment
- Dependencies (context=[previous_task])

### Step 3: Define Tools
Create reusable tools:
- S3 reader: Fetch documents from cloud storage
- JSON validator: Validate output schema
- LLM caller: Make additional LLM queries if needed

### Step 4: Implement Crew Orchestration
```python
crew = Crew(
    agents=[extractor, analyzer, validator],
    tasks=[extract_task, analyze_task, validate_task],
    process=Process.sequential,  # Or Process.hierarchical
    verbose=True
)

result = crew.kickoff(inputs={"doc_path": "s3://bucket/file.pdf"})
```

### Step 5: Add Error Handling
Implement retry logic:
```python
try:
    result = crew.run()
except CrewError as e:
    if "timeout" in str(e):
        # Retry with longer timeout
        result = crew.run(timeout=300)
    elif "parsing" in str(e):
        # Fall back to simpler extraction
        result = fallback_extraction()
```

### Step 6: Test Accuracy
Test on reference documents:
- Measure extraction accuracy ≥90%
- Verify JSON schema compliance
- Check hallucination rate <5%
- Estimate token usage

---

## SUCCESS METRICS

- ✅ Crew has 2-4 agents with clear roles
- ✅ Tasks have explicit expected outputs
- ✅ Accuracy ≥90% on reference documents
- ✅ Hallucination rate <5%
- ✅ Token budget within GPT-4o limits
- ✅ Error handling covers ≥4 scenarios
- ✅ Async/callback pattern for long runs
- ✅ Confidence scores in outputs

---

## HANDOFFS

- **To @api-dev:** If crew needs to be exposed as endpoint ("Create async API for this crew")
- **To @data-analyst:** If crew outputs need to be stored/queried

---

## ACCEPTANCE CHECKLIST

- [ ] Crew defined with minimum 2 agents
- [ ] Each agent has role, goal, backstory, tools
- [ ] Tasks have clear description and expected_output
- [ ] JSON schema defined and validated
- [ ] Prompts include 1-3 examples (few-shot)
- [ ] Error handling with retry logic
- [ ] Token budget estimated (<100K for GPT-4o)
- [ ] Confidence scores in output
- [ ] Tested on 3+ reference documents
- [ ] Async execution pattern for long tasks

**Version:** 1.0 | Last Updated: 2026-05-07
