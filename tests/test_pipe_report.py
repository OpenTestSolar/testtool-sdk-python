import concurrent.futures
import dataclasses
import io
import json
from functools import partial

from testsolar_testtool_sdk.model.encoder import DateTimeEncoder
from testsolar_testtool_sdk.model.load import (
    LoadResult,
    LoadError,
)
from testsolar_testtool_sdk.model.test import TestCase
from testsolar_testtool_sdk.model.testresult import (
    ResultType,
)
from testsolar_testtool_sdk.model.testresult import (
    TestResult,
)
from testsolar_testtool_sdk.pipe_reader import (
    read_load_result,
    read_test_result,
)
from testsolar_testtool_sdk.reporter import PipeReporter
from .prepare_data import (
    generate_demo_load_result,
    generate_test_result,
    send_test_result,
)


def test_report_load_result_with_pipe() -> None:
    # 创建一个Reporter实例
    pipe_io = io.BytesIO()
    reporter = PipeReporter(pipe_io=pipe_io)
    # 创建一个LoadResult实例
    load_result = generate_demo_load_result()

    # 调用report_load_result方法
    reporter.report_load_result(load_result)

    # 检查管道中的魔数
    pipe_io.seek(0)

    loaded = read_load_result(pipe_io)
    assert len(loaded.Tests) == len(load_result.Tests)
    assert len(loaded.LoadErrors) == len(load_result.LoadErrors)
    assert loaded.Tests[0] == load_result.Tests[0]
    assert loaded == load_result


def test_load_result_merge():
    load_data = generate_demo_load_result()
    load_data.merge(
        LoadResult(
            Tests=[TestCase(Name="hello.py?fast_input")],
            LoadErrors=[LoadError(name="a", message="b")],
        )
    )

    assert len(load_data.Tests) == 41
    assert len(load_data.LoadErrors) == 21


def test_datetime_formatted():
    run_case_result = generate_test_result(0)
    data = json.dumps(dataclasses.asdict(run_case_result), cls=DateTimeEncoder)
    tr = json.loads(data)
    assert tr["StartTime"].endswith("Z")
    assert tr["EndTime"].endswith("Z")

    assert tr["Steps"][0]["StartTime"].endswith("Z")
    assert tr["Steps"][0]["EndTime"].endswith("Z")

    assert tr["Steps"][0]["Logs"][0]["Time"].endswith("Z")


def test_report_run_case_result_with_pipe():
    # 创建一个Reporter实例
    pipe_io = io.BytesIO()
    reporter = PipeReporter(pipe_io=pipe_io)
    # 创建五个LoadResult实例并发调用report_run_case_result方法
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        send_action = partial(send_test_result, reporter)
        for i in range(5):
            executor.submit(send_action)

    # 检查管道中的数据，确保每个用例的魔数和数据长度还有数据正确
    pipe_io.seek(0)
    r1: TestResult = read_test_result(pipe_io)
    assert r1.ResultType == ResultType.SUCCEED
    r2 = read_test_result(pipe_io)
    assert r2.ResultType == ResultType.SUCCEED
    r3 = read_test_result(pipe_io)
    assert r3.ResultType == ResultType.SUCCEED
    r4 = read_test_result(pipe_io)
    assert r4.ResultType == ResultType.SUCCEED
    r5 = read_test_result(pipe_io)
    assert r5.ResultType == ResultType.SUCCEED
