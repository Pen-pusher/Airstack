import requests
import pytest
from typing import Dict
from jsonschema import validate


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
        response = requests.post(self.url, json={'query': query})
        response.raise_for_status()
        return response.json()


@pytest.fixture
def graphql_client():
    """
    A fixture that creates a GraphQLClient instance to be used in tests.
    """
    return GraphQLClient("https://devapi.airstack.xyz/gql")


@pytest.fixture
def test_data():
    """
    A fixture that loads test data from a separate module.
    """
    from tests.test_data import (
        VALID_QUERY,
        VALID_EXPECTED_DATA,
        INVALID_BLOCKCHAIN_QUERY,
        INVALID_LIMIT_QUERY,
        INVALID_FILTER_QUERY,
        INVALID_ADDRESS_FORMAT_QUERY,
        RESPONSE_SCHEMA
    )

    return {
        "valid_query": VALID_QUERY,
        "valid_expected_data": VALID_EXPECTED_DATA,
        "invalid_blockchain_query": INVALID_BLOCKCHAIN_QUERY,
        "invalid_limit_query": INVALID_LIMIT_QUERY,
        "invalid_filter_query": INVALID_FILTER_QUERY,
        "invalid_address_format_query": INVALID_ADDRESS_FORMAT_QUERY,
        "response_schema": RESPONSE_SCHEMA
    }

# Positive tests


def test_graphql_query_success(graphql_client, test_data):
    """
    Tests that the GraphQL query returns a successful response with a status code of 200.
    """
    response = graphql_client.query(test_data["valid_query"])
    assert response["data"] is not None
    assert "errors" not in response


def test_graphql_query_data(graphql_client, test_data):
    """
    Tests that the GraphQL query returns the correct data based on the input provided.
    """
    response = graphql_client.query(test_data["valid_query"])
    assert response == test_data["valid_expected_data"]
    # Validate response data against schema
    validate(response, test_data["response_schema"])


def test_graphql_query_limit(graphql_client, test_data):
    """
    Tests that the GraphQL query returns the correct number of results based on the limit parameter provided.
    """
    limits = [5, 20, 50]
    for limit in limits:
        query = f"{test_data['valid_query']} first: {limit}"
        response = graphql_client.query(query)
        assert len(response["data"]["transactions"]["edges"]) == limit
# Test for invalid GraphQL queries


def test_graphql_query_invalid_syntax(graphql_client, test_data):
    """
    Tests that the GraphQL query returns an error message when the query syntax is invalid.
    """
    query = "invalid query"
    response = graphql_client.query(query)
    assert "errors" in response
    assert response["errors"][0]["message"] == "Syntax Error: Unexpected Name 'invalid'"


def test_graphql_query_invalid_field(graphql_client, test_data):
    """
    Tests that the GraphQL query returns an error message when the query includes an invalid field.
    """
    query = "{ transactions { invalidField } }"
    response = graphql_client.query(query)
    assert "errors" in response
    assert response["errors"][0]["message"] == "Cannot query field 'invalidField' on type 'TransactionConnection'."


def test_graphql_query_pagination(graphql_client, test_data):
    """
    Tests that the GraphQL query returns subsequent pages of data when a cursor input is provided.
    """
    # Execute the initial query to get the first page of data
    query = test_data["valid_query"]
    response = graphql_client.query(query)

    # Verify that the response contains the expected number of results
    expected_results = 10  # Replace with the number of expected results
    actual_results = len(response["data"]["transactions"]["edges"])
    assert actual_results == expected_results, f"Expected {expected_results} results, but got {actual_results} instead."

    # Save the end cursor for the next query
    end_cursor = response["data"]["transactions"]["pageInfo"]["endCursor"]

    # Loop through subsequent pages of data until there are no more results
    while response["data"]["transactions"]["pageInfo"]["hasNextPage"]:
        # Execute the next query using the end cursor from the previous query
        query = test_data["valid_query_with_cursor"].format(
            end_cursor=end_cursor)
        response = graphql_client.query(query)

        # Verify that the response contains the expected number of results
        expected_results = 10  # Replace with the number of expected results
        actual_results = len(response["data"]["transactions"]["edges"])
        assert actual_results == expected_results, f"Expected {expected_results} results, but got {actual_results} instead."

        # Save the end cursor for the next query
        end_cursor = response["data"]["transactions"]["pageInfo"]["endCursor"]


def test_graphql_query_rate_limit_exceeded(graphql_client, test_data):
    """
    Tests that the GraphQL query returns an error message when the rate limit is exceeded.
    """
    # Execute the same query repeatedly to exceed the rate limit
    query = test_data["valid_query"]
    for i in range(11):
        response = graphql_client.query(query)

    # Verify that the response contains an error message indicating that the rate limit has been exceeded
    assert "errors" in response
    assert response["errors"][0]["message"] == "You have exceeded the rate limit for this API endpoint."


def test_graphql_query_unauthorized(graphql_client, test_data):
    """
    Tests that the GraphQL query returns an error message when the request is unauthorized.
    """
    # Set up an invalid authorization token
    headers = {"Authorization": "Bearer invalid_token"}

    # Execute the query with the invalid token
    query = test_data["valid_query"]
    response = requests.post(graphql_client.url, json={
                             "query": query}, headers=headers)

    # Verify that the response contains an error message indicating that the request is unauthorized
    assert "errors" in response.json()
    assert response.json()["errors"][0]["message"] == "Unauthorized"

# Test for edge cases


def test_graphql_query_large_limit(graphql_client, test_data):
    """
    Tests that the GraphQL query returns the correct number of results when a large limit parameter is provided.
    """
    # Execute the query with a large limit parameter
    query = f"{test_data['valid_query']} first: 1000"
    response = graphql_client.query(query)

    # Verify that the response contains the expected number of results
    assert len(response["data"]["transactions"]["edges"]) == 1000


def test_graphql_query_invalid_input(graphql_client, test_data):
    """
    Tests that the GraphQL query returns an error message when the input is invalid.
    """
    # Execute the query with invalid input
    query = test_data["invalid_address_format_query"]
    response = graphql_client.query(query)

    # Verify that the response contains an error message indicating that the input is invalid
    assert "errors" in response


def test_graphql_query_unusual_input(graphql_client, test_data):
    """
    Tests that the GraphQL query handles unusual input correctly.
    """
    # Execute the query with unusual input
    query = test_data["valid_query"].replace("transactions", "transacti*ons")
    response = graphql_client.query(query)

    # Verify that the response contains an error message indicating that the input is invalid
    assert "errors" in response
    assert response["errors"][0]["message"] == "Cannot query field 'transacti' on type 'Query'"
