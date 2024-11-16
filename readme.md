These Python scripts are wrappers for [yt-dlp](https://github.com/yt-dlp/yt-dlp), designed for specific use cases relevant to me.

During this project I explored the following Python concepts:
* Command-line arguments using argparse library
* OS-level actions, including file/folder creation and platform-agnostic path construction, using os library
* Running external programs using subprocess library

Python install is required to run; version 3.12.5 or newer is suggested. No external libraries are required.

## get-channel
A wrapper for downloading videos on a per-playlist basis (or per-channel, by passing link to channel's "video" page). I wrote this to simplify creating archives of YouTube content. Entire channel downloads are best performed by passing `https://www.youtube.com/@<handle>/videos` URL to the script.

Each requested playlist gets its own "archive.txt" file, which is passed to yt-dlp. Maintaining per-playlist archives is meant to speed up execution, compared to referencing a single archive.txt of every video ever downloaded.

The `--age` flag specifies a maximum age (in months) for videos to download. (By default it is set to 6 months.) This only applies to archives which *already exist*; when downloading a playlist for the first time, *all* its videos are downloaded. To ignore video age for pre-existing archives, pass `--age 0`.

## get-audio
A wrapper for downloading videos as audio files. By default, downloads best-possible audio quality in mp3 format. 

## buildArchive
A PowerShell script I wrote to create archive.txt files for playlists I had already downloaded. This was so I could use get-channel to easily handle updates going forward. Since I was already naming videos with a standard format that includes the eleven-character video ID, this script simply extracts that from each filename.