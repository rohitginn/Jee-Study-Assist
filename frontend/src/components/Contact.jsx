// src/components/Contact.jsx
function Contact() {
  return (
    <section id="contact" className="py-16 bg-gradient-to-r from-blue-100 to-purple-300">
      <div className="container mx-auto px-6 md:px-16 lg:px-24">
        <div className="flex flex-col md:flex-row justify-center gap-10">
          {/* Contact Form */}
          <div className="w-full md:w-1/2 bg-violet-500 text-white p-8 rounded-xl shadow-xl">
            <h2 className="text-3xl font-bold mb-4">Contact us</h2>
            <p className="mb-6 text-sm">
              Let us know how we can help you and our team will be in touch as soon as possible!
            </p>
            <form className="flex flex-col gap-4">
              <input
                type="text"
                placeholder="Your name"
                className="p-3 rounded-md bg-white text-black focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <input
                type="email"
                placeholder="Email"
                className="p-3 rounded-md bg-white text-black focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <textarea
                placeholder="Message"
                className="p-3 rounded-md bg-white text-black focus:outline-none focus:ring-2 focus:ring-blue-400"
                rows="4"
              />
              <button
                type="submit"
                className="mt-2 bg-white text-blue-700 font-semibold px-6 py-2 rounded-full hover:bg-gray-200 transition"
              >
                Send Message
              </button>
            </form>
          </div>

          {/* Social & Info */}
          
        </div>
      </div>
    </section>
  );
}

export default Contact;
