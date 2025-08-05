# async-pchb-verifier/generate_report.py
import json
import os
from pathlib import Path

def format_trojans(detections):
    """Helper function to format trojan detections"""
    if not detections:
        return "<p class='success'>✓ No trojans detected</p>"
    
    table_rows = []
    for d in detections:
        table_rows.append(f"""
        <tr>
            <td>{d['name']}</td>
            <td>{d['type']}</td>
            <td>{d['severity']}</td>
            <td><pre>{d['model']}</pre></td>
        </tr>
        """)
    
    return f"""
    <table>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Model</th>
        </tr>
        {"".join(table_rows)}
    </table>
    """

def generate_html_report(json_file: str, output_dir: str = "results/latest_run"):
    """Convert JSON results to interactive HTML"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    with open(json_file, encoding='utf-8') as f: 
        data = json.load(f)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PCHB Verification Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            .violation {{ color: #e74c3c; font-weight: bold; }}
            .success {{ color: #27ae60; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            pre {{ margin: 0; }}
        </style>
    </head>
    <body>
        <h1>PCHB Verification Report</h1>
        
        <h2>Handshake Compliance</h2>
        {"<p class='violation'>❌ " + "<br>".join(data['results']['handshake_violations']) + "</p>" 
         if data['results']['handshake_violations'] 
         else "<p class='success'>✓ No violations detected</p>"}
        
        <h2>Trojan Detections</h2>
        {format_trojans(data['results']['trojan_detections'])}
        
        <h2>Timing Violations</h2>
        {"<p class='violation'>❌ " + "<br>".join(data['results']['timing_violations']) + "</p>" 
         if data['results']['timing_violations'] 
         else "<p class='success'>✓ No violations detected</p>"}
    </body>
    </html>
    """
    
    output_path = os.path.join(output_dir, "pchb_report.html")
    with open(output_path, 'w', encoding='utf-8') as f:  # Add encoding here
        f.write(html_content)