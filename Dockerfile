FROM python:latest

RUN mkdir /opt/sfy2ytm
# ADD src/* /opt/sfy2ytm

RUN pip install spotipy ytmusicapi

CMD SPOTIPY_CLIENT_ID=${SFY_CLIENT_ID} \
    SPOTIPY_CLIENT_SECRET=${SFY_CLIENT_SECRET} \
    SPOTIFY_PLAYLIST_URI=${SPOTIFY_PLAYLIST_URI} \
    python /opt/sfy2ytm/migrate.py