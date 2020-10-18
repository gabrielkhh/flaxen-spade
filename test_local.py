from os import path

import pytest

from koro.manipulation import dataset_path


@pytest.mark.usefixtures("config")
def test_dataset_path(config):
    base_path = config.root_path
    assert dataset_path("static/test.csv") == path.join(
        base_path, "raw_datasets/static/test.csv"
    )
    assert dataset_path("static", "test.csv") == path.join(
        base_path, "raw_datasets/static/test.csv"
    )
    assert dataset_path("static", "deep/", "test.csv") == path.join(
        base_path, "raw_datasets/static/deep/test.csv"
    )
