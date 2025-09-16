import { Link } from "react-scroll";

function Navbar() {
  return (
    <nav className="
      fixed top-0 left-0 w-full
      z-50
      bg-slate-900/30
      backdrop-blur-md
      border-b border-white/10
      p-3
      flex justify-between items-center
      shadow-lg
    ">
      {/* App Name */}
      <div className="text-3xl font-extrabold text-amber-600 font-mono tracking-tight">
        AceJEE
      </div>

      {/* Navigation Links */}
      <div className="flex space-x-8 text-md font-medium ">
        <Link
          to="hero"
          smooth={true}
          duration={500}
          className="cursor-pointer text-gray-300 hover:text-indigo-400 transition-colors duration-300 "
        >
          Home
        </Link>
        <Link
          to="about"
          smooth={true}
          duration={500}
          className="cursor-pointer text-gray-300 hover:text-indigo-400 transition-colors duration-300"
        >
          About
        </Link>
        <Link
          to="footer"
          smooth={true}
          duration={500}
          className="cursor-pointer text-gray-300 hover:text-indigo-400 transition-colors duration-300"
        >
          Contact
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
