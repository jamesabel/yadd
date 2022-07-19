from typing import Dict, Tuple, Callable, Iterable, List, DefaultDict
import cmath
from decimal import Decimal
from collections import defaultdict, Counter
from logging import getLogger

from yadd import application_name

log = getLogger(application_name)


class MiscompareException(Exception):
    ...


def are_comparable(a, b) -> bool:
    """
    determine if two object are comparable
    :param a: object a
    :param b: object b
    :return: True if the objects are comparable
    """
    comparable = False
    if type(a) == type(b):
        comparable = True
    elif isinstance(a, (float, int, Decimal, complex)) and isinstance(b, (float, int, Decimal, complex)):
        # various "numbers" are comparable between each other
        comparable = True
    return comparable


class Yadd:

    """
    Yet Another Dict Difference Alternative
    """

    def __init__(
        self,
        expected: Dict | Iterable | float | int | str | Decimal | complex | bool,
        under_test: Dict | Iterable | float | int | str | Decimal | complex | bool,
        description: str = None,
        rel_tol: float = 1e-9,
        abs_tol: float = 0.0,
        miscompare_callback: Callable = log.error,
        expect_dict_key_ordered: bool = False,
        raise_exception_on_miscompare: bool = True,
    ):

        """
        Yet Another Dict Difference Alternative

        :param expected: expected results
        :param under_test: unit under test
        :param description: description of test
        :param rel_tol: for floats, relative error tolerance (default is the same as math.isclose() rel_tol)
        :param abs_tol: for floats, absolute error tolerance (default is the same as math.isclose() abs_tol)
        :param miscompare_callback: function to call on a miscompare (usually a logger such as log.error)
        :param expect_dict_key_ordered: set to True to check if dicts keys have the same order
        :param raise_exception_on_miscompare: True to raise exception on a miscompare
        """

        # function takes description as a tuple
        if description is None:
            _description = tuple()  # type: Tuple
        else:
            _description = (description,)

        self._compare_results = []  # type: List[bool]
        self._numeric_miscompares = defaultdict(list)  # type: DefaultDict[float, List]
        self._match = yadd(
            expected, under_test, _description, rel_tol, abs_tol, miscompare_callback, expect_dict_key_ordered, raise_exception_on_miscompare, self._compare_results, self._numeric_miscompares
        )

    def match(self) -> bool:
        """
        Return True if expected matches under_test
        :return: True on match
        """
        return self._match

    def compare_results(self) -> List[bool]:
        """
        Get the compare results as a list of booleans
        :return: compare results list
        """
        return self._compare_results

    def numeric_miscompares(self) -> Dict[float, List]:
        """
        Get a sorted dict of lists with the key being the difference. Useful for debugging/displaying the largest differences first.
        :return: sorted dict of miscompares
        """
        return {k: self._numeric_miscompares[k] for k in sorted(self._numeric_miscompares.keys(), reverse=True)}

    def pass_rate(self) -> float:
        pass_counter = Counter(self._compare_results)
        pass_rate = float(pass_counter[True]) / float(pass_counter.total())
        return pass_rate


def yadd(
    expected: Dict | Iterable | float | int | str | Decimal | complex | bool,
    under_test: Dict | Iterable | float | int | str | Decimal | complex | bool,
    description: Tuple | str = tuple(),
    rel_tol: float = 1e-9,
    abs_tol: float = 0.0,
    miscompare_callback: Callable = log.error,
    expect_dict_key_ordered: bool = False,
    raise_exception_on_miscompare: bool = True,
    compare_results: List[bool] = None,
    numeric_miscompares: DefaultDict[float, List] = None,
) -> bool:
    """

    Yet Another Dict Difference Alternative

    :param expected: expected results
    :param under_test: unit under test
    :param description: tuple of descriptive strings, one per level
    :param rel_tol: for floats, relative error tolerance (default is the same as math.isclose() rel_tol)
    :param abs_tol: for floats, absolute error tolerance (default is the same as math.isclose() abs_tol)
    :param miscompare_callback: function to call on a miscompare (usually a logger such as log.error)
    :param expect_dict_key_ordered: set to True to check if dicts keys have the same order
    :param raise_exception_on_miscompare: True to raise exception on a miscompare
    :param compare_results: optional list of bools to hold the compare results. Useful for creating a pass rate.
    :param numeric_miscompares: optional dict (actually default dict) of numeric miscompares with the key as the relative error. Useful for debugging value errors.
    :return: True if dicts compare OK
    """
    ...

    if compare_results is None:
        compare_results = []

    if isinstance(description, str):
        description = (description,)

    leaf_result = None

    if are_comparable(expected, under_test):

        if isinstance(expected, (dict, defaultdict)) and isinstance(under_test, (dict, defaultdict)):
            # dicts and defaultdicts
            if (expect_dict_key_ordered and list(expected.keys()) != list(under_test.keys())) or (not expect_dict_key_ordered and set(expected.keys()) != set(under_test.keys())):
                # make sure both dicts keys are the same
                miscompare_callback(f"keys {list(expected.keys())} != {list(under_test.keys())}")
                compare_results.append(False)
                leaf_result = False
            else:
                for key, expected_value in expected.items():
                    uut_value = under_test[key]
                    yadd(
                        expected_value,
                        uut_value,
                        description + (key,),
                        rel_tol,
                        abs_tol,
                        miscompare_callback,
                        expect_dict_key_ordered,
                        raise_exception_on_miscompare,
                        compare_results,
                        numeric_miscompares,
                    )
        elif isinstance(expected, (list, tuple)) and isinstance(under_test, (list, tuple)):
            # lists and tuples
            if len(expected) != len(under_test):
                # make sure both lists/tuples are the same length
                miscompare_callback(f"can not compare lists or tuple of different lengths : {len(expected)=},{len(under_test)=}")
                compare_results.append(False)
                leaf_result = False
            else:
                for i, expected_value in enumerate(expected):
                    uut_value = under_test[i]
                    yadd(
                        expected_value,
                        uut_value,
                        description + (f"index={i}",),
                        rel_tol,
                        abs_tol,
                        miscompare_callback,
                        expect_dict_key_ordered,
                        raise_exception_on_miscompare,
                        compare_results,
                        numeric_miscompares,
                    )
        else:
            # "leaf" values
            if isinstance(expected, (float, int, Decimal, complex)) and isinstance(under_test, (float, int, Decimal, complex)):
                # numbers
                if isinstance(expected, Decimal):
                    expected = float(expected)
                if isinstance(under_test, Decimal):
                    under_test = float(under_test)
                is_close_result = cmath.isclose(expected, under_test, rel_tol=rel_tol, abs_tol=abs_tol)
                compare_results.append(is_close_result)
                if not is_close_result and numeric_miscompares is not None:
                    # handles both scalar and complex values
                    difference = min(abs((expected - under_test) / expected), abs((expected - under_test) / under_test))
                    numeric_miscompares[difference].append(f"{'.'.join(description)} : {expected=} != {under_test=}")
            else:
                # other things that are directly comparable, such as str and bool
                try:
                    compare_results.append(expected == under_test)
                except ValueError as e:
                    compare_results.append(False)
                    miscompare_callback(f"{type(expected)=},{type(under_test)=} not supported ({e})")
            leaf_result = compare_results[-1]
    else:
        miscompare_callback(f"{type(expected)=},{type(under_test)=} not supported")
        if raise_exception_on_miscompare:
            raise MiscompareException("not comparable")

    if leaf_result is False:
        miscompare_callback(f"{'.'.join(description)} : {expected=} != {under_test=}")
        if raise_exception_on_miscompare:
            raise MiscompareException(expected, under_test)

    return all(compare_results)
