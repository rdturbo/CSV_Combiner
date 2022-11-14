import os
import sys


class CSVCombiner:
    def __init__(self, files: list[str]) -> None:
        self.files = files

    def validate_files(self) -> bool:

        if not len(self.files):
            print("Please provide file paths")
            return False

        for file in self.files:
            if not self.validate_file(file):
                return False

        return True

    def validate_file(self, file: str) -> bool:
        return self.check_file_exists(file) and self.check_file_not_empty(file)

    def check_file_exists(self, file: str):
        if not os.path.exists(file):
            print(f"{file} not found")
            return False
        return True

    def check_file_not_empty(self, file: str):
        if not os.stat(file).st_size:
            print(f"{file} is empty")
            return False
        return True

    def combine_csv(self):
        if not self.validate_files():
            return


def main():
    combiner = CSVCombiner(sys.argv[1:])
    combiner.combine_csv()


if __name__ == "__main__":
    main()
