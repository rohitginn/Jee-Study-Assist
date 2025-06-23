import { Link } from "react-scroll";

function Navbar() {
  return (
    <nav className="bg-white/70 backdrop-blur-md p-4 shadow-xl flex justify-between items-center fixed w-full top-0 z-50">
      <div className="text-3xl font-extrabold text-blue-700 font-serif tracking-tight animate-pulse">
        AceJEE
      </div>
      <div className="flex space-x-8 text-lg font-medium">
        <Link to="hero" smooth={true} duration={500} className="cursor-pointer text-gray-800 hover:text-blue-700 transition duration-300">
          Home
        </Link>
        <Link to="about" smooth={true} duration={500} className="cursor-pointer text-gray-800 hover:text-blue-700 transition duration-300">
          About
        </Link>
        <Link to="footer" smooth={true} duration={500} className="cursor-pointer text-gray-800 hover:text-blue-700 transition duration-300">
          Contact
        </Link>
      </div>
    </nav>
  );
}
export default Navbar;
