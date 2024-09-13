# Function to apply a filter condition
from abc import ABC, abstractmethod

from operators import allowed_operators


class TypeFilter(ABC):
    type = None
    @abstractmethod
    def generate_filter(self, column_name, operator, value):
        pass


class LongFilter(TypeFilter):
    type = 'long'
    def generate_filter(self, column_name, operator, value):
        if operator == '=':
            return f"col(\"{column_name}\") = {value}"
        elif operator == '!=':
            return f"col(\"{column_name}\") != {value}"
        elif operator == '>':
            return f"col(\"{column_name}\") > {value}"
        elif operator == '<':
            return f"col(\"{column_name}\") < {value}"
        elif operator == '>=':
            return f"col(\"{column_name}\") >= {value}"
        elif operator == '<=':
            return f"col(\"{column_name}\") <= {value}"
        elif operator == 'between':
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return f"col(\"{column_name}\") >= {value[0]} && col(\"{column_name}\") <= {value[1]}"
            else:
                raise ValueError("For 'between' operator, value must be a tuple or list of two items.")
        else:
            raise ValueError(f"Unsupported operator: {operator} for LongFilter.")


class StringFilter(TypeFilter):
    type = 'string'
    def generate_filter(self, column_name, operator, value):
        if operator == 'contains':
            return f"col(\"{column_name}\").contains(\"{value}\")"
        elif operator == 'startsWith':
            return f"col(\"{column_name}\").startsWith(\"{value}\")"
        elif operator == 'endsWith':
            return f"col(\"{column_name}\").endsWith(\"{value}\")"
        elif operator == 'isNull':
            return f"col(\"{column_name}\").isNull"
        elif operator == 'isNotNull':
            return f"col(\"{column_name}\").isNotNull"
        else:
            raise ValueError(f"Unsupported operator: {operator} for StringFilter.")


class ArrayFilter(TypeFilter):
    type = 'array'
    def generate_filter(self, column_name, operator, value):
        if operator == 'contains':
            return f"col(\"{column_name}\").contains(\"{value}\")"
        elif operator == 'in':
            value_list = ', '.join(map(lambda v: f'\"{v}\"', value))
            return f"col(\"{column_name}\") in ({value_list})"
        else:
            raise ValueError(f"Unsupported operator: {operator} for ArrayFilter.")


class MapFilter(TypeFilter):
    type = 'map'
    def generate_filter(self, column_name, operator, key):
        if operator == 'containsKey':
            return f"col(\"{column_name}\").containsKey(\"{key}\")"
        elif operator == 'containsValue':
            return f"col(\"{column_name}\").values.contains(\"{key}\")"
        else:
            raise ValueError(f"Unsupported operator: {operator} for MapFilter.")


class EnumFilter(TypeFilter):
    type = 'enum'
    def generate_filter(self, column_name, operator, value):
        if operator == '=':
            return f"col(\"{column_name}\") == \"{value}\""
        elif operator == '!=':
            return f"col(\"{column_name}\") != \"{value}\""
        elif operator == 'in':
            if isinstance(value, (list, tuple)):
                value_list = ", ".join(map(lambda v: f'\"{v}\"', value))
                return f"col(\"{column_name}\") in " + f'({value_list})'
            else:
                return f"col(\"{column_name}\") in " + f'(\"{value}\")'
        else:
            raise ValueError(f"Unsupported operator: {operator} for EnumFilter.")


class NullFilter(TypeFilter):
    type = 'null'
    def generate_filter(self, column_name, operator, _):
        if operator == 'isNull':
            return f"col(\"{column_name}\").isNull"
        elif operator == 'isNotNull':
            return f"col(\"{column_name}\").isNotNull"
        else:
            raise ValueError(f"Unsupported operator: {operator} for NullFilter.")


class RecordFilter(TypeFilter):
    type = 'record'

    def __init__(self, inner_filters):
        # inner_filters is expected to be a dictionary where keys are the field names
        # and values are the corresponding TypeFilter objects for those fields
        self.inner_filters = inner_filters

    def generate_filter(self, column_name, operator, value):
        # Generate filters for the inner fields of the record based on the operator
        filters = []

        for field_name, field_value in value.items():
            if field_name in self.inner_filters:
                inner_filter = self.inner_filters[field_name]
                filters.append(inner_filter.generate_filter(f"{column_name}.{field_name}", operator, field_value))
            else:
                raise ValueError(f"Field '{field_name}' is not valid for the RecordFilter of type '{column_name}'.")

class TimestampFilter(TypeFilter):
    type = 'timestamp'
    def generate_filter(self, column_name, operator, value):
        if operator == '=':
            return f"col(\"{column_name}\") == \"{value}\""
        elif operator == '!=':
            return f"col(\"{column_name}\") != \"{value}\""
        elif operator == '>':
            return f"col(\"{column_name}\") > \"{value}\""
        elif operator == '<':
            return f"col(\"{column_name}\") < \"{value}\""
        elif operator == '>=':
            return f"col(\"{column_name}\") >= \"{value}\""
        elif operator == '<=':
            return f"col(\"{column_name}\") <= \"{value}\""
        elif operator == 'between':
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return f"col(\"{column_name}\") >= \"{value[0]}\" && col(\"{column_name}\") <= \"{value[1]}\""
            else:
                raise ValueError("For 'between' operator, value must be a tuple or list of two items.")
        else:
            raise ValueError(f"Unsupported operator: {operator} for TimestampFilter.")


class FilterFactory:
    @staticmethod
    def create_filter(column_type):
        if column_type == "long":
            return LongFilter()
        elif column_type == "string":
            return StringFilter()
        elif column_type == "array":
            return ArrayFilter()
        elif column_type == "map":
            return MapFilter()
        elif column_type == "enum":
            return EnumFilter()
        elif column_type.startswith("union:"):
            # Extract the two types for union
            types = column_type.split(":")[1].split(",")
            if len(types) != 2:
                raise ValueError("UnionFilter requires exactly two types.")
            # Create filters for the two types in the union
            filter1 = FilterFactory.create_filter(types[0].strip())
            filter2 = FilterFactory.create_filter(types[1].strip())
            return UnionFilter(filter1, filter2)
        elif column_type == "null":
            return NullFilter()
        else:
            raise ValueError(f"Unsupported column type: {column_type}")


class UnionFilter(TypeFilter):
    def __init__(self, filter1, filter2):
        self.filter1 = filter1
        self.filter2 = filter2

    def generate_filter(self, column_name, operator, value):
        for t in allowed_operators[self.filter1.type]:
            if t[0] == operator:
                return self.filter1.generate_filter(column_name, operator, value)
        for t in allowed_operators[self.filter2.type]:
            if t[0] == operator:
                return self.filter2.generate_filter(column_name, operator, value)
        raise ValueError(f"Unsupported operator: {operator} for UnionFilter.")