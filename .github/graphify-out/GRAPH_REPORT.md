# Graph Report - .  (2026-05-06)

## Corpus Check
- Corpus is ~49,006 words - fits in a single context window. You may not need a graph.

## Summary
- 917 nodes · 2464 edges · 42 communities detected
- Extraction: 42% EXTRACTED · 58% INFERRED · 0% AMBIGUOUS · INFERRED: 1441 edges (avg confidence: 0.6)
- Token cost: 2,847 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Utilities & Core|Utilities & Core]]
- [[_COMMUNITY_Finance Services|Finance Services]]
- [[_COMMUNITY_Sales Services|Sales Services]]
- [[_COMMUNITY_Document Processing|Document Processing]]
- [[_COMMUNITY_Data Access Layer|Data Access Layer]]
- [[_COMMUNITY_Web Framework|Web Framework]]
- [[_COMMUNITY_API Endpoints|API Endpoints]]
- [[_COMMUNITY_Schema Validation|Schema Validation]]
- [[_COMMUNITY_AI Engine|AI Engine]]
- [[_COMMUNITY_Storage & Cloud|Storage & Cloud]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]

## God Nodes (most connected - your core abstractions)
1. `Logger` - 227 edges
2. `Account` - 61 edges
3. `Project` - 61 edges
4. `RevenueMaster` - 50 edges
5. `PrivateEquity` - 40 edges
6. `ProjectDocument` - 37 edges
7. `LlamaCloudDocumentParser` - 31 edges
8. `ProjectSummary` - 31 edges
9. `DeliveryUnit` - 30 edges
10. `DeliveryUnitOut` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Account Dashboard model for storing account information.` --uses--> `Base`  [INFERRED]
  backend\sales\app\models\account_dashboard.py → backend\db\base.py
- `Extract all tables from lines, avoiding duplicates.` --uses--> `Logger`  [INFERRED]
  backend\doc_insighter\core\llama_parsing.py → backend\doc_insighter\tools\app_logger.py
- `Extract a single complete table and mark lines as processed.` --uses--> `Logger`  [INFERRED]
  backend\doc_insighter\core\llama_parsing.py → backend\doc_insighter\tools\app_logger.py
- `Extract all text content from parsed document in reading order.` --uses--> `Logger`  [INFERRED]
  backend\doc_insighter\core\llama_parsing.py → backend\doc_insighter\tools\app_logger.py
- `Read any file type with automatic handling and optional chunking` --uses--> `Logger`  [INFERRED]
  backend\doc_insighter\tools\file_reader_tool.py → backend\doc_insighter\tools\app_logger.py

## Hyperedges (group relationships)
- **Document Processing Pipeline** — readme_DocumentUploadWorkflow, readme_DocumentProcessor, readme_DocInsighterModule, readme_S3Bucket [INFERRED]
- **AI-Powered Analysis Stack** — readme_AzureOpenAI, readme_CrewAI, readme_LlamaParse, readme_DocInsighterModule [INFERRED]
- **Shared Data & Services** — readme_FinanceModule, readme_SalesModule, readme_DocInsighterModule, readme_PostgreSQL [INFERRED]

## Communities

### Community 0 - "Utilities & Core"
Cohesion: 0.03
Nodes (124): create_account(), create_new_account(), create_account(), delete_account(), read_account(), read_accounts(), delete(), get_by_id() (+116 more)

### Community 1 - "Finance Services"
Cohesion: 0.06
Nodes (106): Account, AccountMetricsMV, AccountRevenueSummary, Update an account and trigger materialized view refresh., Delete an account and all related data, then refresh materialized view., Retrieve accounts with various filters using materialized view., Get total count of accounts, optionally filtered by revenue status., Get top N accounts by revenue using materialized view. (+98 more)

### Community 2 - "Sales Services"
Cohesion: 0.04
Nodes (72): AccountBase, AccountCreate, AccountCreateResponse, AccountOut, AccountUpdate, Config, delete_account_route(), DeliveryUnitOut (+64 more)

### Community 3 - "Document Processing"
Cohesion: 0.05
Nodes (38): Base, CalendarEventBase, CalendarEventCreate, CalendarEventResponse, CalendarEvents, CalendarEventUpdate, get_my_calendar(), Get all calendar events (Tasks, Milestones, Reminders) for the System User. (+30 more)

### Community 4 - "Data Access Layer"
Cohesion: 0.07
Nodes (38): Log debug message with caller info, get_account_document(), get_project_document(), process_best_practices_document(), Retrieve document by account and type, Process Best Practices document, Process Best Practices document, get_account_document() (+30 more)

### Community 5 - "Web Framework"
Cohesion: 0.08
Nodes (49): AccountDashboard, AccountDashboardBase, AccountDashboardCreate, AccountDashboardResponse, AccountDashboardUpdate, Account Dashboard model for storing account information., Create a new account dashboard entry., Fields from the Stakeholder tab that the frontend now sends together. (+41 more)

### Community 6 - "API Endpoints"
Cohesion: 0.06
Nodes (39): GeneralizedAgents, Generalized Agentic Flow for S3-Staged Insights Analysis  A flexible, reusable, Summarizer Agent: Creates final, actionable insights with context-specific forma, Factory for creating generalized researcher, analyzer, and summarizer agents., Researcher Agent: Reads S3-staged JSON and prepares clean context., Analyzer Agent: Performs deep analysis on data retrieved from S3., DataPipeline, fetch_and_upload() (+31 more)

### Community 7 - "Schema Validation"
Cohesion: 0.06
Nodes (17): BaseTool, ProjectScopeCrew, CrewAI implementation for SOW/WSR Analysis.     Generates detailed Circle analy, get_insight_service(), InsightService, Locates SOW and WSR files in the project directory based on filename keywords, Scans the directory for files containing 'sow' and 'wsr' (case-insensitive)., Analyzes the *already uploaded* SOW and WSR documents.     Returns JSON decidin (+9 more)

### Community 8 - "AI Engine"
Cohesion: 0.08
Nodes (18): DataExtractor, DataExtractor_1, PDFToMarkdown, PDFToMarkdown_1, Create the document analyzer agent, Create the extraction task, Extract data from input file or text based on user requirements, ResponseModel (+10 more)

### Community 9 - "Storage & Cloud"
Cohesion: 0.08
Nodes (31): AWS API Gateway, AWS Lambda, Azure OpenAI (GPT-4o), Circle/Team Allocation Insights, CloudFront, CrewAI, Shared PostgreSQL Schema, Doc Insighter (Shared AI Engine) (+23 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (25): Config, create_pe(), create_private_equity(), delete_pe(), delete_private_equity(), get_pe(), get_pes(), get_private_equities() (+17 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (22): get_account(), get_account_count(), get_accounts(), get_accounts_with_filters(), get_top_revenue_accounts(), update_account(), Convert value to float, handling NaN, None, and empty strings., safe_float() (+14 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (21): delete_file(), download_project_file(), FileInfo, list_category_files(), Download a specific file from the project folder via S3 presigned URL., Download a specific file from the project folder via S3 presigned URL., Returns a list of files for a specific project and category.          - **proj, Returns a list of files for a specific project and category.          - **proj (+13 more)

### Community 13 - "Community 13"
Cohesion: 0.23
Nodes (6): _count_tokens(), _extract_json(), InsightsPipeline, Insights Pipeline --------─ Entry point: InsightsPipeline.run(data, instructions, Pull the first valid JSON object out of any LLM response., Serialise data to string.         If over threshold — compress data only with a

### Community 14 - "Community 14"
Cohesion: 0.23
Nodes (7): ABC, AbstractDocScanner, ProjectFileScanner, A shared helper method to format dates, sizes, and URLs.         This makes the, Specific implementation that filters for Excel and CSV files., get_pmo_files(), get_revenue_files()

### Community 15 - "Community 15"
Cohesion: 0.25
Nodes (6): get_delivery_unit(), get_delivery_units(), Retrieve a single delivery unit by ID., Retrieve a list of all delivery units., Retrieve a list of delivery units., read_delivery_units()

### Community 16 - "Community 16"
Cohesion: 0.47
Nodes (4): _generate_processing_hints(), generate_s3_filename(), JSON Transformer for Finance Insights  Converts raw database objects and aggre, transform_data_for_s3()

### Community 17 - "Community 17"
Cohesion: 0.4
Nodes (4): import_and_save_file(), file import handler that saves files and processes them.          Args:, import_project(), import_revenue()

### Community 18 - "Community 18"
Cohesion: 0.4
Nodes (3): BaseSettings, Config, Settings

### Community 19 - "Community 19"
Cohesion: 0.67
Nodes (3): convert_to_markdown(), json_to_md_main(), Converts JSON data (list of parsed document dicts) to a single Markdown string.

### Community 20 - "Community 20"
Cohesion: 0.67
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 0.67
Nodes (2): get_current_user_id(), Returns the hardcoded System User ID.     Used for Approach A (Shared Calendar)

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (2): Run synchronous DB code in a worker thread., run_in_threadpool()

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (2): create_sample_data_task(), run_crew()

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): PromptsTemplates

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Abstract method that must be implemented by child classes.

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (0): 

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (0): 

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **61 isolated node(s):** `Insights Pipeline --------─ Entry point: InsightsPipeline.run(data, instructions`, `Pull the first valid JSON object out of any LLM response.`, `Serialise data to string.         If over threshold — compress data only with a`, `PromptsTemplates`, `Config` (+56 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 24`** (2 nodes): `main.py`, `read_root()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (2 nodes): `prompts.py`, `PromptsTemplates`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Abstract method that must be implemented by child classes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `extract_ast.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Logger` connect `Finance Services` to `Utilities & Core`, `Sales Services`, `Document Processing`, `Data Access Layer`, `Web Framework`, `API Endpoints`, `Schema Validation`, `AI Engine`, `Community 10`, `Community 16`?**
  _High betweenness centrality (0.393) - this node is a cross-community bridge._
- **Why does `ProjectSummary` connect `Finance Services` to `Utilities & Core`, `Sales Services`, `Community 11`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `LlamaCloudDocumentParser` connect `Schema Validation` to `Utilities & Core`, `Finance Services`, `Data Access Layer`, `AI Engine`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 216 inferred relationships involving `Logger` (e.g. with `ResponseModel` and `PDFToMarkdown_1`) actually correct?**
  _`Logger` has 216 INFERRED edges - model-reasoned connections that need verification._
- **Are the 84 inferred relationships involving `str` (e.g. with `.run()` and `.read_data()`) actually correct?**
  _`str` has 84 INFERRED edges - model-reasoned connections that need verification._
- **Are the 59 inferred relationships involving `Account` (e.g. with `Base` and `PrivateEquity`) actually correct?**
  _`Account` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Are the 59 inferred relationships involving `Project` (e.g. with `Base` and `Update an account and trigger materialized view refresh.`) actually correct?**
  _`Project` has 59 INFERRED edges - model-reasoned connections that need verification._