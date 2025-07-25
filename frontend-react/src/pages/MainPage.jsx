import React from "react";
import QuestionForm from "../components/QuestionForm";
import LoadingSpinner from "../components/LoadingSpinner";
import FeedbackDisplay from "../components/FeedbackDisplay";
import useQuestionProcessor from "../hooks/useQuestionProcessor";
import "./../styles/VersionHistory.css";

export default function MainPage() {
  const {
    loading,
    error,
    responseData,
    selectedVersion,
    handleProcessQuestion,
    navigate,
  } = useQuestionProcessor();

  return (
    <div className="app-container fade-in">
      <h1 className="slide-in">AI QC + Enhancement Bot for Question Banks</h1>
      <button
        className="view-history-button"
        style={{ marginBottom: 16, marginRight: 8 }}
        onClick={() => navigate("/csv-view")}
      >
        <i className="fas fa-table"></i> View Full CSV
      </button>

      <div className="scale-in">
        <QuestionForm onSubmit={handleProcessQuestion} loading={loading} />
      </div>

      {responseData?.question_id && (
        <button
          className="view-history-button"
          onClick={() =>
            navigate(`/version-history/${responseData.question_id}`)
          }
        >
          <i className="fas fa-history"></i> View Version History
        </button>
      )}

      {loading && <LoadingSpinner />}
      {error && (
        <div className="error-message slide-in">
          <i className="fas fa-exclamation-circle"></i>
          Error: {error}
        </div>
      )}

      {responseData && selectedVersion && (
        <div className="results-section fade-in">
          <FeedbackDisplay
            feedback={{
              is_correct: selectedVersion.correctness_feedback?.is_correct,
              errors: selectedVersion.correctness_feedback?.errors,
              explanation: selectedVersion.correctness_feedback?.explanation,
              issues_found: selectedVersion.language_feedback?.issues_found,
              feedback: selectedVersion.language_feedback?.feedback,
              language_feedback_explanation:
                selectedVersion.language_feedback?.explanation,
              improved_question:
                selectedVersion.improvement_feedback?.improved_question,
              justification:
                selectedVersion.improvement_feedback?.justification,
              topic: selectedVersion.metadata?.topic,
              subtopic: selectedVersion.metadata?.subtopic,
              blooms_level: selectedVersion.metadata?.blooms_level,
              difficulty: selectedVersion.metadata?.difficulty,
            }}
            processedQuestion={
              selectedVersion.processed_question ||
              selectedVersion.improved_text ||
              selectedVersion.original_text
            }
            originalQuestion={
              selectedVersion.original_question || selectedVersion.original_text
            }
          />
        </div>
      )}
    </div>
  );
}
