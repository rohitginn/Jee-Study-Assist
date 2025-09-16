import Typewriter from "typewriter-effect";

function Hero() {
  return (
    <section
      id="hero"
      className="h-screen w-screen flex flex-col items-center justify-center  bg-neutral-50 dark:bg-neutral-950
      "
    >
      <h1
        className="
          z-10 mb-6 text-5xl md:text-7xl font-bold
          text-blue-800 dark:text-blue-300
        "
      >
        Welcome to{" "}
        <span className="text-purple-600 dark:text-purple-400 font-extrabold">
          AceJEE
        </span>
      </h1>

      <div
        className="
          z-10 mb-8 text-xl md:text-2xl
          text-gray-700 dark:text-gray-300
        "
      >
        <Typewriter
          options={{
            strings: [
              "Master Your JEE Preparation 🚀",
              "Get Quick, Reliable Answers 📚",
              "Ace Every Concept with Confidence! 🎯",
            ],
            autoStart: true,
            loop: true,
          }}
        />
      </div>

      <a
        href="#questionForm"
        className="
          z-10 font-bold py-3 px-8 rounded-full shadow-lg
          bg-blue-600 hover:bg-blue-700
          dark:bg-blue-500 dark:hover:bg-blue-600
          text-white transform hover:scale-105 transition duration-300
        "
      >
        Ask Your Question
      </a>
    </section>
  );
}

export default Hero;
