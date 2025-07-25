import React from "react";
import "./LoadingSpinner.css";

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner-container">
      <div className="loading-spinner-circle"></div>
      <p>Processing your question...</p>
    </div>
  );
};

export default LoadingSpinner;
