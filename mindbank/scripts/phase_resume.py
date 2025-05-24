#!/usr/bin/env python3
import json
import os

file = input("Phase snapshot file path: ")
with open(file) as f:
    context = json.load(f)

print("✅ Phase loaded.")
print(json.dumps(context, indent=2))
