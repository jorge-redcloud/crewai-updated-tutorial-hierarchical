from crewai import Agent
from tools.schema_tool import SchemaTool

class DataAnalysisAgents():
    def manager_agent(self):
        return Agent(
            role='Lead Data Analyst Manager',
            goal='Direct the agents through structured data analysis, ensuring accurate schema recognition, proper diagnostics, and clear, actionable business insights.',
            backstory="""You're the senior analyst in charge of coordinating the end-to-end data analysis process. 
            Your job is to:
            - Assign responsibilities to other agents
            - Ensure data quality checks and schema diagnostics are done first
            - Oversee insight generation and validate that each finding is backed by statistics
            - Communicate findings clearly for a business audience
        
            You summarize the process clearly at the end.""",
            allow_delegation=True,
            verbose=True,
            max_iter=1
    )

    def schema_fetcher_agent(self):
        return Agent(
            role='Schema Validator',
            goal='Identify column names, infer data types, detect formatting issues, and confirm that the data is ready for analysis.',
            backstory="""You're an expert in data wrangling and schema extraction. Your responsibilities include:
            - Reading the dataset and identifying all columns
            - Inferring types (int, float, category, datetime, text)
            - Noting missing values, nulls, or corrupted entries
            - Flagging duplicate columns or rows

            Your output must include:
            - A Markdown table of column names, types, and missing percentages
            - A note on any issues or anomalies in schema""",
            allow_delegation=True,
            verbose=True,
    )

    def schema_analyzer_agent(self):
        return Agent(
            role='Schema Analyzer and Profiler',
            goal='Analyze the schema to extract column-level patterns, such as sparsity, skewness, and irregular data distributions.',
            backstory="""You are a statistical profiler who reads the schema and generates:
            - Notes on column distributions (are they skewed, uniform, normal?)
            - Histograms or summaries (like value counts for categories)
            - Identify columns with poor data quality (e.g., high cardinality or nulls)

            Provide:
            - A bullet list of schema-level observations
            - Suggested actions (e.g., drop, clean, impute, bucket, etc.)
            - Warnings if fields have unexpected data types""",
            allow_delegation=True,
            verbose=True,
    )


    def data_analyzer_agent(self):
        return Agent(
           role='Insight Generator',
           goal='Analyze data and generate human-readable, high-value insights and recommendations.',
           backstory="""You're an expert data scientist focused on deriving meaning from numbers.    
            You:
             - Analyze relationships between variables
             - Identify trends, correlations, and anomalies
             - Summarize findings for a business or product owner
             Your output must:
             - Use markdown
             - Include bullet point insights, trends, and anomalies
             - Suggest clear actionables, backed by observations
             - Use charts or summary stats (if available) to illustrate points""",
             allow_delegation=False,
             verbose=True,
        )
