# ImpGarden

Python utility to merge a folder of albums into single files.

## Install
Requires FFMPEG, python3 and tkinter
To install libraries (for example) on ubuntu:
```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-install ffmpeg python3-tk
```

Install libraries and copy to `$PATH`
```bash
pip install -r requirements.txt 
cp impgarden.py ~/.local/bin/impgarden
```

## Usage
```bash
impgarden
```

Impgarden assumes the source folder is a folder of albums, and will output a merged track in the same audio format as the album.