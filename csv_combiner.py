import os
import sys
import pandas as pd


class CSVCombiner:
    chunk_size = 5000

    def __init__(self, files: list[str]) -> None:
        self.files = files[1:]
        self.chunks = []

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

        for file in self.files:
            self.add_chunks(file, os.path.basename(file))

        self.write_to_file()

    def add_chunks(self, file: str, file_name: str):
        for chunk in pd.read_csv(file, chunksize=CSVCombiner.chunk_size):
            chunk["filename"] = file_name
            self.chunks.append(chunk)

    def write_to_file(self):
        CSVCombiner.print_chunk(self.chunks[0], True)
        if len(self.chunks) > 1:
            for chunk in self.chunks[1:]:
                CSVCombiner.print_chunk(chunk)

    @staticmethod
    def print_chunk(chunk, header=False):
        print(
            chunk.to_csv(
                index=False,
                header=header,
                chunksize=CSVCombiner.chunk_size,
            ),
            end="",
        )


def main():
    combiner = CSVCombiner(sys.argv)
    combiner.combine_csv()


if __name__ == "__main__":
    main()
