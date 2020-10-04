import json
from abc import ABC, abstractmethod
from csv import DictReader
from os import path
from typing import Dict, List, Optional, TextIO

from flask import current_app


class BaseLoader(ABC):
    def resolve_absolute_path(self, filename: str) -> str:
        if current_app.root_path is None:
            raise ValueError("No base path set for flask.")

        return path.join(current_app.root_path, "raw_datasets", filename)

    def load_file(self, filename: str):
        """
        Serialize a file.

        :param filename: Name of the file
        :return: Parsed format of the file
        """
        with open(self.resolve_absolute_path(filename), "r") as file:
            return self.serialize(file)

    @abstractmethod
    def serialize(self, file: TextIO):
        pass


class JsonLoader(BaseLoader):
    def serialize(self, file: TextIO) -> Dict:
        """
        Get a dict representation of the parsed json file.

        :param file: File instance
        :return:
        """
        return json.load(file)


class CsvLoader(BaseLoader):
    def __init__(self, headers: Optional[List[str]] = None):
        """
        :param headers: Different headers passed to DictReader. Will affect key name.
        """
        self.headers = headers

    def serialize(self, file: TextIO) -> List[Dict]:
        """
        Get a list representation of the parsed csv file.

        :param file:
        :return:
        """
        return list(DictReader(file))
