#!/usr/bin/env python3

import sys
import os
import pathlib
import audio_metadata

from pydub import AudioSegment
from functools import reduce

source_folder = sys.argv[1]
output_folder = sys.argv[2]

root_path = pathlib.Path().resolve()
formats = ["mp3", "flac", "wav", "aac"]

def get_track_pos(track):
    metadata = audio_metadata.load(track)
    return int(metadata['tags']['tracknumber'][0])

def audio_format(track):
    return os.path.splitext(track)[1][1:]

def is_track(track):
    return audio_format(track) in formats

def merge_tracks(tracks):
    segments = [AudioSegment.from_file(track) for track in tracks]
    return sum(segments)


for root, albums, _ in os.walk(f"{root_path}/{source_folder}"):
    for album in albums:
        album_path = f"{root}/{album}"
        full_path = lambda x: os.path.abspath(os.path.join(album_path, x))
        tracks = list(filter(is_track, map(full_path, os.listdir(album_path))))
        format = audio_format(tracks[0])
        merged = merge_tracks(sorted(tracks, key=get_track_pos))
        merged.export(f"{album}.{format}", format=format)
        
        
       