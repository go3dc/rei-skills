import re

def normalize_address(address):
    # Protect ordinals (e.g., 51st)
    address = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1\2_protected', address, flags=re.IGNORECASE)
    # Mapping for abbreviations
    mapping = {r'\bst\b': 'street', r'\bstr\b': 'street', r'\brd\b': 'road', 
               r'\bn\b': 'north', r'\bs\b': 'south', r'\be\b': 'east', r'\bw\b': 'west'}
    for pattern, replacement in mapping.items():
        address = re.sub(pattern, replacement, address, flags=re.IGNORECASE)
    return address.replace('_protected', '').lower().strip()
