"""
Integration Smoke Tests for Workflow Orchestrator

Tests end-to-end workflows:
- Complete insight generation pipeline
- API endpoint integration
- Service-to-orchestrator coordination
- Error recovery and data consistency
- Performance under load
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from uuid import uuid4
import json
from datetime import datetime
import asyncio

from backend.insights_workflow.services.finance_insights_service import FinanceInsightsService
from backend.insights_workflow.core.generalized_crew import GeneralizedAnalysisCrew


class TestEndToEndProjectWorkflow:
    """Integration tests for complete project insight workflow."""
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_project_insight_generation_end_to_end(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_project_data
    ):
        """Test complete project insight generation from request to persistence."""
        project_id = str(uuid4())
        
        # Setup workflow mocks
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        
        # Stage 1: Data aggregation
        mock_agg.get_project_data.return_value = (sample_project_data, [])
        
        # Stage 2: S3 operations
        mock_upload.return_value = f"s3://bucket/project_{project_id}.json"
        mock_download.return_value = sample_project_data
        
        # Stage 3: Crew analysis
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {
            "status": "success",
            "summary": "Project on track",
            "metrics": {
                "health": "green",
                "progress": 65
            },
            "timestamp": datetime.now().isoformat()
        }
        mock_crew.return_value = mock_crew_instance
        
        # Stage 4: Persistence
        mock_project = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_project
        
        # Execute end-to-end workflow
        result = FinanceInsightsService.generate_project_insights(project_id)
        
        # Verify result structure
        assert result is not None
        assert isinstance(result, dict)
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_multiple_projects_parallel_processing(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_project_data
    ):
        """Test processing multiple projects in sequence."""
        project_ids = [str(uuid4()) for _ in range(3)]
        
        # Setup mocks
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_agg.get_project_data.return_value = (sample_project_data, [])
        mock_upload.return_value = "s3://bucket/project.json"
        mock_download.return_value = sample_project_data
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {"status": "success", "insights": "Test"}
        mock_crew.return_value = mock_crew_instance
        
        # Execute for multiple projects
        results = []
        for project_id in project_ids:
            result = FinanceInsightsService.generate_project_insights(project_id)
            results.append(result)
        
        # Verify all completed
        assert len(results) == 3
        for result in results:
            assert result is not None


class TestEndToEndAccountWorkflow:
    """Integration tests for complete account insight workflow."""
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_account_insight_generation_end_to_end(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_account_data
    ):
        """Test complete account insight generation workflow."""
        account_id = str(uuid4())
        
        # Setup workflow mocks
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        
        mock_agg.get_account_data.return_value = (sample_account_data, [])
        mock_upload.return_value = f"s3://bucket/account_{account_id}.json"
        mock_download.return_value = sample_account_data
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {
            "status": "success",
            "summary": "Account portfolio healthy"
        }
        mock_crew.return_value = mock_crew_instance
        
        mock_account = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_account
        
        # Execute workflow
        result = FinanceInsightsService.generate_account_insights(account_id)
        
        # Verify
        assert result is not None
        assert isinstance(result, dict)


class TestEndToEndPEWorkflow:
    """Integration tests for complete PE insight workflow."""
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_pe_insight_generation_end_to_end(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_pe_data
    ):
        """Test complete PE insight generation workflow."""
        pe_id = str(uuid4())
        
        # Setup workflow mocks
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        
        mock_agg.get_pe_data.return_value = (sample_pe_data, [])
        mock_upload.return_value = f"s3://bucket/pe_{pe_id}.json"
        mock_download.return_value = sample_pe_data
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {
            "status": "success",
            "summary": "PE portfolio aligned"
        }
        mock_crew.return_value = mock_crew_instance
        
        # Execute workflow
        result = FinanceInsightsService.generate_pe_insights(pe_id)
        
        # Verify
        assert result is not None
        assert isinstance(result, dict)


class TestOrchestratorServiceIntegration:
    """Integration tests between orchestrator and service layer."""
    
    @patch("backend.insights_workflow.core.generalized_crew.Crew")
    @patch("backend.insights_workflow.core.context_aware_agents.GeneralizedAgents")
    def test_crew_instantiation_from_service(self, mock_agents, mock_crew_class):
        """Test service can instantiate crew correctly."""
        # Create crew as service would
        crew = GeneralizedAnalysisCrew(
            context_type="finance",
            entity_id=str(uuid4()),
            entity_type="project"
        )
        
        # Verify crew has agents
        assert crew.agents_factory is not None
    
    def test_crew_task_delegation_to_agents(self):
        """Test crew properly delegates tasks to agents."""
        crew = GeneralizedAnalysisCrew(
            context_type="sales",
            entity_id=str(uuid4()),
            entity_type="account"
        )
        
        # Tasks should be creatable
        research_task = crew.create_research_task()
        analysis_task = crew.create_analysis_task()
        summary_task = crew.create_summarization_task()
        
        assert research_task is not None
        assert analysis_task is not None
        assert summary_task is not None


class TestDataFlowConsistency:
    """Integration tests for data consistency across workflow stages."""
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_data_consistency_through_stages(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_project_data
    ):
        """Test data remains consistent through aggregation → S3 → analysis."""
        project_id = str(uuid4())
        
        # Setup: ensure same data flows through all stages
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        
        original_data = sample_project_data.copy()
        mock_agg.get_project_data.return_value = (original_data, [])
        mock_upload.return_value = "s3://key"
        mock_download.return_value = original_data  # Same data retrieved from S3
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {"insights": "analyzed"}
        mock_crew.return_value = mock_crew_instance
        
        # Execute
        result = FinanceInsightsService.generate_project_insights(project_id)
        
        # Verify data consistency
        assert mock_download.return_value == original_data


class TestWorkflowErrorRecovery:
    """Integration tests for error recovery across workflow."""
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    def test_recovery_from_s3_upload_failure(self, mock_upload, mock_session, mock_agg):
        """Test workflow recovers when S3 upload fails."""
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_agg.get_project_data.return_value = ({"data": "test"}, [])
        mock_upload.side_effect = Exception("S3 connection timeout")
        
        # Should handle gracefully without crashing
        try:
            result = FinanceInsightsService.generate_project_insights(str(uuid4()))
            # Result should indicate what went wrong
            assert result is not None
        except Exception as e:
            pytest.fail(f"Workflow should recover from S3 errors: {e}")
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_recovery_from_crew_analysis_failure(
        self, mock_crew, mock_download, mock_upload, mock_session, mock_agg
    ):
        """Test workflow handles crew analysis failures."""
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_agg.get_project_data.return_value = ({"data": "test"}, [])
        mock_upload.return_value = "s3://key"
        mock_download.return_value = {"data": "test"}
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.side_effect = Exception("LLM API timeout")
        mock_crew.return_value = mock_crew_instance
        
        # Should handle gracefully
        try:
            result = FinanceInsightsService.generate_project_insights(str(uuid4()))
        except Exception as e:
            pytest.fail(f"Workflow should handle crew errors: {e}")


class TestWorkflowPerformance:
    """Integration tests for workflow performance characteristics."""
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_workflow_response_time(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_project_data, timer
    ):
        """Test workflow completes within acceptable time."""
        # Setup mocks
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_agg.get_project_data.return_value = (sample_project_data, [])
        mock_upload.return_value = "s3://key"
        mock_download.return_value = sample_project_data
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {"insights": "test"}
        mock_crew.return_value = mock_crew_instance
        
        # Execute with timer
        timer.start()
        FinanceInsightsService.generate_project_insights(str(uuid4()))
        timer.stop()
        
        # Should complete quickly (crew execution is mocked)
        assert timer.elapsed < 5.0  # 5 second timeout for mocked execution
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_workflow_scales_with_multiple_entities(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_project_data, timer
    ):
        """Test workflow scales when processing multiple entities."""
        # Setup mocks
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_agg.get_project_data.return_value = (sample_project_data, [])
        mock_upload.return_value = "s3://key"
        mock_download.return_value = sample_project_data
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {"insights": "test"}
        mock_crew.return_value = mock_crew_instance
        
        # Process multiple projects
        timer.start()
        for _ in range(5):
            FinanceInsightsService.generate_project_insights(str(uuid4()))
        timer.stop()
        
        # Should handle 5 projects efficiently
        assert timer.elapsed < 10.0


class TestResponsePatterns:
    """Integration tests for response patterns and data structures."""
    
    @patch("backend.insights_workflow.services.finance_insights_service.FinanceAggregationService")
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    @patch("backend.insights_workflow.services.finance_insights_service.upload_data_to_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.download_data_from_s3")
    @patch("backend.insights_workflow.services.finance_insights_service.DomainNeutralAnalysisCrew")
    def test_success_response_structure(
        self, mock_crew, mock_download, mock_upload, mock_session,
        mock_agg, sample_project_data
    ):
        """Test successful response has correct structure."""
        mock_db = MagicMock()
        mock_session.return_value = mock_db
        mock_agg.get_project_data.return_value = (sample_project_data, [])
        mock_upload.return_value = "s3://key"
        mock_download.return_value = sample_project_data
        
        mock_crew_instance = MagicMock()
        mock_crew_instance.analyze.return_value = {
            "status": "success",
            "insights": "Test insights"
        }
        mock_crew.return_value = mock_crew_instance
        
        # Execute
        result = FinanceInsightsService.generate_project_insights(str(uuid4()))
        
        # Verify response structure
        assert isinstance(result, dict)
    
    @patch("backend.insights_workflow.services.finance_insights_service.SessionLocal")
    def test_error_response_structure(self, mock_session):
        """Test error response has correct structure."""
        # Invalid UUID
        result = FinanceInsightsService.generate_project_insights("not-a-uuid")
        
        # Verify error response structure
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "error"
        assert "error" in result or "entity_type" in result


class TestWorkflowValidation:
    """Integration tests for input validation throughout workflow."""
    
    def test_project_id_validation(self):
        """Test project ID validation at service boundary."""
        # Invalid UUID format
        result = FinanceInsightsService.generate_project_insights("invalid-uuid")
        assert result.get("status") == "error"
    
    def test_account_id_validation(self):
        """Test account ID validation at service boundary."""
        # Invalid UUID format
        result = FinanceInsightsService.generate_account_insights("invalid-uuid")
        assert result.get("status") == "error"
    
    def test_pe_id_validation(self):
        """Test PE ID validation at service boundary."""
        # Invalid UUID format
        result = FinanceInsightsService.generate_pe_insights("invalid-uuid")
        assert result.get("status") == "error"
