from yadd import yadd


def test_yadd():
    x = {"a": 1}
    y = {"a": 2}
    yadd(x, y, "test", miscompare_callback=print, raise_exception_on_miscompare=False)

    yadd(
        "hi",
        "hello",
        "test",
        miscompare_callback=print,
        raise_exception_on_miscompare=False,
    )

    yadd(1, 2, "test", miscompare_callback=print, raise_exception_on_miscompare=False)

    yadd(1 + 1j, 0.999 + 0.999j, rel_tol=0.01)  # complex
