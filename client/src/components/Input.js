
const Input = ({ value, onChange, placeholder, className = '' }) => (
  <input
    type="text"
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    className={`w-full bg-white/10 border border-white/30 rounded-xl px-5 py-3 text-white placeholder-blue-200/70 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all duration-300 ${className}`}
  />
);

export default Input;
