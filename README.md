# PMG CSV_Combiner Solution

Solution for PMG's CSV_Combiner Challenge. The python script combines the input csv files (through command line arguments) while adding an additional column called **filename** for each row. The script outputs this new CSV file to `stdout`.

## Installation Requirements
- Python 3.10
- Pandas
- Pytest

Install with help of requirements.txt:
```
$ pip install requirements.txt
```

## Run the script
```
$ python csv_combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv ./fixtures/household_cleaners.csv
```

## Run the test file
```
$ pytest
```

## Github Action for CI/CD
`.github/workflows/python-app.yml` is a simple script to run pytest on push
