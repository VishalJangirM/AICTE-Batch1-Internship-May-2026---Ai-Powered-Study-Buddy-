from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    if not url:
        return None

    url = url.strip()

    
    if len(url) == 11 and not url.startswith("http") and not "/" in url:
        return url

    if "youtu.be" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    parsed = urlparse(url)

    if parsed.path.startswith("/shorts/"):
        return parsed.path.split("/shorts/")[1]

    if parsed.path == "/watch":
        return parse_qs(parsed.query).get("v", [None])[0]

    return None


def get_transcript(url):
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL - Could not parse Video ID")

    try:
        
        transcript_list = YouTubeTranscriptApi().list(video_id)
    except Exception as e:
        raise Exception(f"Failed to retrieve transcript list from YouTube: {str(e)}")

    
    try:
        transcript = transcript_list.find_transcript(['en'])
    except Exception:
        
        try:
            translatable_t = None
            for t in transcript_list:
                if t.is_translatable:
                    translatable_t = t
                    break
            
            if translatable_t:
                transcript = translatable_t.translate('en')
            else:
                
                transcript = next(iter(transcript_list))
        except Exception:
            try:
               
                transcript = next(iter(transcript_list))
            except Exception as e:
                raise Exception(f"No transcripts found for this video: {str(e)}")

    try:
        transcript_data = transcript.fetch()
        return " ".join(item.text for item in transcript_data)
    except Exception as e:
        raise Exception(f"Failed to fetch transcript content: {str(e)}")