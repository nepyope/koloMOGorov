#!/usr/bin/env python3
"""Verify compress.py output matches enwik9_100kb.txt exactly."""
import subprocess, sys, os

script = os.path.join(os.path.dirname(__file__), "compress.py")
target = os.path.join(os.path.dirname(__file__), "enwik9_100kb.txt")

with open(target, "rb") as f:
    expected = f.read()

result = subprocess.run([sys.executable, script], capture_output=True)
got = result.stdout

script_size = os.path.getsize(script)
ratio = script_size / len(expected) * 100

if got == expected:
    print(f"✅ MATCH — lossless ({len(expected)} bytes)")
    print(f"📦 compress.py: {script_size} bytes ({ratio:.1f}% of original)")
else:
    print(f"❌ MISMATCH")
    print(f"   Expected: {len(expected)} bytes")
    print(f"   Got:      {len(got)} bytes")
    # Show first diff
    for i in range(min(len(expected), len(got))):
        if expected[i] != got[i]:
            ctx = 40
            print(f"   First diff at byte {i}:")
            print(f"   Expected: {expected[max(0,i-ctx):i+ctx]!r}")
            print(f"   Got:      {got[max(0,i-ctx):i+ctx]!r}")
            break
    if len(got) != len(expected):
        print(f"   Length diff: {len(got) - len(expected):+d} bytes")
    sys.exit(1)
