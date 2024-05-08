import json

import requests
from rdflib import Graph
from requests import Response


class EMHttpClient:
    """
    Class for the Exchange Manager HTTP client.
    This class is responsible for making HTTP requests to the Exchange Manager API.
    """

    def __init__(self, em_base_url: str, em_api_key: str, em_client_name: str):
        """
        Initializes the EMHttpClient class.

        Args:
            em_base_url (str): The base URL of the Exchange Manager API.
            em_api_key (str): The API key for the Exchange Manager API.
            em_client_name (str): The client name for the Exchange Manager API.

        Raises:
            ValueError: If any of the parameters is None or empty.
        """
        if not em_base_url or not em_api_key or not em_client_name:
            raise ValueError("All parameters must be provided.")

        self.em_base_url = em_base_url
        self.em_api_key = em_api_key
        self.em_client_name = em_client_name

    def insert_graph(self, graph: Graph) -> Response:
        """
        Inserts a graph into Exchange Manager.

        Args:
            graph (Graph): The graph to insert.

        Returns:
            Response: The response from the Exchange Manager API.
        """
        request_url = f"{self.em_base_url}/v1/requests"
        graph_json = json.loads(graph.serialize(format="json-ld"))

        payload = {
            "item_name": "insert_graph",
            "priority": "normal",
            "client_name": self.em_client_name,
            "inputs": {
                "graph": {
                    "type": "graph",
                    "value": [{"@graph": graph_json}],
                    "roots": [
                        graph_json[0]["@id"]
                    ],  # setting only the first pizza as the root
                }
            },
        }

        headers = {
            "x-api-key": self.em_api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        try:
            # Make the POST request
            response = requests.post(
                request_url, headers=headers, json=payload, timeout=500
            )
            return response
        # pylint: disable=broad-exception-caught
        except Exception as e:
            print("An error occurred:", str(e))
