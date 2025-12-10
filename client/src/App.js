import { useState, useEffect } from 'react';
import GlassCard from './components/GlassCard';
import Button from './components/Button';
import Input from './components/Input';
import TextArea from './components/TextArea';
import VideoCard from './components/VideoCard';
import SourceCard from './components/SourceCard';
import Header from './components/Header';
import Footer from './components/Footer';
import { Video, FileText, MessageSquare, Lightbulb, BookOpen, Loader2, Sparkles } from 'lucide-react';
import { videoAPI, questionAPI, summaryAPI } from './services/APIService';

function App() {
  // State variables
  const [videoUrl, setVideoUrl] = useState('');
  const [question, setQuestion] = useState('');
  const [processedVideos, setProcessedVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);

  // Fetch videos on load
  useEffect(() => {
    videoAPI.getProcessedVideos().then(data => {
      const formatted = data.videos.map(v => ({
        id: v.video_id,
        title: v.info.title,
        duration: v.info.transcript_length ? `~${Math.ceil(v.info.transcript_length / 1000)}m words` : 'Unknown',
        channel: v.info.channel || 'Unknown Channel',
        publishDate: v.info.publish_date || 'Unknown Date',
        processedAt: 'Recently'
      }));
      setProcessedVideos(formatted);
    }).catch(err => console.error('Failed to fetch videos', err));
  }, []);
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ process: '', question: '' });

  // Functions to handle video processing
  const processVideo = async () => {
    if (!videoUrl.trim()) {
      setStatus({ ...status, process: '⚠️ Please enter a valid YouTube URL' });
      return;
    }

    setLoading(true);
    setStatus({ ...status, process: '🔄 Processing video...' });

    try {
      const result = await videoAPI.processVideo(videoUrl);

      const newVideo = {
        id: result.video_id || `video-${Date.now()}`,
        url: videoUrl,
        title: result.title || 'Processed Video',
        duration: result.transcript_length ? `~${Math.ceil(result.transcript_length / 1000)}m words` : 'Unknown', // Approximate
        channel: result.channel || 'Unknown Channel',
        publishDate: result.publish_date || 'Unknown Date',
        processedAt: new Date().toLocaleDateString(),
      };

      setProcessedVideos((prev) => [...prev, newVideo]);
      setSelectedVideo(newVideo);
      setVideoUrl('');
      setStatus({ ...status, process: '✅ Video processed successfully!' });
    } catch (error) {
      setStatus({ ...status, process: `❌ Error: ${error.message}` });
      console.error('Video processing error:', error);
    } finally {
      setLoading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) {
      setStatus({ ...status, question: '⚠️ Please enter a question' });
      return;
    }

    if (!selectedVideo) {
      setStatus({ ...status, question: '⚠️ Please select a video first' });
      return;
    }

    setLoading(true);
    setStatus({ ...status, question: '🤔 Generating answer...' });

    try {
      const result = await questionAPI.askQuestion(selectedVideo.id, question);

      setAnswer(result.answer || 'No answer generated');

      // Format sources from the API response
      const formattedSources = result.sources?.map((source) => {
        let label = 'Reference';
        if (source.timestamp) {
          label = `Time: ${source.timestamp}`;
        } else if (source.type === 'web') {
          label = 'Web Source';
        } else if (source.type === 'metadata') {
          label = `Metadata: ${source.source}`;
        } else if (source.source === 'youtube_transcript') {
          label = 'Video Transcript';
        } else if (source.source) {
          label = source.source;
        }

        return {
          timestamp: label,
          text: source.text || '',
        };
      }) || [];

      setSources(formattedSources);
      setStatus({ ...status, question: '✅ Answer generated successfully!' });
      setQuestion('');
    } catch (error) {
      setStatus({ ...status, question: `❌ Error: ${error.message}` });
      console.error('Question answering error:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateSummary = async () => {
    if (!selectedVideo) {
      setStatus({ ...status, process: '⚠️ Please select a video first' });
      return;
    }

    setLoading(true);

    try {
      const result = await summaryAPI.generateSummary(selectedVideo.id);

      let formattedSummary = result.overall_summary || 'No summary generated';

      if (result.highlights && result.highlights.length > 0) {
        formattedSummary += '\n\nKey Highlights:\n';
        result.highlights.forEach(h => {
          formattedSummary += `\n• [${h.timestamp}] ${h.main_point}`;
          if (h.sub_points) {
            h.sub_points.forEach(sp => formattedSummary += `\n  - ${sp}`);
          }
        });
      }

      setSummary(formattedSummary);
    } catch (error) {
      setStatus({ ...status, process: `❌ Error: ${error.message}` });
      console.error('Summary generation error:', error);
    } finally {
      setLoading(false);
    }
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

          {/* Library Section */}
          <GlassCard className="lg:col-span-1">
            <div className="flex items-center gap-3 mb-5">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-white">Library</h2>
            </div>

            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
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
                    onDelete={async (e) => {
                      e.stopPropagation();
                      if (window.confirm('Delete this video?')) {
                        try {
                          await videoAPI.deleteVideo(video.id);
                          setProcessedVideos(prev => prev.filter(v => v.id !== video.id));
                          if (selectedVideo?.id === video.id) setSelectedVideo(null);
                        } catch (err) {
                          console.error('Delete error', err);
                        }
                      }
                    }}
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
