from filter import FilterFactory


def test_long_filter():

    # Reset filter_string before tests
    long_filter = FilterFactory.create_filter("long")
    assert long_filter.generate_filter("column_name", "=", 10) == "col(\"column_name\") = 10"


def test_string_filter():
    string_filter = FilterFactory.create_filter("string")
    assert string_filter.generate_filter("column_name", "contains", "name") == "col(\"column_name\").contains(\"name\")"


def test_array_filter():
    array_filter = FilterFactory.create_filter("array")
    assert array_filter.generate_filter("column_name", "in", ["value1", "value2"]) == "col(\"column_name\").isin(\"value1\", \"value2\")"
