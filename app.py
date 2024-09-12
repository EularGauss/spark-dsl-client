from flask import Flask, jsonify, request, session

from operators import allowed_operators
from schema import parse_schema

app = Flask(__name__)

session = {}


# Function to initialize user state
def initialize_user_state():
    return {
        'dataset_name': "df",
        'filters': [],
        'transformations': [],
        'aggregations': []
    }


@app.route('/initialize', methods=['POST'])
def initialize():
    session['user_state'] = initialize_user_state()
    return jsonify({"status": "State initialized"})


@app.route('/select_schema', methods=['POST'])
def select_schema():
    schema_name = request.get_data("schema")
    schema_data = parse_schema(schema_name)
    session['selected_schema'] = schema_data.get('schemas')

    # Reset state if a new schemas is selected
    session['user_state'] = initialize_user_state()

    return jsonify({
        "status": "Schema selected",
        "selected_schema": session['selected_schema'],
        "user_state": session['user_state']
    })


@app.route('/add_filter', methods=['POST'])
def add_filter():
    filter_data = request.json
    # Ensure user state is initialized
    if 'user_state' not in session:
        session['user_state'] = initialize_user_state()

    session['user_state']['filters'].append(filter_data)
    return jsonify({
        "status": "Filter added",
        "filters": session['user_state']['filters']
    })


@app.route('/add_transformation', methods=['POST'])
def add_transformation():
    transformation_data = request.json
    # Ensure user state is initialized
    if 'user_state' not in session:
        session['user_state'] = initialize_user_state()

    session['user_state']['transformations'].append(transformation_data)
    return jsonify({
        "status": "Transformation added",
        "transformations": session['user_state']['transformations']
    })

@app.route("/clear_session", method="POST")
def clear_session():
    session = {}
    return jsonify({"status": "session cleared"})

@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify(session.get('user_state', initialize_user_state()))