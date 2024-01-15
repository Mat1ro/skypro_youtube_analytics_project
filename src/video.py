import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


class Video:
    def __init__(self, video_id: int):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()

        self.video_id = video_id
        self.title: str = video_response['items'][0]['snippet']['title']
        self.url: str = f"https://www.youtube.com/watch?v={video_id}"
        self.viewers: int = video_response['items'][0]['statistics']['viewCount']
        self.likes: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title
