#! /bin/python

import spotipy
import sys
import os
import time
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from ytmusicapi import YTMusic

print("setting up clients")
ytm = YTMusic("/opt/sfy2ytm/oauth.json")
sfy = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

print("defining playlists")
sfy_source_pl_id = os.getenv('SPOTIFY_PLAYLIST_URI')
ytm_playlist_id = ytm.create_playlist("sfy2ytm_test", "test description")
track_index=0


def add_sfy_track_to_ytm(item):
    global track_index
    
    # validate item
    if 'track' not in item or \
        'id' not in item['track'] or \
        item['track']['id'] is None:
        return False
    
    # get spotify track details
    track_id=(item['track']['id'])
    track = sfy.track(track_id=track_id)
    sfy_track_name=track['name']
    sfy_track_artist=track['artists'][0]['name']
    print("{}: SFY Artist: {} - Track: {}".format(track_index, sfy_track_artist, sfy_track_name))

    # search in ytm
    ytm_results = ytm.search(
        "{} {}".format(sfy_track_artist, sfy_track_name),
        'songs'
    )

    # add to ytm
    ytm_top=ytm_results[0]
    ytm_artist=ytm_top['artists'][0]['name']
    ytm_track_name=ytm_top['title']
    ytm_track_id=ytm_top['videoId']
    print("{}: YTM Artist: {} - Track: {}".format(track_index, ytm_artist, ytm_track_name))

    # add to playlist
    ytm.add_playlist_items(ytm_playlist_id, [ytm_track_id])
    return True


def try_add_sfy_track_to_ytm_backoff(item):
    for timeout in [1, 5, 60]:
        try:
            return add_sfy_track_to_ytm(item)
        except Exception as e:
            print(e)
            print("Failed. Sleeping {}s".format(timeout))
            time.sleep(timeout) # to avoid hitting rate limits
    return False


def add_sfy_items_to_ytm(items):
    # iterate over all spotify tracks in playlist and add to youtube music
    global track_index
    migrated=[]
    failed=[]
    
    for item in items:
        if try_add_sfy_track_to_ytm_backoff(item):
            migrated.append(item)
        else:
            failed.append(item)
        track_index+=1
    
    return migrated, failed


# front load spotify tracks locally
# so they can be reversed/sorted
items=[]
offset=0
while True:
    response = sfy.playlist_items(sfy_source_pl_id, offset=offset, fields='items.track.id,total', additional_types=['track'])
    if len(response['items']) == 0:
        break
    items.extend(response['items'])
    offset = offset + len(response['items'])

items.reverse()

# # debug - jump to offset
# track_index=501
# items=items[track_index:]

print("Loaded {} spotify playlist items".format(len(items)))
migrated, failed = add_sfy_items_to_ytm(items)
# pprint(failed) #debug
print("Finished. Migrated: {} Failed: {}".format(len(migrated), len(failed)))