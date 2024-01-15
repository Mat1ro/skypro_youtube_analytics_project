import os

from dotenv import load_dotenv

from src.video import Video

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.title
