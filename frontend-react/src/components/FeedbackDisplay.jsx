import React from "react";
import "../styles/animations.css";

const FeedbackDisplay = ({ feedback, processedQuestion, originalQuestion }) => {
  if (!feedback) {
    return null;
  }

  return (
    <div className="feedback-display fade-in">
      <div className="accent-bg">
        <h2 className="slide-in">Processed Question & Feedback</h2>
        <div className="response-card card-hover">
          <h3>Original Question:</h3>
          <p>{originalQuestion}</p>
        </div>
        <div className="response-card card-hover scale-in">
          <h3>Processed Question:</h3>
          <p>{processedQuestion}</p>
        </div>
      </div>
      <div className="response-card card-hover">
        <h3>Correctness Feedback:</h3>
        <p>
          <strong>Is Correct:</strong>{" "}
          {feedback.is_correct !== undefined
            ? feedback.is_correct
              ? "Yes"
              : "No"
            : "N/A"}
        </p>
        {feedback.errors && feedback.errors.length > 0 && (
          <>
            <p>
              <strong>Errors:</strong>
            </p>
            <ul>
              {feedback.errors.map((error, index) => (
                <li key={index}>{error}</li>
              ))}
            </ul>
          </>
        )}
        {feedback.explanation && (
          <p>
            <strong>Explanation:</strong> {feedback.explanation}
          </p>
        )}
      </div>
      <div className="response-card">
        <h3>Language Feedback:</h3>
        <p>
          <strong>Issues Found:</strong>{" "}
          {feedback.issues_found !== undefined
            ? feedback.issues_found
              ? "Yes"
              : "No"
            : "N/A"}
        </p>
        {feedback.feedback && feedback.feedback.length > 0 && (
          <>
            <p>
              <strong>Feedback:</strong>
            </p>
            <ul>
              {feedback.feedback.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </>
        )}
        {feedback.language_feedback_explanation && (
          <p>
            <strong>Explanation:</strong>{" "}
            {feedback.language_feedback_explanation}
          </p>
        )}
      </div>
      <div className="response-card">
        <h3>Improvement Feedback:</h3>
        {feedback.improved_question && (
          <p>
            <strong>Improved Question:</strong> {feedback.improved_question}
          </p>
        )}
        {feedback.justification && (
          <p>
            <strong>Justification:</strong> {feedback.justification}
          </p>
        )}
      </div>
      <div className="response-card">
        <h3>Metadata:</h3>
        <p>
          <strong>Topic:</strong> {feedback.topic || "N/A"}
        </p>
        <p>
          <strong>Subtopic:</strong> {feedback.subtopic || "N/A"}
        </p>
        <p>
          <strong>Bloom's Level:</strong> {feedback.blooms_level || "N/A"}
        </p>
        <p>
          <strong>Difficulty:</strong> {feedback.difficulty || "N/A"}
        </p>
      </div>
    </div>
  );
};

export default FeedbackDisplay;
