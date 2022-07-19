from yadd import Yadd


def test_bad_input():
    x = {"a": 1, "b": 2}
    y = {"a": 1, "c": 3}

    compare_result = Yadd(x, y, miscompare_callback=print, raise_exception_on_miscompare=False)
    assert not compare_result.match()
