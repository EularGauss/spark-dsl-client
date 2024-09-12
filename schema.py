import json
import os

schema_directory = os.getcwd() + "/schemas"


def parse_schema(schema_name):
    """
    Parses the Avro-like schemas from a JSON file and returns a mapping of column names to their types and attributes.

    Args:
        schema_name (str): The name of the JSON schemas file (without .json extension).

    Returns:
        dict: A mapping of column names to their types and additional information.
    """
    # Construct the file path
    file_path = schema_directory +  f"/{schema_name}.json"

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The schemas file {file_path} does not exist.")

    # Read the schemas from the JSON file
    with open(file_path, 'r') as file:
        schema = json.load(file)

    parsed_map = {}

    # Function to parse fields recursively
    def parse_fields(fields):
        for field in fields:
            column_name = field.get("name")
            column_type = field.get("type")
            column_doc = field.get("doc", "")
            parsed_map[column_name] = {"type": get_type(column_type), "doc": column_doc}

    def get_type(field_type):
        if isinstance(field_type, dict):
            # Check for specific type structures
            if field_type.get("type") == "enum":
                return field_type.get("symbols", [])  # Return only symbols of the enum
            elif field_type.get("type") == "record":
                # For nested records, parse the fields of the record
                parse_fields(field_type.get("fields", []))
                return "record"  # Return just the string "record"
            elif field_type.get("type") == "map":
                return "map"  # Return just the string "map"
            elif isinstance(field_type.get("type"), list):
                return {
                    "type": "union",
                    "types": [get_type(t) for t in field_type.get("type")]
                }
        else:
            return field_type  # For primitive types (e.g., string, long)

    # Parse the main schemas fields
    parse_fields(schema.get("fields", []))

    return parsed_map

#
# # Example usage
# if __name__ == '__main__':
#     try:
#         schema_name = 'click_stream'  # Specify the schemas name without .json
#         parsed_schema = parse_schema(schema_name)
#         print(json.dumps(parsed_schema, indent=2))
#     except Exception as e:
#         print(f"Error: {e}")