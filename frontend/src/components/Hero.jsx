import { TextLoop } from "../../components/motion-primitives/text-loop";
import { TextEffect } from "../../components/motion-primitives/text-effect";
import Typewriter from "typewriter-effect";
import { ChevronRight, Construction, Rocket } from "lucide-react";
import { ShineBorder } from "../../components/shine-border";
import { AuroraText } from "../../components/aurora-text";
import { cn } from "../lib/utils";
import { AnimatedGradientText } from "../../components/animated-gradient-text";

function Hero() {
  return (
    <section
      id="hero"
      className="h-screen w-screen flex flex-col items-center justify-center  bg-neutral-50 dark:bg-neutral-950
      "
    >
      <div className="absolute top-10 left-0 z-50 w-full bg-transparent ">
  <div className="group relative mx-auto mt-20 flex w-fit items-center justify-center rounded-full px-4 py-1.5 shadow-[inset_0_-8px_10px_#8fdfff1f] transition-shadow duration-500 ease-out hover:shadow-[inset_0_-5px_10px_#8fdfff3f]">
    <span
      className={cn(
        "absolute inset-0 block h-full w-full animate-gradient rounded-[inherit] bg-gradient-to-r from-[#ffaa40]/50 via-[#9c40ff]/50 to-[#ffaa40]/50 bg-[length:300%_100%] p-[1px]"
      )}
      style={{
        WebkitMask:
          "linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)",
        WebkitMaskComposite: "destination-out",
        mask: "linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)",
        maskComposite: "subtract",
        WebkitClipPath: "padding-box",
      }}
    />
    <Construction />
    <hr className="mx-2 h-4 w-px shrink-0 bg-neutral-500" />
    <AnimatedGradientText className="text-sm font-medium">
      Under Construction
    </AnimatedGradientText>
    <ChevronRight className="ml-1 size-4 stroke-neutral-500 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
  </div>
</div>


      <h1
        className="
          z-10  mb-6 text-5xl md:text-7xl font-bold
          text-blue-800 dark:text-[#D1D5DB] font-Zen
        "
      >

        Ready to{" "}
        <AuroraText>AceJee</AuroraText>
      </h1>

      <div
        className="
          z-10 mb-8 text-lg md:text-2xl
          text-gray-700 dark:text-gray-300 font-SUSE
        "
      >
        <TextLoop
          transition={0.8}
          className="text-lg flex items-center justify-center">
          <span>Master Your JEE with Ease 🚀</span>
          <span>Get Quick, Reliable Answers 📚</span>
          <span>Ace Every Concept with Confidence! 🎯</span>
        </TextLoop>

      </div>

      <a
        href="#questionForm"
        className="
          z-10 font-bold py-3 px-8 rounded-full shadow-lg
          
          text-white 
        "
      >

        <button type="button" class="btn">
          <strong>Start to Ace</strong>
          <div id="container-stars">
            <div id="stars"></div>
          </div>

          <div id="glow">
            <div class="circle"></div>
            <div class="circle"></div>
          </div>
        </button>
      </a>
    </section>
  );
}

export default Hero;
