import re
def normalize_address(address):
    address = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1\2_protected', address, flags=re.IGNORECASE)
    mapping = {r'\bst\b': 'street', r'\bstr\b': 'street', r'\brd\b': 'road', 
               r'\bn\b': 'north', r'\bs\b': 'south', r'\be\b': 'east', r'\bw\b': 'west'}
    for p, r in mapping.items(): address = re.sub(p, r, address, flags=re.IGNORECASE)
    return address.replace('_protected', '').lower().strip()
