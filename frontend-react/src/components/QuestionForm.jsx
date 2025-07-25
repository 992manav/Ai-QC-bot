import React, { useState } from "react";

const QuestionForm = ({ onSubmit, loading }) => {
  const [questionText, setQuestionText] = useState("");
  const [createdBy, setCreatedBy] = useState("User");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (questionText.trim()) {
      onSubmit(questionText, createdBy);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="question-form">
      <h2>Submit a New Question</h2>
      <textarea
        value={questionText}
        onChange={(e) => setQuestionText(e.target.value)}
        placeholder="Enter your question here..."
        rows="8"
        required
        disabled={loading}
      ></textarea>
      <input
        type="text"
        value={createdBy}
        onChange={(e) => setCreatedBy(e.target.value)}
        placeholder="Your Name"
        required
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Processing..." : "Process Question"}
      </button>
    </form>
  );
};

export default QuestionForm;
