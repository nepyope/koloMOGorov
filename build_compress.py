#!/usr/bin/env python3

def find_best_patterns(text):
    """Find the absolute best patterns to maximize compression ratio"""
    from collections import Counter
    
    # Look for the most valuable patterns only
    xml_patterns = [
        ('    ', 4),
        ('  ', 2), 
        ('</', 2),
        ('</text>', 7),
        ('<text xml:space="preserve">', 28),
        ('</revision>', 11),
        ('<revision>', 10),
        ('</page>', 7),
        ('</title>', 8),
        ('<title>', 7),
        ('anarchism', 9),
        ('anarchist', 9),
        ('political', 9),
        ('government', 10),
        ('revolution', 10),
        ('philosophy', 10),
        ('individual', 10),
    ]
    
    # Also find 3-10 character frequent patterns dynamically
    dynamic_patterns = {}
    for length in range(3, 11):
        counts = Counter()
        for i in range(len(text) - length + 1):
            substring = text[i:i + length]
            counts[substring] += 1
        
        # Keep top patterns for this length
        for pattern, freq in counts.most_common(5):
            if freq >= 3:
                savings = freq * (len(pattern) - 1) - len(pattern) - 1
                if savings > 5:
                    dynamic_patterns[pattern] = (freq, savings)
    
    # Combine static and dynamic patterns
    all_patterns = []
    
    # Add static patterns
    for pattern, length in xml_patterns:
        count = text.count(pattern)
        if count >= 3:
            savings = count * (length - 1)
            all_patterns.append((pattern, count, savings))
    
    # Add dynamic patterns
    for pattern, (freq, savings) in dynamic_patterns.items():
        all_patterns.append((pattern, freq, savings))
    
    # Remove duplicates and sort by savings
    seen = set()
    unique_patterns = []
    for item in all_patterns:
        if item[0] not in seen:
            seen.add(item[0])
            unique_patterns.append(item)
    
    unique_patterns.sort(key=lambda x: x[2], reverse=True)
    return unique_patterns

def create_ultra_compact_script(text):
    """Create most compact script possible"""
    
    patterns = find_best_patterns(text)
    
    # Use single bytes for replacement, prioritizing efficiency
    compressed = text
    subs = {}
    
    # Find unused characters
    used = set(text)
    avail = [chr(i) for i in range(255, 0, -1) if chr(i) not in used and i > 31][:50]
    
    # Apply only the most valuable substitutions
    for pattern, count, savings in patterns[:len(avail)]:
        if avail:
            replacement = avail.pop(0)
            subs[replacement] = pattern
            compressed = compressed.replace(pattern, replacement)
    
    print(f"Substitutions: {len(subs)}")
    print(f"Text: {len(text)} -> {len(compressed)} chars")
    
    # Create ultra-minimal script with shortest possible syntax
    script = f'#!/usr/bin/env python3\nd={subs}\ns={repr(compressed)}\nfor k,v in d.items():s=s.replace(k,v)\nprint(s,end="")'
    
    return script

def main():
    with open('enwik9_100kb.txt', 'r') as f:
        text = f.read()
    
    original_bytes = len(text.encode('utf-8'))
    print(f"Original: {original_bytes} bytes")
    
    script = create_ultra_compact_script(text)
    
    script_bytes = len(script.encode('utf-8'))
    print(f"Script: {script_bytes} bytes ({script_bytes/original_bytes*100:.1f}%)")
    
    with open('compress.py', 'w') as f:
        f.write(script)
    
    print("Final compress.py generated!")

if __name__ == "__main__":
    main()