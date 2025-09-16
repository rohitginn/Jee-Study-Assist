import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import About from "./components/About";
import QuestionForm from "./components/QuestionForm";
import Footer from "./components/Footer";
import AnswerDisplay from "./components/AnswerDisplay";
import Contact from "./components/Contact";
import { DotPattern } from "./components/ui/dot-pattern";

function App() {
  return (
    <div className="relative h-screen w-screen bg-neutral-50 dark:bg-neutral-950">
      {/* Full-page DotPattern */}
      <DotPattern
        width={24}
        height={24}
        cr={1.5}
        cx={2}
        cy={2}
        x={10}
        y={10}
        glow={true}
        className="fixed inset-0 text-yellow-500 dark:text-amber-600 opacity-100 z-0"
      />

      {/* Page content */}
      <div className=" flex flex-col">
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
    </div>
  );
}

export default App;
