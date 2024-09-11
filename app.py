from flask import Flask, jsonify, request, session

from operators import allowed_operators

app = Flask(__name__)


# Function to initialize user state
def initialize_user_state():
    return {
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
    schema_data = request.json
    session['selected_schema'] = schema_data.get('schema')

    # Reset state if a new schema is selected
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


@app.route('/get_state', methods=['GET'])
def get_state():
    return jsonify(session.get('user_state', initialize_user_state()))