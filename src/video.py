import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


class Video:
    def __init__(self, video_id: int):
        self.youtube = build('youtube', 'v3', developerKey=API_KEY)
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id
                                                             ).execute()
            self.video_id = video_id
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.url: str = f"https://www.youtube.com/watch?v={video_id}"
            self.viewers: int = self.video_response['items'][0]['statistics']['viewCount']
            self.likes: int = self.video_response['items'][0]['statistics']['likeCount']
        except Exception:
            self.title = None
            self.url = None
            self.viewers = None
            self.likes = None

    def __str__(self):
        return self.title
