#!/usr/bin/env python3
"""
Run Phase XVI inference from player_match_temporal_features and write to predictive_outcomes_temporal.
"""

import pandas as pd
import joblib
from clickhouse_connect import get_client
from datetime import datetime

# Connect to ClickHouse
client = get_client(host='localhost', port=9000, username='default', password='')

# Load model
model = joblib.load("tennis_match_predictor_xgb_model.pkl")
model_version = "1.0.0"

# Fetch features
query = """
SELECT match_id, player_id, avg_weighted_dps, avg_decayed_reaction_efficiency, max_temporal_shift_index
FROM player_match_temporal_features
"""
df = client.query_df(query)

# Prepare feature matrix
X = df[["avg_weighted_dps", "avg_decayed_reaction_efficiency", "max_temporal_shift_index"]]

# Predict
preds = model.predict_proba(X)[:, 1]
impact = model.predict(X)

# Insert predictions
for i, row in df.iterrows():
    client.command(f"""
        INSERT INTO predictive_outcomes_temporal (match_id, player_id, win_probability, impact_score, model_version)
        VALUES (
            '{row.match_id}', '{row.player_id}', {float(preds[i])}, {float(impact[i])}, '{model_version}'
        )
    """)

print("✅ Inference complete and predictions inserted.")
