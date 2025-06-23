// // App.jsx
// src/App.jsx
// src/App.jsx
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import QuestionForm from './components/QuestionForm';
import Footer from './components/Footer'; 
import AnswerDisplay from './components/AnswerDisplay';
import Contact from './components/Contact';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 flex flex-col">
      <Navbar />
      <Hero />
      <main className="flex-grow">
        <QuestionForm />
        <AnswerDisplay />
      </main>
      <About />
      <Contact />
      <Footer />
      
    </div>
  );
}

export default App;



// import Hero from './components/Hero';
// import Footer from './components/Footer';

// import { useState } from "react";
// import QuestionForm from "./components/QuestionForm";
// import AnswerDisplay from "./components/AnswerDisplay";

// function App() {
//   const [answerData, setAnswerData] = useState(null);
//   const [lastQuestion, setLastQuestion] = useState("");

//   const handleAskQuestion = async (question) => {
//     setLastQuestion(question);
//     try {
//       const response = await fetch("http://127.0.0.1:8000/ask", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ question: question, mode: "brief" }),
//       });
//       const data = await response.json();
//       setAnswerData(data);
//     } catch (error) {
//       console.error("Error fetching answer:", error);
//     }
//   };

//   const handleViewMore = async () => {
//     try {
//       const response = await fetch("http://127.0.0.1:8000/ask", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ question: lastQuestion, mode: "full" }),
//       });
//       const data = await response.json();
//       setAnswerData(data);
//     } catch (error) {
//       console.error("Error fetching detailed answer:", error);
//     }
//   };

//   return (
//     <div className="max-w-2xl mx-auto mt-10 p-6">
//       <h1 className="text-3xl font-bold mb-6 text-center">JEE Study Assistant</h1>
//       <QuestionForm onSubmit={handleAskQuestion} />
//       <AnswerDisplay answerData={answerData} onViewMore={handleViewMore} />
//     </div>
//   );
// }

// export default App;






// // import React, { useState } from "react";
// // import QuestionForm from "./components/QuestionForm";
// // import AnswerDisplay from "./components/AnswerDisplay";

// // function App() {
// //   const [answer, setAnswer] = useState("");

// //   return (
// //     <div className="min-h-screen bg-gray-500 p-4">
// //       <h1 className="text-3xl font-bold mb-4 text-center">JEE Study Assistant</h1>
// //       <QuestionForm setAnswer={setAnswer} />
// //       <AnswerDisplay answer={answer} />
// //     </div>
// //   );
// // }

// // export default App;

// // const App = () => {
// //   return (
// //     <div className="text-3xl text-red-500">
// //       Tailwind is working ✅
// //     </div>
// //   );
// // };

// // export default App;
