"""
Hardware Trojan Detection Module
This module implements pattern matching and heuristic analysis to detect
potential hardware Trojans in RTL designs.
"""

from collections import defaultdict
import re
from typing import Dict, List

class TrojanDetector:
    def __init__(self):
        self.trojan_patterns = self._load_trojan_patterns()
        self.heuristics = self._load_heuristics()
    
    def _load_trojan_patterns(self) -> Dict:
        """Load known Trojan patterns from database"""
        return {
            'rare_condition': [
                r'enable.*\&\&.*rare_signal',
                r'if\s*\(\s*.*\&\&.*\s*\)',
                r'trigger\s*=\s*.*\&.*'
            ],
            'payload_activation': [
                r'always\s*@\s*\(\s*posedge\s*trigger\s*\)',
                r'if\s*\(\s*trigger\s*\)\s*.*=.*secret',
                r'assign\s*leak\s*=\s*secret\s*when\s*trigger'
            ],
            'information_leakage': [
                r'assign\s*output\s*=\s*.*secret.*',
                r'if\s*\(\s*.*secret.*\s*\)\s*output\s*<=.*',
                r'always\s*@\s*\(\*\)\s*.*secret.*'
            ]
        }
    
    def _load_heuristics(self) -> Dict:
        """Load detection heuristics"""
        return {
            'unused_signals': lambda design: self._find_unused_signals(design),
            'rare_branches': lambda design: self._find_rare_branches(design),
            'hidden_state': lambda design: self._find_hidden_state(design)
        }
    
    def analyze_design(self, rtl_code: str) -> Dict:
        """Analyze RTL code for potential Trojans"""
        results = {
            'pattern_matches': defaultdict(list),
            'heuristic_flags': {},
            'score': 0
        }
        
        # Pattern matching
        for category, patterns in self.trojan_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, rtl_code, re.IGNORECASE)
                if matches:
                    results['pattern_matches'][category].extend(matches)
        
        # Heuristic analysis
        for name, heuristic in self.heuristics.items():
            results['heuristic_flags'][name] = heuristic(rtl_code)
        
        # Calculate threat score
        results['score'] = self._calculate_threat_score(results)
        
        return results
    
    def _find_unused_signals(self, rtl_code: str) -> List[str]:
        """Find signals declared but never used"""
        # This is simplified - real implementation would need full parsing
        declared = set(re.findall(r'input\s+(.*?)[,;]', rtl_code))
        declared.update(re.findall(r'output\s+(.*?)[,;]', rtl_code))
        declared.update(re.findall(r'reg\s+(.*?)[,;]', rtl_code))
        
        used = set(re.findall(r'\.(\w+)\s*\(', rtl_code))
        used.update(re.findall(r'\b(\w+)\s*=', rtl_code))
        used.update(re.findall(r'\b(\w+)\s*\)', rtl_code))
        
        return list(declared - used)
    
    def _find_rare_branches(self, rtl_code: str) -> List[str]:
        """Find branches with complex conditions"""
        branches = re.findall(r'if\s*\((.*?)\)', rtl_code)
        return [b for b in branches if '&&' in b or '||' in b or '^' in b]
    
    def _find_hidden_state(self, rtl_code: str) -> List[str]:
        """Find state elements without reset"""
        state_elements = re.findall(r'reg\s+(.*?)\s*;', rtl_code)
        return [s for s in state_elements 
                if not re.search(r'always\s*@\s*\(.*reset.*\)', rtl_code)]
    
    def _calculate_threat_score(self, results: Dict) -> int:
        """Calculate a threat score based on findings"""
        score = 0
        
        # Pattern matches
        for category, matches in results['pattern_matches'].items():
            score += len(matches) * {
                'rare_condition': 3,
                'payload_activation': 5,
                'information_leakage': 7
            }[category]
        
        # Heuristic flags
        for name, flags in results['heuristic_flags'].items():
            if flags:
                score += {
                    'unused_signals': 2,
                    'rare_branches': 3,
                    'hidden_state': 4
                }[name] * len(flags)
        
        return score