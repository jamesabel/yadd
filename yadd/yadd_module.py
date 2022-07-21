import math
import cmath
from typing import Dict, Tuple, Callable, Iterable, List, DefaultDict
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
        :param miscompare_callback: function to call on a miscompare (can be a logger such as log.error or print to output to stdout)
        :param expect_dict_key_ordered: set to True to check if input dicts keys have the same order
        :param raise_exception_on_miscompare: True to raise exception on a miscompare
        """

        # function takes description as a tuple
        if description is None:
            _description_tuple = tuple()  # type: Tuple
        else:
            _description_tuple = (description,)

        self._rel_tol = rel_tol
        self._abs_tol = abs_tol
        self._miscompare_callback = miscompare_callback
        self._expect_dict_key_ordered = expect_dict_key_ordered
        self._raise_exception_on_miscompare = raise_exception_on_miscompare

        self._compare_results = []  # type: List[bool]
        self._numeric_miscompares = defaultdict(list)  # type: DefaultDict[float, List]
        self._yadd(expected, under_test, _description_tuple)

    def match(self) -> bool:
        """
        Return True if expected matches under_test
        :return: True on match
        """
        return all(self._compare_results)

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

    def _yadd(
        self, expected: Dict | Iterable | float | int | str | Decimal | complex | bool, under_test: Dict | Iterable | float | int | str | Decimal | complex | bool, description: Tuple[str, ...]
    ):
        """
        "core" dict differ

        :param expected: expected results
        :param under_test: unit under test
        :param description: description Tuple

        """

        leaf_result = None

        if are_comparable(expected, under_test):

            if isinstance(expected, (dict, defaultdict)) and isinstance(under_test, (dict, defaultdict)):
                # dicts and defaultdicts
                if (self._expect_dict_key_ordered and list(expected.keys()) != list(under_test.keys())) or (
                    not self._expect_dict_key_ordered and set(expected.keys()) != set(under_test.keys())
                ):
                    # make sure both dicts keys are the same
                    self._miscompare_callback(f"keys {list(expected.keys())} != {list(under_test.keys())}")
                    self._compare_results.append(False)
                    leaf_result = False
                else:
                    for key, expected_value in expected.items():
                        uut_value = under_test[key]
                        t = description + (key,)
                        self._yadd(
                            expected_value,
                            uut_value,
                            t,
                        )
            elif isinstance(expected, (list, tuple)) and isinstance(under_test, (list, tuple)):
                # lists and tuples
                if len(expected) != len(under_test):
                    # make sure both lists/tuples are the same length
                    self._miscompare_callback(f"can not compare lists or tuple of different lengths : {len(expected)=},{len(under_test)=}")
                    self._compare_results.append(False)
                    leaf_result = False
                else:
                    for i, expected_value in enumerate(expected):
                        uut_value = under_test[i]
                        self._yadd(
                            expected_value,
                            uut_value,
                            description + (f"index={i}",),
                        )
            else:
                # "leaf" values
                if isinstance(expected, (float, int, Decimal, complex)) and isinstance(under_test, (float, int, Decimal, complex)):
                    # numbers
                    if isinstance(expected, Decimal):
                        expected = float(expected)
                    if isinstance(under_test, Decimal):
                        under_test = float(under_test)
                    is_close_result = cmath.isclose(expected, under_test, rel_tol=self._rel_tol, abs_tol=self._abs_tol)
                    self._compare_results.append(is_close_result)
                    if not is_close_result and self._numeric_miscompares is not None:
                        # handles both scalar and complex values
                        try:
                            difference = float(min(abs((expected - under_test) / expected), abs((expected - under_test) / under_test)))
                        except ZeroDivisionError:
                            difference = math.nan
                        self._numeric_miscompares[difference].append(f"{'.'.join(description)} : expected={expected=} != under_test={under_test=}")
                else:
                    # other things that are directly comparable, such as str and bool
                    try:
                        self._compare_results.append(expected == under_test)
                    except ValueError as e:
                        self._compare_results.append(False)
                        self._miscompare_callback(f"{type(expected)=},{type(under_test)=} not supported ({e})")
                leaf_result = self._compare_results[-1]
        else:
            self._miscompare_callback(f"{type(expected)=},{type(under_test)=} not supported")
            if self._raise_exception_on_miscompare:
                raise MiscompareException("not comparable", type(expected), type(under_test))

        if leaf_result is False:
            self._miscompare_callback(f"{'.'.join(description)} : expected={expected} != under_test={under_test}")
            if self._raise_exception_on_miscompare:
                raise MiscompareException(expected, under_test)


def yadd(
    expected: Dict | Iterable | float | int | str | Decimal | complex | bool,
    under_test: Dict | Iterable | float | int | str | Decimal | complex | bool,
    description: str = None,
    rel_tol: float = 1e-9,
    abs_tol: float = 0.0,
    miscompare_callback: Callable = print,
    expect_dict_key_ordered: bool = False,
    raise_exception_on_miscompare: bool = True,
) -> bool:
    """
    Yet Another Dict Difference Alternative

    :param expected: expected results
    :param under_test: unit under test
    :param description: description of test
    :param rel_tol: for floats, relative error tolerance (default is the same as math.isclose() rel_tol)
    :param abs_tol: for floats, absolute error tolerance (default is the same as math.isclose() abs_tol)
    :param miscompare_callback: function to call on a miscompare (can be a logger such as log.error or print to output to stdout)
    :param expect_dict_key_ordered: set to True to check if input dicts keys have the same order
    :param raise_exception_on_miscompare: True to raise exception on a miscompare
    """

    _yadd = Yadd(expected, under_test, description, rel_tol, abs_tol, miscompare_callback, expect_dict_key_ordered, raise_exception_on_miscompare)
    return _yadd.match()
