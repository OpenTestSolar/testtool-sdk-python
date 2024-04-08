from typing import Dict

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    __test__ = False

    name: str = Field(alias="Name")
    attrs: Dict[str, str] = Field(alias="Attributes")
