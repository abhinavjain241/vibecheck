from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from collections import defaultdict

from clients.spotify import SpotifyClient
from ra import ResidentAdvisor
from db import VibecheckDB
from spotify_manager import SpotifyEventManager

from datetime import date

app = FastAPI()
templates = Jinja2Templates(directory="templates")

spotify_client = SpotifyClient()
resident_advisor = ResidentAdvisor()
db = VibecheckDB()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
async def login():
    return RedirectResponse(url=spotify_client.get_auth_url())


@app.get("/callback")
async def callback(
    code: str,
    start_date: date = Query(..., description="Start date for events"),
    end_date: date = Query(..., description="End date for events"),
):
    spotify = spotify_client.authorize(code)
    spotify_manager = SpotifyEventManager(spotify)
    user_genres = spotify_manager.get_user_genres()
    events = get_events(str(start_date), str(end_date))
    event_genres = defaultdict(lambda: defaultdict(int))
    event_info_list = []
    for event in events:
        # playlist_id = spotify_manager.create_event_playlist(event)
        for artist_id, artist_name in event["artists"]:
            spotify_artist_id = get_or_create_spotify_artist(
                spotify, artist_id, artist_name
            )
            if spotify_artist_id:
                artist_info = spotify.artist(spotify_artist_id)
                for genre in artist_info["genres"]:
                    event_genres[event["title"]][genre] += 1

        event_title = event["title"]
        event_image_url = event.get(
            "image_url"
        )  # Assuming the event dictionary has an image_url key
        event_genre_histogram = {
            genre: count for genre, count in event_genres[event_title].items()
        }

        event_info_list.append(
            {
                "title": event_title,
                "image_url": event_image_url,
                "date": event["date"],
                "start_time": event["start_time"],
                "end_time": event["end_time"],
                "event_genre_histogram": event_genre_histogram,
            }
        )
        # spotify_manager.add_top_tracks_to_playlist(spotify_artist_id, playlist_id["id"])
    # print(event_genres)
    # most_common_event, max_common_genres = find_most_common_event(user_genres, event_genres)

    user_genre_histogram = {
        genre: user_genres[genre] for genre in list(user_genres.keys())[:10]
    }  # Clip to max 10 genres

    return {
        "event_info": event_info_list,
        "user_genre_histogram": user_genre_histogram,
    }


def get_events(start_date, end_date):
    events_data = resident_advisor.get_ra_events(start_date, end_date)
    return resident_advisor.extract_event_info(events_data)


def get_or_create_spotify_artist(spotify, artist_id, artist_name):
    spotify_artist_id = db.get_spotify_artist_id(artist_id)
    if not spotify_artist_id:
        spotify_artist = spotify_client.search_artist(spotify, artist_name)
        if spotify_artist:
            db.save_artist_mapping(artist_id, spotify_artist.id)
            spotify_artist_id = spotify_artist.id
        else:
            print(f"No Spotify artist found for {artist_name} (RA ID: {artist_id})")
    return spotify_artist_id


def find_most_common_event(user_genres, event_genres):
    most_common_event = None
    max_common_genres = 0
    for event, genres in event_genres.items():
        common_genres = sum(
            min(genres[genre], user_genres[genre])
            for genre in genres.keys() & user_genres.keys()
        )
        if common_genres > max_common_genres:
            max_common_genres = common_genres
            most_common_event = event
    return most_common_event, max_common_genres


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
