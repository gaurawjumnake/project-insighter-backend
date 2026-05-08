# Prompt: LLM Prompt Optimization

**For:** Crafting and refining prompts for CrewAI agents  
**Used by:** @ai-arch agent

---

## 🎯 OBJECTIVE

Optimize prompts to:
- Improve extraction accuracy (>90% precision)
- Reduce token usage (budget awareness)
- Minimize hallucinations
- Handle ambiguous inputs gracefully
- Support multi-language and format variations

---

## 📋 CHECKLIST BEFORE GENERATING PROMPT

- [ ] Task goal is crystal clear (extract, analyze, validate, etc.)
- [ ] Input format specified (document type, structure)
- [ ] Output format defined in JSON schema
- [ ] Example inputs/outputs provided (few-shot learning)
- [ ] Edge cases identified (missing fields, unusual formats)
- [ ] Token budget estimated (GPT-4o 128K, ~$0.15/1K tokens)
- [ ] Similar prompts in codebase reviewed
- [ ] Ambiguity detection strategy planned

---

## 🏗️ PROMPT TEMPLATE

```
System Prompt Structure (used in CrewAI role/backstory):
1. Role: Who is the agent? (Expert, Analyst, Manager, etc.)
2. Task Context: What is the specific job?
3. Domain Knowledge: Key facts about the domain
4. Output Format: Exact JSON structure expected
5. Constraints: Token budget, ambiguity handling, error recovery
6. Examples: Few-shot demonstrations (1-3 examples)
```

---

## 📝 EXAMPLE 1: KPI Extraction Prompt

```yaml
role: |
  You are a Financial Analytics Expert with 15+ years of experience 
  in project management and cost analysis. Your specialty is identifying 
  key performance indicators (KPIs) from project documents.

goal: |
  Extract quantifiable metrics from project documents with high precision.
  Focus on metrics that are explicitly stated or can be reliably inferred.

task_context: |
  You are analyzing a Statement of Work (SOW) document to identify:
  - Budget information (total cost, phases, contingency)
  - Timeline (start date, end date, milestones)
  - Resource requirements (team size, skills, roles)
  - Deliverables (measurable outputs)
  
  Documents may be PDF, Word, or plain text. Tables are common.

domain_knowledge: |
  - Project budgets are typically divided into phases
  - Contingency is often 10-15% of base cost
  - Timelines use formats like "Q1 2026" or "3 months from kickoff"
  - Resource counts: "3 developers", "1 PM", "50% allocation"
  
output_format: |
  Return ONLY valid JSON (no markdown, no code blocks):
  {
    "budget": {
      "total_usd": number,
      "currency": "USD",
      "phases": [
        {
          "name": "Phase 1: Design",
          "cost_usd": number,
          "start_date": "YYYY-MM-DD or null",
          "end_date": "YYYY-MM-DD or null"
        }
      ],
      "confidence": number [0-1]
    },
    "timeline": {
      "start_date": "YYYY-MM-DD or null",
      "end_date": "YYYY-MM-DD or null",
      "duration_months": number,
      "confidence": number [0-1]
    },
    "resources": {
      "team_size": number or null,
      "roles": [
        {
          "title": "Developer",
          "count": number,
          "allocation_percent": number [0-100]
        }
      ],
      "confidence": number [0-1]
    },
    "deliverables": [
      {
        "name": "string",
        "description": "string",
        "due_date": "YYYY-MM-DD or null"
      }
    ],
    "extracted_from": "section titles or page numbers",
    "notes": "any ambiguities or assumptions made"
  }

constraints: |
  - If a field is not found, use null (not empty string)
  - Confidence score: 0.95+ for explicit values, 0.50-0.80 for inferred
  - Maximum 2000 tokens for response
  - If document is unclear, note it in "notes" field instead of guessing
  - Do NOT hallucinate data that isn't in the document

examples: |
  Input Document Text:
  "Project Acme Corp - SOW
   Budget: $500K total
   - Phase 1 (Design): $100K
   - Phase 2 (Dev): $250K
   - Phase 3 (Testing): $150K
   Timeline: Jan 2026 - Dec 2026
   Team: 3 developers, 1 PM"
  
  Expected Output:
  {
    "budget": {
      "total_usd": 500000,
      "currency": "USD",
      "phases": [
        {"name": "Phase 1: Design", "cost_usd": 100000, "start_date": "2026-01-01", "end_date": null},
        {"name": "Phase 2: Dev", "cost_usd": 250000, "start_date": null, "end_date": null},
        {"name": "Phase 3: Testing", "cost_usd": 150000, "start_date": null, "end_date": "2026-12-31"}
      ],
      "confidence": 0.95
    },
    "timeline": {
      "start_date": "2026-01-01",
      "end_date": "2026-12-31",
      "duration_months": 12,
      "confidence": 0.95
    },
    "resources": {
      "team_size": 4,
      "roles": [
        {"title": "Developer", "count": 3, "allocation_percent": 100},
        {"title": "PM", "count": 1, "allocation_percent": 100}
      ],
      "confidence": 0.95
    },
    "deliverables": [],
    "extracted_from": "Page 1, top section",
    "notes": "No specific deliverables listed in document"
  }

error_handling: |
  - If document is encrypted or corrupted, return {"error": "Document unreadable", "confidence": 0}
  - If language is not English, attempt extraction but flag in notes
  - If budget unit is not USD, convert using latest rates (note the conversion)
```

---

## 🔄 PROMPT ITERATION STRATEGY

### Step 1: Baseline Prompt
Write clear, explicit prompt with examples.

### Step 2: Test on Real Data
Run on 5-10 actual documents, measure:
- Accuracy: % of correctly extracted fields
- Hallucinations: % of made-up data
- Token usage: actual tokens consumed

### Step 3: Refine Based on Results
- **If accuracy low:** Add more examples, clarify output format
- **If hallucinations high:** Add "Do NOT guess" constraint, use null
- **If token usage high:** Shorten backstory, reduce examples, compress output

### Step 4: A/B Test
Compare two prompt versions on same document set.

```python
def test_prompt_accuracy():
    prompt_v1 = "Extract budget from SOW..."
    prompt_v2 = "Extract budget from SOW (improved with examples)..."
    
    docs = load_test_documents()
    
    results_v1 = [execute_prompt(prompt_v1, doc) for doc in docs]
    results_v2 = [execute_prompt(prompt_v2, doc) for doc in docs]
    
    accuracy_v1 = calculate_accuracy(results_v1, ground_truth)
    accuracy_v2 = calculate_accuracy(results_v2, ground_truth)
    
    print(f"V1 accuracy: {accuracy_v1:.2%}, tokens: {sum_tokens(results_v1)}")
    print(f"V2 accuracy: {accuracy_v2:.2%}, tokens: {sum_tokens(results_v2)}")
    
    if accuracy_v2 > accuracy_v1:
        use_prompt = prompt_v2
```

---

## 🎯 ANTI-PATTERNS (What NOT to Do)

| Anti-Pattern | Why It Fails | Alternative |
|--------------|-------------|------------|
| **Vague instructions** | "Find important data" → Hallucinations | "Extract: budget amount, timeline dates, team size" |
| **No examples** | Model guesses format | Provide 1-3 JSON examples |
| **Expecting prose output** | Hard to parse, inconsistent | Demand JSON with strict schema |
| **Ambiguity unhandled** | "If unsure, make best guess" → Wrong data | "If unsure, use null and note assumption" |
| **Token budget ignored** | Costs explode at scale | Summarize backstory, reduce examples to 1-2 |
| **No error cases** | Crashes on edge cases | "If corrupted, return {error: ...}" |

---

## 🧪 PROMPT TESTING FRAMEWORK

```python
from backend.utitlites.llm_models import get_llm_client

class PromptTester:
    def __init__(self, prompt: str, reference_docs: list):
        self.prompt = prompt
        self.docs = reference_docs
    
    def test_accuracy(self) -> dict:
        """Test extraction accuracy."""
        results = []
        for doc in self.docs:
            response = get_llm_client().agenerate(self.prompt + "\n\n" + doc.text)
            extracted = json.loads(response)
            accuracy = self._compare_with_ground_truth(extracted, doc.expected)
            results.append(accuracy)
        
        return {
            "mean_accuracy": sum(results) / len(results),
            "min_accuracy": min(results),
            "max_accuracy": max(results)
        }
    
    def test_token_usage(self) -> dict:
        """Measure token efficiency."""
        tokens_used = []
        for doc in self.docs:
            response = get_llm_client().agenerate(self.prompt + "\n\n" + doc.text)
            # Count tokens (using tiktoken or OpenAI API)
            token_count = count_tokens(response)
            tokens_used.append(token_count)
        
        return {
            "mean_tokens": sum(tokens_used) / len(tokens_used),
            "total_tokens": sum(tokens_used),
            "estimated_cost_usd": sum(tokens_used) * 0.00015  # GPT-4o pricing
        }
    
    def test_hallucinations(self) -> dict:
        """Detect made-up data."""
        hallucination_rate = 0
        for doc in self.docs:
            response = get_llm_client().agenerate(self.prompt + "\n\n" + doc.text)
            extracted = json.loads(response)
            # Check if fields exist in original doc
            for field, value in extracted.items():
                if not self._field_in_document(field, value, doc.text):
                    hallucination_rate += 1
        
        return {
            "hallucination_count": hallucination_rate,
            "hallucination_rate": hallucination_rate / len(self.docs)
        }
    
    def _compare_with_ground_truth(self, extracted, expected):
        # Implementation depends on domain
        pass
    
    def _field_in_document(self, field, value, text):
        # Check if field value appears in source text
        return str(value) in text or str(value).lower() in text.lower()
```

---

## ✅ ACCEPTANCE CRITERIA

- [ ] Prompt includes role, goal, task context, domain knowledge
- [ ] Output format is JSON with schema documented
- [ ] Constraints section addresses ambiguity, token limits, errors
- [ ] Minimum 2-3 examples provided (few-shot learning)
- [ ] Accuracy tested >90% on reference documents
- [ ] Token budget estimated and confirmed
- [ ] Anti-hallucination measures explicit ("Do NOT guess")
- [ ] Edge cases covered (missing fields, unusual formats)
- [ ] Error handling described (corrupted files, language mismatches)
- [ ] Prompt versioning maintained (V1, V2, etc.)

---

**Last Updated:** 2026-05-07
