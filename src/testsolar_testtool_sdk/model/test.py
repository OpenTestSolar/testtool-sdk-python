from typing import Dict, List, Union

from dataclasses import dataclass, field


@dataclass
class TestCase:
    __test__ = False

    Name: str
    Attributes: Dict[str, Union[str, List[str]]] = field(default_factory=dict)
