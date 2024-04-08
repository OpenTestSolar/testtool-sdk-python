from typing import List

from pydantic import BaseModel, Field

from .test import TestCase


class LoadError(BaseModel):
    name: str
    message: str


class LoadResult(BaseModel):
    tests: List[TestCase] = Field(alias="Tests")
    load_errors: List[LoadError] = Field(alias="LoadErrors")
