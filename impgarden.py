#!/usr/bin/env python3

import sys
import os
import audio_metadata
import pathlib
from pydub import AudioSegment

"""
    TODO:
    add flag for format
    file overwrite warning
"""

def print_usage():
    usage = """
        Usage: impgarden [source folder] [target folder] [--format=(mp3|flac|wav|aac|aiff)]
    """
    print(usage)

def check_paths(paths):
    for path in paths:
        if not os.path.exists(path):
            print(f"path {path} doesn't exist")
            print_usage()
            os.exit()

def absolutify(path):
    if os.path.isabs(path):
        return path
    return f"{pathlib.Path().resolve()}/{path}"

def get_track_number(track):
    metadata = audio_metadata.load(track)
    return int(metadata['tags']['tracknumber'][0])

def audio_format(track):
    return os.path.splitext(track)[1][1:]

def is_track(track):
    return audio_format(track) in formats

def merge_tracks(tracks):
    segments = [AudioSegment.from_file(track) for track in tracks]
    return sum(segments)

def get_format(track):
    return audio_format(track)

if len(sys.argv) < 3:
    print("Too few arguments...")
    print_usage()
    sys.exit()

source_folder = sys.argv[1]
output_folder = absolutify(sys.argv[2])

formats = ["mp3", "flac"]

if __name__ == "__main__": 

    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} doesn't exist. Exiting...")
        print_usage()
        os.exit()

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)  

    for root, albums, _ in os.walk(source_folder):
        for album in albums:
            album_path = f"{root}/{album}"
            full_path = lambda x: os.path.abspath(os.path.join(album_path, x))
            tracks = list(filter(is_track, map(full_path, os.listdir(album_path))))
            format = get_format(tracks[0])
            merged = merge_tracks(sorted(tracks, key=get_track_number))
            album_path = f"{output_folder}/{os.path.relpath(album)}({format})"
            merged.export(album_path, format=format)
            
            
        