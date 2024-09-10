from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
clickstream_data = [
    {"event_id": "1", "user_id": "user1", "event_type": "CLICK"},
    {"event_id": "2", "user_id": "user2", "event_type": "PAGE_VIEW"},
    {"event_id": "3", "user_id": "user1", "event_type": "SCROLL"}
]

@app.route('/clickstream', methods=['GET'])
def get_clickstream_data():
    return jsonify(clickstream_data)

@app.route('/clickstream/<event_id>', methods=['GET'])
def get_clickstream_by_id(event_id):
    event = next((item for item in clickstream_data if item["event_id"] == event_id), None)
    if event:
        return jsonify(event)
    else:
        return jsonify({"error": "Event not found"}), 404

@app.route('/clickstream', methods=['POST'])
def add_clickstream_event():
    new_event = request.json
    clickstream_data.append(new_event)
    return jsonify(new_event), 201

@app.route('/clickstream/<event_id>', methods=['DELETE'])
def delete_clickstream_event(event_id):
    global clickstream_data
    clickstream_data = [event for event in clickstream_data if event["event_id"] != event_id]
    return jsonify({"message": "Event deleted successfully"}), 204

if __name__ == '__main__':
    app.run(debug=True)
