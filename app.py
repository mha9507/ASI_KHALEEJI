from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from datetime import datetime
import random

app = Flask(__name__)

# -----------------------------
# Load dataset
# -----------------------------

DATASET_PATH = "dataset.csv"
RESPONSES_PATH = "user_responses.csv"

df = pd.read_csv(DATASET_PATH)

# Clean column names just in case there are hidden spaces
df.columns = df.columns.str.strip()

# Make sure correct_answer is clean
df["correct_answer"] = df["correct_answer"].astype(str).str.strip().str.upper()

# Required columns check
required_columns = [
    "scenario_id",
    "scenario_text",
    "question_text",
    "option_A",
    "option_B",
    "option_C",
    "option_D",
    "correct_answer",
    "cultural_explanation",
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns in dataset.csv: {missing}")


# -----------------------------
# Home page
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# API: Get random scenario
# -----------------------------

@app.route("/scenario", methods=["GET"])
def get_scenario():
    row = df.sample(1).iloc[0]

    scenario = {
        "id": row["scenario_id"],
        "scenario_text": row["scenario_text"],
        "question_text": row["question_text"],
        "option_A": row["option_A"],
        "option_B": row["option_B"],
        "option_C": row["option_C"],
        "option_D": row["option_D"],
        "norm_category": row.get("norm_category", ""),
        "language": row.get("language", ""),
        "tom_order": row.get("tom_order", ""),
        "severity": int(row["severity"]) if "severity" in df.columns and pd.notna(row["severity"]) else None,
    }

    return jsonify(scenario)


# -----------------------------
# API: Submit answer
# -----------------------------

@app.route("/submit", methods=["POST"])
def submit_answer():
    data = request.get_json()

    scenario_id = data.get("id")
    user_answer = data.get("answer", "").strip().upper()

    if not scenario_id or user_answer not in ["A", "B", "C", "D"]:
        return jsonify({
            "error": "Missing scenario id or invalid answer."
        }), 400

    matching_rows = df[df["scenario_id"] == scenario_id]

    if matching_rows.empty:
        return jsonify({
            "error": "Scenario not found."
        }), 404

    row = matching_rows.iloc[0]

    correct_answer = str(row["correct_answer"]).strip().upper()
    is_correct = user_answer == correct_answer

    explanation = row["cultural_explanation"]

    response_record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "scenario_id": scenario_id,
        "norm_category": row.get("norm_category", ""),
        "language": row.get("language", ""),
        "tom_order": row.get("tom_order", ""),
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
    }

    log_response(response_record)

    return jsonify({
        "is_correct": is_correct,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "violated_norm": row.get("violated_norm", ""),
        "common_western_misreading": row.get("common_western_misreading", "")
    })


# -----------------------------
# Save user response
# -----------------------------

def log_response(record):
    response_df = pd.DataFrame([record])

    if os.path.exists(RESPONSES_PATH):
        response_df.to_csv(RESPONSES_PATH, mode="a", header=False, index=False)
    else:
        response_df.to_csv(RESPONSES_PATH, mode="w", header=True, index=False)


# -----------------------------
# API: Basic stats
# -----------------------------

@app.route("/stats", methods=["GET"])
def stats():
    if not os.path.exists(RESPONSES_PATH):
        return jsonify({
            "total_responses": 0,
            "accuracy": None
        })

    responses = pd.read_csv(RESPONSES_PATH)

    total = len(responses)
    correct = responses["is_correct"].sum()
    accuracy = correct / total if total > 0 else None

    return jsonify({
        "total_responses": int(total),
        "correct_responses": int(correct),
        "accuracy": round(float(accuracy), 3) if accuracy is not None else None
    })


# -----------------------------
# Run app
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)