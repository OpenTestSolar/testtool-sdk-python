from typing import List

from .test import TestCase

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LoadError:
    name: str
    message: str


@dataclass
class LoadResult:
    Tests: List[TestCase] = field(default_factory=list)
    LoadErrors: List[LoadError] = field(default_factory=list)
