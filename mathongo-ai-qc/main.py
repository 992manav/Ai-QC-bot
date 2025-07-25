import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from fastapi.responses import FileResponse
import os
import json
from langgraph_flow import app as langgraph_app, QuestionState
from utils import append_question_version, get_question_versions, get_next_version_number, initialize_csv

initialize_csv()

app = FastAPI(
    title="AI QC + Enhancement Bot for Question Banks",
    description="Backend system to process MCQ/short-answer questions using Gemini LLM for QC, enhancement, and metadata extraction, with robust versioning.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessQuestionRequest(BaseModel):
    question_text: str
    created_by: str

class CorrectnessFeedback(BaseModel):
    is_correct: Optional[bool] = None
    errors: Optional[List[str]] = None
    explanation: Optional[str] = None

class LanguageFeedback(BaseModel):
    issues_found: Optional[bool] = None
    feedback: Optional[List[str]] = None
    explanation: Optional[str] = None

class ImprovementFeedback(BaseModel):
    improved_question: Optional[str] = None
    justification: Optional[str] = None

class MetadataFeedback(BaseModel):
    topic: Optional[str] = None
    subtopic: Optional[str] = None
    blooms_level: Optional[str] = None
    difficulty: Optional[str] = None

class QuestionVersion(BaseModel):
    question_id: str
    version_number: int
    timestamp: str
    created_by: str
    original_text: str
    improved_text: str
    correctness_feedback: Optional[CorrectnessFeedback] = None
    language_feedback: Optional[LanguageFeedback] = None
    improvement_feedback: Optional[ImprovementFeedback] = None
    metadata: Optional[MetadataFeedback] = None

class ProcessQuestionResponse(BaseModel):
    question_id: str
    version_number: int
    original_question: str
    processed_question: str
    version_history: List[QuestionVersion]

@app.post("/process_question/", response_model=ProcessQuestionResponse, summary="Process a question with AI QC and Enhancement")
async def process_question(request: ProcessQuestionRequest):
    """
    Accepts a question, processes it through AI agents (correctness, language, improvement, metadata),
    saves all versions, and returns combined feedback and version history.
    """
    question_id = str(uuid.uuid4())
    original_text = request.question_text
    created_by = request.created_by

    initial_version_number = get_next_version_number(question_id)
    append_question_version(
        question_id=question_id,
        original_text=original_text,
        created_by=created_by,
        version_number=initial_version_number
    )

    initial_state: QuestionState = {
        "question_text": original_text,
        "original_question_text": original_text,
        "correctness_feedback": {},
        "language_feedback": {},
        "improvement_feedback": {},
        "metadata_feedback": {},
        "errors": []
    }
    final_state = langgraph_app.invoke(initial_state)

    correctness_fb_raw = final_state.get("correctness_feedback", {})
    language_fb_raw = final_state.get("language_feedback", {})
    improvement_fb_raw = final_state.get("improvement_feedback", {})
    metadata_fb_raw = final_state.get("metadata_feedback", {})
    processed_question_text = final_state.get("question_text", original_text)

    ai_version_number = get_next_version_number(question_id)
    append_question_version(
        question_id=question_id,
        original_text=original_text,
        created_by="AI",
        version_number=ai_version_number,
        improved_text=processed_question_text,
        correctness_feedback=correctness_fb_raw,
        language_feedback=language_fb_raw,
        improvement_feedback=improvement_fb_raw,
        metadata_feedback=metadata_fb_raw
    )

    all_versions_raw = get_question_versions(question_id)
    
    all_versions = []
    for v_raw in all_versions_raw:
        correctness_fb = CorrectnessFeedback(
            is_correct=v_raw.get("correctness_feedback_is_correct"),
            errors=v_raw.get("correctness_feedback_errors"),
            explanation=v_raw.get("correctness_feedback_explanation")
        ) if v_raw.get("correctness_feedback_is_correct") is not None else None

        language_fb = LanguageFeedback(
            issues_found=v_raw.get("language_feedback_issues_found"),
            feedback=v_raw.get("language_feedback_feedback"),
            explanation=v_raw.get("language_feedback_explanation")
        ) if v_raw.get("language_feedback_issues_found") is not None else None

        improvement_fb = ImprovementFeedback(
            improved_question=v_raw.get("improved_text"),
            justification=v_raw.get("improvement_justification")
        ) if v_raw.get("improvement_justification") is not None else None

        metadata_fb = MetadataFeedback(
            topic=v_raw.get("metadata_topic"),
            subtopic=v_raw.get("metadata_subtopic"),
            blooms_level=v_raw.get("metadata_blooms_level"),
            difficulty=v_raw.get("metadata_difficulty")
        ) if v_raw.get("metadata_topic") is not None else None

        all_versions.append(QuestionVersion(
            question_id=v_raw["question_id"],
            version_number=v_raw["version_number"],
            timestamp=v_raw["timestamp"],
            created_by=v_raw["created_by"],
            original_text=v_raw["original_text"],
            improved_text=v_raw["improved_text"],
            correctness_feedback=correctness_fb,
            language_feedback=language_fb,
            improvement_feedback=improvement_fb,
            metadata=metadata_fb
        ))

  

        response_data = ProcessQuestionResponse(
            question_id=question_id,
            version_number=ai_version_number,
            original_question=original_text,
            processed_question=processed_question_text,
            version_history=all_versions
        )

        print("[RESPONSE JSON] Final API response:")
        print(json.dumps(response_data.dict()["version_history"][-1], indent=2))

    return response_data


@app.get("/questions/{question_id}/versions", response_model=List[QuestionVersion], summary="Retrieve all versions of a question")
async def get_question_versions_endpoint(question_id: str):
    """
    Retrieves and returns all stored versions for a given question ID.
    """
    versions_raw = get_question_versions(question_id)
    if not versions_raw:
        raise HTTPException(status_code=404, detail=f"No versions found for question_id: {question_id}")
    
    all_versions = []
    for v_raw in versions_raw:
        correctness_fb = CorrectnessFeedback(
            is_correct=v_raw.get("correctness_feedback_is_correct"),
            errors=v_raw.get("correctness_feedback_errors"),
            explanation=v_raw.get("correctness_feedback_explanation")
        ) if v_raw.get("correctness_feedback_is_correct") is not None else None

        language_fb = LanguageFeedback(
            issues_found=v_raw.get("language_feedback_issues_found"),
            feedback=v_raw.get("language_feedback_feedback"),
            explanation=v_raw.get("language_feedback_explanation")
        ) if v_raw.get("language_feedback_issues_found") is not None else None

        improvement_fb = ImprovementFeedback(
            improved_question=v_raw.get("improved_text"),
            justification=v_raw.get("improvement_justification")
        ) if v_raw.get("improvement_justification") is not None else None

        metadata_fb = MetadataFeedback(
            topic=v_raw.get("metadata_topic"),
            subtopic=v_raw.get("metadata_subtopic"),
            blooms_level=v_raw.get("metadata_blooms_level"),
            difficulty=v_raw.get("metadata_difficulty")
        ) if v_raw.get("metadata_topic") is not None else None

        all_versions.append(QuestionVersion(
            question_id=v_raw["question_id"],
            version_number=v_raw["version_number"],
            timestamp=v_raw["timestamp"],
            created_by=v_raw["created_by"],
            original_text=v_raw["original_text"],
            improved_text=v_raw["improved_text"],
            correctness_feedback=correctness_fb,
            language_feedback=language_fb,
            improvement_feedback=improvement_fb,
            metadata=metadata_fb
        ))
    
    return all_versions


from fastapi import HTTPException
from fastapi.responses import FileResponse
import os

@app.get("/download-csv", summary="Download the entire question_versions.csv file")
async def download_csv():
    cwd = os.getcwd()
    print(f"[DOWNLOAD CSV] Current working directory: {cwd}")

    dir_listing = os.listdir(cwd)
    print(f"[DOWNLOAD CSV] Files in cwd: {dir_listing}")

    csv_path = os.path.join(cwd, "question_versions.csv")
    print(f"[DOWNLOAD CSV] Attempting to serve: {csv_path}")

    if not os.path.exists(csv_path):
        print(f"[DOWNLOAD CSV] File not found: {csv_path}")
        raise HTTPException(status_code=404, detail="CSV file not found.")

    print(f"[DOWNLOAD CSV] File found, sending: {csv_path}")
    return FileResponse(csv_path, media_type="text/csv", filename="question_versions.csv")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
