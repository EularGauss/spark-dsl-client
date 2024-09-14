from abc import ABC, abstractmethod


allowed_transformations = [
        {"name": "map", "requires_lambda": True},
        {"name": "filter", "requires_lambda": True},
        {"name": "flatMap", "requires_lambda": True},
        {"name": "groupByKey", "requires_lambda": False},
        {"name": "reduceByKey", "requires_lambda": True},
        {"name": "distinct", "requires_lambda": False}
    ]

class Transformation(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def generate_transform(self):
        pass


class MapTransformation(Transformation):
    def __init__(self, lambda_function):
        self.lambda_function = lambda_function

    def generate_transform(self):
        return f"map({self.lambda_function})"


class FilterTransformation(Transformation):
    def __init__(self, lambda_function):
        self.lambda_function = lambda_function

    def generate_transform(self):
        return f"filter({self.lambda_function})"


class FlatMapTransformation(Transformation):
    def __init__(self, lambda_function):
        self.lambda_function = lambda_function

    def generate_transform(self):
        return f"flatMap({self.lambda_function})"


class GroupByKeyTransformation(Transformation):
    def generate_transform(self):
        return "groupByKey()"


class ReduceByKeyTransformation(Transformation):
    def __init__(self, lambda_function):
        self.lambda_function = lambda_function

    def generate_transform(self):
        return f"reduceByKey({self.lambda_function})"


class DistinctTransformation(Transformation):
    def generate_transform(self):
        return "distinct()"

    @staticmethod
    def convert_lambda_to_scala(lambda_function):
        # A simplified conversion for demonstration purposes
        if "lambda" in lambda_function:
            return lambda_function.split("lambda ")[1].strip()
        return lambda_function


# Factory class to generate transformation instances
class TransformationFactory:
    @staticmethod
    def create_transformation(transformation_type, lambda_function=None):
        if transformation_type == 'map':
            return MapTransformation(lambda_function)
        elif transformation_type == 'filter':
            return FilterTransformation(lambda_function)
        elif transformation_type == 'flatMap':
            return FlatMapTransformation(lambda_function)
        elif transformation_type == 'groupByKey':
            return GroupByKeyTransformation()
        elif transformation_type == 'reduceByKey':
            return ReduceByKeyTransformation(lambda_function)
        elif transformation_type == 'distinct':
            return DistinctTransformation()
        else:
            raise ValueError(f"Unknown transformation type: {transformation_type}")
# Example Usage
# if __name__ == "__main__":
#     dataset = [1, 2, 3, 4, 5]
#
#     transformations = [
#         MapTransformation("lambda x: x ** 2"),
#         FilterTransformation("lambda x: x % 2 == 0"),
#         FlatMapTransformation("lambda x: (x, x ** 2)"),
#         GroupByKeyTransformation(dataset),  # No lambda needed
#         ReduceByKeyTransformation("lambda x, y: x + y"),
#         DistinctTransformation(dataset)
#     ]
#
#     for transformation in transformations:
#         print(transformation.generate_transform())
