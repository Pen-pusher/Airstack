# Airstack
 Code for testing GraphQL API endpoint with pytest and requests library. Includes positive and negative tests for different query types.
# GraphQL API Testing with Pytest
This module contains a set of automated tests for a GraphQL API. It uses Pytest as the testing framework and the requests library for making HTTP requests to the API endpoint.

# Prerequisites
Before running the tests, ensure that the following software is installed on your machine:

Python 3.6 or later
Pytest
requests
jsonschema

# Getting Started
To run this code, you will need to have Python 3 and the required packages installed on your machine.

Start by cloning or downloading the code from the source repository.

Open a terminal or command prompt and navigate to the root directory of the project.

Install the required packages by running the following command:


# pip install -r requirements.txt

This will install the required packages specified in the "requirements.txt" file.

To run the tests, enter the following command:

# pytest

This will execute all the test functions defined in the code.

# Note: The tests assume that the GraphQL API endpoint is available at the specified URL. If the URL changes or the endpoint becomes unavailable, the tests will fail.

# Test Fixtures

The test fixtures  provide reusable setup and teardown logic for the tests. The graphql_client fixture creates an instance of the GraphQLClient class with the URL of the API endpoint to be tested. The test_data fixture loads test data from a separate module and returns it as a dictionary.

# Writing Tests
The tests  are organized into two categories: positive tests and tests for invalid GraphQL queries.

# Positive Tests
The positive tests verify that the GraphQL query returns the expected data when valid input is provided. The following positive tests are included:

#test_graphql_query_success: Tests that the GraphQL query returns a successful response with a status code of 200.
test_graphql_query_data: Tests that the GraphQL query returns the correct data based on the input provided.
test_graphql_query_limit: Tests that the GraphQL query returns the correct number of results based on the limit parameter provided.
test_graphql_query_pagination: Tests that the GraphQL query returns subsequent pages of data when a cursor input is provided.

# Tests for Invalid GraphQL Queries
The tests for invalid GraphQL queries verify that the API returns an error message when invalid input is provided. The following tests for invalid GraphQL queries are included:

test_graphql_query_invalid_syntax: Tests that the GraphQL query returns an error message when the query syntax is invalid.
test_graphql_query_invalid_field: Tests that the GraphQL query returns an error message when the query includes an invalid field.
test_graphql_query_rate_limit_exceeded: Tests that the GraphQL query returns an error message when the rate limit is exceeded.

# Conclusion
This module provides a set of automated tests for a GraphQL API using Pytest. By using these tests, you can ensure that the API behaves as expected and that any changes to the API do not introduce regressions.
