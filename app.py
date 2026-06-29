import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "events.json")

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

def load_events():
    if not os.path.exists(DATA_FILE):
        return [Event(1, "Tech Meetup"), Event(2, "Python Workshop")]

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Event(event["id"], event["title"]) for event in data]


def save_events():
    data = [{"id": event.id, "title": event.title} for event in events]
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


# In-memory "database"
events = load_events()

# Get Events
@app.route('/events', methods=['GET'])
def get_events():
    return (jsonify([event.to_dict() for event in events]), 200)

#GET /events/<id>
@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = next((event for event in events if event.id == id), None)
    return jsonify(event.to_dict()) if event else ('Event not found', 404)
# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not events:
        new_id = 1
    else:
        new_id = max((event.id for event in events), default=0) + 1

    new_event = Event(id=new_id, title=data["title"])
    events.append(new_event)
    save_events()
    return jsonify(new_event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    event = next((event for event in events if event.id == event_id), None)

    if not event:
        return ('Event not found', 404)

    if "title" in data:
        event.title = data["title"]

    save_events()
    return jsonify(event.to_dict()), 200

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((event for event in events if event.id == event_id), None)

    if not event:
        return ('Event not found', 404)

    events.remove(event)
    save_events()
    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)
