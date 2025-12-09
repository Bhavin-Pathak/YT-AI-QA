
const Button = ({ children, onClick, disabled, variant = 'primary', className = '' }) => {
  const variants = {
    primary:
      'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700',
    secondary:
      'bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700',
    success:
      'bg-gradient-to-r from-green-500 to-teal-600 hover:from-green-600 hover:to-teal-700',
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`w-full ${variants[variant]} disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-lg active:scale-95 ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
