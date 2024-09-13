from flask import Flask, jsonify, request, session

from filter import FilterFactory
from operators import allowed_operators
from schema import parse_schema

app = Flask(__name__)

session = {}


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


@app.route('/select_schema', methods=['POST'])
def select_schema():
    global session
    req = request.get_json()
    schema_name = req.get('schema')
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


@app.route('/add_filter', methods=['POST'])
def add_filter():
    global session
    req = request.get_json()
    col_name, type, operator, value = req.get("name"), req.get("type"), req.get("operator"), req.get("value")
    try:
        filter_data = FilterFactory.create_filter(type).generate_filter(col_name, operator, value)
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


@app.route('/add_transformation', methods=['POST'])
def add_transformation():
    global session
    transformation_data = request.json
    # Ensure user state is initialized
    if not session:
        session = initialize_user_state()

    session['transformations'].append(transformation_data)
    return jsonify({
        "status": "Transformation added",
        "transformations": session['user_state']['transformations']
    })


@app.route("/clear_session", methods=["POST"])
def clear_session():
    session = {}
    return jsonify({"status": "session cleared"})


@app.route('/get_full_query', methods=['GET'])
def get_full_query():
    query = session.get("dataset_name")
    for filter in session.get('filters', []):
        query += f".filter({filter})"
    for transformation in session.get('transformations', []):
        query += f".transform({transformation})"
    for aggreation in session.get('transformations', []):
        query += f".aggs({aggreation})"
    return jsonify({"query": query})


if __name__ == "__main__":
    app.run(port=5011)