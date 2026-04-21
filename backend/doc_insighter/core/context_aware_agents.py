"""
Generalized Agentic Flow for Sales and Finance Analysis

A flexible, reusable agentic architecture with three core agents:
- Researcher Agent: Fetches and prepares data from the database
- Analyzer Agent: Performs deep analysis on the prepared data
- Summarizer Agent: Creates actionable insights with context-specific formatting

This design supports:
- Sales Context: Account & Dashboard data analysis with sales-focused insights
- Finance Context: Project & Revenue data analysis with financial-focused insights

The architecture is extensible and can be applied to other analytical tasks.
"""

from crewai import Agent
from uuid import UUID
from backend.doc_insighter.tools.llm_models import llm
from backend.doc_insighter.tools.app_logger import Logger
from backend.doc_insighter.tools.db_tools import DataFetcher
from backend.doc_insighter.tools.generalized_analysis_tools import (
    fetch_entity_data,
    fetch_and_upload_to_s3,
    s3_reader_tool
)
import json

log = Logger()


class GeneralizedAgents:
    """Factory for creating generalized researcher, analyzer, and summarizer agents."""
    
    def __init__(self):
        # self.llm = LLMModels.get_gpt4o()
        self.data_fetcher = DataFetcher()
    
    # ========================================================================
    # CORE AGENTS
    # ========================================================================
    
    def researcher_agent(self) -> Agent:
        """
        Researcher Agent: Fetches data from database and uploads to S3 for scalable processing.
        
        Responsibilities:
        - Extract data from database for the given entity
        - Upload combined data to S3 (metrics + insights)
        - Return S3 key for downstream processing
        - Immediately release database connections (prevents connection pool exhaustion)
        
        This agent bridges the gap between raw data and scalable agent processing.
        By uploading to S3, multiple crews can process data concurrently without
        competing for limited database connections.
        """
        return Agent(
            role="Data Pipeline Engineer",
            backstory="""You are an expert data pipeline engineer with expertise in:
            - Scalable data extraction architectures
            - Data organization and storage optimization
            - Connection pool management and resource efficiency
            - Multi-source data consolidation
            - Concurrent processing patterns
            
            You understand the critical importance of releasing database resources
            quickly to enable scalable concurrent analysis.
            
            Your role is to efficiently extract data to S3 for distributed processing.""",
            goal="""Your mission is to efficiently extract and stage data for analysis:
            
            1. Fetch all relevant metrics and insights from the database
            2. Upload combined data to S3 with proper naming conventions
            3. Return the S3 key for downstream analysts
            4. Ensure database connections are released immediately
            5. Enable concurrent processing by multiple analyst crews
            
            By completing this step, you enable scalable analysis without
            database connection bottlenecks.""",
            llm=llm,
            verbose=False,
            allow_delegation=False,
            tools=[fetch_and_upload_to_s3]
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
            
            Your analytical background spans both Sales and Finance domains:
            - Sales Analysis: Account health, growth potential, engagement metrics
            - Finance Analysis: Profitability, revenue variance, cost efficiency
            
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
            tools=[s3_reader_tool]
        )
    
    def summarizer_agent(self, context_type: str = 'sales') -> Agent:
        """
        Summarizer Agent: Creates final, actionable insights with context-specific formatting.
        
        Args:
            context_type: Either 'sales' or 'finance' to customize output format
        
        Responsibilities:
        - Synthesize analysis into executive summaries
        - Generate context-specific insights
        - Creates actionable recommendations
        - Formats output appropriately for the business context
        
        This agent produces the final deliverable for business stakeholders.
        """
        
        if context_type.lower() == 'finance':
            return Agent(
                role="Financial Insights Synthesizer",
                backstory="""You are an expert financial insights specialist with:
                - CFO-level strategic thinking
                - Financial narrative development
                - Profitability and efficiency focused mindset
                - Revenue and cost optimization expertise
                - Risk and compliance awareness
                
                You synthesize complex financial data into clear,
                executive-ready financial insights that drive business strategy.
                
                You are comfortable working with S3-based data sources and can
                retrieve supporting data as needed for comprehensive analysis.""",
                goal="""Transform analytical findings into compelling financial insights:
                
                1. Distill analysis into key financial findings
                2. Highlight profitability drivers and detractors
                3. Identify financial risks and mitigation strategies
                4. Quantify revenue impact of recommendations
                5. Create executive summary of financial performance
                6. Frame insights in financial/business terms
                
                Format your output as Financial Insights with:
                - Key Financial Findings
                - Profitability Analysis
                - Revenue Optimization Opportunities
                - Financial Risk Assessment
                - Recommendations with Financial Impact
                - Performance Timeline and KPIs""",
                llm=llm,
                verbose=False,
                allow_delegation=False,
                tools=[s3_reader_tool]
            )
        else:  # sales context
            return Agent(
                role="Sales Insights Synthesizer",
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
                tools=[s3_reader_tool]
            )
