import { Play, Clock, Calendar } from 'lucide-react';

const VideoCard = ({ video, isSelected, onClick }) => (
  <div
    onClick={onClick}
    className={`p-4 rounded-xl cursor-pointer transition-all duration-300 transform hover:scale-105 ${
      isSelected
        ? 'bg-gradient-to-br from-blue-500/40 to-purple-500/40 border-2 border-blue-400 shadow-lg'
        : 'bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20'
    }`}
  >
    <div className="flex items-start gap-3">
      <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
        <Play className="w-6 h-6 text-white" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-white font-semibold text-sm truncate mb-1">{video.title}</p>
        <div className="flex items-center gap-3 text-xs text-blue-200">
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {video.duration}
          </span>
          <span className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            {video.processedAt}
          </span>
        </div>
      </div>
    </div>
  </div>
);

export default VideoCard;
