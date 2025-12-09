
const TextArea = ({ value, onChange, placeholder, rows = 4, className = '' }) => (
  <textarea
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    rows={rows}
    className={`w-full bg-white/10 border border-white/30 rounded-xl px-5 py-3 text-white placeholder-blue-200/70 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-300 resize-none ${className}`}
  />
);

export default TextArea;
