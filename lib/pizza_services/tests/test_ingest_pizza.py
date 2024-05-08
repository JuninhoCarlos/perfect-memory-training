from rdflib import Graph

from ..models.pizza_model import PizzaModel
from ..parsers.interfaces.parser_interface import ParserInterface
from ..processes.ingest_pizza import IngestPizza


class MockParserService(ParserInterface):
    def parse(self):
        return [
            {
                "pizza_name": "Margherita",
                "pizza_description": "mozzarella,cheese",
                "pizza_price": "10.00",
            },
            {
                "pizza_name": "Pepperoni",
                "pizza_description": "pepperoni",
                "pizza_price": "12.00",
            },
        ]


def test_init():
    parser_service = MockParserService()
    ingest_pizza = IngestPizza(parser_service)

    assert isinstance(ingest_pizza.pizzas_graph, Graph)
    # we expect 6 triple (id, price, label for each dict)
    assert len(ingest_pizza.pizzas_graph) == 6


def test__mount_pizza_models():
    parser_service = MockParserService()
    ingest_pizza = IngestPizza(parser_service)

    # pylint: disable=protected-access
    pizza_models = ingest_pizza._mount_pizza_models(parser_service.parse())

    assert isinstance(pizza_models, list)
    assert len(pizza_models) == 2

    for pizza_model in pizza_models:
        assert isinstance(pizza_model, PizzaModel)


def test__mount_pizzas_graph():
    parser_service = MockParserService()
    ingest_pizza = IngestPizza(parser_service)

    # pylint: disable=protected-access
    pizza_models = ingest_pizza._mount_pizza_models(parser_service.parse())
    pizza_graph = ingest_pizza._mount_pizzas_graph(pizza_models)

    assert isinstance(pizza_graph, Graph)
    # we expect 6 triple (id, price, label for each dict)
    assert len(pizza_graph) == 6
