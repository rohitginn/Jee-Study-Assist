import React, { useState } from "react";
import ReactMarkdown from "react-markdown";

const AnswerDisplay = ({ answer, loading, mode }) => {
  const [expanded, setExpanded] = useState(false);

  if (loading) {
    return (
      <div className="mt-10 flex justify-center items-center text-gray-500 dark:text-gray-400 animate-pulse">
        Loading answer...
      </div>
    );
  }

  if (!answer) return null;

  // Only show first 150 chars if brief mode and not expanded
  const displayText =
    mode === "brief" && !expanded ? answer.slice(0, 150) + "..." : answer;

  return (
    <div
      className="
        mt-10 w-full max-w-2xl
        p-6
        rounded-2xl
        shadow-lg
        border border-gray-200 dark:border-gray-700
        bg-white dark:bg-gray-800
        text-gray-800 dark:text-gray-100
      "
    >
      <h2 className="text-xl font-semibold mb-4 text-indigo-600">Answer:</h2>

      <ReactMarkdown className="prose prose-sm dark:prose-invert leading-relaxed">
        {displayText}
      </ReactMarkdown>

      {mode === "brief" && answer.length > 300 && (
        <div className="flex justify-center mt-5">
          <button
            onClick={() => setExpanded((prev) => !prev)}
            className="
              px-4 py-2
              bg-indigo-500 hover:bg-indigo-600
              text-white rounded-lg
              transition-colors duration-300
            "
          >
            {expanded ? "View Less" : "View More"}
          </button>
        </div>
      )}
    </div>
  );
};

export default AnswerDisplay;
