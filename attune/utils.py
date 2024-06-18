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
