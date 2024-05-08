import argparse
import logging
import os

from dotenv import load_dotenv
from pizza_services.parsers.csv_parser import CsvParser
from pizza_services.processes.ingest_pizza import IngestPizza
from pizza_services.utils.em_http_client import EMHttpClient

# Cli Parser
parse = argparse.ArgumentParser()
parse.add_argument(
    "-p", "--path", help="Path to the csv file to be parsed and ingested"
)
args = parse.parse_args()


# application configuration
load_dotenv()  # take environment variables from .env.

# basic loggin configuration
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

pizza_csv_parser = CsvParser(
    args.path, ["pizza_price", "pizza_name", "pizza_description"]
)


ingest_pizza = IngestPizza(parser_service=pizza_csv_parser)

em_http_client = EMHttpClient(
    em_base_url=os.getenv("EM_BASE_URL"),
    em_api_key=os.getenv("EM_API_KEY"),
    em_client_name=os.getenv("EM_CLIENT_NAME"),
)
logger.info("Inserting graph into Exchange Manager")

response = em_http_client.insert_graph(ingest_pizza.pizzas_graph)

if response.status_code // 100 == 2:
    logger.info("Graph inserted successfully")
else:
    logger.error("Error inserting the graph into Exchange Manager")
    logger.error("Response: %s", response.text)
