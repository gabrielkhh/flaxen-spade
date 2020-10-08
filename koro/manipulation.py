from os import path

from flask import current_app


def first_true(iterable, pred=None, default=None):
    """
    Returns the first true value in the iterable.

    If no true value is found, returns *default*.
    If *pred* is not None, returns the first item for which pred(item) is true.

    """
    return next(filter(pred, iterable), default)


def base_path() -> str:
    return current_app.root_path


def dataset_path(*args) -> str:
    """
    Generate a fully qualified path to the desired dataset.

    :param args: Paths
    :return: Path to the file
    """

    return path.join(base_path(), "raw_datasets", *args)
