import re
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class YouTubeLoader:
    """
    Loads YouTube video transcripts and converts them into documents.

    Uses the youtube-transcript-api to fetch transcripts and splits them
    into chunks for vector storage.
    """

    def __init__(self):
        """Initialize the YouTube loader with text splitter."""
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        # Initialize the YouTube Transcript API (new v1.0+ API)
        self.ytt_api = YouTubeTranscriptApi()

    def load(self, url: str) -> List[Document]:
        """
        Load and process a YouTube video transcript.

        Args:
            url: YouTube video URL

        Returns:
            List[Document]: List of document chunks with metadata
        """
        video_id = self._extract_id(url)

        # Use the new API: fetch() returns a FetchedTranscript object
        # which can be converted to raw data with .to_raw_data()
        fetched_transcript = self.ytt_api.fetch(video_id, languages=['en'])
        transcript = fetched_transcript.to_raw_data()

        # Format transcript with timestamps
        text = "\n".join([
            f"[{int(s['start']//60):02d}:{int(s['start']%60):02d}] {s['text']}"
            for s in transcript
        ])

        # Split into chunks
        chunks = self.splitter.split_text(text)

        # Create documents with metadata
        return [Document(page_content=c, metadata={"source": url}) for c in chunks]

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

