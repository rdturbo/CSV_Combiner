import os
import pandas as pd

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
    # remove empty file
    os.remove(empty_csv)


def split_output(output: str) -> list[list[str]]:
    """Splits captured output from stdout
       into desired format

    Args:
        output (str): captured output from stdout

    Returns:
        list[list[str]]: output in csv format
    """
    lines = output.split("\n")
    n = len(lines)
    return [line.split(",") for line in lines][: n - 1]  # extra space in stdout


def test_no_input_file(capsys) -> None:
    """Test for no input file path given in command line"""
    command_line_args = [csv_combiner_py]
    combiner = CSVCombiner(command_line_args)
    no_file_msg = "Please provide file paths\n"

    combiner.combine_csv()
    stdout, _ = capsys.readouterr()
    assert no_file_msg == stdout


def test_wrong_input_file(capsys) -> None:
    """Test for wrong input file path given in command line"""
    command_line_args = [csv_combiner_py, "./fixtures/wrong_csv"]
    combiner = CSVCombiner(command_line_args)
    wrong_file_msg = f"./fixtures/wrong_csv not found\n"

    combiner.combine_csv()
    stdout, _ = capsys.readouterr()
    assert wrong_file_msg == stdout


def test_empty_file(capsys) -> None:
    """Test for empty file"""
    command_line_args = [csv_combiner_py, empty_csv]
    combiner = CSVCombiner(command_line_args)
    empty_file_msg = f"{empty_csv} is empty\n"

    combiner.combine_csv()
    stdout, _ = capsys.readouterr()
    assert empty_file_msg == stdout


def test_filename_present_in_header(capsys) -> None:
    """Test for checking if filename header is present"""
    command_line_args = [csv_combiner_py, accessories_csv, clothing_csv]
    combiner = CSVCombiner(command_line_args)
    combiner.combine_csv()
    stdout, _ = capsys.readouterr()

    headers = split_output(stdout)[0]
    assert headers[-1] == "filename"


def test_filename_present_in_data(capsys) -> None:
    """Test for checking one of the filename columns has output in correct format"""
    command_line_args = [csv_combiner_py, accessories_csv, clothing_csv]
    combiner = CSVCombiner(command_line_args)
    combiner.combine_csv()
    stdout, _ = capsys.readouterr()

    data_row_1 = split_output(stdout)[1]
    assert data_row_1[-1] == "accessories.csv"


def test_result_includes_all_rows(capsys) -> None:
    """Test for checking length of final result is inclusive of all input files"""
    command_line_args = [
        csv_combiner_py,
        accessories_csv,
        clothing_csv,
        household_cleaners_csv,
    ]
    combiner = CSVCombiner(command_line_args)

    acc = pd.read_csv(accessories_csv)
    clo = pd.read_csv(clothing_csv)
    hcl = pd.read_csv(household_cleaners_csv)

    # +1 for header row
    total_length = len(acc) + len(clo) + len(hcl) + 1

    combiner.combine_csv()
    stdout, _ = capsys.readouterr()

    final_data = split_output(stdout)
    assert len(final_data) == total_length
