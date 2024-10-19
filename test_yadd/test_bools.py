from yadd import yadd


def test_bools():
    expected = {"a": True}
    unit_under_test = {"a": False}
    assert not yadd(expected, unit_under_test, raise_exception_on_miscompare=False)
