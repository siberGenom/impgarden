#!/usr/bin/env python3

import sys
import os
import audio_metadata
import pathlib
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog

"""
    TODO:
    add flag for format
    file overwrite warning
"""

FORMATS = ["mp3", "flac"]

def select_source_folder():
    global SOURCE_FOLDER
    SOURCE_FOLDER = os.path.relpath(filedialog.askdirectory())

def select_output_folder():
    global OUTPUT_FOLDER
    OUTPUT_FOLDER = filedialog.askdirectory()

def get_track_number(track):
    metadata = audio_metadata.load(track)
    return int(metadata['tags']['tracknumber'][0])

def audio_format(track):
    return os.path.splitext(track)[1][1:]

def is_track(track):
    return audio_format(track) in FORMATS

def merge_tracks(tracks):
    segments = [AudioSegment.from_file(track) for track in tracks]
    return sum(segments)

def get_format(track):
    return audio_format(track)

                
class ImpGarden(tk.Tk):
    def __init__(self, master):
        self.master = master
        master.title("ImpGarden")
        master.resizable(False, False)
        master.geometry("400x300")

        # background
        bg_image = tk.PhotoImage(file="imps.png")
        bg_label = tk.Label(master, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relheight=1, relwidth=1)

        # source folder button
        btn_source = tk.Button(master, text="Select Source Folder", bg="lightblue", command=self.updateSourceFolder)
        btn_source.pack(side=tk.TOP, expand=True)

        # source folder label
        self.source_str_var = tk.StringVar(master)
        label_source = tk.Label(master, textvariable=self.source_str_var)
        label_source.pack(side=tk.TOP, expand=True)

        # output folder button
        btn_output = tk.Button(master, text="Select Output Folder", bg="lightblue", command=self.updateOutputFolder)
        btn_output.pack(side=tk.TOP, expand=True)

        # source folder label
        self.output_folder = ""
        self.output_str_var = tk.StringVar(master, value=self.output_folder)
        label_source = tk.Label(master, textvariable=self.output_str_var)
        label_source.pack(side=tk.TOP, expand=True)

        # merge button
        button3 = tk.Button(master, text="Start", bg="lightblue", command=self.merge_albums)
        button3.pack(side=tk.TOP, expand=True)

    def updateSourceFolder(self):
        folder = filedialog.askdirectory()
        self.source_str_var.set(folder)

    def updateOutputFolder(self):
        folder = filedialog.askdirectory()
        self.output_str_var.set(folder)
        
    def merge_albums(self):
        rel_source_folder = os.path.relpath(self.source_str_var.get())
        for root, albums, _ in os.walk(rel_source_folder):
            for album in albums:
                album_path = f"{root}/{album}"
                full_path = lambda x: os.path.abspath(os.path.join(album_path, x))
                tracks = list(filter(is_track, map(full_path, os.listdir(album_path))))
                format = get_format(tracks[0])
                merged = merge_tracks(sorted(tracks, key=get_track_number))
                album_path = f"{self.output_str_var.get()}/{os.path.relpath(album)}.{format}"
                merged.export(album_path, format=format)

if __name__ == "__main__":
    root = tk.Tk()
    ImpGarden(root)
    root.mainloop()