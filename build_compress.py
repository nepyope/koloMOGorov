#!/usr/bin/env python3
"""Build compress.py using template compression with exact formatting."""
import os
import re

DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(DIR, "enwik9_100kb.txt")
OUTPUT = os.path.join(DIR, "compress.py")

# Read input as bytes to preserve exact content
print("Reading input file...")
with open(INPUT, 'rb') as f:
    data_bytes = f.read()

print(f"Input: {len(data_bytes)} bytes")

# Convert to string for processing
text = data_bytes.decode('utf-8')

# Find the header (everything before first <page>)
page_start = text.find('<page>')
if page_start == -1:
    raise ValueError("No <page> found")

header = text[:page_start]
footer = '</mediawiki>\n'
pages_text = text[page_start:-len(footer)]

print(f"Header: {len(header)} bytes")

# Split into individual pages
page_sections = []
current_pos = 0

while True:
    page_start = pages_text.find('<page>', current_pos)
    if page_start == -1:
        break
    
    page_end = pages_text.find('</page>', page_start)
    if page_end == -1:
        break
        
    page_content = pages_text[page_start:page_end + 7]
    page_sections.append(page_content)
    current_pos = page_end + 7

print(f"Found {len(page_sections)} pages")

# Extract data from each page using the same tab-separated format as iteration 8
page_data = []
for i, page_xml in enumerate(page_sections):
    # Parse each field
    title_m = re.search(r'<title>(.*?)</title>', page_xml, re.DOTALL)
    id_m = re.search(r'<id>(.*?)</id>', page_xml, re.DOTALL)
    rev_id_m = re.search(r'<revision>\s*<id>(.*?)</id>', page_xml, re.DOTALL)
    timestamp_m = re.search(r'<timestamp>(.*?)</timestamp>', page_xml, re.DOTALL)
    
    # Handle both username and IP contributors
    contrib_m = re.search(r'<contributor>\s*(?:<username>(.*?)</username>\s*<id>(.*?)</id>|<ip>(.*?)</ip>)', page_xml, re.DOTALL)
    
    minor_m = re.search(r'<minor\s*/>', page_xml)
    comment_m = re.search(r'<comment>(.*?)</comment>', page_xml, re.DOTALL)
    text_m = re.search(r'<text xml:space="preserve">(.*?)</text>', page_xml, re.DOTALL)
    
    if title_m and id_m and rev_id_m and timestamp_m and text_m:
        title = title_m.group(1)
        page_id = id_m.group(1)
        rev_id = rev_id_m.group(1) 
        timestamp = timestamp_m.group(1)
        
        if contrib_m:
            if contrib_m.group(1):  # username
                user = contrib_m.group(1)
                user_id = contrib_m.group(2)
            else:  # IP
                user = contrib_m.group(3)
                user_id = ''
        else:
            user = ''
            user_id = ''
            
        minor = '1' if minor_m else '0'
        comment = comment_m.group(1) if comment_m else ''
        text_content = text_m.group(1)
        
        # Store as tab-separated values (like iteration 8)
        row = [title, page_id, rev_id, timestamp, user, user_id, minor, comment, text_content]
        page_data.append(row)

print(f"Parsed {len(page_data)} pages successfully")

# Create tab-separated data
lines = []
for row in page_data:
    escaped_row = []
    for field in row:
        field_str = str(field)
        # Escape special characters
        field_str = field_str.replace('\\', '\\\\')
        field_str = field_str.replace('\t', '\\t') 
        field_str = field_str.replace('\n', '\\n')
        escaped_row.append(field_str)
    lines.append('\t'.join(escaped_row))

compressed_data = '\n'.join(lines)
print(f"Compressed data: {len(compressed_data)} bytes")

# Build ultra-compact decompressor based on iteration 8 style
decompressor = f'''import sys
h={repr(header)}
d={repr(compressed_data)}
sys.stdout.write(h)
for line in d.split('\\n'):
 if not line.strip():continue
 parts=line.split('\\t')
 if len(parts)!=9:continue
 title,page_id,rev_id,timestamp,user,user_id,minor,comment,text=parts
 text=text.replace('\\\\n','\\n').replace('\\\\t','\\t').replace('\\\\\\\\','\\\\')
 comment=comment.replace('\\\\n','\\n')
 sys.stdout.write('  <page>\\n    <title>'+title+'</title>\\n    <id>'+page_id+'</id>\\n    <revision>\\n      <id>'+rev_id+'</id>\\n      <timestamp>'+timestamp+'</timestamp>\\n      <contributor>\\n        ')
 if '.' in user and user.count('.')>=3:
  sys.stdout.write('<ip>'+user+'</ip>')
 else:
  sys.stdout.write('<username>'+user+'</username>\\n        <id>'+user_id+'</id>')
 sys.stdout.write('\\n      </contributor>')
 if minor=='1':sys.stdout.write('\\n      <minor />')
 if comment:sys.stdout.write('\\n      <comment>'+comment+'</comment>')
 sys.stdout.write('\\n      <text xml:space="preserve">'+text+'</text>\\n    </revision>\\n  </page>\\n')
sys.stdout.write('</mediawiki>\\n')
'''

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(decompressor)

size = os.path.getsize(OUTPUT)
ratio = size / len(data_bytes) * 100
print(f"compress.py: {size} bytes ({ratio:.1f}%)")

if size < 51200:
    print("🎉 SUCCESS: Under 50% target!")
else:
    print(f"Need to reduce by {size - 51200} bytes ({(size - 51200)/1024:.1f}KB)")