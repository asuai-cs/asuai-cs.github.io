def generate_html_report(json_file: str):
    """Convert JSON results to interactive HTML"""
    with open(json_file) as f:
        data = json.load(f)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PCHB Verification Report</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            .violation {{ color: #e74c3c; }}
            .trojan-model {{ font-family: monospace; }}
        </style>
    </head>
    <body>
        <h1>PCHB Verification Results</h1>
        
        <div id="handshake-results">
            <h2>Handshake Compliance</h2>
            <p>{len(data['results']['handshake_violations'])} violations</p>
        </div>
        
        <div id="trojan-results">
            <h2>Trojan Detections</h2>
            <svg id="trojan-chart" width="400" height="200"></svg>
            <div class="trojan-models">
                {self._format_trojan_findings(data['results']['trojan_detections'])}
            </div>
        </div>
        
        <script>
            // D3.js visualization
            const trojans = {json.dumps(data['results']['trojan_detections'])};
            const svg = d3.select("#trojan-chart");
            
            svg.selectAll("circle")
               .data(trojans)
               .enter()
               .append("circle")
               .attr("cx", (d,i) => 50 + i * 100)
               .attr("cy", 100)
               .attr("r", d => d.severity === 'critical' ? 20 : 10)
               .attr("fill", d => d.severity === 'critical' ? "red" : "orange");
        </script>
    </body>
    </html>
    """
    
    with open("pchb_report.html", "w") as f:
        f.write(html)

def _format_trojan_findings(detections: list) -> str:
    return "\n".join(
        f"<div class='trojan-model'><b>{d['name']}</b>: {d['model']}</div>"
        for d in detections
    )