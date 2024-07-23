import json
from pathlib import Path
from typing import Dict, Any

from .model.load import LoadResult, deserialize_load_result
from .model.test import TestCase
from .model.testresult import TestResult, deserialize_test_result
from .reporter import LOAD_RESULT_FILE_NAME, digest_file_name


# 从管道读取加载结果，仅供单元测试使用
def read_file_load_result(file_report_path: Path) -> LoadResult:
    result_path = file_report_path / LOAD_RESULT_FILE_NAME
    with result_path.open() as f:
        data_dict: Dict[str, Any] = json.loads(f.read())

        return deserialize_load_result(data_dict)


# 从管道读取测试用例结果，仅供单元测试使用
def read_file_test_result(report_path: Path, case: TestCase) -> TestResult:
    file_name = digest_file_name(case)
    result_path = report_path / file_name
    with result_path.open() as f:
        data_dict: Dict[str, Any] = json.loads(f.read())
        return deserialize_test_result(data_dict)
