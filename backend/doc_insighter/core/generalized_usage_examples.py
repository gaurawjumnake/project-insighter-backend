"""
Usage Examples for Generalized Agentic Flow

This module provides practical examples of how to use the generalized
researcher, analyzer, and summarizer agents for Sales and Finance analysis.

The generalized architecture allows the same agent structure to be reused
for different analytical tasks by simply configuring the context type.
"""

# ============================================================================
# EXAMPLE 1: SALES ACCOUNT ANALYSIS
# ============================================================================

def analyze_sales_account(account_id: str):
    """
    Analyze a sales account using the generalized agentic flow.
    
    This example shows how to integrate the three agents for
    comprehensive sales account analysis.
    
    Args:
        account_id: UUID of the account to analyze
    
    Returns:
        Structured sales insights with growth opportunities and risks
    """
    from backend.doc_insighter.core.generalized_crew import create_sales_analysis_crew
    
    # Create a sales analysis crew
    crew = create_sales_analysis_crew(account_id)
    
    # Execute the analysis workflow
    # Step 1: Researcher fetches data from account_dashboard and account_documents
    # Step 2: Analyzer performs sales-focused analysis
    # Step 3: Summarizer creates sales-specific insights
    insights = crew.analyze()
    
    # The insights will be formatted as:
    # - Key Account Findings
    # - Account Health Assessment
    # - Growth and Expansion Opportunities
    # - Risk and Relationship Assessment
    # - Recommended Actions for Account Growth
    # - Success Metrics and Timeline
    
    return insights


# ============================================================================
# EXAMPLE 2: FINANCE PROJECT ANALYSIS
# ============================================================================

def analyze_finance_project(project_id: str):
    """
    Analyze a finance project using the generalized agentic flow.
    
    This example shows how to reuse the same agent structure for
    comprehensive project financial analysis.
    
    Args:
        project_id: UUID of the project to analyze
    
    Returns:
        Structured financial insights with profitability and risks
    """
    from backend.doc_insighter.core.generalized_crew import create_finance_analysis_crew
    
    # Create a finance analysis crew
    crew = create_finance_analysis_crew(project_id)
    
    # Execute the analysis workflow
    # Step 1: Researcher fetches data from projects, project_documents, and revenue_master
    # Step 2: Analyzer performs finance-focused analysis
    # Step 3: Summarizer creates finance-specific insights
    insights = crew.analyze()
    
    # The insights will be formatted as:
    # - Key Financial Findings
    # - Profitability Analysis
    # - Revenue Optimization Opportunities
    # - Financial Risk Assessment
    # - Recommendations with Financial Impact
    # - Performance Timeline and KPIs
    
    return insights


# ============================================================================
# EXAMPLE 3: BATCH ANALYSIS OF MULTIPLE ENTITIES
# ============================================================================

def batch_analyze_sales_accounts(account_ids: list[str]):
    """
    Analyze multiple sales accounts in batch.
    
    This example shows how to apply the generalized workflow
    to multiple entities efficiently.
    
    Args:
        account_ids: List of account UUIDs to analyze
    
    Returns:
        Dictionary with analysis results for each account
    """
    from backend.doc_insighter.core.generalized_crew import create_sales_analysis_crew
    
    results = {}
    
    for account_id in account_ids:
        try:
            crew = create_sales_analysis_crew(account_id)
            insights = crew.analyze()
            results[account_id] = {
                "status": "success",
                "insights": insights
            }
        except Exception as e:
            results[account_id] = {
                "status": "error",
                "error": str(e)
            }
    
    return results


# ============================================================================
# EXAMPLE 4: CUSTOM CREW SETUP WITH DIFFERENT CONTEXT
# ============================================================================

def custom_analysis_with_specific_focus(entity_id: str, context_type: str):
    """
    Create a custom crew for specific analytical focus.
    
    This example shows how to create crews for different contexts
    beyond the standard sales/finance split.
    
    Args:
        entity_id: UUID of the entity to analyze
        context_type: 'sales' or 'finance'
    
    Returns:
        Analysis results formatted for the specified context
    """
    from backend.doc_insighter.core.generalized_crew import GeneralizedAnalysisCrew
    
    # Create crew with specific context
    crew = GeneralizedAnalysisCrew(
        context_type=context_type,
        entity_id=entity_id,
        entity_type=context_type  # The entity type matches context for simplicity
    )
    
    # Execute analysis
    insights = crew.analyze()
    
    return insights


# ============================================================================
# EXAMPLE 5: DIRECT AGENT USAGE (ADVANCED)
# ============================================================================

def use_agents_directly():
    """
    Use individual agents directly without the full crew workflow.
    
    This example shows how to use each agent independently
    for more granular control.
    """
    from backend.doc_insighter.core.context_aware_agents import GeneralizedAgents
    from crewai import Task
    
    agents_factory = GeneralizedAgents()
    
    # Get individual agents
    researcher = agents_factory.researcher_agent()
    analyzer = agents_factory.analyzer_agent()
    summarizer = agents_factory.summarizer_agent(context_type='sales')
    
    # You can now use these agents individually in custom workflows
    # or create specialized crew configurations for specific needs
    
    # Example: Using researcher agent in a custom task
    research_task = Task(
        description="Fetch data for account analysis",
        agent=researcher,
        expected_output="Structured data summary"
    )
    
    return {
        "researcher": researcher,
        "analyzer": analyzer,
        "summarizer": summarizer
    }


# ============================================================================
# EXAMPLE 6: API ENDPOINT INTEGRATION
# ============================================================================

async def api_analyze_account(account_id: str):
    """
    API endpoint for sales account analysis.
    
    This example shows how to integrate the analysis crew
    into an async API endpoint.
    
    Args:
        account_id: UUID of the account
    
    Returns:
        JSON response with analysis insights
    """
    from backend.doc_insighter.core.generalized_crew import create_sales_analysis_crew
    
    try:
        crew = create_sales_analysis_crew(account_id)
        insights = crew.analyze()
        
        return {
            "status": "success",
            "account_id": account_id,
            "analysis_type": "sales",
            "insights": insights
        }
    except Exception as e:
        return {
            "status": "error",
            "account_id": account_id,
            "error": str(e)
        }


async def api_analyze_project(project_id: str):
    """
    API endpoint for finance project analysis.
    
    This example shows how to integrate the analysis crew
    into an async API endpoint for project analysis.
    
    Args:
        project_id: UUID of the project
    
    Returns:
        JSON response with analysis insights
    """
    from backend.doc_insighter.core.generalized_crew import create_finance_analysis_crew
    
    try:
        crew = create_finance_analysis_crew(project_id)
        insights = crew.analyze()
        
        return {
            "status": "success",
            "project_id": project_id,
            "analysis_type": "finance",
            "insights": insights
        }
    except Exception as e:
        return {
            "status": "error",
            "project_id": project_id,
            "error": str(e)
        }


# ============================================================================
# EXAMPLE 7: SCHEDULED BATCH ANALYSIS
# ============================================================================

def schedule_daily_account_analysis():
    """
    Example of scheduling daily analysis for all active accounts.
    
    This would be integrated with a scheduler like APScheduler
    or a task queue like Celery.
    """
    from backend.doc_insighter.core.generalized_crew import create_sales_analysis_crew
    from backend.finance.app.models.account import Account
    from backend.db.session import SessionLocal
    
    db = SessionLocal()
    
    try:
        # Get all active accounts
        accounts = db.query(Account).filter(Account.active == True).all()
        
        results = {}
        for account in accounts:
            try:
                crew = create_sales_analysis_crew(str(account.id))
                insights = crew.analyze()
                results[str(account.id)] = {
                    "status": "success",
                    "account_name": account.name,
                    "insights": insights
                }
            except Exception as e:
                results[str(account.id)] = {
                    "status": "error",
                    "account_name": account.name,
                    "error": str(e)
                }
        
        return results
    finally:
        db.close()


if __name__ == "__main__":
    # Example usage
    print("Generalized Agentic Flow - Usage Examples")
    print("==========================================")
    print()
    print("This module contains example patterns for using the")
    print("generalized researcher, analyzer, and summarizer agents.")
    print()
    print("Key Features:")
    print("- Single architecture for multiple analysis types")
    print("- Flexible context-aware output formatting")
    print("- Easy integration with APIs and scheduled tasks")
    print("- Direct database access via Researcher agent")
    print()
    print("For detailed usage, see functions in this module.")
