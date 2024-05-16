import uuid

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD


class PizzaModel:
    def __init__(self, pizza_dict: dict) -> None:
        # Do the mapping from the json keys to the object attributes
        self.pizza_id = pizza_dict.get("pizza_id", "")

        self.label = pizza_dict.get("pizza_name", "")
        # pizza ingredient has multiple values
        self.ingredients = pizza_dict.get("pizza_description", []).split(",")
        # if the price is empty, set the default to zero
        self.price = pizza_dict.get("pizza_price") or "0.0"

        # random uuid attribute set at build stage
        self.uuid = None

    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return (
            f"Pizza: {self.label}, Ingredients: {self.ingredients}, Price: {self.price}"
        )

    def _add_id(self, rooted_node: Graph = None) -> Graph:
        """
         Adds an id to the graph.

        Args:
            rooted_node (Graph, optional): The graph to add the id to.
            If the graph is None, a new graph is created. Defaults to None.

        Returns:
            Graph: The graph with the id added.
        """
        if not rooted_node:
            g = Graph()
        else:
            g = rooted_node

        if not self.uuid:
            self.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, self.pizza_id)

        g.add(
            (
                URIRef(f"http://www.perfect-memory.com/profile/pizza/kb/{self.uuid}"),
                RDF.type,
                URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#Pizza"),
            )
        )
        return g

    def _add_price(self, id_pizza: str, price: str, rooted_node: Graph) -> Graph:
        """
        Adds the price to an existing graph.

        Args:
            id (str): The id of the node to add the price to.
            price (str): The price to add to the node.
            rooted_node (Graph): The graph to add the price to.

        Returns:
            The graph with the price added.

        """
        rooted_node.add(
            (
                URIRef(f"http://www.perfect-memory.com/profile/pizza/kb/{id_pizza}"),
                URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#price"),
                Literal(price, datatype=XSD.float),
            )
        )
        return rooted_node

    def _add_en_label(self, id_pizza: str, label: str, rooted_node: Graph) -> Graph:
        """
        Adds the english label to an existing graph.

        Args:
            id (str): The id of the node to add the label to.
            label (str): The label to add to the node.
            rooted_node (Graph): The graph to add the label to

        Returns:
            The graph with the label added.
        """

        rooted_node.add(
            (
                URIRef(f"http://www.perfect-memory.com/profile/pizza/kb/{id_pizza}"),
                RDFS.label,
                Literal(label, lang="en"),
            )
        )
        return rooted_node

    def build_node(self, rooted_node: Graph = None) -> Graph:
        """
        Builds the RDF graph for the pizza.

        Args:
            rooted_node (Graph, optional): The graph to add the pizza to.
            If the graph is None, a new graph is created. Defaults to None.

        Returns:
            Graph: The graph with the pizza added.
        """
        graph = self._add_id(rooted_node)
        graph = self._add_price(self.uuid, self.price, graph)
        graph = self._add_en_label(self.uuid, self.label, graph)

        return graph

    def serialize_node(self) -> dict:
        """
        Serializes the node to a string.

        Returns:
            str: The node as a string.
        """
        g = self.build_node()
        return g.serialize(format="json-ld")
