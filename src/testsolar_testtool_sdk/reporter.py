import dataclasses
import json
import logging
import os
import struct
from typing import Optional, BinaryIO, Any, Dict

import portalocker

from .model.encoder import DateTimeEncoder
from .model.load import LoadResult
from .model.testresult import TestResult

# 跟TestSolar uniSDK约定的管道上报魔数，避免乱序导致后续数据全部无法上报
MAGIC_NUMBER = 0x1234ABCD

# 跟TestSolar uniSDK约定的管道上报文件描述符号
PIPE_WRITER = 3

class Reporter:
    def __enter__(self) -> 'Reporter':
        return self

    def __init__(self, pipe_io: Optional[BinaryIO] = None) -> None:
        """
        初始化报告工具类
        :param pipe_io: 可选的管道，用于测试
        """
        self.lock_file = "/tmp/testsolar_reporter.lock"

        if pipe_io:
            self.pipe_io = pipe_io
        else:
            self.pipe_io = os.fdopen(PIPE_WRITER, "wb")

        print(f"====!!!! Reporter initialized with pipe_io: {self.pipe_io}")

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def report_load_result(self, load_result: LoadResult) -> None:
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(dataclasses.asdict(load_result))

    def report_case_result(self, case_result: TestResult) -> None:
        with portalocker.Lock(self.lock_file, timeout=60):
            self._send_json(dataclasses.asdict(case_result))

    def close(self) -> None:
        if self.pipe_io:
            print("======Closing pipe_io=====")
            self.pipe_io.close()
            self.pipe_io = None

    def _send_json(self, result: Dict[Any, Any]) -> None:
        data = json.dumps(result, cls=DateTimeEncoder).encode("utf-8")
        length = len(data)

        # 将魔数写入管道
        self.pipe_io.write(struct.pack("<I", MAGIC_NUMBER))

        # 将 JSON 数据的长度写入管道
        self.pipe_io.write(struct.pack("<I", length))

        # 将 JSON 数据本身写入管道
        self.pipe_io.write(data)

        print(f"====!!!! Sending {length} bytes to pipe {PIPE_WRITER}")

        self.pipe_io.flush()