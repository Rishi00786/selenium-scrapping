from flask import Flask, jsonify, render_template
from scripts.selenium_script import fetch_trends
from database.mongo_utils import store_trends
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-trends')
def fetch_trends_route():
    # Fetch trends data and start/end times
    trends_data = fetch_trends()
    unique_id = str(uuid.uuid4())  # Generate unique ID

    # Store trends and IP address (optional step)
    store_trends(unique_id, trends_data["trends"], trends_data["ip_address"])

    # Return JSON with unique_id, trends, and other data
    return jsonify({
        "unique_id": unique_id,
        "trends": trends_data["trends"],
        "ip_address": trends_data["ip_address"],
        "record": { "_id": unique_id, "trends": trends_data["trends"] },
        "start_time": trends_data["start_time"],
        "end_time": trends_data["end_time"]
    })

if __name__ == '__main__':
    app.run()
