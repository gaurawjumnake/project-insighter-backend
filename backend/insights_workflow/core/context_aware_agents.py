"""
Generalized Agentic Flow for S3-Staged Insights Analysis

A flexible, reusable agentic architecture with three core agents:
- Researcher Agent: Reads S3-staged JSON and prepares context
- Analyzer Agent: Performs deep analysis on the prepared context
- Summarizer Agent: Creates actionable insights with context-specific formatting

This design supports:
- Finance hierarchy analysis: project, account, and private equity insights
- Future insight workflows that stage structured JSON in S3

The architecture is extensible and can be applied to other analytical tasks.
"""

from crewai import Agent
from backend.utitlites.llm_models import llm
from backend.doc_insighter.tools.app_logger import Logger
from backend.insights_workflow.tools.s3_data_reader_tool import S3DataReaderTool

log = Logger()


class GeneralizedAgents:
    """Factory for creating generalized researcher, analyzer, and summarizer agents."""
    
    def __init__(self):
        # self.llm = LLMModels.get_gpt4o()
        self.s3_reader_tool = S3DataReaderTool()
    
    # ========================================================================
    # CORE AGENTS
    # ========================================================================
    
    def researcher_agent(self) -> Agent:
        """
        Researcher Agent: Reads S3-staged JSON and prepares clean context.
        
        Responsibilities:
        - Read structured JSON from S3 for the given entity
        - Parse entity metadata, metrics, documents, warnings, and processing hints
        - Prepare clean context for downstream analysis
        - Flag missing or partial data for the Analyzer
        
        Database extraction and S3 upload happen before the crew starts.
        """
        return Agent(
            role="Research Context Specialist",
            backstory="""You are an expert research analyst with expertise in:
            - Reading structured JSON datasets from S3
            - Understanding metadata, business metrics, and data quality notes
            - Separating strong evidence from partial or missing data
            - Preparing clean, concise context for deeper analysis
            
            You understand that the data has already been extracted from the
            database, transformed into JSON, and staged in S3 before you begin.""",
            goal="""Your mission is to prepare reliable context for analysis:
            
            1. Read the provided S3 JSON using the S3 Data Reader tool
            2. Identify entity metadata, hierarchy level, and available fields
            3. Summarize financial, operational, document, and insight data
            4. Call out warnings, missing data, and confidence limitations
            5. Produce a clean research brief for the Analyzer
            
            Keep the context faithful to the staged data and do not invent facts.""",
            llm=llm,
            verbose=False,
            allow_delegation=False,
            tools=[self.s3_reader_tool]
        )
       
    def analyzer_agent(self) -> Agent:
        """
        Analyzer Agent: Performs deep analysis on data retrieved from S3.
        
        Responsibilities:
        - Download data from S3 using the provided key
        - Identifies patterns and trends in the retrieved data
        - Calculates key metrics
        - Assesses performance against benchmarks
        - Identifies risks and opportunities
        - Provides detailed analytical insights
        
        This agent transforms S3-stored data into actionable intelligence,
        enabling concurrent analysis without database connection constraints.
        """
        return Agent(
            role="Analytics Specialist",
            backstory="""You are an expert analyst with deep analytical prowess:
            - Pattern recognition and trend analysis
            - Financial and operational metrics analysis
            - Risk and opportunity assessment
            - Comparative analysis and benchmarking
            - Data-driven insights generation
            
            Your analytical background spans project, account, and private equity
            portfolio analysis:
            - Project Analysis: Profitability, revenue variance, delivery efficiency
            - Account Analysis: Portfolio performance, growth potential, shortfall risk
            - PE Analysis: Portfolio alignment, capability fit, investment potential
            
            You excel at transforming data into strategic insights.
            
            You have experience working with S3-based data pipelines and can
            efficiently retrieve and analyze data from cloud storage.""",
            goal="""Analyze the data retrieved from S3 comprehensively:
            
            1. Download the complete dataset from S3 using the provided S3 key
            2. Identify key patterns, trends, and anomalies
            3. Calculate critical performance metrics
            4. Assess health, risks, and opportunities
            5. Compare against relevant benchmarks
            6. Generate detailed, data-backed insights
            7. Flag critical issues requiring attention
            
            Your analysis should be thorough, nuanced, and actionable.
            Focus on insights that drive decision-making.""",
            llm=llm,
            verbose=False,
            allow_delegation=False,
            tools=[self.s3_reader_tool]
        )
    
    def summarizer_agent(self, context_type: str = 'project') -> Agent:
        """
        Summarizer Agent: Creates final, actionable insights with context-specific formatting.
        
        Args:
            context_type: Entity type such as 'project', 'account', or 'private_equity'
        
        Responsibilities:
        - Synthesize analysis into executive summaries
        - Generate context-specific insights
        - Creates actionable recommendations
        - Formats output appropriately for the business context
        
        This agent produces the final deliverable for business stakeholders.
        """
        
        if context_type.lower() in ['finance', 'project', 'account', 'private_equity', 'pe']:
            return Agent(
                role="Strategic Insights Synthesizer",
                backstory="""You are an expert strategic insights specialist with:
                - CFO-level strategic thinking
                - Portfolio and account growth perspective
                - Financial narrative development
                - Profitability and efficiency focused mindset
                - Revenue and cost optimization expertise
                - Risk, opportunity, and capability alignment awareness
                
                You synthesize complex project, account, and private equity data
                into clear, executive-ready insights that drive business strategy
                and client expansion.
                
                You are comfortable working with S3-based data sources and can
                retrieve supporting data as needed for comprehensive analysis.""",
                goal="""Transform analytical findings into compelling structured insights:
                
                1. Distill analysis into key strategic and financial findings
                2. Highlight revenue, profitability, delivery, and capability signals
                3. Identify gaps, risks, opportunities, and mitigation strategies
                4. Quantify impact of recommendations where possible
                5. Create an executive summary of business performance
                6. Frame a practical pitch for client expansion or value creation
                
                Format your output as valid JSON with:
                - executive_summary
                - kpis
                - risks
                - opportunities
                - recommended_actions
                - gaps_identified
                - suggestions
                - pitch
                - confidence_score
                - evidence_summary""",
                llm=llm,
                verbose=False,
                allow_delegation=False,
                tools=[self.s3_reader_tool]
            )
        else:
            return Agent(
                role="General Insights Synthesizer",
                backstory="""You are an expert sales insights specialist with:
                - VP Sales level strategic thinking
                - Account growth and expansion expertise
                - Customer relationship management focus
                - Pipeline and opportunity assessment skills
                - Competitive positioning knowledge
                
                You synthesize complex account data into clear,
                actionable sales insights that drive revenue growth.
                
                You are comfortable working with S3-based data sources and can
                retrieve supporting data as needed for comprehensive analysis.""",
                goal="""Transform analytical findings into compelling sales insights:
                
                1. Distill analysis into key sales findings
                2. Identify growth and expansion opportunities
                3. Assess account health and engagement levels
                4. Highlight relationship strengths and risks
                5. Create executive summary of account position
                6. Frame insights in sales/commercial terms
                
                Format your output as Sales Insights with:
                - Key Account Findings
                - Account Health Assessment
                - Growth and Expansion Opportunities
                - Risk and Relationship Assessment
                - Recommended Actions for Account Growth
                - Success Metrics and Timeline""",
                llm=llm,
                verbose=False,
                allow_delegation=False,
                tools=[self.s3_reader_tool]
            )
