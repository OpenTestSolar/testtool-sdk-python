from dataclasses import dataclass, field
from typing import List, Dict, Any

from dacite import from_dict

from .test import TestCase


@dataclass(frozen=True)
class LoadError:
    name: str
    message: str


@dataclass
class LoadResult:
    Tests: List[TestCase] = field(default_factory=list)
    LoadErrors: List[LoadError] = field(default_factory=list)

    def merge(self, data: "LoadResult") -> None:
        self.Tests.extend(data.Tests)
        self.LoadErrors.extend(data.LoadErrors)


def deserialize_load_result(data_dict: Dict[str, Any]) -> LoadResult:
    re: LoadResult = from_dict(data_class=LoadResult, data=data_dict)
    return re
