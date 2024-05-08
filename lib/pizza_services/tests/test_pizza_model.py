import json

import pytest
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

from ..models.pizza_model import PizzaModel


@pytest.fixture(name="pizza_dict")
def setup_pizza_dict():
    return {
        "pizza_name": "Margherita",
        "pizza_description": "mozzarella,cheese",
        "pizza_price": "10.00",
    }


@pytest.fixture(name="pizza_array_dict")
def setup_pizza_array_dict():
    return [
        {
            "pizza_name": "Margherita",
            "pizza_description": "mozzarella,cheese",
            "pizza_price": "10.00",
        },
        {
            "pizza_name": "Pepperoni",
            "pizza_description": "mozzarella,cheese,pepperoni",
            "pizza_price": "12.00",
        },
    ]


def test_init(pizza_dict):
    pizza_model = PizzaModel(pizza_dict)

    assert pizza_model.label == "Margherita"
    assert pizza_model.ingredients == ["mozzarella", "cheese"]
    assert pizza_model.price == "10.00"
    assert pizza_model.random_uuid is None


def test_str(pizza_dict):
    pizza_model = PizzaModel(pizza_dict)

    assert (
        str(pizza_model)
        == "Pizza: Margherita, Ingredients: ['mozzarella', 'cheese'], Price: 10.00"
    )


def test_add_id(pizza_dict):
    pizza_model = PizzaModel(pizza_dict)

    # pylint: disable=protected-access
    graph = pizza_model._add_id()

    assert isinstance(graph, Graph)
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        RDF.type,
        URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#Pizza"),
    ) in graph


def test_add_id_with_rooted_node(pizza_array_dict):
    pizza_model = PizzaModel(pizza_array_dict[0])
    # pylint: disable=protected-access
    graph = pizza_model._add_id()

    assert isinstance(graph, Graph)
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        RDF.type,
        URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#Pizza"),
    ) in graph

    # insert second pizza using pizza one as rooted node
    pizza_model = PizzaModel(pizza_array_dict[1])

    graph = pizza_model._add_id(graph)

    assert isinstance(graph, Graph)
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        RDF.type,
        URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#Pizza"),
    ) in graph

    assert isinstance(graph, Graph)


def test_add_price(pizza_dict):
    pizza_model = PizzaModel(pizza_dict)

    graph = Graph()
    # pylint: disable=protected-access
    graph = pizza_model._add_price(pizza_model.random_uuid, pizza_model.price, graph)

    assert isinstance(graph, Graph)
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#price"),
        Literal("10.00", datatype=XSD.float),
    ) in graph


def test_add_en_label(pizza_dict):
    pizza_model = PizzaModel(pizza_dict)

    graph = Graph()
    # pylint: disable=protected-access
    graph = pizza_model._add_en_label(pizza_model.random_uuid, pizza_model.label, graph)

    assert isinstance(graph, Graph)
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        RDFS.label,
        Literal("Margherita", lang="en"),
    ) in graph


def test_build_node(pizza_dict):
    pizza_model = PizzaModel(pizza_dict)

    graph = pizza_model.build_node()

    assert isinstance(graph, Graph)
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        RDF.type,
        URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#Pizza"),
    ) in graph
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#price"),
        Literal("10.00", datatype=XSD.float),
    ) in graph
    assert (
        URIRef(
            f"http://www.perfect-memory.com/profile/pizza/kb/{pizza_model.random_uuid}"
        ),
        RDFS.label,
        Literal("Margherita", lang="en"),
    ) in graph


def test_serialize_node(pizza_dict):
    pizza_model = PizzaModel(pizza_dict)

    serialized_graph = pizza_model.serialize_node()

    assert isinstance(serialized_graph, str)
    json_graph = json.loads(serialized_graph)[0]

    assert "@id" in json_graph.keys()  # assures that an id was set
    assert "@type" in json_graph.keys()  # assures that an type was set
    assert (
        "http://www.perfect-memory.com/ontology/pizza/1.1#price" in json_graph.keys()
    )  # assures that price attribute was set
    assert (
        "http://www.w3.org/2000/01/rdf-schema#label" in json_graph.keys()
    )  # assures that label attribute was set
