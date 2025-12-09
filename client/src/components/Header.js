import { Sparkles } from 'lucide-react';

const Header = () => {
  return (
    <header className="backdrop-blur-xl bg-white/5 border-b border-white/10 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              AI-Powered Video Analysis
            </h1>
            <p className="text-blue-200 text-sm">Ask questions and get insights from any YouTube video</p>
          </div>
        </div>
        <div className="hidden md:flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-yellow-400 animate-pulse" />
          <span className="text-blue-200 text-sm font-medium">Powered by Ollama</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
