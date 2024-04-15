from typing import Dict, List

from dataclasses import dataclass, field


@dataclass
class EntryParam:
    TaskId: str
    ProjectPath: str
    FileReportPath: str
    Collectors: List[str] = field(default_factory=list)
    Context: Dict[str, str] = field(default_factory=dict)
    TestSelectors: List[str] = field(default_factory=list)
