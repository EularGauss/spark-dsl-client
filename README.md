## Overview 
This tool is designed to streamline the process of generating Scala code for Apache Spark jobs based on Avro schema files. It provides a user-friendly interface for specifying filter, transformation, and aggregation operations, facilitating the rapid development of data processing jobs in a Spark environment.
<img width="654" alt="Screenshot 2024-09-15 at 1 31 18 AM" src="https://github.com/user-attachments/assets/6a981fc7-a95f-4b30-b839-5743ccacaec7">




## Features
1. **Avro Schema Processing:** The tool accepts Avro schema files, which define the structure of the data. This allows users to leverage a standard format for data serialization when working with Spark.
2. **Scala Code Generation:** Upon receiving an Avro schema, the tool automatically generates the corresponding Scala code tailored for Spark jobs, enhancing development efficiency.
3. **User-Friendly Interface:** The application includes dropdown menus for selecting schema files and specifying desired operations, simplifying the interaction for users.

## Usage Instructions
To utilize the tool effectively, follow the steps outlined below 
1. You need to have `docker` and `docker-compose` installed on your machine. If you don't have them, you can install them by following the instructions provided [here](https://docs.docker.com/get-docker/).
2. **Schema File Placement:** Store your Avro schema files in the `schemas` directory within the project structure.
3. **Start the Application:** Use Docker Compose to build and run the application environment by executing the following command in your terminal:
```bash
docker-compose up
```
4. **Select Schema:** Once the application is running, access the interface on `localhost:3000` where you can select your desired schema file from a dropdown menu.
5. **Specify Operations:** Choose the appropriate filter, transformation, or aggregation queries from the provided dropdown lists. These options will dictate how the data is processed.
6. **Generate Code:** Click the "Add *" buttons to produce the Scala code based on the selected schema and operations. The code will be displayed on the screen for review (in `Current query` area) and further use.
7. Please note that the generated code is a template and may require additional modifications to suit your specific use case.
8. You can choose the filter, transformation, and aggregation operations in any order but they will be applied in the order `Filter -> Transformation -> Aggregation` in the generated code.

### Limitations
While the tool is powerful, several limitations must be considered:
1. **UDF Validity Check:** The tool does not perform validation on User Defined Functions (UDFs), which may lead to runtime errors if the provided functions are incorrect.
2. **Comprehensive Job Validation:** Although the correctness of individual filters, aggregations, and transformations is validated, the overall integrity and correctness of the complete Spark job is not verified.
3. **Unsupported Operations:** Certain operators may not be functional for specific data types (e.g., the "between" operator is not supported for enum types), limiting the tool's versatility.
4. **Non-Persistent Generated Code:** The generated Scala code is not persistent. If the page is refreshed or reset, all input data and the generated code will be lost.

### Proposed Solutions for Limitations
To address the limitations mentioned above, the following solutions are proposed for future development:
1. **Enhanced UDF Validation:** Introduce a dedicated UDF validator that checks the validity of Scala functions, integrating this feature into the current tool to mitigate potential runtime issues.
2. **Comprehensive Job Validation:** Implement a mechanism that runs the generated Scala code against sample data to verify the output and ensure the correctness of the entire Spark job.
3. **Operator Validity Enhancement:** Develop a plugin that validates operator applicability for the chosen data types upon submission, expanding the tool's operational capacity.
4. **Complex Operation Support:** Although the underlying architecture has the capability to handle more complex operations, implementation is pending due to time constraints. Future updates will focus on incorporating additional operators.


