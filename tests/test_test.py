from testsolar_testtool_sdk.model.test import TestCase


def test_test_case_duplicate():
    case1 = TestCase(Name="aa", Attributes={})

    case2 = TestCase(Name="aa", Attributes={"A": "B"})

    case3 = TestCase(Name="bb", Attributes={"A": "B"})

    assert case1 == case2
    assert case1 != case3

    data = [case1, case2]

    uniq_data = list(set(data))

    assert len(uniq_data) == 1
