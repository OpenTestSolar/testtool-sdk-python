import json
import struct
from typing import BinaryIO, Dict, Any

from .model.load import LoadResult, deserialize_load_result
from .model.testresult import TestResult, deserialize_test_result
from .reporter import MAGIC_NUMBER


# 从管道读取加载结果，仅供单元测试使用
def read_load_result(pipe_io: BinaryIO) -> LoadResult:
    result_data = _read_model(pipe_io)

    data_dict: Dict[str, Any] = json.loads(result_data)

    return deserialize_load_result(data_dict)


# 从管道读取测试用例结果，仅供单元测试使用
def read_test_result(pipe_io: BinaryIO) -> TestResult:
    result_data = _read_model(pipe_io)

    data_dict: Dict[str, Any] = json.loads(result_data)
    return deserialize_test_result(data_dict)


def _read_model(pipe_io: BinaryIO) -> str:
    magic_number = struct.unpack("<I", pipe_io.read(4))[0]
    assert magic_number == MAGIC_NUMBER, f"Magic number does not match ${MAGIC_NUMBER}"

    length = struct.unpack("<I", pipe_io.read(4))[0]

    result_data = pipe_io.read(length).decode("utf-8")
    return result_data
