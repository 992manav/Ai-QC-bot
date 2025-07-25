import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { processQuestion } from "../api";

export default function useQuestionProcessor() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [selectedVersion, setSelectedVersion] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedVersion = localStorage.getItem("selectedVersion");
    if (storedVersion) {
      try {
        setSelectedVersion(JSON.parse(storedVersion));
      } catch (e) {
        console.error("Error parsing stored version:", e);
      }
      localStorage.removeItem("selectedVersion");
    }
  }, []);

  const handleProcessQuestion = useCallback(async (questionText, createdBy) => {
    setLoading(true);
    setError(null);
    setResponseData(null);
    setSelectedVersion(null);

    try {
      const data = await processQuestion(questionText, createdBy);
      setResponseData(data);
      const latestAIProcessedVersion = Array.isArray(data.version_history)
        ? data.version_history.find(
            (v) => v.version_number === data.version_number
          )
        : null;
      setSelectedVersion(latestAIProcessedVersion || data);
    } catch (err) {
      setError(err.message || "An unknown error occurred");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    responseData,
    selectedVersion,
    handleProcessQuestion,
    navigate,
  };
}
