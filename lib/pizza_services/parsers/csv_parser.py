import csv

from .interfaces.parser_interface import ParserInterface


class CsvParser(ParserInterface):
    """Implements a Csv Parser"""

    def __init__(self, path_to_csv: str, mapper: "list[str]"):
        """
        Initializes the CsvPizzaParser class.

        Args:
            path_to_csv (str): The path to the CSV file to be parsed.
            mapper (list): A list of string mapping the columns names in the CSV file to be
            extract in the parse stage. The dict output from parse method will have the data
            extract from the columns that have a column in the mapping.
        """

        self.path_to_csv = path_to_csv
        self._mapper = self._build_mapper(mapper)

    def _build_mapper(self, mapper: "list[str]") -> dict:
        """
        generate a mapper dict that maps the key to the index of the column in the
        csv file to help in the parse step

        Args:
            mapper (list): A list of string mapping the columns names in the CSV file
            to be extract in the parse stage.

        Return a ``dict`` containing the key and the index of the respecting key in the csv file
        """

        # cast the array to a set to make the search O(1) instead of O(n)
        column_map_set = set(mapper)

        mapper_dict = {}
        with open(self.path_to_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # iterates only in the header row of the table
                for index, column in enumerate(row):
                    if column in column_map_set:
                        mapper_dict[column] = index

                break

        return mapper_dict

    def parse(self) -> dict:
        """
        Parses the CSV file and returns a dict

        The parsed is performed based on the path of the csv file and in the mapper list that was
        passed in the class constructor
        """
        result = []
        with open(self.path_to_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            for index, row in enumerate(reader):
                # Skip header row
                if index == 0:
                    continue
                # pylint: disable=consider-using-dict-items
                row_dict = dict([(key, row[self._mapper[key]]) for key in self._mapper])
                result.append(row_dict)

        return result
