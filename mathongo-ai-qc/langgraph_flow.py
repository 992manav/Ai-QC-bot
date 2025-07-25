from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator

from agents.correctness_agent import correctness_agent
from agents.language_agent import language_agent
from agents.improvement_agent import improvement_agent
from agents.metadata_agent import metadata_agent

class QuestionState(TypedDict):
    question_text: str
    original_question_text: str
    correctness_feedback: dict
    language_feedback: dict
    improvement_feedback: dict
    metadata_feedback: dict
    errors: Annotated[list[str], operator.add]

def call_correctness_agent(state: QuestionState):
    print("Calling Correctness Agent...")
    question_text = state["question_text"]
    try:
        feedback = correctness_agent(question_text)
        return {"correctness_feedback": feedback}
    except Exception as e:
        error_msg = f"Error calling correctness_agent: {e}"
        print(error_msg)
        return {"correctness_feedback": {"is_correct": False, "errors": [error_msg], "explanation": error_msg}, "errors": [error_msg]}

def call_language_agent(state: QuestionState):
    print("Calling Language Agent...")
    question_text = state["question_text"]
    try:
        feedback = language_agent(question_text)
        return {"language_feedback": feedback}
    except Exception as e:
        error_msg = f"Error calling language_agent: {e}"
        print(error_msg)
        return {"language_feedback": {"issues_found": True, "feedback": [error_msg], "explanation": error_msg}, "errors": [error_msg]}

def call_improvement_agent(state: QuestionState):
    print("Calling Improvement Agent...")
    question_text = state["question_text"]
    try:
        feedback = improvement_agent(question_text)
        return {"improvement_feedback": feedback, "question_text": feedback.get("improved_question", question_text)}
    except Exception as e:
        error_msg = f"Error calling improvement_agent: {e}"
        print(error_msg)
        return {"improvement_feedback": {"improved_question": question_text, "justification": error_msg}, "errors": [error_msg]}

def call_metadata_agent(state: QuestionState):
    print("Calling Metadata Agent...")
    question_text = state["question_text"]
    try:
        feedback = metadata_agent(question_text)
        return {"metadata_feedback": feedback}
    except Exception as e:
        error_msg = f"Error calling metadata_agent: {e}"
        print(error_msg)
        return {"metadata_feedback": {"topic": "Error", "subtopic": "Error", "blooms_level": "Error", "difficulty": "Error"}, "errors": [error_msg]}

workflow = StateGraph(QuestionState)

workflow.add_node("correctness", call_correctness_agent)
workflow.add_node("language", call_language_agent)
workflow.add_node("improvement", call_improvement_agent)
workflow.add_node("metadata", call_metadata_agent)

workflow.set_entry_point("correctness")

workflow.add_edge("correctness", "language")
workflow.add_edge("language", "improvement")
workflow.add_edge("improvement", "metadata")

workflow.add_edge("metadata", END)

app = workflow.compile()
