# Workflow Orchestrator Smoke Test Suite

Comprehensive smoke test suite for the Project Insighter workflow orchestrator and insights generation pipeline.

## Overview

This test suite validates critical components of the workflow orchestrator:

- **Orchestrator Core**: Agent factory, crew creation, task orchestration
- **Service Layer**: Insight generation services, data aggregation, persistence
- **End-to-End Workflows**: Complete insight generation pipelines
- **Error Handling**: Recovery and validation across all layers
- **Performance**: Response times and scalability

## Test Structure

```
tests/
├── conftest.py                          # Shared fixtures and mocks
├── pytest.ini                           # Pytest configuration
├── test_insights_workflow/
│   ├── test_orchestrator.py            # Orchestrator component tests
│   ├── test_services.py                # Service layer tests
│   └── test_integration.py             # End-to-end integration tests
├── fixtures/                           # Test data and fixtures
└── README_TESTS.md                    # This file
```

## Quick Start

### Installation

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-mock pytest-cov

# Or use the project's pyproject.toml
uv sync
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_insights_workflow/test_orchestrator.py

# Run with coverage
pytest --cov=backend.insights_workflow tests/

# Run smoke tests only
pytest -m smoke

# Run with verbose output
pytest -vv

# Run integration tests
pytest tests/test_insights_workflow/test_integration.py -v
```

## Test Categories

### Orchestrator Tests (`test_orchestrator.py`)

Tests for the workflow orchestration engine:

- **Agent Factory** (`TestGeneralizedAgentsFactory`)
  - Agent initialization and configuration
  - Tool allocation and backstory setup
  - LLM configuration

- **Crew Orchestration** (`TestGeneralizedAnalysisCrew`)
  - Crew initialization for different contexts (sales, finance)
  - Task creation and delegation
  - Workflow execution

- **Domain-Neutral Crew** (`TestDomainNeutralAnalysisCrew`)
  - Custom analysis goals
  - Output schema configuration
  - Multi-entity support (project, account, PE)

- **Error Handling** (`TestOrchestratorErrorHandling`)
  - Invalid input validation
  - Graceful error recovery
  - Edge case handling

- **Performance** (`TestOrchestratorPerformance`)
  - Agent creation performance
  - Crew initialization speed
  - Response time benchmarks

### Service Layer Tests (`test_services.py`)

Tests for insight generation services:

- **Project Insights** (`TestProjectInsightGeneration`)
  - Project insight generation workflow
  - Data aggregation
  - Error handling

- **Account Insights** (`TestAccountInsightGeneration`)
  - Account-level analysis
  - Portfolio assessment
  - Multi-project aggregation

- **Private Equity Insights** (`TestPEInsightGeneration`)
  - PE portfolio analysis
  - Company capability alignment
  - Investment assessment

- **JSON Transformation** (`TestJsonTransformer`)
  - Data format conversion
  - Schema validation
  - Output consistency

- **Workflow Execution** (`TestInsightServiceWorkflow`)
  - Complete workflow stages
  - S3 operations
  - Data persistence

### Integration Tests (`test_integration.py`)

End-to-end workflow tests:

- **Project Workflow** (`TestEndToEndProjectWorkflow`)
  - Request → Aggregation → Analysis → Persistence
  - Multi-project parallel processing
  - Data consistency

- **Account Workflow** (`TestEndToEndAccountWorkflow`)
  - Account insight generation
  - Portfolio analysis
  - Data aggregation

- **PE Workflow** (`TestEndToEndPEWorkflow`)
  - PE insight generation
  - Portfolio alignment
  - Investment assessment

- **Error Recovery** (`TestWorkflowErrorRecovery`)
  - S3 failure recovery
  - LLM timeout handling
  - Graceful degradation

- **Performance** (`TestWorkflowPerformance`)
  - Response time validation
  - Scalability testing
  - Load handling

## Fixtures

Common fixtures in `conftest.py`:

### Configuration
- `test_config`: Test configuration with safe defaults
- `timer`: Simple timer for performance testing

### Database
- `mock_db_session`: Mocked SQLAlchemy session

### S3 Storage
- `mock_s3_client`: Mocked AWS S3 client
- `mock_s3_storage`: Patched S3 upload/download functions

### LLM & CrewAI
- `mock_llm`: Mocked LLM client
- `mock_crew_agent`: Mocked CrewAI Agent
- `mock_crew_execution`: Mocked crew execution result

### Test Data
- `sample_project_data`: Sample project JSON
- `sample_account_data`: Sample account JSON
- `sample_pe_data`: Sample PE JSON

### Patching
- `patch_external_dependencies`: Comprehensive mock patch

## Example Test

```python
def test_project_insight_generation(mock_s3_storage, sample_project_data):
    """Test project insight generation workflow."""
    project_id = str(uuid4())
    
    # Execute workflow
    result = FinanceInsightsService.generate_project_insights(project_id)
    
    # Verify result
    assert result is not None
    assert result["status"] == "success"
    
    # Verify mocks were called
    assert mock_s3_storage["upload"].called
    assert mock_s3_storage["download"].called
```

## Performance Benchmarks

Target performance metrics:

| Operation | Target | Notes |
|-----------|--------|-------|
| Agent Creation | < 1 sec | Per agent |
| Crew Initialization | < 500 ms | Per context |
| Project Analysis | < 30 sec | Mocked LLM |
| Multi-Project (5x) | < 120 sec | Sequential |
| Error Recovery | < 5 sec | Graceful handling |

## Coverage Goals

- **Orchestrator**: 85%+ coverage
- **Services**: 80%+ coverage
- **Integration**: Critical path coverage

Run coverage report:

```bash
pytest --cov=backend.insights_workflow --cov-report=html tests/
```

## Continuous Integration

Run tests in CI/CD pipeline:

```bash
# Run all tests with coverage
pytest --cov=backend.insights_workflow \
       --cov-report=xml \
       --junitxml=test-results.xml \
       tests/

# Generate coverage badge
coverage-badge -o coverage.svg
```

## Troubleshooting

### Common Issues

**Issue**: Tests fail with "ModuleNotFoundError"
- **Solution**: Ensure Python path includes project root
  ```bash
  export PYTHONPATH="${PYTHONPATH}:$(pwd)"
  pytest tests/
  ```

**Issue**: S3 mock not working
- **Solution**: Verify patch paths match actual imports
  ```python
  @patch("backend.utitlites.s3_storage.upload_data_to_s3")
  ```

**Issue**: Async tests timeout
- **Solution**: Increase timeout in pytest.ini or use markers
  ```bash
  pytest --timeout=60 tests/
  ```

## Adding New Tests

### Test Template

```python
class TestNewFeature:
    """Tests for new feature."""
    
    @pytest.mark.smoke
    def test_basic_functionality(self):
        """Test basic functionality."""
        # Arrange
        fixture_data = {...}
        
        # Act
        result = function_under_test(fixture_data)
        
        # Assert
        assert result is not None
        assert result.status == "success"
    
    @pytest.mark.integration
    @patch("module.external_dependency")
    def test_with_mocks(self, mock_dep):
        """Test with mocked dependencies."""
        mock_dep.return_value = {"mocked": True}
        
        result = function_under_test()
        
        assert mock_dep.called
        assert result is not None
```

### Guidelines

1. **Use Descriptive Names**: `test_*_with_*_should_*`
2. **Organize with Classes**: Group related tests
3. **Mock External Dependencies**: S3, LLM, Database
4. **Include Docstrings**: Document test purpose
5. **Use Fixtures**: Leverage conftest.py fixtures
6. **Assert Clearly**: One primary assertion per test
7. **Handle Async**: Use `@pytest.mark.asyncio` for async tests

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Project Insighter README](../readme.md)

## Test Maintenance

### Regular Tasks

- Review test coverage quarterly
- Update fixtures when data models change
- Validate performance benchmarks
- Update mocks when dependencies change

### Deprecation

Mark deprecated tests:

```python
@pytest.mark.skip(reason="Feature deprecated in v2.0")
def test_old_feature():
    pass
```

## Questions & Support

For test-related questions:
1. Check test documentation in docstrings
2. Review example tests in same category
3. Check conftest.py for available fixtures
4. Consult pytest documentation
