from flask import Flask, jsonify, request, session
from flask_cors import CORS

from aggregate import allowed_aggregations, AggregateFactory
from filter import FilterFactory
from schema import parse_schema, schema_directory, get_all_schema_names
from transform import allowed_transformations, TransformationFactory

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

session = {}

schemas = get_all_schema_names()


# Function to initialize user state
def initialize_user_state():
    return {
        'schema': None,
        'dataset_name': "df",
        'filters': [],
        'transformations': [],
        'aggregations': []
    }


@app.route('/initialize', methods=['POST'])
def initialize():
    global session
    session = initialize_user_state()
    return jsonify({"status": "State initialized"})


@app.route('/schemas', methods=['GET'])
def get_schemas():
    global schemas

    return jsonify({
        "schemas": schemas
    })


@app.route('/schema/<schema_name>', methods=['POST'])
def select_schema(schema_name):
    global session
    if not schema_name:
        return jsonify({
            "status": "Schema not provided",
            "code": 400
        })
    schema_data = parse_schema(schema_name)
    # Reset state if a new schemas is selected
    session = initialize_user_state()
    session['selected_schema'] = schema_data

    return jsonify({
        "status": "Schema selected",
        "selected_schema": session['selected_schema'],
    })


@app.route('/filter/add', methods=['POST'])
def add_filter():
    global session
    req = request.get_json()
    col_name, type= req.get("name", ""), req.get("type", "")
    operator, value = req.get("operator", ""), req.get("value", "")
    try:
        filter = FilterFactory.create_filter(type)
        filter_data = filter.generate_filter(col_name, operator, value)
    except Exception as e:
        return jsonify({
            "status": "Invalid filter type",
            "message": str(e),
            "code": 400
        })
    # Ensure user state is initialized
    if not session:
        session = initialize_user_state()

    session['filters'].append(filter_data)
    return jsonify({
        "status": "Filter added",
        "filters": session['filters']
    })


@app.route('/transformations', methods=['GET'])
def get_transformations():
    return jsonify({
        "status": "success",
        "transformations": allowed_transformations
    })

@app.route('/aggregations', methods=['GET'])
def get_aggregations():
    return jsonify({
        "status": "success",
        "aggregations": allowed_aggregations
    })


@app.route('/transformation/add', methods=['POST'])
def add_transformation():
    global session
    transformation_data = request.json
    # Ensure user state is initialized
    if not session:
        session = initialize_user_state()
    try:
        transformation = TransformationFactory.create_transformation(transformation_data.get("type"), transformation_data.get("function"))
        filter_data = transformation.generate_transform()
    except Exception as e:
        return jsonify({
            "status": "Invalid filter type",
            "message": str(e),
            "code": 400
        })
    session['transformations'].append(filter_data)
    return jsonify({
        "status": "Transformation added",
        "transformations": session['transformations']
    })


@app.route('/aggregations/add', methods=['POST'])
def add_aggregations():
    global session
    aggregation_data = request.json
    # Ensure user state is initialized
    if not session:
        session = initialize_user_state()
    try:
        aggregations = AggregateFactory.create_aggregation(aggregation_data.get("type"), aggregation_data.get("column"))
        aggregation_data = aggregations.generate_aggregation()
    except Exception as e:
        return jsonify({
            "status": "Invalid filter type",
            "message": str(e),
            "code": 400
        })
    session['aggregations'].append(aggregation_data)
    return jsonify({
        "status": "Transformation added",
        "aggregations": session['aggregations']
    })


@app.route("/session/reset", methods=["POST"])
def clear_session():
    global session
    session = {}
    return jsonify({"status": "session cleared"})


@app.route('/query', methods=['GET'])
def get_full_query():
    query = session.get("dataset_name")
    for filter in session.get('filters', []):
        query += f".filter({filter})"
    for transformation in session.get('transformations', []):
        query += f".{transformation}"
    for aggreation in session.get('aggregations', []):
        query += f".{aggreation}"
    return jsonify({"query": query})


if __name__ == "__main__":
    app.run(port=5011)