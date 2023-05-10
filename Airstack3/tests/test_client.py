import os
import pytest
from graphql_client.client import GraphQLClient
from graphql_client.common import validate_response
from graphql_client.test_data import (
    VALID_QUERY,
    VALID_EXPECTED_DATA,
    INVALID_BLOCKCHAIN_QUERY,
    INVALID_LIMIT_QUERY,
    INVALID_FILTER_QUERY,
    INVALID_ADDRESS_FORMAT_QUERY,
    RESPONSE_SCHEMA,
)


@pytest.fixture
def graphql_client():
    """
    A fixture that creates a GraphQLClient instance to be used in tests.
    """
    url = os.environ.get("GRAPHQL_API_URL")
    if not url:
        pytest.skip("GRAPHQL_API_URL environment variable not set")
    return GraphQLClient(url)


@pytest.fixture
def test_data():
    """
    A fixture that loads test data from the graphql_client.test_data module.
    """
    return {
        "valid_query": VALID_QUERY,
        "valid_expected_data": VALID_EXPECTED_DATA,
        "invalid_blockchain_query": INVALID_BLOCKCHAIN_QUERY,
        "invalid_limit_query": INVALID_LIMIT_QUERY,
        "invalid_filter_query": INVALID_FILTER_QUERY,
        "invalid_address_format_query": INVALID_ADDRESS_FORMAT_QUERY,
    }