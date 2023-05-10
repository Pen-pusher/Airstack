VALID_QUERY = """
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

VALID_EXPECTED_DATA = {
    "data": {
        "transactions": {
            "edges": [
                {
                    "node": {
                        "hash": "0x1234567890abcdef",
                        "block": {"height": 12345},
                    }
                },
                {
                    "node": {
                        "hash": "0xabcdef1234567890",
                        "block": {"height": 12344},
                    }
                },
            ]
        }
    }
}

INVALID_BLOCKCHAIN_QUERY = """
query {
  transactions(blockchain: "invalid") {
    edges {
      node {
        hash
      }
    }
  }
}
"""

INVALID_LIMIT_QUERY = """
query {
  transactions(first: -1) {
    edges {
      node {
        hash
      }
    }
  }
}
"""

INVALID_FILTER_QUERY = """
query {
  transactions(filter: {invalidField: "invalidValue"}) {
    edges {
      node {
        hash
      }
    }
  }
}
"""

INVALID_ADDRESS_FORMAT_QUERY = """
query {
  transactions(address: "invalid") {
    edges {
      node {
        hash
      }
    }
  }
}
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "transactions": {
                    "type": "object",
                    "properties": {
                        "edges": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "node": {
                                        "type": "object",
                                        "properties": {
                                            "hash": {"type": "string"},
                                            "block": {
                                                "type": "object",
                                                "properties": {
                                                    "height": {"type": "integer"}
                                                },
                                                "required": ["height"],
                                            },
                                        },
                                        "required": ["hash", "block"],
                                    }
                                },
                                "required": ["node"],
                            },
                        }
                    },
                    "required": ["edges"],
                }
            },
            "required": ["transactions"],
        }
    },
    "required": ["data"],
}