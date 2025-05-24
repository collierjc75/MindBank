#!/usr/bin/env python3
import os
import json
import datetime

snapshot = {
    "phase": "XV",
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    "directive_version": "2.1",
    "active_dataset": "match_stats_enriched",
    "model_state": "pre-inference"
}

filename = f"phase_XV_snapshot_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
path = os.path.expanduser(f"~/gpt-memory/mindbank/snapshots/{filename}")

with open(path, "w") as f:
    json.dump(snapshot, f, indent=2)

print(f"✅ Snapshot saved: {path}")
