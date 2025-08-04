"""
Hardware Security Properties for Formal Verification
This file contains common security properties that can be checked against RTL designs
to detect potential hardware Trojans or security vulnerabilities.
"""

# Generic Properties
GENERIC_PROPERTIES = [
    # No hidden state modifications
    "Implies(And(clk == True, rst == False), Not(Exists([r for r in z3_model if 'reg' in r], z3_model[r] != next(z3_model[r])))",
    
    # No unconditional privilege escalation
    "ForAll([z3_model['user_mode']], z3_model['privileged'] == False)",
    
    # No secret-dependent branches
    "ForAll([z3_model['secret_data']], z3_model['branch_condition'] == False)",
    
    # No unauthenticated configuration changes
    "Implies(z3_model['config_change'] == True, z3_model['auth_valid'] == True)",
]

# AES-Specific Properties
AES_PROPERTIES = [
    # S-box should be pure combinational
    "ForAll([z3_model['sbox_in']], z3_model['sbox_out'] == sbox_lookup(z3_model['sbox_in']))",
    
    # Key schedule should not depend on plaintext
    "ForAll([z3_model['plaintext']], z3_model['round_key'] == previous(z3_model['round_key']))",
    
    # No early termination
    "z3_model['done'] == False Until z3_model['round'] == 10",
    
    # Constant-time execution
    "ForAll([z3_model['plaintext1'], z3_model['plaintext2']], "
    "z3_model['cycles'] == 10)"
]

# Trojan-Specific Properties
TROJAN_PROPERTIES = [
    # Check for rare trigger conditions
    "Not(And(z3_model['rare_signal1'] == True, z3_model['rare_signal2'] == True))",
    
    # Check for payload activation
    "Implies(z3_model['trigger_condition'] == True, z3_model['payload'] == False)",
    
    # Check for information leakage
    "ForAll([z3_model['secret']], z3_model['output'] & 0xFF != z3_model['secret'] & 0xFF)"
]

def get_properties_for_design(design_type: str) -> List[str]:
    """Get appropriate properties based on design type"""
    if design_type.lower() == 'aes':
        return GENERIC_PROPERTIES + AES_PROPERTIES + TROJAN_PROPERTIES
    else:
        return GENERIC_PROPERTIES + TROJAN_PROPERTIES