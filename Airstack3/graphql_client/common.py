from jsonschema import validate


def validate_response(response: Dict, schema: Dict):
    """
    Validates a GraphQL response against a JSON schema.

    :param response: The response to validate.
    :param schema: The JSON schema to validate against.
    """
    validate(response, schema)