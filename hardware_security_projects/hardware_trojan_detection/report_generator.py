"""
Verification Report Generator
This module generates comprehensive reports from verification results.
"""

import json
from datetime import datetime
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np

class ReportGenerator:
    def __init__(self):
        self.template = {
            'metadata': {
                'generated_at': None,
                'tool_version': '1.0',
                'verification_mode': 'formal'
            },
            'design_info': {},
            'verification_summary': {},
            'detailed_findings': [],
            'recommendations': []
        }
    
    def generate_html_report(self, results: Dict, output_file: str):
        """Generate an HTML verification report"""
        self._prepare_data(results)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hardware Security Verification Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                .summary {{ background: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .finding {{ margin-bottom: 20px; padding: 10px; border-left: 4px solid #3498db; }}
                .critical {{ border-color: #e74c3c; background: #fde8e8; }}
                .warning {{ border-color: #f39c12; background: #fef5e8; }}
                .plot {{ margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <h1>Hardware Security Verification Report</h1>
            <p>Generated at: {self.template['metadata']['generated_at']}</p>
            
            <h2>Design Information</h2>
            <table>
                <tr><th>Design Name</th><td>{self.template['design_info'].get('name', 'N/A')}</td></tr>
                <tr><th>Signals</th><td>{self.template['design_info'].get('signal_count', 0)}</td></tr>
                <tr><th>Verification Time</th><td>{self.template['verification_summary'].get('time_sec', 0)} seconds</td></tr>
            </table>
            
            <h2>Verification Summary</h2>
            <div class="summary">
                <p>Properties checked: {self.template['verification_summary'].get('properties_checked', 0)}</p>
                <p>Violations found: {self.template['verification_summary'].get('violations_found', 0)}</p>
                <p>Potential Trojans: {self.template['verification_summary'].get('potential_trojans', 0)}</p>
            </div>
            
            <div class="plot">
                {self._generate_plot_html(results)}
            </div>
            
            <h2>Detailed Findings</h2>
            {self._generate_findings_html()}
            
            <h2>Recommendations</h2>
            <ul>
                {''.join(f'<li>{rec}</li>' for rec in self.template['recommendations'])}
            </ul>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html)
    
    def _prepare_data(self, results: Dict):
        """Prepare data for reporting"""
        self.template['metadata']['generated_at'] = datetime.now().isoformat()
        
        # Design info
        self.template['design_info'] = {
            'name': results.get('design', 'Unknown'),
            'signal_count': len(results.get('signals', {}))
        }
        
        # Verification summary
        self.template['verification_summary'] = {
            'properties_checked': results.get('verification_stats', {}).get('properties_checked', 0),
            'violations_found': results.get('verification_stats', {}).get('violations_found', 0),
            'time_sec': results.get('verification_stats', {}).get('verification_time', 0),
            'potential_trojans': sum(1 for issue in results.get('detected_issues', []) 
                               if issue.get('potential_trojan', False))
        }
        
        # Detailed findings
        self.template['detailed_findings'] = results.get('detected_issues', [])
        
        # Recommendations
        self._generate_recommendations()
    
    def _generate_plot_html(self, results: Dict) -> str:
        """Generate plot HTML for the report"""
        try:
            # Create a simple bar plot
            categories = ['Properties', 'Violations', 'Potential Trojans']
            values = [
                self.template['verification_summary']['properties_checked'],
                self.template['verification_summary']['violations_found'],
                self.template['verification_summary']['potential_trojans']
            ]
            
            plt.figure(figsize=(8, 4))
            bars = plt.bar(categories, values, color=['#3498db', '#e74c3c', '#f39c12'])
            plt.title('Verification Results Summary')
            plt.ylabel('Count')
            
            # Save plot to temp file
            plot_file = 'temp_plot.png'
            plt.savefig(plot_file, bbox_inches='tight')
            plt.close()
            
            # Read and encode as base64
            import base64
            with open(plot_file, 'rb') as f:
                plot_data = base64.b64encode(f.read()).decode('utf-8')
            
            return f'<img src="data:image/png;base64,{plot_data}" alt="Verification Results Plot">'
            
        except Exception as e:
            print(f"Failed to generate plot: {str(e)}")
            return "<p>Plot generation failed</p>"
    
    def _generate_findings_html(self) -> str:
        """Generate HTML for findings section"""
        findings_html = []
        
        for finding in self.template['detailed_findings']:
            severity = finding.get('severity', 'info')
            
            finding_html = f"""
            <div class="finding {severity}">
                <h3>{finding.get('property', 'Unknown Property')}</h3>
                <p><strong>Severity:</strong> {severity.upper()}</p>
                {self._generate_counterexample_html(finding.get('counterexample', {}))}
                {self._generate_trojan_analysis_html(finding)}
            </div>
            """
            
            findings_html.append(finding_html)
        
        return ''.join(findings_html)
    
    def _generate_counterexample_html(self, counterexample: Dict) -> str:
        """Generate HTML for counterexample section"""
        if not counterexample:
            return ""
            
        rows = []
        for sig, val in counterexample.items():
            rows.append(f"<tr><td>{sig}</td><td>{val}</td></tr>")
        
        return f"""
        <p><strong>Counterexample:</strong></p>
        <table>
            <tr><th>Signal</th><th>Value</th></tr>
            {''.join(rows)}
        </table>
        """
    
    def _generate_trojan_analysis_html(self, finding: Dict) -> str:
        """Generate HTML for Trojan analysis section"""
        if not finding.get('potential_trojan', False):
            return ""
            
        return """
        <div class="trojan-warning">
            <p><strong>⚠ POTENTIAL HARDWARE TROJAN DETECTED</strong></p>
            <p>This violation matches known Trojan behavior patterns:</p>
            <ul>
                <li>Rare trigger condition detected</li>
                <li>Potential information leakage</li>
                <li>Unauthorized state modification</li>
            </ul>
        </div>
        """
    
    def _generate_recommendations(self):
        """Generate recommendations based on findings"""
        self.template['recommendations'] = []
        
        # General recommendations
        self.template['recommendations'].append(
            "Review all property violations before tapeout."
        )
        
        # Trojan-specific recommendations
        if any(issue.get('potential_trojan', False) 
               for issue in self.template['detailed_findings']):
            self.template['recommendations'].extend([
                "Conduct manual review of potential Trojan triggers.",
                "Consider adding additional monitoring for rare signal combinations.",
                "Implement runtime checks for unexpected behavior."
            ])
        
        # Performance recommendations
        if self.template['verification_summary']['properties_checked'] > 50:
            self.template['recommendations'].append(
                "Consider property decomposition for better verification performance."
            )