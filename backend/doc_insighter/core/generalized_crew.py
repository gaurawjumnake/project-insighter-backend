"""
Generalized Crew Workflow for Sales and Finance Analysis

This module demonstrates how to use the three generalized agents
(Researcher, Analyzer, Summarizer) in a flexible agentic workflow.

The same crew structure can be reused for different analytical tasks
by simply changing the context_type parameter and data source.

Example Usage:
    # For Sales Analysis
    crew = GeneralizedAnalysisCrew(
        context_type='sales',
        entity_id='<account-uuid>',
        entity_type='sales'
    )
    result = crew.analyze()
    
    # For Finance Analysis
    crew = GeneralizedAnalysisCrew(
        context_type='finance',
        entity_id='<project-uuid>',
        entity_type='finance'
    )
    result = crew.analyze()
"""

from crewai import Crew, Task
from uuid import UUID
from backend.doc_insighter.core.context_aware_agents import GeneralizedAgents
from backend.doc_insighter.tools.app_logger import Logger

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
# FACTORY FUNCTION FOR EASY CREW CREATION
# ============================================================================

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
