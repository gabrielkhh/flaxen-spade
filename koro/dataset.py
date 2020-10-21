import json
from abc import ABC, abstractmethod
from csv import DictReader
from typing import Dict, List, Optional, TextIO

from cache import cache
from koro.manipulation import dataset_path


class BaseLoader(ABC):
    def resolve_absolute_path(self, filename: str) -> str:
        return dataset_path(filename)

    @cache.memoize(500)
    def load_file(self, filename: str):
        """
        Serialize a file.

        :param filename: Name of the file
        :return: Parsed format of the file
        """
        with open(self.resolve_absolute_path(filename), "r", encoding="utf-8") as file:
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
    def __init__(self, headers: Optional[List[str]] = None, delimiter=","):
        """
        :param headers: Different headers passed to DictReader. Will affect key name.
        """
        self.headers = headers
        self.delimiter = delimiter

    def serialize(self, file: TextIO) -> List[Dict]:
        """
        Get a list representation of the parsed csv file.

        :param file:
        :return:
        """
        return list(DictReader(file, delimiter=self.delimiter))
