#!/usr/bin/env python3
"""
Hardware Security Formal Verifier v2.1
- Detects hardware Trojans in Verilog designs
- Supports comprehensive security property checking
- Generates detailed JSON reports
"""

from z3 import *
import re
import json
from datetime import datetime
from typing import Dict, List, Union

class VerilogParser:
    """Advanced Verilog parser with security analysis"""
    
    def __init__(self):
        self.signals = {}
        self.assignments = []
        self.always_blocks = []
        self.security_warnings = []
        
        # Known Trojan patterns
        self.trojan_patterns = {
            'rare_condition': r'rare_signal1\s*&&\s*rare_signal2',
            'key_leakage': r'ciphertext\s*\[.*?\]\s*<=\s*key\[.*?\]',
            'hidden_state': r'if\s*\(\s*!\s*reset\s*\)\s*begin.*?secret'
        }
    
    def parse(self, verilog_file: str):
        """Parse Verilog file with security analysis"""
        try:
            with open(verilog_file, 'r') as f:
                content = f.read()
            
            self._detect_suspicious_patterns(content)
            content = self._remove_comments(content)
            self._extract_module_io(content)
            self._extract_registers(content)
            self._extract_assignments(content)
            self._extract_always_blocks(content)
            return True
            
        except Exception as e:
            self.security_warnings.append({
                'type': 'parse_error',
                'severity': 'high',
                'description': f"Failed to parse Verilog: {str(e)}"
            })
            return False
    
    def _remove_comments(self, content: str) -> str:
        """Remove Verilog comments"""
        content = re.sub(r'//.*?\n', '\n', content)
        return re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    def _extract_module_io(self, content: str):
        """Extract module ports with security context"""
        module_match = re.search(r'module\s+(\w+)\s*\((.*?)\)\s*;', content, re.DOTALL)
        if not module_match:
            raise ValueError("No module declaration found")
            
        ports = module_match.group(2).replace('\n', ' ')
        for port in re.split(r'\s*,\s*', ports.strip()):
            if not port: continue
            dir_match = re.match(r'(input|output|inout)\s*(?:\[.*?\])?\s*(\w+)', port.strip())
            if dir_match:
                direction, name = dir_match.groups()
                self.signals[name] = {
                    'type': direction,
                    'width': self._parse_width(port),
                    'security': 'sensitive' if 'key' in name else 'normal'
                }
    
    def _extract_registers(self, content: str):
        """Extract registers with security context"""
        reg_matches = re.finditer(r'reg\s*(?:\[(.*?)\])?\s*(\w+)\s*;', content)
        for match in reg_matches:
            width_str, name = match.groups()
            self.signals[name] = {
                'type': 'reg',
                'width': self._parse_width(width_str) if width_str else 1,
                'security': 'critical' if 'secret' in name else 'normal'
            }
    
    def _extract_assignments(self, content: str):
        """Extract continuous assignments"""
        wire_matches = re.finditer(r'wire\s*(?:\[(.*?)\])?\s*(\w+)\s*(?:=\s*(.*?)\s*)?;', content)
        for match in wire_matches:
            width_str, name, assignment = match.groups()
            self.signals[name] = {
                'type': 'wire',
                'width': self._parse_width(width_str) if width_str else 1,
                'security': 'normal'
            }
            if assignment:
                self.assignments.append((name, assignment))
    
    def _extract_always_blocks(self, content: str):
        """Extract always blocks with security analysis"""
        always_blocks = re.finditer(r'always\s*@\s*\((.*?)\)\s*begin(.*?)end', content, re.DOTALL)
        for match in always_blocks:
            sensitivity, logic = match.groups()
            self.always_blocks.append({
                'sensitivity': sensitivity.strip(),
                'logic': logic.strip(),
                'security_issues': self._analyze_block_security(logic)
            })
    
    def _parse_width(self, width_str: str) -> int:
        """Convert Verilog width specification to integer"""
        if not width_str: return 1
        match = re.match(r'(\d+)\s*:\s*(\d+)', width_str)
        if match:
            msb, lsb = map(int, match.groups())
            return abs(msb - lsb) + 1
        return 1
    
    def _detect_suspicious_patterns(self, content: str):
        """Pre-scan for known Trojan patterns"""
        for pattern_type, pattern in self.trojan_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                self.security_warnings.append({
                    'type': pattern_type,
                    'severity': 'high',
                    'description': f'Potential {pattern_type.replace("_", " ")} detected'
                })
    
    def _analyze_block_security(self, logic: str) -> List[Dict]:
        """Analyze always block for security issues"""
        issues = []
        if 'key' in logic and ('if' in logic or 'case' in logic):
            issues.append({
                'type': 'key_conditional',
                'severity': 'critical',
                'description': 'Key material used in conditional logic'
            })
        return issues

class FormalVerifier:
    """Advanced Hardware Security Verifier"""
    
    def __init__(self):
        self.solver = Solver()
        self.parser = VerilogParser()
        self.results = {
            'metadata': {
                'tool': 'Hardware Security Verifier',
                'version': '2.1',
                'timestamp': datetime.now().isoformat()
            },
            'signals': {},
            'properties_checked': 0,
            'violations_found': 0,
            'trojan_findings': [],
            'security_warnings': [],
            'execution_time': 0.0
        }
    
    def load_design(self, verilog_file: str) -> bool:
        """Load and analyze Verilog design"""
        print(f"🔍 Loading design from {verilog_file}")
        start_time = datetime.now()
        
        success = self.parser.parse(verilog_file)
        self.results['signals'] = self.parser.signals
        self.results['security_warnings'] = self.parser.security_warnings
        self.results['execution_time'] = (datetime.now() - start_time).total_seconds()
        
        if success:
            print(f"✅ Found {len(self.parser.signals)} signals")
            if self.parser.security_warnings:
                print(f"⚠️  Detected {len(self.parser.security_warnings)} security warnings during parsing")
            return True
        else:
            print("❌ Failed to parse design")
            return False
    
    def load_properties(self, property_file: str) -> bool:
        """Load security properties from file"""
        try:
            with open(property_file, 'r') as f:
                self.properties = [p.strip() for p in f.readlines() 
                                if p.strip() and not p.startswith('#')]
            print(f"📜 Loaded {len(self.properties)} security properties")
            return True
        except Exception as e:
            print(f"❌ Failed to load properties: {str(e)}")
            self.results['security_warnings'].append({
                'type': 'property_error',
                'severity': 'high',
                'description': f"Failed to load properties: {str(e)}"
            })
            return False
    
    def verify(self) -> bool:
        """Run comprehensive security verification"""
        if not hasattr(self, 'properties'):
            print("⚠️  No properties loaded")
            return False
        
        start_time = datetime.now()
        z3_vars = self._create_z3_vars()
        
        print("\n🔎 Running formal verification...")
        self._verify_generic_properties(z3_vars)
        self._verify_trojan_specific(z3_vars)
        
        self.results['execution_time'] += (datetime.now() - start_time).total_seconds()
        self._generate_report()
        return True
    
    def _create_z3_vars(self) -> Dict[str, Union[BoolRef, BitVecRef]]:
        """Create Z3 variables for all signals"""
        z3_vars = {}
        for name, info in self.parser.signals.items():
            if info['width'] == 1:
                z3_vars[name] = Bool(name)
            else:
                z3_vars[name] = BitVec(name, info['width'])
        return z3_vars
    
    def _verify_generic_properties(self, z3_vars: Dict):
        """Verify all loaded security properties"""
        for prop in self.properties:
            self.results['properties_checked'] += 1
            try:
                if 'ForAll' in prop:
                    self._verify_forall(prop, z3_vars)
                elif 'Exists' in prop:
                    self._verify_exists(prop, z3_vars)
                elif 'Implies' in prop:
                    self._verify_implies(prop, z3_vars)
                else:
                    self._verify_expression(prop, z3_vars)
            except Exception as e:
                self.results['security_warnings'].append({
                    'type': 'property_error',
                    'severity': 'medium',
                    'description': f"Failed to verify property: {prop}",
                    'error': str(e)
                })
    
    def _verify_forall(self, prop: str, z3_vars: Dict):
        """Verify ForAll quantified properties"""
        match = re.match(r'ForAll\s*\(\s*\[(.*?)\]\s*,\s*(.*?)\s*\)', prop)
        if not match:
            raise ValueError("Malformed ForAll expression")
            
        vars_str, expr = match.groups()
        variables = [v.strip() for v in vars_str.split(',') if v.strip() in z3_vars]
        
        if not variables:
            raise ValueError("No valid variables in ForAll")
            
        body = eval(expr, {'__builtins__': None}, z3_vars)
        self.solver.add(ForAll([z3_vars[v] for v in variables], body))
        
        if self.solver.check() == unsat:
            self.results['violations_found'] += 1
            print(f"🚨 Violation: {prop}")
        self.solver.reset()
    
    def _verify_exists(self, prop: str, z3_vars: Dict):
        """Verify Exists quantified properties"""
        match = re.match(r'Exists\s*\(\s*\[(.*?)\]\s*,\s*(.*?)\s*\)', prop)
        if not match:
            raise ValueError("Malformed Exists expression")
            
        vars_str, expr = match.groups()
        variables = [v.strip() for v in vars_str.split(',') if v.strip() in z3_vars]
        
        if not variables:
            raise ValueError("No valid variables in Exists")
            
        body = eval(expr, {'__builtins__': None}, z3_vars)
        self.solver.add(Exists([z3_vars[v] for v in variables], body))
        
        if self.solver.check() == unsat:
            self.results['violations_found'] += 1
            print(f"🚨 Violation: {prop}")
        self.solver.reset()
    
    def _verify_implies(self, prop: str, z3_vars: Dict):
        """Verify Implies properties"""
        parts = re.split(r'Implies\s*\(\s*', prop, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) != 2:
            raise ValueError("Malformed Implies expression")
            
        consequent = parts[1].rsplit(')', 1)[0]
        antecedent = parts[0].strip()
        
        ant = eval(antecedent, {'__builtins__': None}, z3_vars)
        cons = eval(consequent, {'__builtins__': None}, z3_vars)
        self.solver.add(Implies(ant, cons))
        
        if self.solver.check() == unsat:
            self.results['violations_found'] += 1
            print(f"🚨 Violation: {prop}")
        self.solver.reset()
    
    def _verify_expression(self, prop: str, z3_vars: Dict):
        """Verify simple expressions"""
        expr = eval(prop, {'__builtins__': None}, z3_vars)
        self.solver.add(expr)
        
        if self.solver.check() == unsat:
            self.results['violations_found'] += 1
            print(f"🚨 Violation: {prop}")
        self.solver.reset()
    
    def _verify_trojan_specific(self, z3_vars: Dict):
        """Run specialized Trojan detection checks"""
        print("\n🕵️‍♂️ Running dedicated Trojan detection...")
        
        # Check 1: Rare signal activation
        if 'rare_signal1' in z3_vars and 'rare_signal2' in z3_vars:
            rare_cond = And(
                z3_vars['rare_signal1'] == True,
                z3_vars['rare_signal2'] == True
            )
            self.solver.add(rare_cond)
            if self.solver.check() == sat:
                model = self.solver.model()
                self.results['trojan_findings'].append({
                    'type': 'rare_trigger',
                    'severity': 'critical',
                    'description': 'Rare signal combination activates Trojan',
                    'signals': {
                        'rare_signal1': str(model[z3_vars['rare_signal1']]),
                        'rare_signal2': str(model[z3_vars['rare_signal2']])
                    }
                })
                self.results['violations_found'] += 1
                print("🚨 CRITICAL: Rare signal trigger detected")
            self.solver.reset()
        
        # Check 2: Key leakage
        if 'ciphertext' in z3_vars and 'key' in z3_vars:
            key_leak = z3_vars['ciphertext'][7:0] == z3_vars['key'][7:0]
            self.solver.add(key_leak)
            if self.solver.check() == sat:
                model = self.solver.model()
                self.results['trojan_findings'].append({
                    'type': 'key_leakage',
                    'severity': 'critical',
                    'description': 'Key material leaked to ciphertext',
                    'bits': 'ciphertext[7:0]',
                    'value': str(model[z3_vars['ciphertext'][7:0]])
                })
                self.results['violations_found'] += 1
                print("🚨 CRITICAL: Key leakage detected")
            self.solver.reset()
    
    def generate_html_report(self, json_filepath: str):
        """Convert JSON results to HTML"""
        try:
            with open(json_filepath, 'r') as f:
                data = json.load(f)

            html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Hardware Security Report</title>
        <style>
           body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .critical {{ color: #e74c3c; font-weight: bold; }}
            .finding {{ margin: 15px 0; padding: 10px; border-left: 4px solid #e74c3c; }}
            pre {{ background: #f8f9fa; padding: 10px; }}
        </style>
    </head>
    <body>
        <h1>Hardware Security Verification Report</h1>
        <p>Generated: {data['metadata']['timestamp']}</p>

    
        <h2>Summary</h2>
        <ul>
            <li>Properties checked: {data['properties_checked']}</li>
            <li>Violations found: <span class="critical">{data['violations_found']}</span></li>
            <li>Trojan findings: {len(data['trojan_findings'])}</li>
        </ul>
        
        
        <!-- ===== VISUALIZATION ADDITION ===== -->
        <h2>Visual Analysis</h2>
        <div id="chart" style="width:600px; height:400px;"></div>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
            var data = {{
                x: ['Properties', 'Violations', 'Trojans'],
                y: [{data['properties_checked']}, {data['violations_found']}, {len(data['trojan_findings'])}],
                type: 'bar',
                marker: {{ color: ['#3498db', '#e74c3c', '#f39c12'] }}
            }};
            Plotly.newPlot('chart', [data], {{
                title: 'Verification Metrics Overview',
                yaxis: {{ title: 'Count' }}
            }});
        </script>
        <!-- ===== END VISUALIZATION ===== -->

        <h2>Detailed Findings</h2>
        <div class="finding">
            <h3>Trojan Detected</h3>
            <pre>{json.dumps(data['trojan_findings'], indent=2)}</pre>
        </div>
    </body>
    </html>"""

            html_file = json_filepath.replace('.json', '.html')
            with open(html_file, 'w') as f:
                f.write(html)
            print(f"✅ HTML report generated: {html_file}")
        
        except Exception as e:
            print(f"❌ Failed to generate HTML report: {str(e)}")
        
    def _generate_report(self):
        """Generate comprehensive JSON report"""
        json_file = "security_report.json"
    
        # Prepare serializable results
        serializable_results = {
            'metadata': self.results['metadata'],
            'signals': self.results['signals'],
            'properties_checked': self.results['properties_checked'],
            'violations_found': self.results['violations_found'],
            'trojan_findings': self.results['trojan_findings'],
            'security_warnings': self.results['security_warnings'],
            'execution_time': self.results['execution_time']
        }
    
        try:
            # Save JSON report
            with open(json_file, 'w') as f:
                json.dump(serializable_results, f, indent=2)
        
            print(f"\n📊 Verification complete:")
            print(f"   Properties checked: {self.results['properties_checked']}")
            print(f"   Violations found: {self.results['violations_found']}")
            print(f"   Trojan findings: {len(self.results['trojan_findings'])}")
            print(f"   Report saved to {json_file}")

            # Generate HTML report - pass the FILE PATH, not self
            self.generate_html_report(json_file)
        
        except Exception as e:
            print(f"❌ Failed to generate report: {str(e)}")

if __name__ == "__main__":
    verifier = FormalVerifier()
    
    # Load and verify the design
    if verifier.load_design("rtl_examples/aes_core.v"):
        if verifier.load_properties("verification_properties/aes_properties.txt"):
            verifier.verify()