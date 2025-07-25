import React, { useState, useEffect } from "react";
import { getQuestionVersions } from "../api";
import "../styles/VersionHistory.css";

const VersionHistory = ({ questionId }) => {
  const [expandedVersion, setExpandedVersion] = useState(null);
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (questionId) {
      fetchVersions(questionId);
    }
  }, [questionId]);

  const fetchVersions = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getQuestionVersions(id);
      setVersions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!questionId) {
    return <p>Submit a question to see its version history.</p>;
  }

  if (loading) {
    return <p>Loading version history...</p>;
  }

  if (error) {
    return <p className="error-message">Error loading versions: {error}</p>;
  }

  if (versions.length === 0) {
    return <p>No version history available for this question.</p>;
  }

  return (
    <div className="version-history">
      <div className="accent-bg">
        <h3>Version History</h3>
        <table>
          <thead>
            <tr>
              <th>Version</th>
              <th>Created By</th>
              <th>Timestamp</th>
              <th>Summary</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {versions.map((version) => (
              <React.Fragment key={version.version_number}>
                <tr>
                  <td>{version.version_number}</td>
                  <td>{version.created_by}</td>
                  <td>{new Date(version.timestamp).toLocaleString()}</td>
                  <td>
                    <div className="question-preview">
                      {(version.created_by === "User"
                        ? version.original_text
                        : version.improved_text
                      )?.substring(0, 100) ||
                        "No question text provided for this version"}
                      {(version.created_by === "User"
                        ? version.original_text
                        : version.improved_text
                      )?.length > 100 && "..."}
                    </div>
                  </td>
                  <td>
                    <button
                      onClick={() =>
                        setExpandedVersion(
                          expandedVersion === version.version_number
                            ? null
                            : version.version_number
                        )
                      }
                    >
                      {expandedVersion === version.version_number
                        ? "Collapse"
                        : "View Details"}
                    </button>
                  </td>
                </tr>
                {expandedVersion === version.version_number && (
                  <tr className="version-details">
                    <td colSpan="5">
                      <div className="detail-section">
                        <h4>Full Question Text</h4>
                        <pre>
                          {version.created_by === "User"
                            ? version.original_text
                            : version.improved_text ||
                              "No question text provided for this version"}
                        </pre>

                        <h4>Processing Details</h4>
                        <div className="detail-grid">
                          <div>
                            <strong>Correctness:</strong>
                            <pre>
                              {version.correctness_feedback &&
                              Object.keys(version.correctness_feedback).length >
                                0
                                ? JSON.stringify(
                                    version.correctness_feedback,
                                    null,
                                    2
                                  )
                                : "No feedback available"}
                            </pre>
                          </div>
                          <div>
                            <strong>Language Issues:</strong>
                            <pre>
                              {version.language_feedback &&
                              Object.keys(version.language_feedback).length > 0
                                ? JSON.stringify(
                                    version.language_feedback,
                                    null,
                                    2
                                  )
                                : "No feedback available"}
                            </pre>
                          </div>
                          <div>
                            <strong>Improvements:</strong>
                            <pre>
                              {version.improvement_feedback &&
                              Object.keys(version.improvement_feedback).length >
                                0
                                ? JSON.stringify(
                                    version.improvement_feedback,
                                    null,
                                    2
                                  )
                                : "No feedback available"}
                            </pre>
                          </div>
                          <div>
                            <strong>Metadata:</strong>
                            <pre>
                              {version.metadata &&
                              (version.metadata.topic ||
                                version.metadata.subtopic ||
                                version.metadata.blooms_level ||
                                version.metadata.difficulty)
                                ? JSON.stringify(version.metadata, null, 2)
                                : "No metadata available"}
                            </pre>
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VersionHistory;
