"""
Generalized Crew Workflow for Multi-Domain Analysis

This module provides two crew implementations:

1. GeneralizedAnalysisCrew (DEPRECATED - kept for backward compatibility)
   - Legacy version for sales/finance with DB fetching in research phase
   - Context-specific output formatting

2. DomainNeutralAnalysisCrew (NEW - recommended)
   - Domain-neutral crew for any entity type
   - Accepts pre-prepared JSON from S3
   - Supports custom analysis goals and output schemas
   - Returns JSON-compatible results for DB persistence

The domain-neutral approach:
- Decouples data fetching from analysis
- Enables reuse for project, account, PE, or future entity types
- Supports flexible analysis goals and output schemas
- Produces JSON output for reliable DB storage

Example Usage (Domain-Neutral):
    crew = DomainNeutralAnalysisCrew(
        entity_type='account',
        s3_key='temp/account_<id>_<date>.json',
        analysis_goal='Comprehensive financial and operational insights',
        output_schema_hint='JSON with level, executive_summary, kpis, risks, opportunities, recommendations'
    )
    result = crew.analyze()
"""

from crewai import Crew, Task
from uuid import UUID
from typing import Optional, Dict, Any
from backend.insights_workflow.core.context_aware_agents import GeneralizedAgents
from backend.doc_insighter.tools.app_logger import Logger
import json

log = Logger()


class GeneralizedAnalysisCrew:
    """
    A flexible crew workflow for Sales and Finance analysis.
    
    This crew orchestrates three agents in a sequential workflow:
    1. Researcher: Fetches data from the database
    2. Analyzer: Analyzes the data and identifies insights
    3. Summarizer: Creates context-specific final insights
    
    The same workflow can be applied to different analyses by varying:
    - context_type: 'sales' or 'finance'
    - entity_id: UUID of the entity to analyze
    - entity_type: Type of entity to analyze
    """
    
    def __init__(self, context_type: str = 'sales', entity_id: str = '', entity_type: str = ''):
        """
        Initialize the crew with context and entity information.
        
        Args:
            context_type: 'sales' or 'finance' - determines output format and analysis focus
            entity_id: UUID of the Account or Project to analyze
            entity_type: Type of entity ('sales'/'account' or 'finance'/'project')
        """
        self.context_type = context_type.lower()
        self.entity_id = entity_id
        self.entity_type = entity_type.lower()
        
        # Initialize agents factory
        self.agents_factory = GeneralizedAgents()
        
        # Validate context type
        if self.context_type not in ['sales', 'finance']:
            raise ValueError(f"Invalid context_type: {context_type}. Must be 'sales' or 'finance'")
        
        log.log_info(f"Initialized GeneralizedAnalysisCrew for {context_type} analysis")
    
    def create_research_task(self) -> Task:
        """Create the research task for data fetching and S3 upload.
        
        This task orchestrates the data extraction and S3 upload process:
        1. Fetch data from database (metrics and insights)
        2. Upload combined data to S3
        3. Return S3 key for downstream processing
        """
        return Task(
            description=f"""
            Fetch comprehensive data for the {self.context_type} entity (ID: {self.entity_id}) and upload to S3.
            
            Critical Task - Data Pipeline Stage:
            1. Use the fetch_and_upload_to_s3 tool to extract data from database
            2. The tool will automatically combine metrics and document insights
            3. Upload the complete dataset to S3 for scalable processing
            4. Extract and provide the S3 key from the response
            
            This is a critical step that:
            - Releases database connections immediately (prevents connection pool exhaustion)
            - Enables concurrent analysis from S3 without database contention
            - Allows multiple teams to analyze data simultaneously
            
            Return the S3 key and entity information. The analyzer will use this key
            to download and perform deep analysis without database overhead.
            """,
            agent=self.agents_factory.researcher_agent(),
            expected_output="""
            S3 Data Location including:
            - S3 key (e.g., 'temp/account_<id>_<date>.json')
            - Entity ID
            - Entity type
            - Confirmation of successful upload to S3
            - Any data quality notes or warnings
            """
        )
    
    def create_analysis_task(self, research_output: str) -> Task:
        """Create the analysis task for deep insights.
        
        This task uses the S3 key from the research phase to download data
        and perform comprehensive analysis.
        """
        return Task(
            description=f"""
            Perform comprehensive analysis on the data uploaded to S3 by the researcher.
            
            Research Output from Previous Stage (contains S3 key):
            {research_output}
            
            Your Analysis Task:
            1. Extract the S3 key from the research output above
            2. Use the S3 Data Reader tool to download the complete dataset
            3. Perform thorough {self.context_type} analysis:
            
            For Sales Analysis:
            - Account health assessment (engagement, growth potential)
            - Growth and expansion opportunities (cross-sell, upsell, new services)
            - Risk assessment and relationship factors
            - Account positioning and competitive strength
            
            For Finance Analysis:
            - Profitability analysis (margins, efficiency, drivers)
            - Revenue variance analysis (actual vs expected)
            - Cost efficiency and optimization opportunities
            - Financial risks and variance explanations
            
            Analysis Steps:
            1. Identify key patterns, trends, and anomalies in the data
            2. Calculate critical performance metrics and KPIs
            3. Assess overall health, risks, and opportunities
            4. Compare against relevant benchmarks where applicable
            5. Generate detailed, data-backed insights
            6. Flag critical issues requiring immediate attention
            
            Your analysis should be thorough, data-driven, and actionable.
            Focus on insights that inform strategic decision-making.
            """,
            agent=self.agents_factory.analyzer_agent(),
            expected_output="""
            Detailed analytical insights including:
            - Entity overview from the retrieved data
            - Key findings and patterns identified
            - Performance metrics and assessments
            - Health/strength evaluation
            - Risk and opportunity identification
            - Benchmark comparisons (where relevant)
            - Critical issues and their priorities
            - Data-backed strategic recommendations
            """
        )
    
    def create_summarization_task(self) -> Task:
        """Create the summarization task for final insights."""
        context_specific_format = self._get_output_format_instructions()
        
        return Task(
            description=f"""
            Synthesize the analytical findings into compelling, actionable insights.
            
            Context Requirements:
            - Analysis Type: {self.context_type.upper()}
            - Output Format: {context_specific_format}
            
            Your task:
            1. Distill key findings into executive-ready insights
            2. Identify the 3-5 most critical insights
            3. Develop actionable recommendations
            4. Frame insights in {self.context_type} business terms
            5. Quantify impact where possible
            """,
            agent=self.agents_factory.summarizer_agent(context_type=self.context_type),
            expected_output=context_specific_format
        )
    
    def _get_output_format_instructions(self) -> str:
        """Get output format instructions based on context type."""
        if self.context_type == 'finance':
            return """
            FINANCIAL INSIGHTS FORMAT:
            
            1. EXECUTIVE SUMMARY
               - Overall financial health score
               - Key financial performance indicators
               - Top opportunities and risks
            
            2. KEY FINANCIAL FINDINGS
               - Profitability status and trends
               - Revenue realization performance
               - Cost and margin analysis
            
            3. PROFITABILITY ANALYSIS
               - Gross margin assessment
               - Cost efficiency evaluation
               - Profitability drivers and detractors
            
            4. REVENUE OPTIMIZATION OPPORTUNITIES
               - Specific optimization initiatives
               - Estimated financial impact
               - Implementation complexity and timeline
            
            5. FINANCIAL RISK ASSESSMENT
               - Top financial risks (ranked by impact)
               - Probability and mitigation strategies
               - Contingency recommendations
            
            6. RECOMMENDATIONS WITH FINANCIAL IMPACT
               - Prioritized action items
               - Expected financial outcomes
               - Success metrics and KPIs
            
            7. PERFORMANCE TIMELINE AND KPIS
               - Key performance indicators to monitor
               - Expected timeline for improvements
               - Review and monitoring cadence
            """
        else:  # sales context
            return """
            SALES INSIGHTS FORMAT:
            
            1. EXECUTIVE SUMMARY
               - Overall account health score
               - Key account metrics
               - Top opportunities and risks
            
            2. KEY ACCOUNT FINDINGS
               - Current account position and strength
               - Engagement and relationship status
               - Historical performance trends
            
            3. ACCOUNT HEALTH ASSESSMENT
               - Health score (0-100)
               - Key strengths and weaknesses
               - Engagement level assessment
               - Stakeholder relationship quality
            
            4. GROWTH AND EXPANSION OPPORTUNITIES
               - Specific growth vectors (cross-sell, upsell, new services)
               - Market expansion potential
               - Estimated revenue uplift per opportunity
               - Success probability and timeline
            
            5. RISK AND RELATIONSHIP ASSESSMENT
               - Top account risks (ranked by probability/impact)
               - Churn probability and early warning signs
               - Relationship vulnerabilities
               - Mitigation strategies
            
            6. RECOMMENDED ACTIONS FOR ACCOUNT GROWTH
               - Prioritized action items
               - Resource requirements
               - Expected outcomes and timeline
               - Success metrics
            
            7. SUCCESS METRICS AND TIMELINE
               - Key success indicators to monitor
               - 90-day, 180-day, 12-month milestones
               - Review and engagement cadence
            """
    
    def analyze(self) -> str:
        """
        Execute the complete S3-based analysis workflow.
        
        Workflow:
        1. Researcher: Extract data from database and upload to S3
        2. Analyzer: Download from S3 and perform deep analysis
        3. Summarizer: Create actionable insights from analysis
        
        This S3-based approach:
        - Releases database connections immediately after extraction
        - Enables concurrent analysis without database connection limits
        - Supports scalable processing for multiple teams simultaneously
        
        Returns:
            The final synthesized insights from the summarizer agent
        """
        try:
            log.log_info(f"Starting S3-based analysis for {self.context_type} entity: {self.entity_id}")
            log.log_info(f"Entity Type: {self.entity_type}")
            
            # Create research task (uploads data to S3)
            research_task = self.create_research_task()
            
            # Create analysis task (downloads from S3 and analyzes)
            analysis_task = self.create_analysis_task(
                "Will receive S3 key from research task - contains metrics and insights data"
            )
            
            # Create summarization task (final insights)
            summarization_task = self.create_summarization_task()
            
            # Create the crew with all tasks in dependency order
            crew = Crew(
                agents=[
                    self.agents_factory.researcher_agent(),
                    self.agents_factory.analyzer_agent(),
                    self.agents_factory.summarizer_agent(context_type=self.context_type)
                ],
                tasks=[
                    research_task,
                    analysis_task,
                    summarization_task
                ],
                verbose=True
            )
            
            log.log_info("=" * 80)
            log.log_info("INITIATING S3-BASED ANALYSIS WORKFLOW")
            log.log_info("=" * 80)
            log.log_info("Step 1: Researcher - Extract data from DB and upload to S3...")
            log.log_info("Step 2: Analyzer - Download from S3 and perform analysis...")
            log.log_info("Step 3: Summarizer - Synthesize insights based on analysis...")
            log.log_info("=" * 80)
            
            # Execute the crew with inputs
            result = crew.kickoff(inputs={
                'entity_id': self.entity_id,
                'entity_type': self.entity_type,
                'context_type': self.context_type
            })
            
            log.log_info("=" * 80)
            log.log_info(f"Analysis completed successfully for {self.context_type} entity")
            log.log_info("=" * 80)
            return result
            
        except Exception as e:
            log.log_error(f"Error during analysis: {str(e)}")
            raise


# ============================================================================
# DOMAIN-NEUTRAL ANALYSIS CREW (NEW)
# ============================================================================

class DomainNeutralAnalysisCrew:
    """
    Domain-neutral crew for analyzing any entity type from S3 data.
    
    This crew is designed to work with pre-prepared JSON data from S3,
    making it reusable for projects, accounts, PE entities, or any future
    entity types without code changes.
    
    Key design principles:
    1. Researcher: Parses S3 JSON and prepares clean context for analysis
    2. Analyzer: Performs domain-neutral analysis based on instructions
    3. Summarizer: Produces JSON-compatible output for DB persistence
    
    Decouples data fetching from analysis, enabling scalable processing.
    """
    
    def __init__(
        self,
        entity_type: str,
        s3_key: str,
        analysis_goal: str,
        output_schema_hint: Optional[str] = None,
        entity_id: Optional[str] = None,
        entity_name: Optional[str] = None
    ):
        """
        Initialize domain-neutral crew.
        
        Args:
            entity_type: Type of entity ('project', 'account', 'private_equity', or any custom type)
            s3_key: S3 key where JSON data is staged (e.g., 'temp/account_<id>_<date>.json')
            analysis_goal: Desired analysis objective (e.g., "Comprehensive financial insights")
            output_schema_hint: Optional hint for output format (e.g., "JSON with kpis, risks, opportunities")
            entity_id: Optional entity UUID for reference
            entity_name: Optional entity name for reference
        """
        self.entity_type = entity_type.lower()
        self.s3_key = s3_key
        self.analysis_goal = analysis_goal
        self.output_schema_hint = output_schema_hint or self._get_default_schema_hint(entity_type)
        self.entity_id = entity_id or "unknown"
        self.entity_name = entity_name or f"{entity_type.title()} Analysis"
        
        # Initialize agents factory
        self.agents_factory = GeneralizedAgents()
        
        log.log_info(f"Initialized DomainNeutralAnalysisCrew for {entity_type}")
        log.log_info(f"Analysis Goal: {analysis_goal}")
        log.log_info(f"S3 Key: {s3_key}")
    
    def _get_default_schema_hint(self, entity_type: str) -> str:
        """Get appropriate output schema hint based on entity type."""
        entity_type_lower = entity_type.lower()
        
        if entity_type_lower == "project":
            return """
            STRICT PROJECT JSON with keys: project_name, health_score, summary,
            delivery_insights, financial_insights, ai_insights, engineering_insights,
            timeline_insights, governance_insights, risks, opportunities, recommendations.
            Return only valid JSON and do not include explanations outside JSON.
            """
        elif entity_type_lower == "account":
            return """
            JSON with keys: level, entity_id, entity_name, generated_at, executive_summary,
            kpis (dict with revenue, shortfall, portfolio metrics), risks (list),
            opportunities (list), recommended_actions (list), gaps_identified (list),
            suggestions (list), pitch (dict), confidence_score (0-1), evidence_summary
            """
        elif entity_type_lower in ["pe", "private_equity"]:
            return """
            JSON with keys: level, entity_id, entity_name, generated_at, executive_summary,
            kpis (dict with portfolio metrics), risks (list), opportunities (list),
            recommended_actions (list), gaps_identified (list), suggestions (list),
            pitch (dict), confidence_score (0-1), evidence_summary
            """
        else:
            return """
            JSON with keys: level, entity_id, entity_name, generated_at, executive_summary,
            kpis (dict), risks (list), opportunities (list), recommended_actions (list),
            gaps_identified (list), suggestions (list), pitch (dict),
            confidence_score (0-1), evidence_summary
            """
    
    def create_research_task(self) -> Task:
        """
        Create research task for parsing and contextualizing S3 data.
        
        This task:
        1. Downloads JSON from S3 using the provided s3_key
        2. Parses and cleans the data
        3. Prepares structured context for analysis
        """
        return Task(
            description=f"""
            Parse and prepare analysis context from S3 data.
            
            S3 Data Location: {self.s3_key}
            Entity Type: {self.entity_type}
            Entity ID: {self.entity_id}
            
            Task:
            1. Use the S3 Data Reader tool to download JSON from the S3 key: {self.s3_key}
            2. Parse the downloaded JSON data
            3. Extract key sections:
               - Entity metadata (entity_id, entity_name, hierarchy_level)
               - Financial/operational metrics
               - Project/account/PE data summaries
               - Data quality notes and warnings
            4. Identify available data fields and their completeness
            5. Prepare clean, structured context for deep analysis
            6. Flag any data quality issues or gaps
            7. Create a summary of what data is available for analysis
            
            Return a comprehensive context summary that includes:
            - Cleaned entity data
            - Available metrics and their quality
            - Data gaps and limitations
            - Suggestions for analysis focus areas
            - Warning about any partial or missing data
            """,
            agent=self.agents_factory.researcher_agent(),
            expected_output=f"""
            Parsed context including:
            - Entity metadata and key identifiers
            - All available data fields and their values
            - Data quality assessment
            - Completeness indicators
            - Identified gaps or limitations
            - Suggested analysis focus areas
            """
        )
    
    def create_analysis_task(self, research_output: str) -> Task:
        """
        Create analysis task for domain-neutral insights generation.
        
        This task performs entity-type-aware analysis without entity-specific code.
        """
        if self.entity_type == "project":
            return Task(
                description=f"""
                You are a Project Intelligence Analyst AI.

                Objective:
                Generate accurate, structured, and actionable decision-grade insights
                about the project across:
                - Delivery health
                - Financial/timeline risk
                - AI utilization
                - Engineering quality
                - Governance/process maturity

                Analysis Goal: {self.analysis_goal}
                Entity: {self.entity_name} (ID: {self.entity_id})
                S3 Data Source: {self.s3_key}

                Research Context from Previous Stage:
                {research_output}

                Analysis Instructions:

                Step 1: Extract Signals. Do not summarize documents. Identify:
                - delivery delays, blockers, and delivery risks
                - roadmap progress versus commitments
                - SOW versus execution mismatch
                - AI usage patterns, including direct versus assist usage
                - engineering quality issues, including coverage and practices
                - missing or weak reporting signals
                - contradictions, especially where status appears healthy but reports show issues

                Step 2: Compute Derived Indicators where data is available:
                - total_ai_hours = ai_direct_hours + ai_assist_hours
                - detect AI underuse or overuse patterns
                - compare current date, from_date, and to_date for timeline health
                - classify code_coverage_pct:
                  - < 50: high risk
                  - 50 to 70: moderate risk
                  - > 70: good

                Step 3: Generate insights using these rules:
                - Do not repeat or summarize source documents
                - Every insight must be specific, evidence-based, and decision-relevant
                - Prefer reasoning like: "X indicates Y risk because Z"
                - Detect contradictions explicitly
                - If data is missing, infer cautiously and state the limitation
                - If there is no strong signal, produce fewer insights rather than generic ones
                - Avoid vague statements such as "project is doing well" or "AI can be improved"

                Required focus areas:
                - delivery_insights
                - financial_insights
                - ai_insights
                - engineering_insights
                - timeline_insights
                - governance_insights
                - risks
                - opportunities
                - recommendations
                """,
                agent=self.agents_factory.analyzer_agent(),
                expected_output="""
                Decision-grade project analysis findings including:
                - Project health score reasoning
                - Delivery, financial, AI, engineering, timeline, and governance signals
                - Explicit contradictions or inconsistencies
                - Evidence-backed risks and opportunities
                - Actionable recommendations
                - Notes on missing data or weak evidence
                """
            )

        return Task(
            description=f"""
            Perform comprehensive analysis based on prepared context.
            
            Analysis Goal: {self.analysis_goal}
            Entity Type: {self.entity_type}
            Entity: {self.entity_name} (ID: {self.entity_id})
            S3 Data Source: {self.s3_key}
            
            Research Context from Previous Stage:
            {research_output}
            
            Your Analysis Task:
            
            1. Review the prepared context from the researcher
            2. Identify key patterns, trends, and anomalies in the data
            3. Calculate critical performance metrics and KPIs
            4. Assess health, risks, and opportunities
            
            For any entity type (project/account/PE/other), analyze:
            - Financial performance and trends (if applicable)
            - Operational efficiency and effectiveness
            - Risk factors and their probability/impact
            - Growth and improvement opportunities
            - Benchmarking against available standards
            - Data-backed patterns and correlations
            
            Entity-Specific Considerations:
            - For Projects: Revenue variance, cost efficiency, profitability
            - For Accounts: Portfolio performance, shortfall analysis, growth potential
            - For PE: Portfolio alignment, company capabilities, investment potential
            
            Analysis Steps:
            1. Organize available data into logical categories
            2. Identify the 5-10 most significant findings
            3. Classify findings as: critical, high priority, medium priority, low priority
            4. Develop evidence-backed recommendations
            5. Quantify impact where possible
            6. Flag data limitations that affect confidence in findings
            
            Output Format Requirements:
            - Be specific and data-backed
            - Quantify impact where possible
            - Prioritize by impact and actionability
            - Note any assumptions due to missing data
            - Stay objective and analytical
            """,
            agent=self.agents_factory.analyzer_agent(),
            expected_output=f"""
            Comprehensive analytical findings including:
            - Entity overview and key identifiers
            - 5-10 most significant findings (prioritized)
            - Performance metrics and assessments
            - Health/strength evaluation
            - Risk and opportunity identification
            - Key patterns and correlations
            - Data-backed strategic recommendations
            - Confidence level for each finding
            - Identified limitations in analysis
            """
        )
    
    def create_summarization_task(self, analysis_output: Task) -> Task:
        """
        Create summarization task for JSON-compatible output.
        
        This task transforms analysis findings into structured JSON
        that matches the required schema for DB persistence.
        """
        if self.entity_type == "project":
            return Task(
                description=f"""
                Convert the project analysis into STRICT JSON only.

                Analysis Target: {self.entity_name} ({self.entity_type})

                Output rules:
                - Return only valid JSON
                - Do not include markdown
                - Do not include explanations outside JSON
                - Do not summarize documents
                - Keep insights concise but meaningful
                - Every insight should be evidence-based and decision-relevant
                - If data is missing, infer cautiously and avoid hallucination
                - If there is no strong signal for a category, return an empty list or fewer insights

                Required JSON schema:
                {{
                  "project_name": "",
                  "health_score": 0,
                  "summary": "2-3 line executive summary",
                  "delivery_insights": [],
                  "financial_insights": [],
                  "ai_insights": [],
                  "engineering_insights": [],
                  "timeline_insights": [],
                  "governance_insights": [],
                  "risks": [
                    {{
                      "type": "delivery | financial | engineering | ai | governance",
                      "severity": "low | medium | high",
                      "message": "..."
                    }}
                  ],
                  "opportunities": [
                    {{
                      "type": "ai_adoption | optimization | expansion | quality_improvement",
                      "impact": "low | medium | high",
                      "message": "..."
                    }}
                  ],
                  "recommendations": []
                }}

                Health score guidance:
                - 80-100: strong health, only minor issues
                - 60-79: generally workable but clear risks or gaps exist
                - 40-59: material delivery, financial, engineering, or governance risk
                - 0-39: critical risk or insufficient evidence with severe warning signs
                """,
                agent=self.agents_factory.summarizer_agent(context_type=self.entity_type),
                context=[analysis_output],
                expected_output="""
                Valid JSON object only:
                {
                  "project_name": "",
                  "health_score": 0,
                  "summary": "",
                  "delivery_insights": [],
                  "financial_insights": [],
                  "ai_insights": [],
                  "engineering_insights": [],
                  "timeline_insights": [],
                  "governance_insights": [],
                  "risks": [],
                  "opportunities": [],
                  "recommendations": []
                }
                """
            )
        elif self.entity_type == "account":
            return Task(
                description=f"""
                Generate ACCOUNT-LEVEL STRATEGIC INSIGHTS in STRICT JSON.

                Analysis Target: {self.entity_name}

                You are an Account Intelligence Analyst AI.

                Your job:
                - Identify CROSS-PROJECT patterns (NOT project summaries)
                - Detect systemic risks, dependencies, inefficiencies
                - Correlate delivery + revenue + AI signals
                - Provide leadership-grade insights

                CRITICAL:
                - Do NOT list projects individually
                - Focus on patterns across projects
                - Highlight only systemic issues

                Required JSON schema:
                {{
                "account_name": "",
                "overall_health_score": 0,
                "summary": "3-4 line executive summary",

                "portfolio_insights": [],
                "financial_insights": [],
                "delivery_insights": [],
                "ai_insights": [],
                "governance_insights": [],

                "risks": [
                    {{
                    "type": "delivery | financial | ai | governance | concentration",
                    "severity": "low | medium | high",
                    "message": ""
                    }}
                ],

                "opportunities": [
                    {{
                    "type": "ai_scaling | revenue_expansion | optimization | cross_project_reuse",
                    "impact": "low | medium | high",
                    "message": ""
                    }}
                ],

                "recommendations": []
                }}

                Scoring Guidance:
                - Base on avg project health
                - Adjust down for:
                - repeated risks
                - revenue shortfall
                - weak AI ROI
                """,
                agent=self.agents_factory.summarizer_agent(context_type="account"),
                context=[analysis_output],
                expected_output="""
                {
                "account_name": "",
                "overall_health_score": 0,
                "summary": "",
                "portfolio_insights": [],
                "financial_insights": [],
                "delivery_insights": [],
                "ai_insights": [],
                "governance_insights": [],
                "risks": [],
                "opportunities": [],
                "recommendations": []
                }
                """
            )

    # ---------------- PRIVATE EQUITY LEVEL ----------------
        elif self.entity_type in ["private_equity", "pe"]:
            return Task(
                description=f"""
                Generate PORTFOLIO-LEVEL STRATEGIC INSIGHTS in STRICT JSON.

                Analysis Target: {self.entity_name}

                You are a Private Equity Portfolio Intelligence AI.

                Your job:
                - Analyze across ALL portfolio accounts
                - Identify patterns, gaps, and transformation opportunities
                - Compare PE strategy vs actual execution
                - Map gaps to company capabilities

                CRITICAL:
                - Do NOT summarize individual accounts
                - Think PORTFOLIO-WIDE
                - Focus on transformation and value creation

                Required JSON schema:
                {{
                "pe_name": "",
                "portfolio_summary": "",

                "portfolio_insights": [],

                "strategic_gaps": [
                    {{
                    "gap_type": "technology | ai | delivery | revenue | governance",
                    "description": "",
                    "impact": "low | medium | high"
                    }}
                ],

                "capability_alignment": [
                    {{
                    "gap": "",
                    "relevant_capability": "",
                    "solution_approach": ""
                    }}
                ],

                "opportunities": [
                    {{
                    "type": "portfolio_transformation | ai_scaling | modernization | optimization",
                    "impact": "low | medium | high",
                    "description": ""
                    }}
                ],

                "risks": [
                    {{
                    "type": "portfolio | financial | execution",
                    "severity": "low | medium | high",
                    "description": ""
                    }}
                ],

                "strategic_recommendations": [],

                "leadership_pitch": []
                }}
                """,
                agent=self.agents_factory.summarizer_agent(context_type="private_equity"),
                context=[analysis_output],
                expected_output="""
                {
                "pe_name": "",
                "portfolio_summary": "",
                "portfolio_insights": [],
                "strategic_gaps": [],
                "capability_alignment": [],
                "opportunities": [],
                "risks": [],
                "strategic_recommendations": [],
                "leadership_pitch": []
                }
                """
            )

        return Task(
            description=f"""
            Synthesize analysis findings into structured insights JSON.
            
            Analysis Target: {self.entity_name} ({self.entity_type})
            Output Schema Hint: {self.output_schema_hint}
            
            Your Summarization Task:
            
            1. Review the analysis findings
            2. Extract key insights and metrics
            3. Create a comprehensive JSON output with these sections:
            
               a) Entity Reference:
                  - level: "{self.entity_type}"
                  - entity_id: string (from data)
                  - entity_name: string (from data)
                  - generated_at: ISO datetime
            
               b) Executive Summary:
                  - executive_summary: 2-3 paragraph concise overview
                  - confidence_score: 0-1 (credibility of analysis)
            
               c) Key Performance Indicators:
                  - kpis: dict with 5-7 most important metrics specific to entity type
                    Example for accounts: {{"revenue_target": X, "forecast": Y, "shortfall": Z}}
                    Example for projects: {{"actual_revenue": X, "expected": Y, "variance": Z}}
            
               d) Risk Assessment:
                  - risks: list of 3-5 key risks, each with:
                    {{"name": "...", "probability": "high/medium/low", "impact": "high/medium/low", "mitigation": "..."}}
            
               e) Opportunities:
                  - opportunities: list of 3-5 key opportunities, each with:
                    {{"name": "...", "potential_impact": "...", "effort": "high/medium/low", "timeline": "..."}}
            
               f) Recommended Actions:
                  - recommended_actions: list of 3-5 prioritized actions, each with:
                    {{"priority": "1-5", "action": "...", "expected_outcome": "...", "timeline": "..."}}
            
               g) Gaps Identified:
                  - gaps_identified: list of 3-5 gaps, each with:
                    {{"gap": "...", "impact": "high/medium/low", "evidence": "...", "suggested_fix": "..."}}
                  - Include capability gaps, revenue gaps, delivery gaps, data gaps, relationship gaps, or portfolio gaps as applicable.
            
               h) Suggestions:
                  - suggestions: list of 3-5 practical suggestions, each with:
                    {{"suggestion": "...", "rationale": "...", "expected_benefit": "...", "priority": "high/medium/low"}}
                  - Suggestions should be concrete, business-useful, and based on the available data.
            
               i) Pitch:
                  - pitch: dict describing how to position or pitch an opportunity to win or expand client work:
                    {{
                        "target_audience": "...",
                        "value_proposition": "...",
                        "talking_points": ["...", "..."],
                        "recommended_offer": "...",
                        "why_now": "...",
                        "expected_client_benefit": "..."
                    }}
                  - For projects, focus on expansion or modernization opportunities.
                  - For accounts, focus on cross-sell, upsell, and portfolio growth.
                  - For PE, focus on portfolio-wide value creation and capability alignment.
            
               j) Evidence and Notes:
                  - evidence_summary: Key data points supporting the analysis
                  - data_quality_notes: Any limitations or caveats
            
            4. Ensure the output is valid JSON
            5. Ensure all required fields are present
            6. Make confidence_score between 0 and 1
            7. Ensure lists and dictionaries are well-formed
            
            CRITICAL: The output MUST be a single valid JSON object that can be
            directly parsed and stored in a database JSONB column.
            """,
            agent=self.agents_factory.summarizer_agent(context_type=self.entity_type),
            context=[analysis_output],
            expected_output=f"""
            Valid JSON object with structure:
            {{
                "level": "{self.entity_type}",
                "entity_id": "...",
                "entity_name": "...",
                "generated_at": "ISO datetime",
                "executive_summary": "...",
                "kpis": {{}},
                "risks": [],
                "opportunities": [],
                "recommended_actions": [],
                "gaps_identified": [],
                "suggestions": [],
                "pitch": {{
                    "target_audience": "...",
                    "value_proposition": "...",
                    "talking_points": [],
                    "recommended_offer": "...",
                    "why_now": "...",
                    "expected_client_benefit": "..."
                }},
                "confidence_score": 0.0-1.0,
                "evidence_summary": "...",
                "data_quality_notes": "..."
            }}
            """
        )
    
    def analyze(self) -> Dict[str, Any]:
        """
        Execute domain-neutral analysis workflow.
        
        Workflow:
        1. Researcher: Parse S3 JSON and prepare context
        2. Analyzer: Perform domain-neutral analysis
        3. Summarizer: Produce JSON-compatible output
        
        Returns:
            Dictionary with analysis results and metadata
        """
        try:
            log.log_info(f"Starting domain-neutral analysis for {self.entity_type}")
            log.log_info(f"S3 Key: {self.s3_key}")
            log.log_info(f"Analysis Goal: {self.analysis_goal}")
            
            # Create tasks with explicit context linking
            research_task = self.create_research_task()
            
            # Analysis task receives output from research task
            analysis_task = self.create_analysis_task("Research output will be provided via task context.")
            analysis_task.context = [research_task]
            
            # Summarization task receives output from analysis task
            summarization_task = self.create_summarization_task(analysis_task)
            
            # Create crew
            crew = Crew(
                agents=[
                    self.agents_factory.researcher_agent(),
                    self.agents_factory.analyzer_agent(),
                    self.agents_factory.summarizer_agent(context_type=self.entity_type)
                ],
                tasks=[
                    research_task,
                    analysis_task,
                    summarization_task
                ],
                verbose=True
            )
            
            log.log_info("=" * 80)
            log.log_info("INITIATING DOMAIN-NEUTRAL ANALYSIS WORKFLOW")
            log.log_info("=" * 80)
            log.log_info("Step 1: Researcher - Parse S3 JSON and prepare context...")
            log.log_info("Step 2: Analyzer - Perform comprehensive analysis...")
            log.log_info("Step 3: Summarizer - Produce JSON-compatible insights...")
            log.log_info("=" * 80)
            
            # Execute crew
            raw_result = crew.kickoff(inputs={
                'entity_type': self.entity_type,
                's3_key': self.s3_key,
                'analysis_goal': self.analysis_goal,
                'entity_id': self.entity_id,
                'entity_name': self.entity_name
            })
            
            log.log_info("=" * 80)
            log.log_info(f"Analysis completed for {self.entity_type}")
            log.log_info("=" * 80)
            
            # Parse output as JSON
            try:
                if isinstance(raw_result, dict):
                    insights_dict = raw_result
                elif isinstance(raw_result, str):
                    # Try to extract JSON from result
                    import json as json_module
                    insights_dict = json_module.loads(raw_result)
                else:
                    insights_dict = {"raw_output": str(raw_result)}
            except Exception as parse_error:
                log.log_error(f"Error parsing crew output as JSON: {str(parse_error)}")
                insights_dict = {"raw_output": str(raw_result)}
            
            return {
                "status": "success",
                "entity_type": self.entity_type,
                "entity_id": self.entity_id,
                "entity_name": self.entity_name,
                "s3_key": self.s3_key,
                "insights": insights_dict,
                "generated_at": __import__('datetime').datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            log.log_error(f"Error during domain-neutral analysis: {str(e)}")
            return {
                "status": "error",
                "entity_type": self.entity_type,
                "entity_id": self.entity_id,
                "error": str(e),
                "generated_at": __import__('datetime').datetime.utcnow().isoformat()
            }



def create_sales_analysis_crew(account_id: str) -> GeneralizedAnalysisCrew:
    """
    Create a sales analysis crew for the given account.
    
    Args:
        account_id: UUID of the account to analyze
    
    Returns:
        Configured GeneralizedAnalysisCrew for sales analysis
    """
    return GeneralizedAnalysisCrew(
        context_type='sales',
        entity_id=account_id,
        entity_type='sales'
    )


def create_finance_analysis_crew(project_id: str) -> GeneralizedAnalysisCrew:
    """
    Create a finance analysis crew for the given project.
    
    Args:
        project_id: UUID of the project to analyze
    
    Returns:
        Configured GeneralizedAnalysisCrew for finance analysis
    """
    return GeneralizedAnalysisCrew(
        context_type='finance',
        entity_id=project_id,
        entity_type='finance'
    )
