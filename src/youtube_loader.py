import re
import json
from typing import List
import yt_dlp
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class YouTubeLoader:
    """
    Loads YouTube video transcripts and converts them into documents.

    Uses yt-dlp to fetch transcripts, which is more robust and can bypass
    IP blocks that affect youtube-transcript-api.
    """

    def __init__(self):
        """Initialize the YouTube loader with text splitter."""
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        # Configure yt-dlp options
        self.ydl_opts = {
            'skip_download': True,  # Don't download video
            'writesubtitles': True,  # Get subtitles
            'writeautomaticsub': True,  # Get auto-generated subs if manual not available
            'subtitleslangs': ['en'],  # English subtitles
            'quiet': True,  # Suppress output
            'no_warnings': True,  # Suppress warnings
        }

    def load(self, url: str) -> List[Document]:
        """
        Load and process a YouTube video transcript using yt-dlp.

        Args:
            url: YouTube video URL

        Returns:
            List[Document]: List of document chunks with metadata

        Raises:
            Exception: If transcript cannot be retrieved
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract video info including subtitles
                info = ydl.extract_info(url, download=False)

                # Try to get subtitles
                subtitles = info.get('subtitles', {})
                automatic_captions = info.get('automatic_captions', {})

                # Prefer manual subtitles, fall back to auto-generated
                transcript_data = None
                if 'en' in subtitles:
                    transcript_data = subtitles['en']
                elif 'en' in automatic_captions:
                    transcript_data = automatic_captions['en']
                else:
                    raise Exception("No English subtitles/captions available for this video")

                # Find JSON3 format (most detailed)
                json3_subtitle = None
                for sub in transcript_data:
                    if sub.get('ext') == 'json3':
                        json3_subtitle = sub
                        break

                # If no JSON3, try other formats
                if not json3_subtitle and transcript_data:
                    json3_subtitle = transcript_data[0]

                # Download subtitle data
                subtitle_url = json3_subtitle.get('url')
                if not subtitle_url:
                    raise Exception("Could not find subtitle URL")

                # Fetch subtitle content
                import urllib.request
                with urllib.request.urlopen(subtitle_url) as response:
                    subtitle_content = response.read().decode('utf-8')

                # Parse subtitle content
                transcript = self._parse_subtitles(subtitle_content, json3_subtitle.get('ext', 'json3'))

                # Format transcript with timestamps
                text = "\n".join([
                    f"[{int(s['start']//60):02d}:{int(s['start']%60):02d}] {s['text']}"
                    for s in transcript
                ])

                # Split into chunks
                chunks = self.splitter.split_text(text)

                # Create documents with metadata
                return [Document(page_content=c, metadata={"source": url}) for c in chunks]

        except Exception as e:
            raise Exception(f"Failed to load YouTube transcript: {str(e)}")

    def _parse_subtitles(self, content: str, format_type: str) -> List[dict]:
        """
        Parse subtitle content into transcript format.

        Args:
            content: Raw subtitle content
            format_type: Format type (json3, srv3, etc.)

        Returns:
            List of dicts with 'start' and 'text' keys
        """
        transcript = []

        try:
            if format_type == 'json3':
                # Parse JSON3 format
                data = json.loads(content)
                events = data.get('events', [])

                for event in events:
                    if 'segs' in event:
                        start_time = event.get('tStartMs', 0) / 1000.0
                        text_parts = []
                        for seg in event['segs']:
                            if 'utf8' in seg:
                                text_parts.append(seg['utf8'])

                        if text_parts:
                            text = ''.join(text_parts).strip()
                            if text:
                                transcript.append({
                                    'start': start_time,
                                    'text': text
                                })
            else:
                # Try to parse as JSON (srv3 or other formats)
                data = json.loads(content)
                if isinstance(data, list):
                    for item in data:
                        if 'start' in item and 'text' in item:
                            transcript.append({
                                'start': float(item['start']),
                                'text': item['text'].strip()
                            })
        except Exception as e:
            raise Exception(f"Failed to parse subtitles: {str(e)}")

        if not transcript:
            raise Exception("No transcript data could be extracted")

        return transcript

    def _extract_id(self, url: str) -> str:
        """
        Extract video ID from YouTube URL.

        Args:
            url: YouTube video URL

        Returns:
            str: Video ID

        Raises:
            ValueError: If URL format is invalid
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        ]
        for p in patterns:
            if match := re.search(p, url):
                return match.group(1)
        raise ValueError("Invalid YouTube URL")

