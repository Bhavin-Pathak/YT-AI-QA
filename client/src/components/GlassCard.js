
const GlassCard = ({ children, className = '' }) => (
  <div
    className={`backdrop-blur-xl bg-white/10 rounded-3xl p-6 border border-white/20 shadow-2xl hover:bg-white/15 transition-all duration-300 ${className}`}
  >
    {children}
  </div>
);

export default GlassCard;
