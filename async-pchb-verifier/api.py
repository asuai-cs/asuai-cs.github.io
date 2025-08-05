from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    result = subprocess.run(
        ['python', 'pchb_verifier.py'],
        capture_output=True, text=True
    )
    return jsonify({
        'output': result.stdout,
        'report': 'results/latest_run/pchb_report.html'
    })

if __name__ == '__main__':
    app.run(port=5002)