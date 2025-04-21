from crewai.tools import BaseTool
from typing import Any
from pydantic import PrivateAttr

class DatasetTool(BaseTool):
    name: str = "DatasetTool"
    description: str = "Provides access to the structured dataset"

    _dataset: dict = PrivateAttr()

    def __init__(self, dataset: dict):
        super().__init__()
        self._dataset = dataset

    def _run(self, *args, **kwargs) -> Any:
        return self._dataset