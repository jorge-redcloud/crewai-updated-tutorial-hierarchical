from crewai.tools import BaseTool
from typing import Any
from pydantic import PrivateAttr
import pandas as pd

class SchemaTool(BaseTool):
    name: str = "SchemaInspector"
    description: str = "Inspects a Pandas DataFrame for column types, missing values, and schema structure."
    _df: pd.DataFrame = PrivateAttr()

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self._df = df

    def _run(self, *args, **kwargs) -> Any:
        schema = pd.DataFrame({
            "Column Name": self._df.columns,
            "Data Type": [self._df[col].dtype.name for col in self._df.columns],
            "Missing (%)": [round(self._df[col].isnull().mean() * 100, 2) for col in self._df.columns]
        })

        markdown = "### 🧾 Schema Summary\n\n"
        markdown += "| Column Name | Data Type | Missing (%) |\n"
        markdown += "|-------------|-----------|-------------|\n"
        for _, row in schema.iterrows():
            markdown += f"| {row['Column Name']} | {row['Data Type']} | {row['Missing (%)']}% |\n"

        categorical = schema[schema["Data Type"].isin(['object', 'category'])]["Column Name"].tolist()
        numerics = schema[schema["Data Type"].isin(['int64', 'float64'])]["Column Name"].tolist()

        observations = "\n\n### ⚠️ Schema Observations\n"
        observations += f"- 🎯 Categorical columns: `{', '.join(categorical)}`\n"
        observations += f"- 📏 Numeric columns: `{', '.join(numerics)}`\n"

        return markdown + observations
