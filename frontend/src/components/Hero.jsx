import Typewriter from "typewriter-effect";

function Hero() {
  return (
    <section
      id="hero"
      className="h-screen flex flex-col justify-center items-center text-center bg-gradient-to-br from-blue-100 to-purple-200 pt-20 px-6"
    >
      <h1 className="text-5xl md:text-7xl font-bold text-blue-800 mb-6">
        Welcome to <span className="text-purple-600 font-extrabold">AceJEE</span>
      </h1>

      <div className="text-xl md:text-2xl text-gray-700 mb-8">
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
        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full shadow-lg transform hover:scale-105 transition duration-300"
      >
        Ask Your Question
      </a>
    </section>
  );
}
export default Hero;