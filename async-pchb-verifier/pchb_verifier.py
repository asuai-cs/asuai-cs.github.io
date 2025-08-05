#!/usr/bin/env python3
"""
Formal Verification Engine for PCHB Circuits
- Implements NULL Convention Logic (NCL) rules
- Checks 4-phase handshake compliance
- Detects Trojan-induced timing violations
"""

from z3 import *
import json
import re
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PCHBProperties:
    handshake: list
    stability: list
    trojan_patterns: list

class PCHBVerifier:
    def __init__(self):
        self.solver = Solver()
        self.signals = {}
        self.results = {
            "handshake_violations": [],
            "trojan_detections": [],
            "timing_violations": []
        }
    
    def _load_properties(self, file_path: str) -> PCHBProperties:
        """Load verification properties from JSON file"""
        with open(file_path) as f:
            data = json.load(f)
    
        return PCHBProperties(
            handshake=data["handshake"],
            stability=data["stability"],
            trojan_patterns=data["trojan_patterns"]
        )
        
    def load_design(self, verilog_file: str):
        """Parse PCHB circuit signals"""
        # Simplified parsing - extend with real Verilog parsing
        with open(verilog_file) as f:
            content = f.read()
        
        # Extract PCHB-specific signals with next state variables
        self.signals = {
            "req": Bool("req"),
            "req_next": Bool("req_next"),
            "ack": Bool("ack"),
            "ack_next": Bool("ack_next"),
            "data": [Bool(f"data_{i}") for i in range(32)],  # 32-bit example
            "data_next": [Bool(f"data_next_{i}") for i in range(32)],
            "en": Bool("en"),
            "en_next": Bool("en_next"),
            "reset": Bool("reset")
        }
        print(f"Loaded {len(self.signals)} PCHB signals")

    def verify(self, properties_file: str):
        """Main verification procedure"""
        props = self._load_properties(properties_file)
        
        # Phase 1: Handshake Protocol Verification
        self._verify_handshake(props.handshake)
        
        # Phase 2: Stability Checks
        self._verify_stability(props.stability)
        
        # Phase 3: Trojan Pattern Matching
        self._detect_trojans(props.trojan_patterns)
        
        # Generate report
        self._generate_report()

    def _verify_handshake(self, rules: list):
        """4-phase handshake compliance"""
        req, req_next = self.signals["req"], self.signals["req_next"]
        ack, ack_next = self.signals["ack"], self.signals["ack_next"]
        
        # Rule 1: Request must precede acknowledge
        self.solver.add(Implies(req, Not(ack)))
        
        # Rule 2: Acknowledge clearance
        self.solver.add(Implies(ack, req_next == False))
        
        # Rule 3: Request must stay low until acknowledge is low
        self.solver.add(Implies(And(ack, req == False), ack_next == False))
        
        if self.solver.check() == unsat:
            self.results["handshake_violations"].append(
                "Handshake protocol violation detected"
            )

    def _verify_stability(self, rules: list):
        """Data stability during evaluation phase"""
        data = self.signals["data"]
        data_next = self.signals["data_next"]
        en = self.signals["en"]
        
        # Data must remain stable when enabled
        for bit, bit_next in zip(data, data_next):
            self.solver.add(Implies(en, bit == bit_next))
            
        if self.solver.check() == unsat:
            self.results["timing_violations"].append(
                "Data stability violation during evaluation"
            )

    def _detect_trojans(self, patterns: list):
        """Check for known Trojan signatures"""
        for pattern in patterns:
            try:
                # Build Z3 constraints from pattern
                constraint = self._pattern_to_z3(pattern["logic"])
                if constraint is not None:
                    self.solver.push()  # Create a new scope for this check
                    self.solver.add(constraint)
                    
                    if self.solver.check() == sat:
                        self.results["trojan_detections"].append({
                            "name": pattern["name"],
                            "type": pattern["type"],
                            "severity": pattern["severity"],
                            "model": str(self.solver.model())
                        })
                    self.solver.pop()  # Remove the constraint after checking
            except Exception as e:
                print(f"Error processing pattern {pattern.get('name', 'unnamed')}: {str(e)}")
                continue

    def _pattern_to_z3(self, pattern: str) -> BoolRef:
        """Convert Trojan pattern to Z3 expression"""
        if not pattern or not isinstance(pattern, str):
            return None
            
        # Tokenize the pattern with proper operator handling
        tokens = re.findall(r"(\w+|&&|\|\||!|\(|\))", pattern)
        stack = []
        ops = []
        
        # Define operator precedence
        precedence = {'!': 3, '&&': 2, '||': 1}
        
        for token in tokens:
            if token in self.signals:
                stack.append(self.signals[token])
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    self._apply_operator(ops.pop(), stack)
                ops.pop()  # Remove the '('
            elif token in precedence:
                while (ops and ops[-1] != '(' and
                       precedence[ops[-1]] >= precedence[token]):
                    self._apply_operator(ops.pop(), stack)
                ops.append(token)
        
        while ops:
            self._apply_operator(ops.pop(), stack)
            
        return stack[0] if stack else None

    def _apply_operator(self, op: str, stack: list):
        """Apply operator to the stack"""
        if op == '!':
            if not stack:
                raise ValueError("Missing operand for ! operator")
            stack.append(Not(stack.pop()))
        elif op in ('&&', '||'):
            if len(stack) < 2:
                raise ValueError(f"Missing operands for {op} operator")
            right = stack.pop()
            left = stack.pop()
            if op == '&&':
                stack.append(And(left, right))
            else:
                stack.append(Or(left, right))

    def _generate_report(self):
        """Output verification results"""
        report = {
            "metadata": {
                "tool": "PCHB-Verifier",
                "version": "1.0"
            },
            "results": self.results
        }
        
        with open("pchb_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("Verification complete. Report generated at pchb_report.json")

if __name__ == "__main__":
    verifier = PCHBVerifier()
    verifier.load_design("designs/pchb_adder.v")
    verifier.verify("lib/pchb_properties.json")