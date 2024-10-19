import math

from yadd import Yadd


def test_pass_rate():
    x = {"a": 1, "b": 2, "c": 1.1}
    y = {"a": 1, "b": 3, "c": 0.9}

    compare_result = Yadd(x, y, miscompare_callback=print, raise_exception_on_miscompare=False)

    pass_flag = compare_result.match()
    assert pass_flag is False

    pass_rate = compare_result.pass_rate()
    print(f"{compare_result.pass_rate()=}")
    assert math.isclose(pass_rate, 1.0 / 3.0)

    print("miscompares:")
    for k, v in compare_result.get_numeric_miscompares().items():
        print(f"{k} : {v}")
