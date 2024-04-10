from typing import Dict

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TestCase:
    __test__ = False

    Name: str
    Attributes: Dict[str, str] = field(default_factory=dict)
