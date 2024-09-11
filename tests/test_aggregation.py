
from aggregate import (
    CountAggregation, SumAggregation, AverageAggregation,
    MinAggregation, MaxAggregation, GroupByAggregation,
    AggregateFactory
)

def test_aggregate_factory_sum():
    factory_sum = AggregateFactory.create_aggregation('sum', "score")
    assert factory_sum.generate_aggregation() ==  "sum(score)"


def test_aggregate_factory_avg():
    factory_avg = AggregateFactory.create_aggregation('avg', "age")
    assert factory_avg.generate_aggregation() ==  "avg(age)"


def test_aggregate_factory_min():
    factory_min = AggregateFactory.create_aggregation('min', "age")
    assert factory_min.generate_aggregation() ==  "min(age)"


def test_aggregate_factory_max():
    factory_max = AggregateFactory.create_aggregation('max', "score")
    assert factory_max, MaxAggregation
    assert factory_max.generate_aggregation() ==  "max(score)"


def test_aggregate_factory_group_by():
    factory_group_by = AggregateFactory.create_aggregation('groupBy', "name")
    assert factory_group_by, GroupByAggregation
    assert factory_group_by.generate_aggregation() ==  "groupBy(name)"




