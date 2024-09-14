import json

allowed_operators = {
    'string': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('contains', 'method', 'single_input'),
        ('startsWith', 'method', 'single_input'),
        ('endsWith', 'method', 'single_input'),
        ('regex', 'method', 'single_input')
    ],
    'long': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method', "double_input")
    ],
    'double': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method', "double_input")
    ],
    'enum': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('in', 'method', "list_input")
    ],
    'map': [
        ('containsKey', 'method', 'single_input'),
        ('containsValue', 'method', 'single_input'),
    ],
    'array': [
        ('array_contains', 'method', 'single_input'),
        ('in', 'method')
    ],
    'timestamp': [
        ('=', 'symbol'),
        ('!=', 'symbol'),
        ('>', 'symbol'),
        ('<', 'symbol'),
        ('>=', 'symbol'),
        ('<=', 'symbol'),
        ('between', 'method', "double_input")
    ],
    'null': [
        ('isNull', 'method', "no_input"),
        ('isNotNull', 'method' "no_input")
    ]
}


def get_columns_and_types(schema_file_path):
    """
    Reads a schemas JSON file and returns a dictionary of column names and their types.

    :param schema_file_path: The path to the JSON schemas file.
    :return: A dictionary with column names as keys and their types as values.
    """
    try:
        # Read the schemas file
        with open(schema_file_path, 'r') as file:
            schema_json = json.load(file)

        # Initialize a dictionary to hold column names and types
        columns_types = {}

        # Extract fields from the JSON schemas
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
        print("Error: The schemas file is not a valid JSON.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def map_column_type(type_value):
    """
    Maps the schemas types to a more Python-readable format.

    :param type_value: The type from the schemas.
    :return: The corresponding type as a string.
    """
    if isinstance(type_value, str):
        return type_value  # Return as-is for simple types
    elif isinstance(type_value, dict) and type_value.get('type') == 'enum':
        return type_value.get('name')
    elif isinstance(type_value, list):
        # Handle Union types in schemas
        for item in type_value:
            if isinstance(item, str):
                return item  # Return the first simple type found
    else:
        return 'unknown column type'