#!/usr/bin/env python3
import os
import difflib

local_dir = os.path.expanduser("~/gpt-memory/mindbank/schemas/")
github_dir = os.path.expanduser("~/MindBank/mindbank/schemas/")

for filename in os.listdir(local_dir):
    local_path = os.path.join(local_dir, filename)
    github_path = os.path.join(github_dir, filename)
    if os.path.exists(github_path):
        with open(local_path) as f1, open(github_path) as f2:
            diff = list(difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile='local', tofile='github'))
            if diff:
                print(f"⚠️ Difference in {filename}:
" + "".join(diff))
            else:
                print(f"✅ {filename} matches.")
    else:
        print(f"🟡 Missing in GitHub: {filename}")
