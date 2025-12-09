const year = new Date().getFullYear();

const Footer = () => {
  return (
    <footer className="mt-auto">
      <div className="py-6 text-center bg-white/5 border-t border-white/10 flex flex-col md:flex-row items-center justify-center gap-4">
        <p className="text-sm text-gray-400">© {year} Design And Developed By <span className="font-semibold text-white">BHAVIN PATHAK</span></p>
      </div>
    </footer>
  );
};

export default Footer;
