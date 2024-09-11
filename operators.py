import json

allowed_operators = {
    'string': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('contains', 'method'),
        ('startsWith', 'method'),
        ('endsWith', 'method'),
        ('regex', 'method')
    ],
    'long': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method')
    ],
    'double': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method')
    ],
    'enum': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('in', 'method')
    ],
    'map': [
        ('containsKey', 'method'),
        ('containsValue', 'method')
    ],
    'array': [
        ('array_contains', 'method'),
        ('in', 'method')
    ],
    'timestamp': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method')
    ],
    'null': [
        ('isNull', 'method'),
        ('isNotNull', 'method')
    ]
}


def get_columns_and_types(schema_file_path):
    """
    Reads a schema JSON file and returns a dictionary of column names and their types.

    :param schema_file_path: The path to the JSON schema file.
    :return: A dictionary with column names as keys and their types as values.
    """
    try:
        # Read the schema file
        with open(schema_file_path, 'r') as file:
            schema_json = json.load(file)

        # Initialize a dictionary to hold column names and types
        columns_types = {}

        # Extract fields from the JSON schema
        fields = schema_json.get('fields', [])

        for field in fields:
            column_name = field.get('name')
            column_type = map_column_type(field.get('type'))

            # Store the column name and its type
            columns_types[column_name] = column_type

        return columns_types

    except FileNotFoundError:
        print(f"Error: The file {schema_file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: The schema file is not a valid JSON.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def map_column_type(type_value):
    """
    Maps the schema types to a more Python-readable format.

    :param type_value: The type from the schema.
    :return: The corresponding type as a string.
    """
    if isinstance(type_value, str):
        return type_value  # Return as-is for simple types
    elif isinstance(type_value, dict) and type_value.get('type') == 'enum':
        return type_value.get('name')
    elif isinstance(type_value, list):
        # Handle Union types in schema
        for item in type_value:
            if isinstance(item, str):
                return item  # Return the first simple type found
    else:
        return 'unknown'  # Handle unknown types


# Example usage
schema_path = 'root/schema/clickstream_schema.json'  # Replace with your actual schema path
columns_with_types = get_columns_and_types(schema_path)

# Print the columns and their types
for column, col_type in columns_with_types.items():
    print(f"Column: {column}, Type: {col_type}")
