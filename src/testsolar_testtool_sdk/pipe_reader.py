import struct
from typing import BinaryIO

from src.testsolar_testtool_sdk.model.load import LoadResult
from testsolar_testtool_sdk.model.testresult import TestResult
from testsolar_testtool_sdk.reporter import MAGIC_NUMBER


# 从管道读取加载结果，仅供单元测试使用
def read_load_result(pipe_io: BinaryIO) -> LoadResult:
    result_data = _read_model(pipe_io)

    re = LoadResult.model_validate_json(result_data)
    return re


# 从管道读取测试用例结果，仅供单元测试使用
def read_test_result(pipe_io: BinaryIO) -> TestResult:
    result_data = _read_model(pipe_io)
    re = TestResult.model_validate_json(result_data)
    return re


def _read_model(pipe_io: BinaryIO) -> str:
    magic_number = struct.unpack("<I", pipe_io.read(4))[0]
    assert (
            magic_number == MAGIC_NUMBER
    ), f"Magic number does not match ${MAGIC_NUMBER}"

    length = struct.unpack("<I", pipe_io.read(4))[0]

    result_data = pipe_io.read(length).decode("utf-8")
    return result_data
