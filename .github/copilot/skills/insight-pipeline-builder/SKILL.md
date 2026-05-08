# Skill: Insight Pipeline Builder

**Purpose:** Generate end-to-end insight generation pipeline (extract → analyze → format → store)  
**Agent:** @ai-arch (with @data-analyst & @api-dev coordination)  
**Duration:** 10-15 minutes

---

## QUERY PATTERN

```
@ai-arch Build insight pipeline for {analysis_type}
where analysis_type = [financial-analysis, risk-assessment, quality-metrics, ...]

Examples:
- Build financial insights pipeline for project profitability analysis
- Build risk assessment pipeline for document-based threat analysis
- Build quality metrics pipeline for code review aggregation
```

---

## IMPLEMENTATION

### Step 1: Define Insight Flow
Map data pipeline stages:
1. **Extract:** Fetch data from PostgreSQL (project, documents, historical)
2. **Stage:** Write raw data to S3 for reproducibility
3. **Analyze:** Run multi-agent crews on staged data
4. **Aggregate:** Combine crew results into unified insights
5. **Format:** Convert to JSON/Markdown for API response
6. **Store:** Persist insights and metadata to PostgreSQL

**Flow Diagram:**
```
PostgreSQL (Project)
     ↓
S3 Staging (s3://project-insighter/staging/{job_id}/)
     ↓
Crew 1 (Finance Analysis Crew)    Crew 2 (Risk Crew)    Crew 3 (Allocation Crew)
     ↓                                  ↓                      ↓
     ├──────────────────────────────────┼──────────────────────┤
                                        ↓
                          Aggregation Service
                                        ↓
                           Format (JSON + Markdown)
                                        ↓
                    Store in PostgreSQL + Return 202
```

### Step 2: Create Service Layer
```python
class InsightGenerationService:
    def generate_insights(
        self,
        account_id: int,
        analysis_types: list[str]
    ) -> InsightGenerationResult:
        """
        Generate aggregated insights for account.
        
        Process:
        1. Load context from DB
        2. Stage raw data to S3
        3. Run parallel analysis crews
        4. Aggregate results
        5. Format + store
        """
        
        # Step 1: Load context
        account = self.db.query(Account).get(account_id)
        projects = account.projects
        documents = self._fetch_related_documents(account_id)
        
        # Step 2: Stage to S3
        job_id = str(uuid.uuid4())
        staged_data = {
            "account": account.dict(),
            "projects": [p.dict() for p in projects],
            "documents": [d.dict() for d in documents]
        }
        self.s3.upload_json(
            f"s3://project-insighter/staging/{job_id}/input.json",
            staged_data
        )
        
        # Step 3: Run crews
        crews = {
            "finance": FinanceAnalyzerCrew(),
            "risk": RiskAnalyzerCrew(),
            "allocation": AllocationAnalyzerCrew()
        }
        
        results = {}
        for crew_name, crew in crews.items():
            result = crew.run(s3_path=f"s3://project-insighter/staging/{job_id}/")
            results[crew_name] = result
        
        # Step 4: Aggregate
        aggregated = self._aggregate_results(results)
        
        # Step 5: Format
        formatted = self._format_for_api(aggregated)
        
        # Step 6: Store
        insight = InsightRecord(
            account_id=account_id,
            job_id=job_id,
            data=json.dumps(aggregated),
            formatted=formatted,
            created_at=datetime.utcnow()
        )
        self.db.add(insight)
        self.db.commit()
        
        return InsightGenerationResult(
            job_id=job_id,
            status="completed",
            data=formatted
        )
```

### Step 3: Create API Endpoint (with @api-dev)
```python
@router.post("/api/v1/insights/generate")
async def generate_insights(
    req: InsightGenerationRequest,
    db: Session = Depends(get_db)
):
    """Trigger insight generation (async)."""
    
    service = InsightGenerationService(db)
    job_id = str(uuid.uuid4())
    
    # Start async task
    asyncio.create_task(
        service.generate_insights_async(
            account_id=req.account_id,
            job_id=job_id
        )
    )
    
    # Return immediately with job_id
    return {
        "job_id": job_id,
        "status": "processing",
        "estimated_completion": "5 minutes"
    }

# Poll for results
@router.get("/api/v1/insights/{job_id}")
async def get_insights(job_id: str, db: Session = Depends(get_db)):
    """Get completed insights."""
    
    insight = db.query(InsightRecord).filter(
        InsightRecord.job_id == job_id
    ).first()
    
    if not insight:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        "status": "completed" if insight.completed_at else "processing",
        "data": json.loads(insight.data) if insight.completed_at else None
    }
```

### Step 4: Error Handling & Resilience
```python
class InsightPipelineException(Exception):
    pass

async def generate_insights_async(
    self,
    account_id: int,
    job_id: str
):
    """Async insight generation with error recovery."""
    
    try:
        # Step 1-6 as above...
        result = self.generate_insights(account_id)
        
        # Mark as completed
        insight = self.db.query(InsightRecord).get(job_id)
        insight.completed_at = datetime.utcnow()
        insight.status = "completed"
        self.db.commit()
    
    except CrewExecutionError as e:
        # Crew failed - store partial results
        logger.error(f"Crew failed for job {job_id}", exc_info=e)
        insight = self.db.query(InsightRecord).get(job_id)
        insight.status = "partial"
        insight.error = str(e)
        self.db.commit()
    
    except Exception as e:
        # Unexpected error - notify admin
        logger.critical(f"Pipeline failed for job {job_id}", exc_info=e)
        insight = self.db.query(InsightRecord).get(job_id)
        insight.status = "failed"
        insight.error = str(e)
        self.db.commit()
        # Could send alert email, PagerDuty, etc.
```

### Step 5: Add Monitoring
```python
class InsightPipelineMonitor:
    def track_pipeline_execution(self, job_id: str):
        """Log pipeline metrics for monitoring."""
        
        metrics = {
            "job_id": job_id,
            "start_time": datetime.utcnow(),
            "crew_execution_times": {},
            "total_tokens_used": 0,
            "status": "pending"
        }
        
        # Store in CloudWatch / monitoring system
        logger.info("Pipeline started", extra=metrics)
        
        return metrics
```

### Step 6: Testing
```python
def test_insight_pipeline_happy_path():
    """Test full pipeline with valid account."""
    service = InsightGenerationService(db)
    
    account = create_test_account()
    result = service.generate_insights(account.id)
    
    assert result.status == "completed"
    assert "finance" in result.data
    assert "risk" in result.data

def test_insight_pipeline_handles_missing_data():
    """Test graceful degradation with missing documents."""
    service = InsightGenerationService(db)
    
    account = create_test_account()
    # No documents attached
    
    result = service.generate_insights(account.id)
    
    assert result.status == "partial"
    assert "finance" in result.data
    assert result.data["warnings"] > 0
```

---

## SUCCESS METRICS

- ✅ Full pipeline E2E tested
- ✅ Async execution (202 Accepted)
- ✅ Error recovery (partial results, fallbacks)
- ✅ Data persisted (PostgreSQL + S3)
- ✅ Monitoring enabled (metrics logged)
- ✅ Performance <5 min for avg account
- ✅ Cross-module coordination validated
- ✅ Documentation complete

---

## HANDOFFS

- **From @api-dev:** API endpoint defined
- **From @ai-arch:** Crews designed and working
- **From @data-analyst:** Schema for storing results
- **Coordinates:** All three agents for end-to-end feature

---

## ACCEPTANCE CHECKLIST

- [ ] Insight service orchestrates all pipeline stages
- [ ] API endpoint returns 202 Accepted (async)
- [ ] Async job execution with proper error handling
- [ ] Data staged to S3 for reproducibility
- [ ] Multiple crews run in parallel (if independent)
- [ ] Results aggregated and formatted
- [ ] Stored in PostgreSQL + S3
- [ ] Monitoring/logging enabled
- [ ] Tested with valid + edge case inputs
- [ ] Documentation includes flow diagram

**Version:** 1.0 | Last Updated: 2026-05-07
