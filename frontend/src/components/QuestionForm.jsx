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
      className="
        relative z-10
        pt-20 pb-24
        min-h-[100vh]  /* fills viewport before asking */
        w-full
        flex flex-col items-center
        bg-neutral-50 dark:bg-transparent
        px-4
      "
    >
      <form
        onSubmit={handleSubmit}
        className="
          w-full max-w-2xl p-8 rounded-xl shadow-lg
          bg-white dark:bg-gray-800
          text-gray-800 dark:text-gray-100
          border border-gray-200 dark:border-gray-700
        "
      >
        <h1 className="text-2xl font-bold text-center mb-6 font-SUSE">
          Your JEE Question
        </h1>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask your question here..."
          rows="4"
          required
          className="
            w-full p-4 mb-6 border rounded-lg
            text-gray-800 dark:text-gray-100
            bg-white dark:bg-gray-700
            focus:outline-none focus:ring-2 focus:ring-indigo-400
          "
        />

        {/* Mode Selection */}
        <div className="flex justify-center items-center gap-8 mb-6">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="mode"
              value="brief"
              checked={mode === "brief"}
              onChange={() => setMode("brief")}
            />
            <span>Brief Answer</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="mode"
              value="full"
              checked={mode === "full"}
              onChange={() => setMode("full")}
            />
            <span>Detailed Answer</span>
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 rounded-lg bg-indigo-500 text-white font-semibold text-lg"
        >
          {loading ? (
            <div className="flex justify-center items-center">
              <div style={{ transform: "scale(0.5)" }}>
                <div className="book">
                  <div className="book__pg-shadow"></div>
                  <div className="book__pg"></div>
                  <div className="book__pg book__pg--2"></div>
                  <div className="book__pg book__pg--3"></div>
                  <div className="book__pg book__pg--4"></div>
                  <div className="book__pg book__pg--5"></div>
                </div>
              </div>
            </div>
          ) : (
            "Ask Now"
          )}
        </button>
      </form>

      {error && (
        <div className="mt-6 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 w-full max-w-2xl rounded-lg">
          {error}
        </div>
      )}

      {answer && (
        <div className="mt-10 p-6 bg-white dark:bg-gray-800 dark:text-gray-100 rounded-2xl shadow-lg w-full max-w-2xl">
          <h2 className="text-xl font-semibold mb-3 text-indigo-600">
            Answer:
          </h2>
          <Markdown>{String(answer)}</Markdown>
        </div>
      )}
    </section>
  );
};

export default QuestionForm;
