
# GraphQL Client
This is a Python client for the GraphQL API endpoint at https://devapi.airstack.xyz/gql. The client provides a simple interface for executing GraphQL queries and handling responses.

# Installation
To install the client, run the following command:

# install graphql-client

# Usage

To use the client, create an instance of the 
GraphQLClient class and call the query
method with a GraphQL query string. The 
query method returns a dictionary containing the JSON response from the API endpoint.

graphql_client.client import GraphQLClient

client = GraphQLClient("https://devapi.airstack.xyz/gql")

query = """
query {
  transactions {
    edges {
      node {
        hash
        block {
          height
        }
      }
    }
  }
}
"""

response = client.query(query)
print(response)

# Testing

To run the tests, install 
and run the following command:

# pytest


The tests are defined in the 
# tests/test_client.py
module and cover various scenarios, including successful queries, invalid queries, and edge cases.

# Known Issues
At the time of writing, there are no known issues with the project. However, if you encounter any problems while running the tests or working with the code, please feel free to open an issue on the project repository.

# Conclusion
This module provides a set of automated tests for a GraphQL API using Pytest. By using these tests, you can ensure that the API behaves as expected and that any changes to the API do not introduce regressions.
