from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/verify/<design>')
def verify(design):
    result = subprocess.run(
        ['python', 'formal_verifier.py', f'rtl_examples/{design}.v'],
        capture_output=True, text=True
    )
    return jsonify({
        'output': result.stdout,
        'report': 'security_report.html'
    })