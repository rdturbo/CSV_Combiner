import contextlib
import os
import pandas as pd
from io import StringIO

import generatefixtures
from csv_combiner import CSVCombiner

# paths to csv
csv_combiner_py: str = None
output_csv_path: str = None
accessories_csv: str = None
clothing_csv: str = None
household_cleaners_csv: str = None
empty_csv: str = None


def setup_module(module):
    # generate all csv files
    generatefixtures.main()

    # paths to csv
    global csv_combiner_py, output_csv_path, accessories_csv, clothing_csv, household_cleaners_csv, empty_csv
    csv_combiner_py = "./csv_combiner.py"
    accessories_csv = "./fixtures/accessories.csv"
    clothing_csv = "./fixtures/clothing.csv"
    household_cleaners_csv = "./fixtures/household_cleaners.csv"
    empty_csv = "./fixtures/empty.csv"


def teardown_module(module):
    os.remove(empty_csv)


def split_output(output: str) -> list[list[str]]:
    lines = output.split("\n")
    n = len(lines)
    return [line.split(",") for line in lines][: n - 1]  # extra space in stdout


def test_no_input_file() -> None:
    command_line_args = [csv_combiner_py]
    combiner = CSVCombiner(command_line_args)
    no_file_msg = "Please provide file paths\n"
    no_file_output = StringIO()

    with contextlib.redirect_stdout(no_file_output):
        combiner.combine_csv()

    assert no_file_msg == no_file_output.getvalue()


def test_wrong_input_file() -> None:
    command_line_args = [csv_combiner_py, "./fixtures/wrong_csv"]
    combiner = CSVCombiner(command_line_args)
    wrong_file_msg = f"./fixtures/wrong_csv not found\n"
    wrong_file_output = StringIO()

    with contextlib.redirect_stdout(wrong_file_output):
        combiner.combine_csv()

    assert wrong_file_msg == wrong_file_output.getvalue()


def test_empty_file() -> None:
    command_line_args = [csv_combiner_py, empty_csv]
    combiner = CSVCombiner(command_line_args)
    empty_file_msg = f"{empty_csv} is empty\n"
    empty_file_output = StringIO()

    with contextlib.redirect_stdout(empty_file_output):
        combiner.combine_csv()

    assert empty_file_msg == empty_file_output.getvalue()


def test_filename_present_in_header() -> None:
    command_line_args = [csv_combiner_py, accessories_csv, clothing_csv]
    combiner = CSVCombiner(command_line_args)
    filename_header_output = StringIO()

    with contextlib.redirect_stdout(filename_header_output):
        combiner.combine_csv()

    headers = split_output(filename_header_output.getvalue())[0]
    assert headers[-1] == "filename"


def test_filename_present_in_data() -> None:
    command_line_args = [csv_combiner_py, accessories_csv, clothing_csv]
    combiner = CSVCombiner(command_line_args)
    filename_row_output = StringIO()

    with contextlib.redirect_stdout(filename_row_output):
        combiner.combine_csv()

    data_row_1 = split_output(filename_row_output.getvalue())[1]
    assert data_row_1[-1] == "accessories.csv"


def test_result_includes_all_rows() -> None:
    command_line_args = [
        csv_combiner_py,
        accessories_csv,
        clothing_csv,
        household_cleaners_csv,
    ]
    combiner = CSVCombiner(command_line_args)
    all_rows = StringIO()

    acc = pd.read_csv(accessories_csv)
    clo = pd.read_csv(clothing_csv)
    hcl = pd.read_csv(household_cleaners_csv)

    # +1 for header row
    total_length = len(acc) + len(clo) + len(hcl) + 1

    with contextlib.redirect_stdout(all_rows):
        combiner.combine_csv()

    final_data = split_output(all_rows.getvalue())
    assert len(final_data) == total_length
