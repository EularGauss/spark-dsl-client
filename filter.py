# Function to apply a filter condition
from abc import ABC, abstractmethod


class TypeFilter(ABC):
    @abstractmethod
    def generate_filter(self, column_name, operator, value):
        pass


class LongFilter(TypeFilter):
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
    def generate_filter(self, column_name, operator, value):
        if operator == 'contains':
            return f"col(\"{column_name}\").contains(\"{value}\")"
        elif operator == 'in':
            value_list = ', '.join(map(lambda v: f'\"{v}\"', value))
            return f"col(\"{column_name}\") in ({value_list})"
        else:
            raise ValueError(f"Unsupported operator: {operator} for ArrayFilter.")


class MapFilter(TypeFilter):
    def generate_filter(self, column_name, operator, key):
        if operator == 'containsKey':
            return f"col(\"{column_name}\").containsKey(\"{key}\")"
        elif operator == 'containsValue':
            return f"col(\"{column_name}\").values.contains(\"{key}\")"
        else:
            raise ValueError(f"Unsupported operator: {operator} for MapFilter.")


class EnumFilter(TypeFilter):
    def generate_filter(self, column_name, operator, value):
        if operator == '=':
            return f"col(\"{column_name}\") === \"{value}\""
        elif operator == '!=':
            return f"col(\"{column_name}\") =!= \"{value}\""
        elif operator == 'in':
            if isinstance(value, (list, tuple)):
                value_list = ", ".join(map(lambda v: f'\"{v}\"', value))
                return f"col(\"{column_name}\") in " + f'({value_list})'
            else:
                return f"col(\"{column_name}\") in " + f'(\"{value}\")'
        else:
            raise ValueError(f"Unsupported operator: {operator} for EnumFilter.")


class NullFilter(TypeFilter):
    def generate_filter(self, column_name, operator, _):
        if operator == 'isNull':
            return f"col(\"{column_name}\") isNull"
        elif operator == 'isNotNull':
            return f"col(\"{column_name}\") isNotNull"
        else:
            raise ValueError(f"Unsupported operator: {operator} for NullFilter.")


class TimestampFilter(TypeFilter):
    def generate_filter(self, column_name, operator, value):
        if operator == '=':
            return f"col(\"{column_name}\") === \"{value}\""
        elif operator == '!=':
            return f"col(\"{column_name}\") =!= \"{value}\""
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
        elif column_type == "null":
            return NullFilter()
        else:
            raise ValueError(f"Unsupported column type: {column_type}")


