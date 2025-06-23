import React, { useState } from "react";
import Markdown from "react-markdown";

const QuestionForm = () => {
  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState("brief");
  const [answer, setAnswer] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setAnswer(null);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, mode }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) throw new Error("Failed to fetch answer");
      const data = await response.json();
      setAnswer(data.llm_answer);
    } catch (error) {
      console.error(error);
      setError("⚠️ Failed to get the answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section
      id="questionForm"
      className="pt-20 min-h-screen flex flex-col items-center justify-start gap-4 bg-gradient-to-br from-blue-100 to-purple-200 px-4 transition-all duration-500"
    >
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg rounded-xl p-8 w-full max-w-2xl animate-fade-in"
      >

        <h1 className="text-3xl font-bold text-center mb-6 text-gray-800 transition-all duration-300">
          Your JEE Question
        </h1>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask your question here..."
          className="w-full p-4 border rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition-all duration-300"
          rows="4"
          required
        ></textarea>

        <div className="flex justify-center items-center gap-6 mb-6 transition-all duration-300">
          <label className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition">
            <input
              type="radio"
              name="mode"
              value="brief"
              checked={mode === "brief"}
              onChange={(e) => setMode(e.target.value)}
            />
            Brief Answer
          </label>
          <label className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition">
            <input
              type="radio"
              name="mode"
              value="full"
              checked={mode === "full"}
              onChange={(e) => setMode(e.target.value)}
            />
            Detailed Answer
          </label>
        </div>

        <button
  type="submit"
  className="w-full py-3 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold text-lg shadow-md hover:opacity-90 transition relative"
  disabled={loading}
>
  {loading ? (
    <span className="flex justify-center items-center gap-2">
      <svg
        className="animate-spin h-5 w-5 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8z"
              ></path>
            </svg>
            Loading...
          </span>
        ) : (
            "Ask Now"
       )}
      </button>

      </form>

      {error && (
        <div className="mt-6 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 w-full max-w-2xl rounded-lg animate-pulse">
          {error}
        </div>
      )}

      {answer && (
        <div className="mt-10 p-6 bg-white rounded-2xl shadow-lg w-full max-w-2xl transition-opacity duration-500 ease-in-out animate-fade-in">
          <h2 className="text-xl font-semibold mb-3 text-indigo-600">Answer:</h2>
          <Markdown>{String(answer)}</Markdown>
        </div>
      )}
    </section>
  );
};

export default QuestionForm;
