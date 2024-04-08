from typing import Dict

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    name: str = Field(alias="Name")
    attrs: Dict[str, str] = Field(alias="Attributes")
