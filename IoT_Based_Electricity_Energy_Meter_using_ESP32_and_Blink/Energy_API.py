```python
"""
Project: IoT-Based Smart Energy Monitoring System (REST API)

Summary:
This Flask-based REST API serves historical energy data from the SQLite database to the web dashboard. It runs on the same server as the MQTT and ML script, providing endpoints to fetch recent energy data for visualization. The API supports CORS for cross-origin requests from the React dashboard.

Implementation Details:
1. Software Setup:
   - Installed Flask and flask-cors alongside existing Python dependencies.
   - Ensured SQLite database 'energy_data.db' is accessible.
   - Ran the API on port 5000 (configurable).

2. API Endpoints:
   - /history: Returns the last 100 records of energy data (timestamp, voltage, current, power, predicted_power).
   - Ensured JSON format for compatibility with the React dashboard.

3. Testing and Deployment:
   - Tested API locally using `curl` or Postman.
   - Deployed with Gunicorn or similar for production on AWS EC2 or local server.
   - Configured Nginx as a reverse proxy to handle HTTPS.

4. Optimization:
   - Limited query results to prevent performance issues.
   - Added error handling for database connection failures.
   - Secured API with authentication for production (not implemented here).

Note: Run this script alongside Energy_Server.py on the same server. Ensure port 5000 is open and CORS is configured correctly.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/history', methods=['GET'])
def get_history():
    try:
        conn = sqlite3.connect('energy_data.db')
        c = conn.cursor()
        c.execute("SELECT timestamp, voltage, current, power, predicted_power FROM energy_data ORDER BY timestamp DESC LIMIT 100")
        rows = c.fetchall()
        conn.close()
        
        data = [
            {
                "timestamp": row[0],
                "voltage": row[1],
                "current": row[2],
                "power": row[3],
                "predicted_power": row[4]
            } for row in rows
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```