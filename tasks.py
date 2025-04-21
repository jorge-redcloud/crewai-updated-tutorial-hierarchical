from crewai import Task

class DataAnalysisTasks():
    def fetch_schema_task(self, agent, schema_tool):
        return Task(
            description=(
                "Your task is to **extract the schema** of the dataset provided using the `SchemaInspector` tool. "
                "Analyze the column names, data types, and any potential data issues such as nulls, inconsistent formatting, or unknown types.\n\n"
                "Return the result in structured JSON format and a concise markdown summary suitable for reporting. "
                "Ensure the schema is valid, clean, and ready for downstream analytics."
            ),
            agent=agent,
            tools=[schema_tool],
            async_execution=False,
            expected_output="""
            {
              "columns": [
                {"name": "user_id", "type": "int64"},
                {"name": "screen_time_minutes", "type": "float64"},
                {"name": "device_type", "type": "object"}
              ],
              "issues": [
                "Column 'screen_time_minutes' has 8% missing values",
                "Column 'device_type' has mixed string formats"
              ],
              "markdown": "Markdown table of schema (column | type | missing%)"
            }
            """
        )

    def analyze_schema_task(self, agent, dataset_tool):
        return Task(
            description=(
                "Review the dataset structure and **evaluate schema-level characteristics** such as sparsity, missing values, mixed types, and outlier-prone fields.\n\n"
                "Identify high-risk columns, poorly formatted types, or features that may impact analysis. Suggest pre-processing actions like type casting, imputation, or column removal if necessary.\n\n"
                "Make your observations precise, structured, and useful for a data engineering or data science team."
            ),
            agent=agent,
            tools=[dataset_tool],
            async_execution=False,
            expected_output="""
            {
              "summary": "Dataset has 12 columns. Columns 'X', 'Y', and 'Z' have over 50% missing values.",
              "recommendations": [
                "Consider dropping 'Z' due to excessive missing values",
                "Impute missing values in 'Y' using median",
                "Convert 'X' to categorical"
              ]
            }
            """
        )

    def analyze_data_task(self, agent, dataset_tool):
        return Task(
            description=(
                "Perform **descriptive and exploratory data analysis (EDA)** on the dataset. "
                "Look for trends, correlations, distributions, and anomalies. Focus on uncovering **business-relevant insights** "
                "such as patterns in user behavior, operational inefficiencies, or data relationships worth deeper modeling.\n\n"
                "Summarize insights in plain language (bullet points) and provide optional recommendations."
            ),
            agent=agent,
            tools=[dataset_tool],
            async_execution=True,
            expected_output="""
            {
              "insights": [
                "Users aged 18-24 spend the most screen time on average.",
                "Tablet users have the highest engagement time.",
                "There is a positive correlation between session count and total time spent."
              ],
              "recommendations": [
                "Target high screen-time users with upsell offers.",
                "Investigate outliers in screen time over 1200 minutes."
              ]
            }
            """
        )
