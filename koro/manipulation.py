import os
import pathlib

from flask import current_app

from cache import cache


def first_true(iterable, pred=None, default=None):
    """
    Returns the first true value in the iterable.

    If no true value is found, returns *default*.
    If *pred* is not None, returns the first item for which pred(item) is true.

    """
    return next(filter(pred, iterable), default)


def base_path() -> str:
    if current_app.root_path is None:
        raise ValueError("No base path set for flask.")

    return current_app.root_path


def dataset_path(*args) -> str:
    """
    Generate a fully qualified path to the desired dataset.

    :param args: Paths
    :return: Path to the file
    """

    return os.path.join(base_path(), "raw_datasets", *args)


@cache.memoize()
def directory_size(folder: str) -> int:
    return sum(file.stat().st_size for file in pathlib.Path(folder).rglob("*"))


def size_for_humans(size: int) -> str:
    suffixes = ["B", "KB", "MB", "GB", "TB"]
    suffix = 0
    while size > 1024 and suffix < 4:
        suffix += 1
        size = size / 1024.0
    return f"{size:.2f} {suffixes[suffix]}"
