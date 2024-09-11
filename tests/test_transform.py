from transform import TransformationFactory


def test_map_transformation():
    map_transformation = TransformationFactory.create_transformation('map',  "x => x ** 2")
    assert map_transformation.generate_transform() == "map(x => x ** 2)"


def test_filter_transformation():
    filter_transformation = TransformationFactory.create_transformation('filter',  "x => x % 2 == 0")
    assert filter_transformation.generate_transform() == "filter(x => x % 2 == 0)"


def test_flatMap_transformation():
    flat_map_transformation = TransformationFactory.create_transformation('flatMap',  "x => (x, x ** 2)")
    assert flat_map_transformation.generate_transform() == "flatMap(x => (x, x ** 2))"


def test_groupByKey_transformation():
    group_by_key_transformation = TransformationFactory.create_transformation('groupByKey')
    assert group_by_key_transformation.generate_transform() == "groupByKey()"


def test_reduceByKey_transformation():
    reduce_by_key_transformation = TransformationFactory.create_transformation('reduceByKey',  "(x, y) => x + y")
    assert reduce_by_key_transformation.generate_transform() == "reduceByKey((x, y) => x + y)"


def test_distinct_transformation():
    distinct_transformation = TransformationFactory.create_transformation('distinct')
    assert distinct_transformation.generate_transform() == "distinct()"

