import os
from re import sub


def touch(path):
    with open(path, "a"):
        os.utime(path, None)


def snake_case(s):
    return "_".join(
        sub(
            "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))
        ).split()
    ).lower()


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def print_table(headers, *columns):
    """
    Prints a tabular display with the given headers and columns.

    Args:
        headers (list): A list of strings representing the headers for each column.
        *columns (list): Variable number of lists, each representing a column of data.
    """
    spacing = 4

    # Calculate the maximum width for each column
    col_widths = [
        max(len(str(item)) for item in [header] + list(column)) + spacing
        for header, column in zip(headers, columns)
    ]

    # Print the header row
    print(" ".join(f"{header:{width}}" for header, width in zip(headers, col_widths)))

    # Print a separator line
    print("-" * (sum(col_widths) + len(col_widths) - 1))

    # Print each row of data
    for row in zip(*columns):
        print(" ".join(f"{item:{width}}" for item, width in zip(row, col_widths)))
