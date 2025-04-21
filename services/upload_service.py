import pandas as pd

def process_csv_upload(file) -> dict:
    try:
        df = pd.read_csv(file)
        # Analyze the schema: column names, data types, and missing percentages
        schema_info = pd.DataFrame({
         "Column Name": df.columns,
         "Data Type": [df[col].dtype for col in df.columns],
        "Missing (%)": [df[col].isnull().mean() * 100 for col in df.columns]
        })
        return schema_info # format suitable for analysis
    except Exception as e:
        return {"error": str(e)}