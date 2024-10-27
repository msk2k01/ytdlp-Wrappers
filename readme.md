These Python scripts are wrappers for [yt-dlp](https://github.com/yt-dlp/yt-dlp), designed for specific use cases relevant to me.

## Programs

### get-channel
A wrapper for downloading videos on a per-channel or per-playlist basis. Playlists are assumed to all contain videos from the same channel, such as for a series of videos from creator's channel. If downloading a playlist with videos across multiple channels, using yt-dlp alone is preferable.

This script can be used to check for new videos added to the channel or playlist. Included in the output folder is an archive which yt-dlp can use to check for already downloaded videos. The script points yt-dlp to the correct archive to draw from at runtime. Using separate archive files for each playlist is intended to speed up checks for existing videos compared to maintaining a single archive of all videos. By default, the script has yt-dlp ignore videos older than six months; this can be adjusted with the `--age` flag. (Passing an age of 0 has yt-dlp attempt to download all videos, regardless of age.) 

Entire channel downloads are best performed by passing `https://www.youtube.com/@<handle>/videos` URL to the script.

### get-audio
A wrapper for downloading videos as audio files. By default, downloads best-possible audio quality in mp3 format. 

### buildArchive
A PowerShell script I wrote to create `archive.txt` files for playlists I had already downloaded. This was so I could use `get-channel.py` to easily handle updates going forward. Since I was already naming videos with a standard format that includes the eleven-character video ID, this script simply extracts that from each filename.

## Concepts Explored
During this project I explored the following Python concepts:
* Command-line arguments using argparse library
* OS-level actions, including file/folder creation and platform-agnostic path construction, using os library
* Running external programs using subprocess library
* Colored terminal output using colorama library (went unused)

## Prerequisites
Python install is required to run; version 3.12.5 or newer is suggested. No exteranl libraries are required.