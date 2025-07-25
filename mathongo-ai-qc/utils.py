import csv
import os
from datetime import datetime
import uuid

CSV_FILE = "question_versions.csv"

def load_prompt(prompt_name: str) -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", f"{prompt_name}.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "question_id", "version_number", "timestamp", "created_by",
                "original_text", "improved_text",
                "correctness_feedback_is_correct", "correctness_feedback_errors", "correctness_feedback_explanation",
                "language_feedback_issues_found", "language_feedback_feedback", "language_feedback_explanation",
                "improvement_justification",
                "metadata_topic", "metadata_subtopic", "metadata_blooms_level", "metadata_difficulty"
            ])
        print(f"Initialized CSV file: {CSV_FILE}")

def append_question_version(
    question_id: str,
    original_text: str,
    created_by: str,
    version_number: int,
    improved_text: str = "",
    correctness_feedback: dict = None,
    language_feedback: dict = None,
    improvement_feedback: dict = None,
    metadata_feedback: dict = None
):
    timestamp = datetime.now().isoformat()

    correctness_is_correct = correctness_feedback.get("is_correct") if correctness_feedback else None
    correctness_errors = "; ".join(correctness_feedback.get("errors", [])) if correctness_feedback and correctness_feedback.get("errors") else ""
    correctness_explanation = correctness_feedback.get("explanation") if correctness_feedback else ""

    language_issues_found = language_feedback.get("issues_found") if language_feedback else None
    language_feedback_str = "; ".join(language_feedback.get("feedback", [])) if language_feedback and language_feedback.get("feedback") else ""
    language_explanation = language_feedback.get("explanation") if language_feedback else ""

    improvement_justification = improvement_feedback.get("justification") if improvement_feedback else ""

    metadata_topic = metadata_feedback.get("topic") if metadata_feedback else ""
    metadata_subtopic = metadata_feedback.get("subtopic") if metadata_feedback else ""
    metadata_blooms_level = metadata_feedback.get("blooms_level") if metadata_feedback else ""
    metadata_difficulty = metadata_feedback.get("difficulty") if metadata_feedback else ""

    row = {
        "question_id": question_id,
        "version_number": version_number,
        "timestamp": timestamp,
        "created_by": created_by,
        "original_text": original_text,
        "improved_text": improved_text,
        "correctness_feedback_is_correct": str(correctness_is_correct).lower() if correctness_is_correct is not None else "",
        "correctness_feedback_errors": correctness_errors,
        "correctness_feedback_explanation": correctness_explanation,
        "language_feedback_issues_found": str(language_issues_found).lower() if language_issues_found is not None else "",
        "language_feedback_feedback": language_feedback_str,
        "language_feedback_explanation": language_explanation,
        "improvement_justification": improvement_justification,
        "metadata_topic": metadata_topic,
        "metadata_subtopic": metadata_subtopic,
        "metadata_blooms_level": metadata_blooms_level,
        "metadata_difficulty": metadata_difficulty
    }

    headers = [
        "question_id", "version_number", "timestamp", "created_by",
        "original_text", "improved_text",
        "correctness_feedback_is_correct", "correctness_feedback_errors", "correctness_feedback_explanation",
        "language_feedback_issues_found", "language_feedback_feedback", "language_feedback_explanation",
        "improvement_justification",
        "metadata_topic", "metadata_subtopic", "metadata_blooms_level", "metadata_difficulty"
    ]

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(row)
    print(f"Appended version {version_number} for question {question_id} to {CSV_FILE}")


def get_question_versions(question_id: str):
    if not os.path.exists(CSV_FILE):
        return []

    versions = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("question_id") == question_id:
                if "version_number" in row:
                    row["version_number"] = int(row["version_number"])
                if "correctness_feedback_is_correct" in row:
                    row["correctness_feedback_is_correct"] = row["correctness_feedback_is_correct"].lower() == 'true'
                if "language_feedback_issues_found" in row:
                    row["language_feedback_issues_found"] = row["language_feedback_issues_found"].lower() == 'true'
                if "correctness_feedback_errors" in row and row["correctness_feedback_errors"]:
                    row["correctness_feedback_errors"] = row["correctness_feedback_errors"].split('; ')
                else:
                    row["correctness_feedback_errors"] = []
                if "language_feedback_feedback" in row and row["language_feedback_feedback"]:
                    row["language_feedback_feedback"] = row["language_feedback_feedback"].split('; ')
                else:
                    row["language_feedback_feedback"] = []

                versions.append(row)
    return versions

def get_next_version_number(question_id: str) -> int:
    versions = get_question_versions(question_id)
    if not versions:
        return 1
    return max(v["version_number"] for v in versions) + 1

if __name__ == "__main__":
    pass
