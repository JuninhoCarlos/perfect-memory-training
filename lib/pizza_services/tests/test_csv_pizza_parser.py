import csv
import os

import pytest

from ..parsers.csv_parser import CsvParser


@pytest.fixture(name="csv_file")
def setup_csv_file():
    """
    Create a temporary CSV file for testing.

    The CSV file will have the following contents:

    ```
    name,toppings,price
    Margherita,mozzarella,cheese,10.00
    Pepperoni,pepperoni,12.00
    Hawaiian,ham,pineapple,14.00
    ```

    Yields:
        The path to the temporary CSV file.
    """
    with open("test.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "toppings", "price"])
        writer.writerow(["Margherita", "mozzarella,cheese", "10.00"])
        writer.writerow(["Pepperoni", "pepperoni", "12.00"])
        writer.writerow(["Hawaiian", "ham,pineapple", "14.00"])

    yield "test.csv"

    os.remove("test.csv")


def test_init(csv_file):
    """
    Test the __init__ method of the CsvPizzaParser class.
    """
    parser = CsvParser(csv_file, ["name", "toppings", "price"])

    assert parser.path_to_csv == csv_file
    # pylint: disable=protected-access
    assert parser._mapper == {"name": 0, "toppings": 1, "price": 2}


def test_parse(csv_file):
    """
    Test the parse method of the CsvPizzaParser class.
    """
    parser = CsvParser(csv_file, ["name", "toppings", "price"])

    result = parser.parse()

    assert result == [
        {"name": "Margherita", "toppings": "mozzarella,cheese", "price": "10.00"},
        {"name": "Pepperoni", "toppings": "pepperoni", "price": "12.00"},
        {"name": "Hawaiian", "toppings": "ham,pineapple", "price": "14.00"},
    ]
