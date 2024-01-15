import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self._channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/" + channel["items"][0]["snippet"]["customUrl"]
        self.subscribers = int(channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(channel["items"][0]["statistics"]["videoCount"])
        self.views = int(channel["items"][0]["statistics"]["viewCount"])

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        return self.subscribers - other.subscribers

    def __le__(self, other):
        return self.subscribers <= other.subscribers

    def __eq__(self, other):
        return self.subscribers == other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    def __lt__(self, other):
        return self.subscribers < other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    @property
    def channel_id(self):
        return self._channel_id

    @staticmethod
    def get_service():
        return build('youtube', 'v3', developerKey=API_KEY)

    def to_json(self, path):
        path = f"data/{path}"
        absolute_path = os.path.abspath(os.path.join(os.getcwd(), path))
        data = {
            "channel_id": self._channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "views": self.views,
        }
        with open(absolute_path, "a") as f:
            if os.stat(absolute_path).st_size == 0:
                json.dump([data], f, ensure_ascii=False)
            else:
                with open(absolute_path, encoding="utf-8") as json_file:
                    data_list = json.load(json_file)
                data_list.append(data)
                with open(absolute_path, "w", encoding="utf-8") as json_file:
                    json.dump(data_list, json_file, ensure_ascii=False)
