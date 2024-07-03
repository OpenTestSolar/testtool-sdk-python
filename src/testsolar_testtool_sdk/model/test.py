from typing import Dict, Any

from dataclasses import dataclass, field


@dataclass()
class TestCase:
    __test__ = False

    Name: str
    Attributes: Dict[str, str] = field(default_factory=dict)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.Name == other.Name
        else:
            return False

    def __hash__(self) -> int:
        """
        Name相同认为是同一个用例
        """
        return hash(self.Name)
