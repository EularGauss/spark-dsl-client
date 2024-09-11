# Initial transformation string (if any)
transformation_string = ""


# Function to apply a UDF transformation
def apply_udf_transformation(data_set: str, column: str, udf_name: str):
    global transformation_string
    # Construct a new transformation string using the UDF
    new_transformation = f'{data_set}.withColumn("{column}", {udf_name}({dataset_name}.{column}))'

    # Update the transformation string
    if transformation_string:
        transformation_string += f".transform({new_transformation})"
    else:
        transformation_string = new_transformation


# Example: Function to simulate transforming a DataFrame with a UDF
def apply_transformation(transformation_type: str, column: str, udf_name: str):
    global transformation_string
    if transformation_type == "withColumn":
        apply_udf_transformation(column, udf_name)