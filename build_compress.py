#!/usr/bin/env python3

def find_safe_patterns(text):
    """Find patterns that can be safely substituted"""
    from collections import Counter
    
    # Find repeated patterns
    patterns = []
    
    # Look for XML patterns first
    xml_patterns = [
        ('    ', 4),  # 4 spaces 
        ('  ', 2),    # 2 spaces
        ('</', 2),
        ('</text>', 7),
        ('<text xml:space="preserve">', 28),
        ('</revision>', 11),
        ('<revision>', 10),
        ('</page>', 7),
        ('</title>', 8),
        ('<title>', 7),
        ('xmlns:', 6),
        ('anarchism', 9),
        ('Anarchism', 9),
        ('anarchist', 9),
        ('political', 9),
        ('government', 10),
        ('revolution', 10),
        ('philosophy', 10),
        ('individual', 10),
        ('social', 6),
        ('society', 7),
        ('economic', 8),
        ('freedom', 7),
        ('property', 8),
        ('capitalism', 10),
        ('socialist', 9),
        ('communist', 9),
    ]
    
    # Count occurrences and calculate savings
    valid_patterns = []
    for pattern, length in xml_patterns:
        count = text.count(pattern)
        savings = count * (length - 1)  # Each replacement saves (length-1) characters
        if count >= 3 and savings > 10:  # Must save at least 10 characters total
            valid_patterns.append((pattern, count, savings))
    
    # Sort by savings
    valid_patterns.sort(key=lambda x: x[2], reverse=True)
    return valid_patterns

def create_minimal_script(text):
    """Create the most minimal possible script"""
    
    patterns = find_safe_patterns(text)
    
    # Use single byte substitution characters that don't appear in the text
    compressed = text
    substitutions = {}
    
    # Find unused characters (prioritize high bytes to avoid UTF-8 issues)
    used_chars = set(text)
    available = []
    for i in range(255, 0, -1):
        if chr(i) not in used_chars:
            available.append(chr(i))
    
    # Apply substitutions for highest-saving patterns
    char_idx = 0
    actual_savings = 0
    for pattern, count, savings in patterns[:min(len(available), 50)]:
        if char_idx >= len(available):
            break
        
        replacement = available[char_idx]
        substitutions[replacement] = pattern
        compressed = compressed.replace(pattern, replacement)
        actual_savings += count * (len(pattern) - 1)
        char_idx += 1
    
    print(f"Applied {len(substitutions)} substitutions")
    print(f"Text reduced from {len(text)} to {len(compressed)} chars")
    print(f"Estimated savings: {actual_savings} characters")
    
    # Create ultra-minimal script
    script = f"""#!/usr/bin/env python3
d={repr(substitutions)}
s={repr(compressed)}
for k,v in d.items():s=s.replace(k,v)
print(s,end='')"""
    
    return script

def main():
    # Read original data
    with open('enwik9_100kb.txt', 'r') as f:
        text = f.read()
    
    original_bytes = len(text.encode('utf-8'))
    print(f"Original size: {original_bytes} bytes")
    
    # Create script
    script = create_minimal_script(text)
    
    script_bytes = len(script.encode('utf-8'))
    print(f"Script size: {script_bytes} bytes")
    print(f"Compression ratio: {script_bytes / original_bytes * 100:.1f}%")
    
    # Save script
    with open('compress.py', 'w') as f:
        f.write(script)
    
    print("compress.py generated!")

if __name__ == "__main__":
    main()