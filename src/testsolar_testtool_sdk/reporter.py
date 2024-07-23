import dataclasses
import hashlib
import json
import logging
import os
import struct
from pathlib import Path
from typing import Optional, BinaryIO, Any, Dict
from abc import ABC, abstractmethod

import portalocker

from .model.encoder import DateTimeEncoder
from .model.load import LoadResult
from .model.testresult import TestResult
from .model.test import TestCase

# 跟TestSolar uniSDK约定的管道上报魔数，避免乱序导致后续数据全部无法上报
MAGIC_NUMBER = 0x1234ABCD

# 跟TestSolar uniSDK约定的管道上报文件描述符号
PIPE_WRITER = 3


class BaseReporter(ABC):
    @abstractmethod
    def report_load_result(self, load_result: LoadResult) -> None: ...

    @abstractmethod
    def report_case_result(self, case_result: TestResult) -> None: ...


class Reporter(BaseReporter):
    def __init__(self, pipe_io: Optional[BinaryIO] = None) -> None:
        """
        初始化报告工具类
        :param pipe_io: 可选的管道，用于测试
        """
        lock_path = Path.home().joinpath("testsolar_reporter.lock")
        self.lock_file: str = str(lock_path)

        if pipe_io:
            self.pipe_io = pipe_io
        else:
            self.pipe_io = os.fdopen(PIPE_WRITER, "wb")

    def report_load_result(self, load_result: LoadResult) -> None:
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(dataclasses.asdict(load_result))

    def report_case_result(self, case_result: TestResult) -> None:
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(dataclasses.asdict(case_result))

    def _send_json(self, result: Dict[Any, Any]) -> None:
        data = json.dumps(result, cls=DateTimeEncoder).encode("utf-8")
        length = len(data)

        # 将魔数写入管道
        self.pipe_io.write(struct.pack("<I", MAGIC_NUMBER))

        # 将 JSON 数据的长度写入管道
        self.pipe_io.write(struct.pack("<I", length))

        # 将 JSON 数据本身写入管道
        self.pipe_io.write(data)

        logging.debug(f"Sending {length} bytes to pipe {PIPE_WRITER}")

        self.pipe_io.flush()


PipeReporter = Reporter

LOAD_RESULT_FILE_NAME = "result.json"


class FileReporter(BaseReporter):
    def __init__(self, report_path: Path) -> None:
        self.report_path: Path = report_path

    def report_load_result(self, load_result: LoadResult) -> None:
        out_file = self.report_path.joinpath(LOAD_RESULT_FILE_NAME)
        logging.debug(f"Writing load results to {out_file}")
        with open(out_file, "wb") as f:
            data = json.dumps(
                dataclasses.asdict(load_result),
                indent=2,
                ensure_ascii=False,
                cls=DateTimeEncoder,
            ).encode("utf-8")
            f.write(data)

    def report_case_result(self, case_result: TestResult) -> None:
        retry_id = case_result.Test.Attributes.get("retry", "0")
        filename = digest_file_name(case_result.Test)
        out_file = self.report_path.joinpath(filename)

        logging.debug(
            f"Writing case [{case_result.Test.Name}.{retry_id}] results to {out_file}"
        )

        with open(out_file, "wb") as f:
            data = json.dumps(
                dataclasses.asdict(case_result),
                indent=2,
                ensure_ascii=False,
                cls=DateTimeEncoder,
            ).encode("utf-8")
            f.write(data)


def digest_file_name(case: TestCase) -> str:
    retry_id = case.Attributes.get("retry", "0")
    filename = (
        hashlib.md5(f"{case.Name}.{retry_id}".encode("utf-8")).hexdigest() + ".json"
    )
    return filename
