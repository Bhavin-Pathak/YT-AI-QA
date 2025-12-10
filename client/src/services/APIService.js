/**
 * API Service - Frontend utility to connect with FastAPI backend
 * Base URL: http://localhost:8001
 */

const API_BASE_URL = 'http://localhost:8001';

/**
 * Video Processing API
 */
export const videoAPI = {
  /**
   * Process a YouTube video and create vector store
   * POST /videos/process
   */
  processVideo: async (videoUrl) => {
    const response = await fetch(`${API_BASE_URL}/videos/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ video_url: videoUrl }),
    });
    if (!response.ok) {
      throw new Error(`Failed to process video: ${response.statusText}`);
    }
    return response.json();
  },

  /**
   * Get list of processed videos
   * GET /videos/list
   */
  getProcessedVideos: async () => {
    const response = await fetch(`${API_BASE_URL}/videos/list`);
    if (!response.ok) {
      throw new Error(`Failed to fetch videos: ${response.statusText}`);
    }
    return response.json();
  },

  /**
   * Delete a processed video
   * DELETE /videos/{video_id}
   */
  deleteVideo: async (videoId) => {
    const response = await fetch(`${API_BASE_URL}/videos/${videoId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`Failed to delete video: ${response.statusText}`);
    }
    return response.json();
  },
};

/**
 * Question Answering API
 */
export const questionAPI = {
  /**
   * Ask a question about a processed video
   * POST /questions/ask
   */
  askQuestion: async (videoId, question) => {
    const response = await fetch(`${API_BASE_URL}/questions/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ video_id: videoId, question }),
    });
    if (!response.ok) {
      throw new Error(`Failed to ask question: ${response.statusText}`);
    }
    return response.json();
  },

  /**
   * Get conversation history for a video
   * GET /questions/history/{video_id}
   */
  getHistory: async (videoId) => {
    const response = await fetch(`${API_BASE_URL}/questions/history/${videoId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch history: ${response.statusText}`);
    }
    return response.json();
  },
};

/**
 * Summary API
 */
export const summaryAPI = {
  /**
   * Generate a summary of a processed video
   * POST /summaries/generate
   */
  generateSummary: async (videoId) => {
    const response = await fetch(`${API_BASE_URL}/summaries/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ video_id: videoId }),
    });
    if (!response.ok) {
      throw new Error(`Failed to generate summary: ${response.statusText}`);
    }
    return response.json();
  },

  /**
   * Get stored summary for a video
   * GET /summaries/{video_id}
   */
  getSummary: async (videoId) => {
    const response = await fetch(`${API_BASE_URL}/summaries/${videoId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch summary: ${response.statusText}`);
    }
    return response.json();
  },
};

/**
 * Health Check API
 */
export const healthAPI = {
  /**
   * Check if backend is running
   * GET /health
   */
  check: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, { timeout: 5000 });
      return response.ok;
    } catch (error) {
      return false;
    }
  },
};

const apiServices = { videoAPI, questionAPI, summaryAPI, healthAPI };

export default apiServices;
