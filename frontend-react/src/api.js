const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const processQuestion = async (questionText, createdBy) => {
  try {
    const response = await fetch(`${API_BASE_URL}/process_question/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question_text: questionText,
        created_by: createdBy,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to process question");
    }

    return await response.json();
  } catch (error) {
    console.error("Error processing question:", error);
    throw error;
  }
};

export const getQuestionVersions = async (questionId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/questions/${questionId}/versions`
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fetch question versions");
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching versions for question ${questionId}:`, error);
    throw error;
  }
};
