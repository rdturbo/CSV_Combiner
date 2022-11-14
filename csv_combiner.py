import os
import sys
import pandas as pd


class CSVCombiner:
    chunk_size = 5000

    def __init__(self, files: list[str]) -> None:
        self.files = files[1:]  # list of file paths
        self.chunks = []  # list of chunks

    def validate_files(self) -> bool:
        """Validates all file paths

        Returns:
            bool: True if satisfies conditions else False
        """

        # checks if command line args is empty
        if not len(self.files):
            print("Please provide file paths")
            return False

        # validates files one-by-one
        for file in self.files:
            if not self.validate_file(file):
                return False

        return True

    def validate_file(self, file: str) -> bool:
        """Validates given file path

        Args:
            file (str): file_path

        Returns:
            bool: True if satisfies conditions else False
        """
        return self.check_file_exists(file) and self.check_file_not_empty(file)

    def check_file_exists(self, file: str) -> bool:
        """Checks if file exists in given directory

        Args:
            file (str): file_path

        Returns:
            bool: True if file exists else False
        """
        if not os.path.exists(file):
            print(f"{file} not found")
            return False
        return True

    def check_file_not_empty(self, file: str) -> bool:
        """Checks if file is empty

        Args:
            file (str): file_path

        Returns:
            bool: True if not empty else False
        """
        if not os.stat(file).st_size:
            print(f"{file} is empty")
            return False
        return True

    def combine_csv(self) -> None:
        """Main combine method to combine csv files with additional filename column"""
        if not self.validate_files():
            return

        for file in self.files:
            self.add_chunks(file, os.path.basename(file))

        self.write_to_file()

    def add_chunks(self, file: str, file_name: str) -> None:
        """Seperates input file into chunks and adds it to list

        Args:
            file (str): file_path
            file_name (str): file_name
        """
        for chunk in pd.read_csv(file, chunksize=CSVCombiner.chunk_size):
            chunk["filename"] = file_name
            self.chunks.append(chunk)

    def write_to_file(self) -> None:
        """Helper func for printing to stdout"""
        # Prints along with header
        CSVCombiner.print_chunk(self.chunks[0], True)
        if len(self.chunks) > 1:
            # Doesn't print with header
            for chunk in self.chunks[1:]:
                CSVCombiner.print_chunk(chunk)

    @staticmethod
    def print_chunk(chunk, header=False) -> None:
        """Helper method to prints chunk to stdout in csv format

        Args:
            chunk : Pandas chunks of rows (max_size 5000)
            header (bool, optional): Header flag. Defaults to False.
        """
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
