// src/components/About.jsx
function About() {
    return (
      <section id="about" className="py-16 bg-gradient-to-br from-blue-100 to-purple-200 text-center">
        <div className="container mx-auto text-center px-6">
          <h2 className="text-4xl font-bold text-blue-700 mb-6 animate-none">About AceJEE</h2>
          <p className="text-lg text-gray-700 max-w-3xl mx-auto leading-relaxed">
            AceJEE is an AI-powered study companion specially designed for JEE aspirants. It retrieves
            accurate answers from textbooks using Retrieval-Augmented Generation (RAG) and refines them
            with powerful language models. Our mission is to empower students with instant, reliable,
            and personalized learning!
          </p>
        </div>
      </section>
    );
  }
  
  export default About;
  