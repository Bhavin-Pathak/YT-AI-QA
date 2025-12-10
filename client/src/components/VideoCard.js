import { Play, Calendar, User, Trash2 } from 'lucide-react';

const VideoCard = ({ video, isSelected, onClick, onDelete }) => (
  <div
    onClick={onClick}
    className={`group relative p-4 rounded-xl cursor-pointer transition-all duration-300 ${isSelected
      ? 'bg-gradient-to-br from-blue-500/20 to-purple-500/20 border-2 border-blue-400 shadow-lg'
      : 'bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20'
      }`}
  >
    <button
      onClick={onDelete}
      className={`absolute top-2 right-2 p-1.5 rounded-full bg-red-500/20 hover:bg-red-500 text-red-300 hover:text-white transition-colors opacity-0 group-hover:opacity-100 ${isSelected ? 'opacity-100' : ''}`}
      title="Delete Video"
    >
      <Trash2 className="w-3.5 h-3.5" />
    </button>

    <div className="flex items-start gap-3">
      <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
        <Play className="w-5 h-5 text-white" />
      </div>
      <div className="flex-1 min-w-0 pr-6">
        <p className="text-white font-semibold text-sm truncate mb-1" title={video.title}>{video.title}</p>

        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs text-blue-200/80">
            <User className="w-3 h-3 text-blue-400" />
            <span className="truncate">{video.channel}</span>
          </div>

          <div className="flex items-center gap-3 text-xs text-blue-200/60">
            <span className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              {video.publishDate}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default VideoCard;
