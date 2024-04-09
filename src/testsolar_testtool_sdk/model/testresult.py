from enum import Enum
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from .test import TestCase


class ResultType(str, Enum):
    UNKNOWN = "UNKNOWN"
    SUCCEED = "SUCCEED"
    FAILED = "FAILED"
    LOAD_FAILED = "LOAD_FAILED"
    IGNORED = "IGNORED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"


class LogLevel(str, Enum):
    TRACE = "VERBOSE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARNNING"
    ERROR = "ERROR"


class AttachmentType(str, Enum):
    FILE = "FILE"
    URL = "URL"
    IFRAME = "IFRAME"


class TestCaseAssertError(BaseModel):
    __test__ = False

    expect: str = Field(alias="Expect")
    actual: str = Field(alias="Actual")
    message: str = Field(alias="Message")


class TestCaseRuntimeError(BaseModel):
    __test__ = False

    summary: str = Field(alias="Summary")
    detail: str = Field(alias="Detail")


class Attachment(BaseModel):
    name: str = Field(alias="Name")
    url: str = Field(alias="Url")
    type: AttachmentType = Field(alias="AttachmentType")


class TestCaseLog(BaseModel):
    __test__ = False

    time: datetime = Field(alias="Time")
    level: LogLevel = Field(alias="Level")
    content: str = Field(alias="Content")
    attachments: List[Attachment] = Field(alias="Attachments")
    assert_error: TestCaseAssertError = Field(alias="AssertError")
    runtime_error: Optional[TestCaseRuntimeError] = Field(None, alias="RuntimeError")

    class Config:
        json_encoders = {
            datetime: lambda dt: _format_datetime(dt),
        }


class TestCaseStep(BaseModel):
    __test__ = False

    start_time: datetime = Field(alias="StartTime")
    end_time: Optional[datetime] = Field(alias="EndTime")
    title: str = Field(alias="Title")
    logs: List[TestCaseLog] = Field(alias="Logs")

    class Config:
        json_encoders = {
            datetime: lambda dt: _format_datetime(dt),
        }


def _format_datetime(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


class TestResult(BaseModel):
    __test__ = False

    test: TestCase = Field(alias="Test")
    start_time: datetime = Field(alias="StartTime")
    end_time: Optional[datetime] = Field(alias="EndTime")
    result_type: ResultType = Field(alias="ResultType")
    message: str = Field(alias="Message")
    steps: List[TestCaseStep] = Field(alias="Steps")

    class Config:
        json_encoders = {
            datetime: lambda dt: _format_datetime(dt),
        }
