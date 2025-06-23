import React from "react";

function Loader() {
  return (
    <div className="flex justify-center mt-8">
      <div className="flex space-x-2">
        <div className="h-4 w-4 bg-purple-500 rounded-full animate-bounce"></div>
        <div className="h-4 w-4 bg-purple-500 rounded-full animate-bounce delay-150"></div>
        <div className="h-4 w-4 bg-purple-500 rounded-full animate-bounce delay-300"></div>
      </div>
    </div>
  );
}

export default Loader;
