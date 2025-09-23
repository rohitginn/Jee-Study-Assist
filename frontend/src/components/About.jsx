import React from "react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../../components/accordion";

const AboutPage = () => {
  const accordionItems = [
  {
    id: "1",
    title: "How does AceJEE fetch textbook answers?",
    content:
      "AceJEE uses Retrieval-Augmented Generation (RAG) with AI models to fetch relevant answers from JEE textbooks in real-time.",
  },
  {
    id: "2",
    title: "Can AceJEE provide step-by-step solutions?",
    content:
      "Yes, for each concept or problem, AceJEE generates detailed, step-by-step explanations tailored for JEE aspirants.",
  },
  {
    id: "3",
    title: "Does AceJEE cover all JEE subjects?",
    content:
      "AceJEE currently covers Physics, Chemistry, and Mathematics with comprehensive content aligned to JEE syllabus.",
  },
  {
    id: "4",
    title: "Can I use AceJEE for previous year questions?",
    content:
      "Absolutely. AceJEE can fetch, explain, and solve previous year JEE questions with detailed insights and tricks.",
  },
  {
    id: "5",
    title: "Is AceJEE available in multiple languages?",
    content:
      "Currently, AceJEE supports English but can be extended to other languages in future updates.",
  },
  {
    id: "6",
    title: "Can AceJEE help with personalized learning?",
    content:
      "Yes, AceJEE tracks your learning pattern and provides personalized explanations and problem suggestions to improve performance.",
  },
];


  return (
    <div className="h-auto flex flex-col dark:bg-neutral-950">
      {/* About Section */}
      <section
        id="about"
        className=" flex items-center justify-center px-4 py-20"
      >
        <div className="max-w-4xl text-center">
          <h2 className="text-3xl font-Bricolage sm:text-5xl font-extrabold text-blue-700 dark:text-blue-400 mb-8 animate-fadeIn">
            About <span className="text-blue-500">AceJEE</span>
          </h2>

          <p className="text-lg font-Hanuman sm:text-xl leading-relaxed text-gray-700 dark:text-gray-300">
            <strong>AceJEE</strong> is an AI-powered study companion crafted
            for JEE aspirants. It leverages{" "}
            <span className="font-semibold text-blue-600 dark:text-blue-400">
              Retrieval-Augmented Generation (RAG)
            </span>{" "}
            and advanced language models to fetch accurate answers straight
            from textbooks, refine them, and deliver instant, personalized
            explanations. <br /> <br />
            Our mission is to help students study smarter — not harder — by
            providing reliable, easy-to-understand solutions for every concept.
          </p>
        </div>
      </section>

      {/* Accordion Section */}
      <section className="flex-1  overflow-auto mb-10 px-30 py-15">
        <h2 className="text-[20px] sm:text-3xl font-Source font-bold mb-10 text-center">Frequently Asked Questions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {accordionItems.map((item) => (
            <Accordion
              key={item.id}
              type="single"
              collapsible
              className="w-full"
              defaultValue="0"
            >
              <AccordionItem value={item.id} className="py-2">
                <AccordionTrigger className="py-2 text-[15px] font-Figtree leading-6 hover:no-underline">
                  {item.title}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground font-Hanuman pb-2">
                  {item.content}
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          ))}
        </div>
      </section>
    </div>
  );
};

export default AboutPage;
