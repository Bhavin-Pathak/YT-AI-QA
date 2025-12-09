import { useState } from 'react';
import GlassCard from './components/GlassCard';
import Button from './components/Button';
import Input from './components/Input';
import TextArea from './components/TextArea';
import VideoCard from './components/VideoCard';
import SourceCard from './components/SourceCard';
import Header from './components/Header';
import Footer from './components/Footer';
import {Video,FileText,MessageSquare,Lightbulb,BookOpen,Loader2,Sparkles} from 'lucide-react';

function App() {
  // State variables
  const [videoUrl, setVideoUrl] = useState('');
  const [question, setQuestion] = useState('');
  const [processedVideos, setProcessedVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ process: '', question: '' });

  // Functions to handle video processing
  const processVideo = () => {
    if (!videoUrl.trim()) {
      setStatus({ ...status, process: '⚠️ Please enter a valid YouTube URL' });
      return;
    }

    setLoading(true);
    setStatus({ ...status, process: '🔄 Processing video...' });

    setTimeout(() => {
      const videoId = videoUrl.split('v=')[1]?.split('&')[0] || `demo-${Date.now()}`;

      const newVideo = {
        id: videoId,
        url: videoUrl,
        title: 'Understanding AI and Machine Learning',
        duration: '15:30',
        processedAt: new Date().toLocaleDateString(),
      };

      setProcessedVideos((prev) => [...prev, newVideo]);
      setSelectedVideo(newVideo);
      setVideoUrl('');
      setStatus({ ...status, process: '✅ Video processed successfully!' });
      setLoading(false);
    }, 1500);
  };

  const askQuestion = () => {
    if (!question.trim()) {
      setStatus({ ...status, question: '⚠️ Please enter a question' });
      return;
    }

    setLoading(true);
    setStatus({ ...status, question: '🤔 Generating answer...' });

    setTimeout(() => {
      setAnswer(
        'Based on the video content, artificial intelligence and machine learning are transforming technology...'
      );

      setSources([
        { timestamp: '02:15', text: 'AI fundamentals explained.' },
        { timestamp: '05:42', text: 'Machine learning neural network breakdown.' },
        { timestamp: '08:30', text: 'Real-world applications like recommendations.' },
        { timestamp: '12:10', text: 'Ethical concerns & future impact.' },
      ]);

      setStatus({ ...status, question: '✅ Answer generated successfully!' });
      setQuestion('');
      setLoading(false);
    }, 1200);
  };

  const generateSummary = () => {
    setLoading(true);

    setTimeout(() => {
      setSummary(
        `**Introduction to AI & Machine Learning**\n\n00:00 - Overview\n02:30 - What is AI?\n05:15 - ML fundamentals\n08:45 - Real-world applications\n13:00 - Ethics & future`
      );
      setLoading(false);
    }, 1800);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <GlassCard>
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
                <Video className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-white">Process Video</h2>
            </div>
            <Input
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              placeholder="https://youtube.com/watch?v=..."
              className="mb-4"
            />
            <Button onClick={processVideo} disabled={loading} variant="primary">
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing...
                </span>
              ) : (
                'Process Video'
              )}
            </Button>
            {status.process && (
              <div className="mt-4 p-3 bg-white/5 rounded-lg border border-white/10">
                <p className="text-sm text-blue-200">{status.process}</p>
              </div>
            )}
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-white">Library</h2>
            </div>
            <div className="space-y-3 max-h-[280px] overflow-y-auto pr-2 custom-scrollbar">
              {processedVideos.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="w-12 h-12 text-blue-300/30 mx-auto mb-3" />
                  <p className="text-blue-200/60 text-sm">No videos yet. Process one to get started!</p>
                </div>
              ) : (
                processedVideos.map((video) => (
                  <VideoCard
                    key={video.id}
                    video={video}
                    isSelected={selectedVideo?.id === video.id}
                    onClick={() => setSelectedVideo(video)}
                  />
                ))
              )}
            </div>
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 bg-gradient-to-br from-pink-500 to-purple-600 rounded-xl flex items-center justify-center">
                <MessageSquare className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-white">Ask Question</h2>
            </div>
            <TextArea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="What would you like to know about this video?"
              rows={5}
              className="mb-4"
            />
            <Button onClick={askQuestion} disabled={!selectedVideo || loading} variant="secondary">
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Thinking...
                </span>
              ) : (
                'Ask Question'
              )}
            </Button>
            {status.question && (
              <div className="mt-4 p-3 bg-white/5 rounded-lg border border-white/10">
                <p className="text-sm text-blue-200">{status.question}</p>
              </div>
            )}
          </GlassCard>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <GlassCard className="lg:col-span-2">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-xl flex items-center justify-center">
                <Lightbulb className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-white">AI Answer</h2>
            </div>
            <div className="bg-gradient-to-br from-white/5 to-white/10 rounded-xl p-5 border border-white/10 min-h-[200px]">
              {answer ? (
                <p className="text-blue-100 leading-relaxed">{answer}</p>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-center py-8">
                  <Sparkles className="w-12 h-12 text-blue-300/30 mb-3" />
                  <p className="text-blue-200/60 text-sm">Process a video and ask a question to see AI-generated answers here.</p>
                </div>
              )}
            </div>
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-teal-600 rounded-xl flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-white">Summary</h2>
            </div>
            <Button onClick={generateSummary} disabled={!selectedVideo || loading} variant="success" className="mb-4">
              Generate Summary
            </Button>
            <div className="bg-gradient-to-br from-white/5 to-white/10 rounded-xl p-4 border border-white/10 max-h-[300px] overflow-y-auto custom-scrollbar">
              {summary ? (
                <div className="text-blue-100 text-sm leading-relaxed whitespace-pre-line">{summary}</div>
              ) : (
                <div className="flex flex-col items-center justify-center text-center py-8">
                  <FileText className="w-10 h-10 text-blue-300/30 mb-2" />
                  <p className="text-blue-200/60 text-xs">Click the button to generate a timestamped summary.</p>
                </div>
              )}
            </div>
          </GlassCard>
        </div>

        {sources.length > 0 && (
          <div className="mt-8">
            <GlassCard>
              <div className="flex items-center gap-3 mb-5">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-xl flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-white" />
                </div>
                <h2 className="text-xl font-bold text-white">Referenced Sources</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {sources.map((source, idx) => (
                  <SourceCard key={idx} timestamp={source.timestamp} text={source.text} />
                ))}
              </div>
            </GlassCard>
          </div>
        )}
      </main>

      <Footer />

      {loading && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-50">
          <GlassCard className="max-w-sm">
            <div className="flex flex-col items-center gap-4 py-4">
              <Loader2 className="w-16 h-16 text-blue-400 animate-spin" />
              <div className="text-center">
                <p className="text-white text-xl font-bold mb-2">Processing...</p>
                <p className="text-blue-200 text-sm">Please wait while we analyze the content</p>
              </div>
            </div>
          </GlassCard>
        </div>
      )}

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(147, 197, 253, 0.5);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(147, 197, 253, 0.7);
        }
      `}</style>
    </div>
  );
}

export default App;
