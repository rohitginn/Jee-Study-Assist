import ReactMarkdown from "react-markdown";

const AnswerDisplay = ({ answer, loading, mode }) => {
  if (loading) {
    return (
      <div className="mt-6 text-center text-gray-500 animate-pulse">
        Loading answer...
      </div>
    );
  }

  if (!answer) return null;

  return (
    <div className="mt-6 p-4 border rounded-xl bg-gray-50">
      <h2 className="text-lg font-bold mb-2">Answer:</h2>

      {/* Render answer based on mode */}
      <ReactMarkdown className="text-gray-700 whitespace-pre-wrap">
        {mode === "brief" ? answer.slice(0, 300) : answer}  {/* Show brief or full answer */}
      </ReactMarkdown>
    </div>
  );
};

export default AnswerDisplay;






// import { useState } from 'react';

// function AnswerDisplay({ answer }) {
//   const [linesToShow, setLinesToShow] = useState(5);

//   if (!answer) {
//     return null;
//   }

//   // Split answer into lines
//   const lines = answer.split('\n');

//   // Only show limited lines
//   const visibleText = lines.slice(0, linesToShow).join('\n');

//   const handleViewMore = () => {
//     if (linesToShow < 10) {
//       setLinesToShow(10);
//     }
//   };

//   return (
//     <div className="p-4 bg-gray-100 rounded shadow">
//       <h2 className="text-lg font-bold mb-2">Answer:</h2>
//       <pre className="text-gray-800 whitespace-pre-wrap">{visibleText}</pre>

//       {lines.length > linesToShow && (
//         <button
//           onClick={handleViewMore}
//           className="mt-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
//         >
//           View More
//         </button>
//       )}
//     </div>
//   );
// }

// export default AnswerDisplay;
