from rdflib import Graph

from ..models.pizza_model import PizzaModel
from ..parsers.interfaces.parser_interface import ParserInterface


class IngestPizza:

    def __init__(self, parser_service: ParserInterface):
        """
        Initializes the CsvPizzaParser class.

        Args:
            parser_service (ParserInterface): An implementation of the ParserInterface.
        """

        pizza_array = parser_service.parse()

        pizzas = self._mount_pizza_models(pizza_array)
        self.pizzas_graph = self._mount_pizzas_graph(pizzas)

    def _mount_pizza_models(self, pizzas: "list[dict]") -> "list[PizzaModel]":
        """
        Mounts a list of PizzaModel objects from a list of dictionaries.

        Args:
            pizzas (list): A list of dictionaries. Each dictionary represents a pizza.


        Returns:
            list[PizzaModel]: A list of PizzaModel objects.
        """
        pizza_models = []
        for pizza in pizzas:
            pizza_models.append(PizzaModel(pizza))

        return pizza_models

    def _mount_pizzas_graph(self, pizza_models_array: "list[PizzaModel]") -> Graph:
        """
        Mounts a Graph object from a list of PizzaModel objects.

        Args:
            pizza_models_array (list): A list of PizzaModel objects.

        Returns:
            Graph: A Graph object.
        """
        pizza_graph = Graph()
        for pizza in pizza_models_array:
            pizza_graph = pizza.build_node(pizza_graph)

        return pizza_graph
