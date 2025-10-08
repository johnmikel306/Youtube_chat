import re
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class YouTubeLoader:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

    def load(self, url: str) -> List[Document]:
        video_id = self._extract_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = "\n".join([f"[{int(s['start']//60):02d}:{int(s['start']%60):02d}] {s['text']}"
                         for s in transcript])
        chunks = self.splitter.split_text(text)
        return [Document(page_content=c, metadata={"source": url}) for c in chunks]

    def _extract_id(self, url: str) -> str:
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        ]
        for p in patterns:
            if match := re.search(p, url):
                return match.group(1)
        raise ValueError("Invalid YouTube URL")

