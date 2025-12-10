"""Summary generation service"""
from typing import List, Dict
from langchain_ollama import ChatOllama
from app.core.config import OLLAMA_BASE_URL, OLLAMA_MODEL, SUMMARY_INTERVAL_SECONDS, MAX_SUMMARY_SEGMENTS
from app.core.storage import video_transcripts
from app.utils.youtube_utils import format_timestamp


def group_transcript_by_time(transcript_data: List[Dict], interval_seconds: int = SUMMARY_INTERVAL_SECONDS) -> List[Dict]:
    """Group transcript snippets into time-based segments"""
    if not transcript_data:
        return []
    
    segments = []
    current_segment = {
        "start_time": 0,
        "text": ""
    }
    
    for snippet in transcript_data:
        if snippet["start"] - current_segment["start_time"] >= interval_seconds:
            if current_segment["text"]:
                segments.append(current_segment)
            current_segment = {
                "start_time": snippet["start"],
                "text": snippet["text"]
            }
        else:
            current_segment["text"] += " " + snippet["text"]
    
    if current_segment["text"]:
        segments.append(current_segment)
    
    return segments


def generate_summary(video_id: str) -> Dict:
    """Generate comprehensive timestamped summary for a video"""
    if video_id not in video_transcripts:
        raise ValueError("Video not found. Please process the video first.")
    
    transcript_data = video_transcripts[video_id]
    full_transcript = " ".join([snippet["text"] for snippet in transcript_data])
    
    # Create LLM
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.3,
        base_url=OLLAMA_BASE_URL
    )
    
    # Generate overall summary
    overall_prompt = f"""Analyze the following YouTube video transcript and provide a comprehensive 2-3 sentence summary that captures the main theme and key discussion points.

Transcript:
{full_transcript[:4000]}

Summary:"""
    
    overall_summary_msg = llm.invoke(overall_prompt)
    overall_summary = overall_summary_msg.content if hasattr(overall_summary_msg, 'content') else str(overall_summary_msg)
    overall_summary = overall_summary.strip()
    
    # Group transcript into segments
    segments = group_transcript_by_time(transcript_data, interval_seconds=SUMMARY_INTERVAL_SECONDS)
    
    # Generate highlights
    highlights = []
    for segment in segments[:MAX_SUMMARY_SEGMENTS]:
        timestamp = format_timestamp(segment["start_time"])
        segment_text = segment["text"][:2000]
        
        highlight_prompt = f"""Analyze this video segment and extract:
1. A single main point or topic (one sentence, max 25 words)
2. 2-4 key supporting points or details (each as a separate bullet, max 20 words each)

Segment text:
{segment_text}

Format your response EXACTLY as:
MAIN: [main point here]
BULLET: [first supporting point]
BULLET: [second supporting point]
BULLET: [third supporting point]"""
        
        response_msg = llm.invoke(highlight_prompt)
        response = response_msg.content if hasattr(response_msg, 'content') else str(response_msg)
        response = response.strip()
        
        # Parse response
        main_point = ""
        sub_points = []
        
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('MAIN:'):
                main_point = line.replace('MAIN:', '').strip()
            elif line.startswith('BULLET:'):
                bullet = line.replace('BULLET:', '').strip()
                if bullet:
                    sub_points.append(bullet)
        
        # Fallback
        if not main_point:
            lines = [l.strip() for l in response.split('\n') if l.strip()]
            main_point = lines[0] if lines else "Key discussion point"
            sub_points = lines[1:4] if len(lines) > 1 else ["Important topic covered in this section"]
        
        highlights.append({
            "timestamp": timestamp,
            "main_point": main_point,
            "sub_points": sub_points[:4]
        })
    
    return {
        "video_id": video_id,
        "overall_summary": overall_summary,
        "highlights": highlights,
        "status": "success"
    }
