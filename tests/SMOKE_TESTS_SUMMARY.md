# Smoke Test Suite - Project Insighter Backend

## Overview

A comprehensive smoke test suite has been created for the Project Insighter workflow orchestrator and insights generation pipeline. The suite validates critical components including orchestration, service layer, and end-to-end workflows.

## What's Included

### Test Files

1. **[tests/conftest.py](conftest.py)** (180+ lines)
   - Shared pytest fixtures and mocks
   - Database, S3, LLM, and CrewAI mocks
   - Test data fixtures for projects, accounts, and PE records
   - Configuration and utility fixtures

2. **[tests/test_insights_workflow/test_orchestrator.py](tests/test_insights_workflow/test_orchestrator.py)** (310+ lines)
   - **GeneralizedAgentsFactory** tests: Agent creation, configuration, and tool allocation
   - **GeneralizedAnalysisCrew** tests: Crew initialization for sales/finance contexts
   - **DomainNeutralAnalysisCrew** tests: Custom analysis goals and entity types
   - **Task Creation** tests: Research, analysis, and summarization tasks
   - **Error Handling** tests: Validation and graceful error recovery
   - **Performance** tests: Response time and initialization speed

3. **[tests/test_insights_workflow/test_services.py](tests/test_insights_workflow/test_services.py)** (350+ lines)
   - **FinanceInsightsService** tests for all entity types:
     - Project insight generation
     - Account insight generation
     - Private equity insight generation
   - **JsonTransformer** tests: Data format conversion and validation
   - **Workflow** tests: Complete stages from aggregation to persistence
   - **Error Handling** tests: Database, S3, and crew failures
   - **Data Persistence** tests: Database operation verification

4. **[tests/test_insights_workflow/test_integration.py](tests/test_insights_workflow/test_integration.py)** (350+ lines)
   - **End-to-End Workflows** for project, account, and PE entities
   - **Multi-Entity Processing** tests: Parallel and sequential processing
   - **Orchestrator-Service Integration** tests
   - **Data Flow Consistency** tests
   - **Error Recovery** tests: Graceful handling of S3 and LLM failures
   - **Performance** tests: Response times and scalability
   - **Response Pattern** tests: Validation of response structures

### Configuration & Documentation

5. **[pytest.ini](pytest.ini)** (40+ lines)
   - Pytest configuration with markers for categorizing tests
   - Test discovery patterns
   - Coverage options
   - Output formatting

6. **[tests/README_TESTS.md](tests/README_TESTS.md)** (280+ lines)
   - Comprehensive test documentation
   - Quick start guide
   - Test categories and examples
   - Performance benchmarks
   - Troubleshooting guide
   - Guidelines for adding new tests

7. **[run_smoke_tests.py](run_smoke_tests.py)** (140+ lines)
   - Convenient CLI test runner
   - Commands for running specific test suites
   - Coverage report generation
   - Fast test mode (unit tests only)

8. **[tests/__init__.py](tests/__init__.py)** & **[tests/test_insights_workflow/__init__.py](tests/test_insights_workflow/__init__.py)**
   - Package initialization files

## Test Coverage

### Orchestrator Tests (50+ test cases)
- ✅ Agent factory and initialization
- ✅ Crew creation for multiple contexts
- ✅ Task orchestration and delegation
- ✅ Domain-neutral analysis crew
- ✅ Error validation and recovery
- ✅ Performance benchmarks

### Service Tests (40+ test cases)
- ✅ Project insight generation
- ✅ Account insight generation
- ✅ Private equity insight generation
- ✅ JSON transformation
- ✅ Complete workflow execution
- ✅ Database persistence
- ✅ Error handling and recovery

### Integration Tests (35+ test cases)
- ✅ End-to-end project workflows
- ✅ End-to-end account workflows
- ✅ End-to-end PE workflows
- ✅ Multi-entity parallel processing
- ✅ Service-orchestrator coordination
- ✅ Data consistency validation
- ✅ Error recovery patterns
- ✅ Performance benchmarks
- ✅ Response structure validation

## Quick Start

### Installation

```bash
# Install pytest and dependencies
pip install pytest pytest-mock pytest-asyncio

# Or sync with uv
uv sync
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Or use the convenience script
python run_smoke_tests.py all

# Run specific test suites
python run_smoke_tests.py orchestrator   # Orchestrator tests
python run_smoke_tests.py services       # Service layer tests
python run_smoke_tests.py integration    # Integration tests
python run_smoke_tests.py smoke          # Smoke tests only
python run_smoke_tests.py fast           # Fast tests (unit only)
python run_smoke_tests.py coverage       # With coverage report

# Run a specific test
pytest tests/test_insights_workflow/test_orchestrator.py::TestGeneralizedAgentsFactory::test_factory_initialization -v
```

## Test Statistics

| Category | Count | Status |
|----------|-------|--------|
| Orchestrator Tests | 50+ | ✅ Complete |
| Service Tests | 40+ | ✅ Complete |
| Integration Tests | 35+ | ✅ Complete |
| **Total Test Cases** | **125+** | ✅ Complete |
| Fixtures | 15+ | ✅ Complete |
| Documentation | Complete | ✅ Complete |

## Key Features

### Comprehensive Mocking
- S3 upload/download operations
- LLM (Azure OpenAI) responses
- Database sessions and ORM operations
- CrewAI crew and agent execution

### Multiple Entity Types Tested
- **Projects**: Individual project insight generation
- **Accounts**: Account portfolio analysis
- **Private Equity**: PE portfolio assessment

### Real-World Scenarios
- ✅ Invalid UUID handling
- ✅ Missing data graceful handling
- ✅ S3 connection failures
- ✅ LLM timeout scenarios
- ✅ Database connection errors
- ✅ Multi-entity processing
- ✅ Response time validation

### Performance Testing
- Agent creation: < 1 second
- Crew initialization: < 500 ms
- Complete workflow: < 30 seconds (with mocks)
- Multi-project processing: Scalability validated

## Project Structure

```
project-insighter-backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                       # Shared fixtures
│   ├── pytest.ini                        # Pytest configuration
│   ├── README_TESTS.md                   # Documentation
│   └── test_insights_workflow/
│       ├── __init__.py
│       ├── test_orchestrator.py          # Orchestrator tests
│       ├── test_services.py              # Service tests
│       └── test_integration.py           # Integration tests
├── run_smoke_tests.py                    # Test runner
├── backend/
│   └── insights_workflow/
│       ├── core/
│       │   ├── generalized_crew.py       # Crew implementation
│       │   └── context_aware_agents.py   # Agent factory
│       └── services/
│           ├── finance_insights_service.py
│           ├── finance_aggregation_service.py
│           └── json_transformer.py
```

## Next Steps

1. **Run Tests**: Execute `pytest tests/` or `python run_smoke_tests.py all`
2. **View Coverage**: Run `python run_smoke_tests.py coverage` for detailed coverage
3. **Add More Tests**: Follow guidelines in [tests/README_TESTS.md](tests/README_TESTS.md#adding-new-tests)
4. **CI/CD Integration**: Integrate test suite into your CI/CD pipeline

## CI/CD Integration Example

```bash
# GitHub Actions example
- name: Run Smoke Tests
  run: |
    pip install pytest pytest-mock pytest-asyncio
    pytest tests/ --cov=backend.insights_workflow --cov-report=xml
```

## Maintenance

- Review test coverage quarterly
- Update mocks when dependencies change
- Validate performance benchmarks periodically
- Add tests for new features
- Keep documentation in sync with code changes

## Support

For issues or questions:
1. Check [tests/README_TESTS.md](tests/README_TESTS.md) for documentation
2. Review example tests in the same category
3. Check conftest.py for available fixtures
4. Consult pytest documentation

---

**Created**: May 7, 2026
**Test Suite Version**: 1.0
**Status**: Complete and ready for use ✅
