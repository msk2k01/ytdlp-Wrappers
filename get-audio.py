import argparse, subprocess, os

# parse commandline arguments
parser = argparse.ArgumentParser(prog='Get-Channel', description='A wrapper for yt-dlp, specifically for downloading per-channel or per-playlist.')
parser.add_argument('link', help='YouTube video URL. Pass as a string encased in quotes.')
parser.add_argument('-f', '--format', help='Audio format for downloaded file. Accepts all options yt-dlp accepts.', default='mp3', choices=['aac', 'alac', 'flac', 'm4a', 'mp3', 'opus', 'vorbis', 'wav', 'best'])
args = parser.parse_args()

# output and yt-dlp install location currently hardcoded
outputRoot = os.path.join('F:\\','media','youtube','other') # folder the playlist folder goes in
ytdlpInstall = os.path.join('F:\\','media','youtube','yt-dlp.exe')

# constants for folder and file output paths
FOLDER_PATH_TEMPLATE = os.path.join(outputRoot, r'%(channel)s__%(playlist)s')
FILE_PATH_TEMPLATE = os.path.join(FOLDER_PATH_TEMPLATE, r'%(title)s__%(id)s.%(ext)s')

subprocess.run([ytdlpInstall, args.link, 
                '--extract-audio',
                '--audio-quality', '0',
                '--audio-format', args.format,
                '--output', f'{FILE_PATH_TEMPLATE}'])