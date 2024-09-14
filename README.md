## Features
1. This tool can accept avro schema file and can help generate scala code for spark jobs.


## Usage
1. Place the schema file in schemas folder
2. Run the docker-comose file using the command `docker-compose up`

## Limitations
1. The tool does not check the UDF validity
2. The correctness of the individual filter, aggregation and transformations are checked but
the correctness of the entire job is not checked.
3. Some of the supported operators for some types (ex. between for enum type) are not supported

### Solution for limitations
1. UDF validity can be supported with another validator specifically for scala functions and can be integrated with this tool.
2. The correctness of the entire job can be checked by running the generated code on a sample data and checking the output.
3. For validity check of the entire job can be supported by a plugin on submit click
4. All the operators have the required data to support more complex operations but due to the lack of time, they are not implemented.
