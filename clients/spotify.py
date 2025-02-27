from dataclasses import dataclass
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import asyncio


@dataclass
class SpotifyArtist:
    id: str
    name: str
    genres: list[str]


class SpotifyClient:
    def __init__(self):
        self.SPOTIPY_CLIENT_ID = "68206b2fe8684cb984cd5199fdd9a58c"
        self.SPOTIPY_CLIENT_SECRET = "92ad7105d3ec45e4982b1f3c8c70617d"
        self.SPOTIPY_REDIRECT_URI = "http://localhost:8000/callback"
        self.spoauth = SpotifyOAuth(
            client_id=self.SPOTIPY_CLIENT_ID,
            client_secret=self.SPOTIPY_CLIENT_SECRET,
            redirect_uri=self.SPOTIPY_REDIRECT_URI,
            scope="user-top-read user-follow-read playlist-modify-public playlist-modify-private",
        )

    def get_auth_url(self):
        return self.spoauth.get_authorize_url()

    def get_client(self):
        if not self.access_token:
            raise ValueError("Access token is not set")
        return spotipy.Spotify(auth=self.access_token)

    def authorize(self, code):
        token_info = self.spoauth.get_access_token(code)
        self.access_token = token_info["access_token"]
        return self.get_client()

    async def search_artist(self, spotify, name) -> Optional[SpotifyArtist]:
        results = await asyncio.to_thread(
            spotify.search, q="artist:" + name, type="artist"
        )
        try:
            artist = next(
                a
                for a in results["artists"]["items"]
                if a["name"].lower() == name.lower()
            )
            return SpotifyArtist(
                id=artist["id"], name=artist["name"], genres=artist["genres"]
            )
        except StopIteration:
            return None
