from yadd import yadd


def my_yadd(expected: float | int, under_test: float | int) -> bool:
    return yadd(expected, under_test, rel_tol=1e-3, abs_tol=1e-9, expect_dict_key_ordered=True)


def test_customization():
    assert my_yadd(1.0, 1.0000001)
    assert my_yadd(2, 1.99999999)
