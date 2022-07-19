from pathlib import Path
import json
from argparse import ArgumentParser

from yadd import yadd, application_name


def yadd_cli():
    parser = ArgumentParser(application_name)
    parser.add_argument("expected_result_file_path", metavar="<expected results file path>", help="expected results JSON file path")
    parser.add_argument("uut_file_path", metavar="<unit under test file path>", help="unit under test JSON file path")
    args = parser.parse_args()

    with Path(args.expected_result_file_path).open() as expected_results_file:
        expected = json.load(expected_results_file)
    with Path(args.uut_file_path).open() as uut_file:
        uut = json.load(uut_file)
    ok = yadd(expected, uut, miscompare_callback=print, raise_exception_on_miscompare=False)
    if ok:
        print("pass")
