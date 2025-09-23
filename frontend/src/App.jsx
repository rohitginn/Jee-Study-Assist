import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import About from "./components/About";
import QuestionForm from "./components/QuestionForm";
import Footer from "./components/Footer";
import AnswerDisplay from "./components/AnswerDisplay";
import Contact from "./components/Contact";
import { DotPattern } from "./components/ui/dot-pattern";
import Features from "./components/Features";


function App() {
  return (
    <div className="relative h-screen w-screen bg-neutral-50 dark:bg-neutral-950">
      {/* Full-page DotPattern */}
      <div className="min-h-screen w-full relative bg-black">
        {/* Prismatic Aurora Burst - Multi-layered Gradient */}
        <div
          className="absolute h-screen inset-0 z-0"
          style={{
            background: `
          radial-gradient(ellipse 120% 80% at 70% 20%, rgba(255, 20, 147, 0.15), transparent 40%),
          radial-gradient(ellipse 100% 60% at 30% 10%, rgba(0, 255, 255, 0.12), transparent 40%),
          radial-gradient(ellipse 90% 70% at 50% 0%, rgba(138, 43, 226, 0.18), transparent 65%),
          radial-gradient(ellipse 110% 50% at 80% 30%, rgba(255, 215, 0, 0.08), transparent 40%),
          #000000
        `,
          }}
        />
        {/* Your Content/Components */}
        <div className=" flex flex-col">
          <Navbar />
          <Hero />
          <Features />

          <div className="min-h-screen w-full relative">
            {/* Azure Depths */}
            <div
              className="absolute inset-0 z-0"
              style={{
                background: "radial-gradient(125% 125% at 40% 10%, #000000 10%, #010133 100%)",
              }}
            />
            {/* Your Content/Components */}
            <main className="flex-grow">
              <QuestionForm />
              <AnswerDisplay />
            </main>
            
          </div>
          <About />
          <Contact />
          <Footer />
        </div>
      </div>

      {/* Page content */}
    </div>
  );
}

export default App;
