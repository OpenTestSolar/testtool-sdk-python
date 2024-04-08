from typing import Dict, List

from pydantic import BaseModel, Field


class EntryParam(BaseModel):
    context: Dict[str, str] = Field(alias="Context")
    task_id: str = Field(alias="TaskId")
    project_path: str = Field(alias="ProjectPath")
    test_selectors: List[str] = Field(alias="TestSelectors")
    collectors: List[str] = Field(alias="Collectors")
    fileReportPath: str = Field(alias="FileReportPath")
