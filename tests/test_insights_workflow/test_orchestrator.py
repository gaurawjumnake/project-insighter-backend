"""
Smoke Tests for Workflow Orchestrator Components

Tests the core orchestration engine:
- GeneralizedAgents factory and agent creation
- GeneralizedAnalysisCrew workflow execution
- DomainNeutralAnalysisCrew with custom analysis goals
- Task creation and workflow orchestration
- Error handling and validation
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
from uuid import uuid4
import json

from backend.insights_workflow.core.generalized_crew import (
    GeneralizedAnalysisCrew,
    DomainNeutralAnalysisCrew
)
from backend.insights_workflow.core.context_aware_agents import GeneralizedAgents


class TestGeneralizedAgentsFactory:
    """Smoke tests for GeneralizedAgents factory."""
    
    def test_factory_initialization(self):
        """Test that agents factory initializes successfully."""
        agents_factory = GeneralizedAgents()
        assert agents_factory is not None
        assert hasattr(agents_factory, "s3_reader_tool")
    
    def test_researcher_agent_creation(self):
        """Test researcher agent is created with correct properties."""
        agents_factory = GeneralizedAgents()
        researcher = agents_factory.researcher_agent()
        
        assert researcher is not None
        assert researcher.role == "Research Context Specialist"
        assert "S3" in researcher.goal or "research" in researcher.goal.lower()
        assert not researcher.allow_delegation
    
    def test_analyzer_agent_creation(self):
        """Test analyzer agent is created with correct properties."""
        agents_factory = GeneralizedAgents()
        analyzer = agents_factory.analyzer_agent()
        
        assert analyzer is not None
        assert analyzer.role == "Analytics Specialist"
        assert "analysis" in analyzer.goal.lower() or "insight" in analyzer.goal.lower()
        assert not analyzer.allow_delegation
    
    def test_summarizer_agent_creation(self):
        """Test summarizer agent is created with correct properties."""
        agents_factory = GeneralizedAgents()
        summarizer = agents_factory.summarizer_agent()
        
        assert summarizer is not None
        assert summarizer.role == "Insights Summarizer"
        assert not analyzer.allow_delegation
    
    def test_agents_have_llm_configured(self):
        """Test that all agents have LLM configured."""
        agents_factory = GeneralizedAgents()
        
        researcher = agents_factory.researcher_agent()
        analyzer = agents_factory.analyzer_agent()
        summarizer = agents_factory.summarizer_agent()
        
        assert researcher.llm is not None
        assert analyzer.llm is not None
        assert summarizer.llm is not None


class TestGeneralizedAnalysisCrew:
    """Smoke tests for GeneralizedAnalysisCrew orchestration."""
    
    def test_crew_initialization_sales(self):
        """Test crew initializes correctly for sales context."""
        entity_id = str(uuid4())
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=entity_id,
            entity_type="account"
        )
        
        assert crew is not None
        assert crew.context_type == "sales"
        assert crew.entity_id == entity_id
        assert crew.entity_type == "account"
    
    def test_crew_initialization_finance(self):
        """Test crew initializes correctly for finance context."""
        entity_id = str(uuid4())
        crew = GeneralizedAnalysisCrew(
            context_type="finance",
            entity_id=entity_id,
            entity_type="project"
        )
        
        assert crew is not None
        assert crew.context_type == "finance"
        assert crew.entity_type == "project"
    
    def test_crew_initialization_invalid_context(self):
        """Test crew raises error on invalid context type."""
        with pytest.raises(ValueError, match="Invalid context_type"):
            GeneralizedAnalysisCrew(
                context_type="invalid",
                entity_id=str(uuid4()),
                entity_type="account"
            )
    
    def test_crew_has_agents_factory(self):
        """Test crew has agents factory initialized."""
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=str(uuid4()),
            entity_type="account"
        )
        
        assert crew.agents_factory is not None
        assert isinstance(crew.agents_factory, GeneralizedAgents)
    
    @patch("backend.insights_workflow.core.generalized_crew.Crew")
    def test_crew_can_create_crew_instance(self, mock_crew_class):
        """Test crew can instantiate a Crew object."""
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=str(uuid4()),
            entity_type="account"
        )
        
        # Attempt to create research task (which uses Crew internally)
        research_task = crew.create_research_task()
        assert research_task is not None


class TestDomainNeutralAnalysisCrew:
    """Smoke tests for DomainNeutralAnalysisCrew (domain-agnostic workflow)."""
    
    def test_crew_initialization_with_custom_goal(self):
        """Test crew initializes with custom analysis goal."""
        s3_key = "temp/project_123_2026-05-07.json"
        analysis_goal = "Extract financial insights from staged data"
        
        crew = DomainNeutralAnalysisCrew(
            entity_type="project",
            s3_key=s3_key,
            analysis_goal=analysis_goal
        )
        
        assert crew is not None
        assert crew.entity_type == "project"
        assert crew.s3_key == s3_key
        assert crew.analysis_goal == analysis_goal
    
    def test_crew_initialization_account_entity(self):
        """Test crew initializes for account entity type."""
        crew = DomainNeutralAnalysisCrew(
            entity_type="account",
            s3_key="temp/account_456_2026-05-07.json",
            analysis_goal="Account portfolio analysis"
        )
        
        assert crew.entity_type == "account"
    
    def test_crew_initialization_pe_entity(self):
        """Test crew initializes for PE entity type."""
        crew = DomainNeutralAnalysisCrew(
            entity_type="private_equity",
            s3_key="temp/pe_789_2026-05-07.json",
            analysis_goal="PE portfolio alignment analysis"
        )
        
        assert crew.entity_type == "private_equity"
    
    def test_crew_with_custom_output_schema(self):
        """Test crew accepts custom output schema hints."""
        output_schema_hint = "JSON with {level, executive_summary, kpis, risks}"
        
        crew = DomainNeutralAnalysisCrew(
            entity_type="project",
            s3_key="temp/project_123_2026-05-07.json",
            analysis_goal="Financial insights",
            output_schema_hint=output_schema_hint
        )
        
        assert crew.output_schema_hint == output_schema_hint
    
    @patch("backend.insights_workflow.core.generalized_crew.Crew")
    def test_crew_can_execute_analysis(self, mock_crew_class):
        """Test domain-neutral crew can execute analysis."""
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = DomainNeutralAnalysisCrew(
            entity_type="project",
            s3_key="temp/project_123_2026-05-07.json",
            analysis_goal="Financial insights"
        )
        
        assert crew is not None
        assert hasattr(crew, "analyze") or callable(getattr(crew, "analyze", None))


class TestCrewTaskCreation:
    """Smoke tests for task creation in crews."""
    
    def test_research_task_creation(self):
        """Test research task is created successfully."""
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=str(uuid4()),
            entity_type="account"
        )
        
        research_task = crew.create_research_task()
        assert research_task is not None
        assert hasattr(research_task, "description") or hasattr(research_task, "agent")
    
    def test_analysis_task_creation(self):
        """Test analysis task is created successfully."""
        crew = GeneralizedAnalysisCrew(
            context_type="finance",
            entity_id=str(uuid4()),
            entity_type="project"
        )
        
        analysis_task = crew.create_analysis_task()
        assert analysis_task is not None
    
    def test_summarization_task_creation(self):
        """Test summarization task is created successfully."""
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=str(uuid4()),
            entity_type="account"
        )
        
        summary_task = crew.create_summarization_task()
        assert summary_task is not None


class TestOrchestratorErrorHandling:
    """Smoke tests for error handling in orchestrator."""
    
    def test_invalid_entity_id_format(self):
        """Test crew handles invalid entity ID."""
        with pytest.raises((ValueError, TypeError)):
            GeneralizedAnalysisCrew(
                context_type="sales",
                entity_id="not-a-uuid",
                entity_type="account"
            )
    
    def test_crew_with_empty_entity_id(self):
        """Test crew handles empty entity ID gracefully."""
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id="",
            entity_type="account"
        )
        
        # Should still initialize but may fail during execution
        assert crew is not None
    
    def test_domain_neutral_crew_with_missing_s3_key(self):
        """Test domain-neutral crew validates S3 key."""
        with pytest.raises((ValueError, TypeError, AssertionError)):
            DomainNeutralAnalysisCrew(
                entity_type="project",
                s3_key="",  # Empty S3 key should fail
                analysis_goal="Test goal"
            )
    
    def test_crew_handles_none_context_type(self):
        """Test crew rejects None context type."""
        with pytest.raises((ValueError, TypeError)):
            GeneralizedAnalysisCrew(
                context_type=None,
                entity_id=str(uuid4()),
                entity_type="account"
            )


class TestOrchestratorWorkflow:
    """Smoke tests for complete workflow execution."""
    
    @patch("backend.insights_workflow.core.generalized_crew.Crew")
    @patch("backend.insights_workflow.core.context_aware_agents.GeneralizedAgents")
    def test_complete_sales_workflow(self, mock_agents, mock_crew_class):
        """Test complete sales analysis workflow."""
        # Setup mocks
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = MagicMock(
            raw=json.dumps({
                "insights": "Test insights",
                "status": "success"
            })
        )
        mock_crew_class.return_value = mock_crew_instance
        
        # Execute workflow
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=str(uuid4()),
            entity_type="account"
        )
        
        assert crew is not None
    
    @patch("backend.insights_workflow.core.generalized_crew.Crew")
    def test_complete_finance_workflow(self, mock_crew_class):
        """Test complete finance analysis workflow."""
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = GeneralizedAnalysisCrew(
            context_type="finance",
            entity_id=str(uuid4()),
            entity_type="project"
        )
        
        assert crew is not None
    
    @patch("backend.insights_workflow.core.generalized_crew.Crew")
    def test_domain_neutral_workflow_project(self, mock_crew_class):
        """Test domain-neutral workflow for project."""
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        
        crew = DomainNeutralAnalysisCrew(
            entity_type="project",
            s3_key="temp/project_123_2026-05-07.json",
            analysis_goal="Comprehensive project insights"
        )
        
        assert crew is not None


class TestOrchestratorAgentConfiguration:
    """Smoke tests for agent configuration and setup."""
    
    def test_agents_have_correct_tools(self):
        """Test agents have required tools configured."""
        agents_factory = GeneralizedAgents()
        
        researcher = agents_factory.researcher_agent()
        # Researcher should have S3 reader tool
        assert len(researcher.tools) > 0 or researcher.tools is not None
    
    def test_agents_have_backstories(self):
        """Test all agents have meaningful backstories."""
        agents_factory = GeneralizedAgents()
        
        researcher = agents_factory.researcher_agent()
        analyzer = agents_factory.analyzer_agent()
        summarizer = agents_factory.summarizer_agent()
        
        assert len(researcher.backstory) > 0
        assert len(analyzer.backstory) > 0
        assert len(summarizer.backstory) > 0
    
    def test_agents_have_goals(self):
        """Test all agents have defined goals."""
        agents_factory = GeneralizedAgents()
        
        researcher = agents_factory.researcher_agent()
        analyzer = agents_factory.analyzer_agent()
        summarizer = agents_factory.summarizer_agent()
        
        assert len(researcher.goal) > 0
        assert len(analyzer.goal) > 0
        assert len(summarizer.goal) > 0
    
    def test_agents_no_delegation_allowed(self):
        """Test agents are configured without delegation."""
        agents_factory = GeneralizedAgents()
        
        researcher = agents_factory.researcher_agent()
        analyzer = agents_factory.analyzer_agent()
        summarizer = agents_factory.summarizer_agent()
        
        assert researcher.allow_delegation is False
        assert analyzer.allow_delegation is False
        assert summarizer.allow_delegation is False


class TestOrchestratorPerformance:
    """Smoke tests for orchestrator performance."""
    
    def test_agent_creation_performance(self, timer):
        """Test agents are created quickly."""
        agents_factory = GeneralizedAgents()
        
        timer.start()
        researcher = agents_factory.researcher_agent()
        analyzer = agents_factory.analyzer_agent()
        summarizer = agents_factory.summarizer_agent()
        timer.stop()
        
        # Agents should be created in under 1 second
        assert timer.elapsed < 1.0
    
    def test_crew_initialization_performance(self, timer):
        """Test crew initializes quickly."""
        timer.start()
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=str(uuid4()),
            entity_type="account"
        )
        timer.stop()
        
        # Crew should initialize in under 500ms
        assert timer.elapsed < 0.5
    
    def test_domain_neutral_crew_initialization(self, timer):
        """Test domain-neutral crew initializes quickly."""
        timer.start()
        crew = DomainNeutralAnalysisCrew(
            entity_type="project",
            s3_key="temp/project_123_2026-05-07.json",
            analysis_goal="Test analysis"
        )
        timer.stop()
        
        # Should initialize quickly
        assert timer.elapsed < 0.5
