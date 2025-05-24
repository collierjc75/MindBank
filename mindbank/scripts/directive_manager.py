#!/usr/bin/env python3
import json
import os
import datetime

input_file = input("Path to directive JSON: ")
with open(input_file) as f:
    directives = json.load(f)

version = directives.get("version", "unversioned")
ts = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
target_path = os.path.expanduser(f"~/gpt-memory/mindbank/directives/directives_{version}_{ts}.json")

with open(target_path, "w") as f:
    json.dump(directives, f, indent=2)

print(f"✅ Directive version saved: {target_path}")
