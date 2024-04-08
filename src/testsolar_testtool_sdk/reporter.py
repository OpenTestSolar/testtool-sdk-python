import hashlib
import os
import struct
from enum import Enum
from typing import Optional, BinaryIO

import portalocker
from loguru import logger
from pydantic import BaseModel

from .model.load import LoadResult
from .model.testresult import TestResult

# 跟TestSolar uniSDK约定的管道上报魔数，避免乱序导致后续数据全部无法上报
MAGIC_NUMBER = 0x1234ABCD

# 跟TestSolar uniSDK约定的管道上报文件描述符号
PIPE_WRITER = 3


class ReportType(str, Enum):
    Pipeline = 'pipeline'
    File = 'file'


class Reporter:
    def __init__(self, reporter_type: ReportType, pipe_io: Optional[BinaryIO] = None, report_path: str = '') -> None:
        """
        初始化报告工具类
        :param reporter_type: 报告类型，支持管道类型和文件类型
        :param pipe_io: 可选的管道，用于测试
        :param report_path: 上报文件路径
        """
        self.lock_file = "/tmp/testsolar_reporter.lock"
        self.reporter_type = reporter_type
        if reporter_type == ReportType.Pipeline:
            if pipe_io:
                self.pipe_io = pipe_io
            else:
                self.pipe_io = os.fdopen(PIPE_WRITER, "wb")
        elif reporter_type == ReportType.File:
            if not report_path:
                raise RuntimeError('report_path is required')
            self.report_path = report_path

    def report_load_result(self, load_result: LoadResult) -> None:
        if self.reporter_type == ReportType.Pipeline:
            with portalocker.Lock(self.lock_file, timeout=60):
                self._send_json(load_result)
        elif self.reporter_type == ReportType.File:
            self._write_load_file(load_result)

    def report_run_case_result(self, run_case_result: TestResult) -> None:
        if self.reporter_type == ReportType.Pipeline:
            with portalocker.Lock(self.lock_file, timeout=60):
                self._send_json(run_case_result)
        elif self.reporter_type == ReportType.File:
            self._write_case_result(run_case_result)

    def close(self) -> None:
        if self.pipe_io:
            self.pipe_io.close()

    def _send_json(self, result: BaseModel) -> None:
        data = result.model_dump_json(by_alias=True).encode("utf-8")
        length = len(data)

        # 将魔数写入管道
        self.pipe_io.write(struct.pack("<I", MAGIC_NUMBER))

        # 将 JSON 数据的长度写入管道
        self.pipe_io.write(struct.pack("<I", length))

        # 将 JSON 数据本身写入管道
        self.pipe_io.write(data)

        logger.debug(f"Sending {length} bytes to pipe {PIPE_WRITER}")

        self.pipe_io.flush()

    def _write_load_file(self, load_result: LoadResult) -> None:
        with open(os.path.join(self.report_path, 'result.json'), "wb") as f:
            logger.debug(f"Writing load results to {self.report_path}")
            f.write(load_result.model_dump_json(by_alias=True, indent=2).encode('utf-8'))

    def _write_case_result(self, case_result: TestResult) -> None:
        retry_id = case_result.test.attrs.get('retry', '0')
        filename = hashlib.md5(f"{case_result.test.name}.{retry_id}".encode('utf-8')).hexdigest() + ".json"
        with open(os.path.join(self.report_path, filename), "wb") as f:
            logger.debug(f"Writing case results to {self.report_path}")
            f.write(case_result.model_dump_json(by_alias=True, indent=2).encode('utf-8'))
