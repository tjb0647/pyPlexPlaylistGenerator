#!/usr/bin/python3.7
from plexapi.server import PlexServer
import random
import logging

# plex location and token
baseurl = 'http://10.0.1.7:32400'
token = 'nYr-QVm-jNx-jBQNL_43'

library = "TV Shows"
primeshow = ' '  # 'The Late Show with Stephen Colbert'
notwatchedplaylist = "Not.Watched.Recently.Playlist"
playlistname = "Late Night TV"
# [number of episodes when colbert is new, number of episdoes when not new]
howmanyepisodes = [3, 5]
episode_list = []

# create connection to plex
plex = PlexServer(baseurl, token)
showlibrary = plex.library.section(library)
# grab the prime show with the latest numbered episode

try:
    primeshow = showlibrary.get(primeshow).episodes()[-1]
    includeprime = True
    if primeshow.isWatched:
        includeprime = False
except:
    includeprime = False
    pass

# grab n random episodes from the smart playlist
episode_list = random.sample(
    showlibrary.playlist(notwatchedplaylist).items(),
    k=howmanyepisodes[1 if not includeprime else 0]
)

if includeprime:
    episode_list.insert(0, primeshow)

try:
    plex.playlist(playlistname).delete()
except:
    pass

plex.createPlaylist(playlistname, showlibrary, episode_list)
