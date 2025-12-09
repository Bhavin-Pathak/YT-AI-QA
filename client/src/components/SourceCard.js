import { ChevronRight } from 'lucide-react';

const SourceCard = ({ timestamp, text }) => (
  <div className="bg-gradient-to-br from-white/5 to-white/10 border border-white/10 rounded-xl p-4 hover:border-white/20 transition-all duration-300">
    <div className="flex items-center gap-2 mb-2">
      <div className="px-3 py-1 bg-blue-500/30 rounded-full">
        <p className="text-blue-300 font-semibold text-xs">{timestamp}</p>
      </div>
      <ChevronRight className="w-4 h-4 text-blue-400" />
    </div>
    <p className="text-blue-100 text-sm leading-relaxed">{text}</p>
  </div>
);

export default SourceCard;
