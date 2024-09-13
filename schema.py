import json
import os
from abc import ABC, abstractmethod

from operators import allowed_operators  # Ensure it's correctly imported

schema_directory = os.getcwd() + "/schemas"


def get_all_schema_names():
    """
    Returns a list of all the schema names available in the schema directory.

    Returns:
        list: A list of schema names.
    """
    return [f.split(".")[0] for f in os.listdir(schema_directory) if f.endswith(".json")]


class BaseParser(ABC):
    def __init__(self, field):
        self.field = field

    @abstractmethod
    def parse(self):
        pass


class PrimitiveParser(BaseParser):
    def parse(self):
        column_name = self.field.get("name")
        column_type = self.field.get("type")
        return {
            "name": column_name,
            "type": column_type,
            "allowed_operators": allowed_operators.get(column_type, [])
        }


class RecordParser(BaseParser):
    def __init__(self, field, prefix=""):
        super().__init__(field,)
        self.prefix = prefix
        self.fields = field.get("type", {}).get("fields", [])

    def parse(self, prefix=""):
        parsed_fields = {}
        for f in self.fields:
            column_name = f.get("name")
            full_column_name = f"{self.prefix}.{column_name}" if self.prefix else column_name
            column_type = f.get("type")

            # Create an instance based on type
            if isinstance(column_type, dict) and column_type.get("type") == "record":
                nested_parser = RecordParser(f)
                parsed_fields.update(nested_parser.parse(full_column_name + "."))
            elif isinstance(column_type, dict) and column_type.get("type") == "enum":
                # Added handling for enum types
                primitive_parser = PrimitiveParser(f)
                parsed_fields[full_column_name] = primitive_parser.parse()
            elif isinstance(column_type, list) and all(isinstance(t, str) for t in column_type):
                union_parser = UnionParser(f)
                parsed_fields[full_column_name] = union_parser.parse()
            else:
                primitive_parser = PrimitiveParser(f)
                parsed_fields[full_column_name] = primitive_parser.parse()

        return parsed_fields


class UnionParser(BaseParser):
    def parse(self):
        allowed_ops = []
        column_name = self.field.get("name")
        types = self.field.get("type", [])
        name = column_name
        # Check that types are in list format
        if isinstance(types, list):
            for t in types:
                if isinstance(t, str):
                    name += f", {t}"
                    allowed_ops.extend(allowed_operators.get(t, []))

        return {
            "name": name,
            "type": "union",
            "allowed_operators": allowed_ops
        }


def parse_schema(schema):
    parsed_map = {}

    def parse_fields(fields):
        for field in fields:
            column_type = field.get("type")
            if isinstance(column_type, dict):
                if column_type.get("type") == "record":  # Check for record type
                    parser = RecordParser(field,field.get("name"))
                elif column_type.get("type") == "enum":  # Check for enum type
                    parser = PrimitiveParser(field.get("type"))  # Assuming PrimitiveParser handles enums
                else:
                    continue  # Skip unknown types
            elif isinstance(column_type, list):
                parser = UnionParser(field)  # Handle unions
            else:
                parser = PrimitiveParser(field)  # Handle primitives

            field_data = parser.parse()  # Get parsed data
            # Nested record type
            if not field_data.get("name", None):
                # process each record separately
                for k, v in field_data.items():
                    parsed_map[k] = v
            else:
                parsed_map[field_data.get("name")] = field_data

        # Read schema from the JSON file

    schema_file_path = os.path.join(schema_directory, f"{schema}.json")

    try:
        with open(schema_file_path, 'r') as schema_file:
            schema = json.load(schema_file)
    except FileNotFoundError:
        raise ValueError(f"Schema file '{schema_file_path}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from schema file '{schema_file_path}'.")
    # Parse the main schemas fields
    parse_fields(schema.get("fields", []))

    return parsed_map
