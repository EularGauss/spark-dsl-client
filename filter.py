# Function to apply a filter condition
def apply_filter(dataset_name: str, column: str, condition: str, value: int):
    global filter_string
    # Create a new filter condition
    new_condition = f"{column} {condition} {value}"

    # If we have existing filters, append the new one
    if filter_string:
        filter_string += f".filter({new_condition})"
    else:
        filter_string = f"{dataset_name}.filter({new_condition})"