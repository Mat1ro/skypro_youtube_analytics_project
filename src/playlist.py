import datetime
import os
from pprint import pprint

import isodate
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


class PlayList:
    def __init__(self, playlist_id: int) -> None:
        self.youtube = build('youtube', 'v3', developerKey=API_KEY)
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self._playlist_id: int = playlist_id
        self.title: str = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlists?part=snippet%2Clocalizations&id={self._playlist_id}"
            f"&fields=items(localizations%2Csnippet%2Flocalized%2Ftitle)&key={API_KEY}").json().get('items')[
            0].get('snippet').get('localized').get('title')
        self.url: str = f"https://www.youtube.com/playlist?list={self._playlist_id}"

    @property
    def total_duration(self) -> datetime.timedelta:
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        delta = datetime.timedelta(0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            delta += duration
        return delta

    def show_best_video(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        best_video_id: str = ""
        best_likes: int = 0
        for video in video_response["items"]:
            if best_likes < int(video["statistics"]["likeCount"]):
                best_likes = int(video["statistics"]["likeCount"])
                best_video_id = video["id"]
        return f"https://youtu.be/{best_video_id}"
