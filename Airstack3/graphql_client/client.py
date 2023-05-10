import requests
from typing import Dict


class GraphQLClient:
    """
    A class that encapsulates the logic for making requests to the GraphQL API endpoint.
    """

    def __init__(self, url: str):
        self.url = url

    def query(self, query: str) -> Dict:
        """
        Executes a GraphQL query against the API endpoint.

        :param query: The query to execute.
        :return: A dictionary containing the JSON response from the API endpoint.
        """
        response = requests.post(self.url, json={"query": query})
        response.raise_for_status()
        return response.json()