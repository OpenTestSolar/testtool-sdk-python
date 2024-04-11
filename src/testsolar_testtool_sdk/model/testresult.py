from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

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


@dataclass(frozen=True)
class TestCaseAssertError:
    __test__ = False

    Expect: str
    Actual: str
    Message: str


@dataclass(frozen=True)
class TestCaseRuntimeError:
    __test__ = False

    Summary: str
    Detail: str


@dataclass(frozen=True)
class Attachment:
    Name: str
    Url: str
    AttachmentType: AttachmentType


@dataclass
class TestCaseLog:
    __test__ = False

    Time: datetime
    Level: LogLevel
    Content: str
    AssertError: Optional[TestCaseAssertError] = None
    RuntimeError: Optional[TestCaseRuntimeError] = None
    Attachments: List[Attachment] = field(default_factory=list)


@dataclass
class TestCaseStep:
    __test__ = False

    StartTime: datetime
    Title: str
    ResultType: ResultType
    EndTime: Optional[datetime] = None
    Logs: List[TestCaseLog] = field(default_factory=list)


@dataclass
class TestResult:
    __test__ = False

    Test: TestCase
    StartTime: datetime
    ResultType: ResultType
    Message: str
    EndTime: Optional[datetime] = None
    Steps: List[TestCaseStep] = field(default_factory=list)

    def is_final(self) -> bool:
        return self.ResultType in [
            ResultType.SUCCEED,
            ResultType.FAILED,
            ResultType.IGNORED,
            ResultType.LOAD_FAILED,
            ResultType.UNKNOWN,
        ]
