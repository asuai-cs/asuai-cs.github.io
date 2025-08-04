# Add new file 'showcase.py'
from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    with open('security_report.json') as f:
        data = json.load(f)
    return render_template('report.html', **data)

if __name__ == '__main__':
    app.run(port=5000)