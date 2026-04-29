"""
Data Pipeline Utility: DB → S3 → Agents

This module demonstrates the complete workflow for:
1. Fetching data from the database
2. Uploading to S3 with entity-aware naming
3. Passing S3 key to agents
4. Agents downloading and processing the data

File Naming Convention:
- Account data: temp/account_<account_id>_<YYYYMMDD_HHMMSS>.json
- Project data: temp/project_<project_id>_<YYYYMMDD_HHMMSS>.json

This makes it clear what type of entity the file contains.
"""

from uuid import UUID
from backend.insights_workflow.tools.db_tools import DataFetcher
from backend.insights_workflow.tools.s3_data_reader_tool import S3DataReaderTool
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()


class DataPipeline:
    """Orchestrates the complete data pipeline from DB to S3 to Agents."""
    
    @staticmethod
    def fetch_and_upload(entity_id: UUID, entity_type: str) -> dict:
        """
        Step 1: Fetch data from DB and upload to S3.
        
        Args:
            entity_id: UUID of account or project
            entity_type: 'account' or 'project'
        
        Returns:
            {
                "s3_key": "temp/account_<id>_<date>.json",
                "entity_id": "<id>",
                "entity_type": "account",
                "bucket": "nit-project-insighter",
                "status": "success"
            }
        
        Example:
            result = DataPipeline.fetch_and_upload(
                entity_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
                entity_type="account"
            )
            s3_key = result["s3_key"]  # Use this in agents
        """
        log.log_info(f"Step 1: Fetching and uploading {entity_type} data...")
        return DataFetcher.fetch_and_upload_data_to_s3(entity_id, entity_type)
    
    @staticmethod
    def get_agent_s3_key(entity_id: UUID, entity_type: str) -> str:
        """
        Convenience method to get just the S3 key for passing to agents.
        
        Args:
            entity_id: UUID of account or project
            entity_type: 'account' or 'project'
        
        Returns:
            S3 key string (e.g., "temp/account_550e8400_20260415_152033.json")
        
        Example:
            s3_key = DataPipeline.get_agent_s3_key(entity_id, "account")
            # Pass to agent tool: s3_data_reader.run(s3_key=s3_key)
        """
        result = DataPipeline.fetch_and_upload(entity_id, entity_type)
        if result.get("status") == "success":
            return result["s3_key"]
        else:
            raise Exception(f"Failed to upload data: {result.get('error')}")


# ============================================================================
# AGENT USAGE EXAMPLES
# ============================================================================

"""
Example 1: In a CrewAI Agent
-------------------------------

from crewai import Agent, Task, Crew
from backend.doc_insighter.tools.s3_data_reader_tool import S3DataReaderTool
from backend.doc_insighter.tools.db_tools import DataFetcher
from uuid import UUID

# Step 1: Get the S3 key by fetching and uploading data
entity_id = UUID("550e8400-e29b-41d4-a716-446655440000")
result = DataFetcher.fetch_and_upload_data_to_s3(entity_id, "account")
s3_key = result["s3_key"]

# Step 2: Create agent with S3 reader tool
s3_reader = S3DataReaderTool()

agent = Agent(
    role="Financial Analyst",
    goal="Analyze uploaded account data",
    backstory="You are an expert financial analyst",
    tools=[s3_reader],  # Agent can now use S3DataReaderTool
    verbose=True
)

task = Task(
    description=f"Read and analyze the account data from S3 key: {s3_key}",
    agent=agent,
    expected_output="Analysis results"
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)


Example 2: Direct Agent Tool Usage
-----------------------------------

from crewai.tools import BaseTool
from backend.doc_insighter.tools.s3_data_reader_tool import S3DataReaderTool

# In your agent task
s3_reader = S3DataReaderTool()

# Option 1: Get data as dictionary
data_dict = s3_reader._run(
    s3_key="temp/account_550e8400_20260415_152033.json",
    return_as="dict"
)
print(f"Entity Type: {data_dict['_metadata']['entity_type']}")
print(f"Metrics: {data_dict['metrics']}")

# Option 2: Download to local file for processing
local_path = s3_reader._run(
    s3_key="temp/account_550e8400_20260415_152033.json",
    return_as="local_path"
)
# Now pass this path to file_reader_tool or other processors

# Option 3: Get as JSON string
json_str = s3_reader._run(
    s3_key="temp/account_550e8400_20260415_152033.json",
    return_as="json"
)


Example 3: Multi-step Pipeline
-------------------------------

from uuid import UUID
from backend.doc_insighter.tools.db_tools import DataFetcher

# Define your entities
entities = [
    {"id": UUID("550e8400-e29b-41d4-a716-446655440000"), "type": "account"},
    {"id": UUID("660e8400-e29b-41d4-a716-446655440001"), "type": "project"},
]

# Process each entity
s3_keys = []
for entity in entities:
    result = DataFetcher.fetch_and_upload_data_to_s3(
        entity_id=entity["id"],
        entity_type=entity["type"]
    )
    if result["status"] == "success":
        s3_keys.append(result["s3_key"])
        print(f"Uploaded {entity['type']} data to: {result['s3_key']}")

# Now pass these s3_keys to different agents for processing
for s3_key in s3_keys:
    # Each agent can independently download and process its assigned S3 key
    pass
"""
