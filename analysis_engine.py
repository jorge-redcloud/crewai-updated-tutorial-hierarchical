from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import DataAnalysisAgents
from tasks import DataAnalysisTasks
from tools.data_tool import DatasetTool
from tools.schema_tool import SchemaTool
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

def sample_data(data_dict: dict, max_rows: int = 10) -> dict:
    return {
        key: values[:max_rows] if isinstance(values, list) else values
        for key, values in data_dict.items()
    }

def analyze_data(data_context):
    agents = DataAnalysisAgents()
    tasks = DataAnalysisTasks()

    # SAMPLE the data before passing to the tool
    sampled_data = sample_data(data_context, max_rows=10)

    # Tool to inject data into tasks
    dataset_tool = DatasetTool(dataset=data_context)
    schema_tool = SchemaTool(df=pd.DataFrame(sampled_data))  # ✅ Use your new schema tool


    # LLM Configuration
    OpenAIGPT4 = ChatOpenAI(model="gpt-4o", temperature=0.5, verbose=True)

    # Agents
    manager = agents.manager_agent()
    schema_fetcher = agents.schema_fetcher_agent()
    schema_analyzer = agents.schema_analyzer_agent()
    data_analyzer = agents.data_analyzer_agent()

    # Tasks using tools instead of context
    fetch_schema = tasks.fetch_schema_task(schema_fetcher, schema_tool)  # ✅ Use new tool here
    analyze_schema = tasks.analyze_schema_task(schema_analyzer, dataset_tool)
    analyze_data = tasks.analyze_data_task(data_analyzer, dataset_tool)

    # Crew assembly
    crew = Crew(
        agents=[manager, schema_fetcher, schema_analyzer, data_analyzer],
        tasks=[fetch_schema, analyze_schema, analyze_data],
        process=Process.hierarchical,
        manager_llm=OpenAIGPT4,
        verbose=True
    )

    output = crew.kickoff()

    print("=== DEBUG CREW OUTPUT ===")
    import pprint
    pprint.pprint(output.__dict__)
    print("=========================")


  
    # Return both the final result and the full trace of agent interactions
    return {
        "result": output.result if hasattr(output, "result") else str(output),
        "raw_output": getattr(output, "raw_output", {})  # includes .steps[]
    }