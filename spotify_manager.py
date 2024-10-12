from collections import defaultdict
from datetime import datetime


class SpotifyEventManager:
    def __init__(self, spotify):
        self.spotify = spotify

    def get_user_genres(self):
        top_artists = self.spotify.current_user_top_artists(limit=50)
        current_followed = self.spotify.current_user_followed_artists(limit=30)
        user_genres = defaultdict(int)
        for artist in top_artists["items"] + current_followed["artists"]["items"]:
            for genre in artist["genres"]:
                user_genres[genre] += 1
        return user_genres

    def create_event_playlist(self, event):
        playlist_id = self.spotify.user_playlist_create(
            user=self.spotify.current_user()["id"],
            name=event["title"],
            description=f"Playlist for {event['title']}",
        )
        return playlist_id

    def add_top_tracks_to_playlist(self, spotify_artist_id, playlist_id):
        top_tracks = self.spotify.artist_top_tracks(spotify_artist_id, country="GB")
        top_tracks_ids = [track["id"] for track in top_tracks["tracks"][:3]]
        if top_tracks_ids:
            self.spotify.user_playlist_add_tracks(
                user=self.spotify.current_user()["id"],
                playlist_id=playlist_id,
                tracks=top_tracks_ids,
            )
