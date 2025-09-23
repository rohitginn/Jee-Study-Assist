"use client";

import React from "react";
import { Particles } from "../../components/particles";
import {
    Card,
    CardHeader,
    CardTitle,
    CardDescription,
    CardContent,
} from "../../components/card";
import { ShineBorder } from "../../components/shine-border";
import RotatingText from "../../components/RotatingText";

const featuresData = [
    {
        title: "Smart Question Answering",
        description:
            "Ask questions from JEE topics and get instant answers. Powered by AI & RAG system for accurate responses.",
    },
    {
        title: "Topic Summaries",
        description:
            "Get concise summaries of chapters or concepts. Save time with focused study notes.",
    },
    {
        title: "Concept Rephrasing & Understanding",
        description:
            "Rephrase complex concepts in simpler terms. Enhance your understanding with clear explanations.",
    },
];

export default function Features() {
    return (
        <section className="relative h-screen w-full overflow-hidden">
            {/* Background Particles */}
            <Particles quantity={100} staticity={60} ease={60} size={0.5} />

            <div className="relative z-10 max-w-5xl  mx-auto px-4 py-20 text-center ">
                {/* Rotating text above the heading */}
                <div className=" mb-20 gap-2 flex justify-center items-center backdrop-blur-xl ">
                    <h2 className="text-4xl font-extrabold font-Figtree text-white px-4 py-2 rounded-lg">
                        Study
                    </h2>

                    <RotatingText
                        texts={["Smart", "Easier", "Faster", "Cool!"]}
                        mainClassName="text-4xl font-extrabold font-Figtree text-white px-4 py-2 rounded-lg overflow-hidden"
                        style={{ backgroundColor: "#5227FF" }}
                        staggerFrom="first"
                        initial={{ y: "100%" }}
                        animate={{ y: 0 }}
                        exit={{ y: "-120%" }}
                        staggerDuration={0.025}
                        splitLevelClassName="overflow-hidden pb-0.5"
                        transition={{ type: 'spring', damping: 30, stiffness: 400 }}
                        rotationInterval={2000}
                    />
                </div>


                {/* Section heading */}
                <h1 className="text-4xl font-extrabold font-Bricolage mb-16 dark:text-white">
                    Features of Our Website
                </h1>

                {/* Features grid */}
                <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                    {featuresData.map((feature, idx) => (
                        <Card
                            key={idx}
                            className="backdrop-blur-sm bg-white/80 dark:bg-gray-800/70 border dark:border-gray-900 shadow-xl hover:scale-105 transition-transform"
                        >
                            <ShineBorder shineColor={["#A07CFE", "#FE8FB5", "#FFBE7B"]} />
                            <CardHeader>
                                <CardTitle className="text-xl font-bold font-Hanuman dark:text-gray-100">
                                    {feature.title}
                                </CardTitle>
                                <CardDescription className="dark:text-gray-300 font-mono">
                                    {feature.description}
                                </CardDescription>
                            </CardHeader>
                            <CardContent />
                        </Card>
                    ))}
                </div>
            </div>
        </section>
    );
}
