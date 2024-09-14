from abc import ABC, abstractmethod

allowed_aggregations = [
    {"name": "count", "requires_column": False},
    {"name": "sum", "requires_column": True},
    {"name": "avg", "requires_column": True},
    {"name": "min", "requires_column": True},
    {"name": "max", "requires_column": True},
    {"name": "groupBy", "requires_column": True}
]

class Aggregation(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate_aggregation(self):
        pass


class CountAggregation(Aggregation):
    def generate_aggregation(self):
        return "count()"


class SumAggregation(Aggregation):
    def __init__(self, column_name):
        self.column_name = column_name

    def generate_aggregation(self):
        return f"sum(\"{self.column_name}\")"


class AverageAggregation(Aggregation):
    def __init__(self, column_name):
        self.column_name = column_name

    def generate_aggregation(self):
        return f"avg(\"{self.column_name}\")"


class MinAggregation(Aggregation):
    def __init__(self, column_name):
        self.column_name = column_name

    def generate_aggregation(self):
        return f"min(\"{self.column_name}\")"


class MaxAggregation(Aggregation):
    def __init__(self, column_name):
        self.column_name = column_name

    def generate_aggregation(self):
        return f"max(\"{self.column_name}\")"


class GroupByAggregation(Aggregation):
    def __init__(self, group_by_column):
        self.group_by_column = group_by_column

    def generate_aggregation(self):
        return f"groupBy(\"{self.group_by_column}\")"


class AggregateFactory:
    @staticmethod
    def create_aggregation(aggregation_type, column_name=None):
        if aggregation_type == 'count':
            return CountAggregation()
        elif aggregation_type == 'sum':
            return SumAggregation(column_name)
        elif aggregation_type == 'avg':
            return AverageAggregation(column_name)
        elif aggregation_type == 'min':
            return MinAggregation(column_name)
        elif aggregation_type == 'max':
            return MaxAggregation(column_name)
        elif aggregation_type == 'groupBy':
            return GroupByAggregation(column_name)
        else:
            raise ValueError(f"Unknown aggregation type: {aggregation_type}")


# Example Usage
if __name__ == "__main__":
    aggregations = [
        CountAggregation(),
        SumAggregation("score"),
        AverageAggregation("age"),
        MinAggregation("age"),
        MaxAggregation("score"),
        GroupByAggregation("name")
    ]

    for aggregation in aggregations:
        print(aggregation.generate_aggregation())
