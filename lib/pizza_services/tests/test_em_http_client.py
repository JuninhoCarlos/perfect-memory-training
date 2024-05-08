import pytest
import responses
from rdflib import RDF, RDFS, XSD, Graph, Literal, URIRef

from ..utils.em_http_client import EMHttpClient


@pytest.fixture(name="em_http_client")
def setup_em_http_client():
    return EMHttpClient(
        em_base_url="http://localhost:8080",
        em_api_key="1234567890",
        em_client_name="pizza_service",
    )


@pytest.fixture(name="graph")
def setup_graph():
    g = Graph()
    g.add(
        (
            URIRef("http://www.perfect-memory.com/profile/pizza/kb/12345"),
            RDF.type,
            URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#Pizza"),
        )
    )
    g.add(
        (
            URIRef("http://www.perfect-memory.com/profile/pizza/kb/12345"),
            URIRef("http://www.perfect-memory.com/ontology/pizza/1.1#price"),
            Literal("10.00", datatype=XSD.float),
        )
    )
    g.add(
        (
            URIRef("http://www.perfect-memory.com/profile/pizza/kb/12345"),
            RDFS.label,
            Literal("Margherita", lang="en"),
        )
    )
    return g


def test_init(em_http_client):
    assert em_http_client.em_base_url == "http://localhost:8080"
    assert em_http_client.em_api_key == "1234567890"
    assert em_http_client.em_client_name == "pizza_service"


@responses.activate
def test_insert_graph(em_http_client, graph):
    responses.add(
        responses.POST,
        "http://localhost:8080/v1/requests",
        json={"status": "success"},
        status=200,
    )

    response = em_http_client.insert_graph(graph)

    assert response.status_code == 200
    assert response.json() == {"status": "success"}


@responses.activate
def test_insert_graph_error(em_http_client, graph):
    responses.add(
        responses.POST,
        "http://localhost:8080/v1/requests",
        json={"error": "An error occurred"},
        status=500,
    )

    response = em_http_client.insert_graph(graph)

    assert response.status_code == 500
    assert response.json() == {"error": "An error occurred"}
