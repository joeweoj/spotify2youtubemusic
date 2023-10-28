# Spotify 2 Youtube Music

## Setup

### Build Image
1. Required for auth setup and running
    ```bash
    docker build -t sfy2ytm .
    ```


### Youtube Music Credentials
1. Run command and follow `ytmusicapi oauth` instructions to auth with Google via browser
    ```bash
    docker run -it --entrypoint bash sfy2ytm -c 'ytmusicapi oauth; cat oauth.json'
    ```
1. Copy the JSON blob into `src/oauth.json`


### Spotify Credentials
1. [Create a Spotify app](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app)
1. [Request Access Token](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#request-an-access-token)
1. Obtain `Client ID` and `Client secret` from [Developer Portal](https://developer.spotify.com/dashboard)


## Run
```bash
docker run -it -v ./src:/opt/sfy2ytm \
    -e SFY_CLIENT_ID='<Spotify Client ID>' \
    -e SFY_CLIENT_SECRET='<Spotify Client secret>' \
    -e SPOTIFY_PLAYLIST_URI='spotify:playlist:3ej1snYYTQRwtnx9LxTp1g' \
    sfy2ytm
```

### Expected Output
A new playlist `sfy2ytm_test` will be created in the target Youtube Music account, and begin to be populated.

```
setting up clients
defining playlists
Loaded 902 spotify playlist items
0: SFY Artist: Ry Cooder - Track: Tattler
0: YTM Artist: Ry Cooder - Track: Tattler
1: SFY Artist: Ry Cooder - Track: Stand by Me
1: YTM Artist: Ry Cooder - Track: Stand by Me
2: SFY Artist: Nick Cave & The Bad Seeds - Track: O Children
2: YTM Artist: Nick Cave & The Bad Seeds - Track: O Children
3: SFY Artist: Cream - Track: Badge
3: YTM Artist: Cream - Track: Badge
4: SFY Artist: Max Richter - Track: On the Nature of Daylight
4: YTM Artist: Max Richter Orchestra - Track: Richter: On The Nature Of Daylight (Orchestral Version)
5: SFY Artist: La Roux - Track: Let Me Down Gently
5: YTM Artist: La Roux - Track: Let Me Down Gently
6: SFY Artist: Balthazar - Track: Blood Like Wine
6: YTM Artist: Balthazar - Track: Blood Like Wine
7: SFY Artist: Florence + The Machine - Track: King
7: YTM Artist: Florence + The Machine - Track: King
8: SFY Artist: Pink Floyd - Track: A Great Day For Freedom - 2011 Remaster
8: YTM Artist: Pink Floyd - Track: A Great Day For Freedom
```

## Operation

Note: This only works on a single playlist

1. Create a new Youtube Music playlist
1. Get all tracks in playlist, then for each
1. Get track details (title, artist)
1. Search Youtube Music given title and artist
1. Add the first hit to the new YTM playlist

## Notes

* Built using [Spotipy](https://ytmusicapi.readthedocs.io/en/stable/index.html) and [ytmusicapi](https://ytmusicapi.readthedocs.io/en/stable/index.html) 🙏
* This was a personal project to migrate a few specific playlist, therefore it is very hacky, unsupported, subject to occassional rate limiting, use at own risk etc etc
