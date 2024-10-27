import argparse, subprocess, os

# parse commandline arguments
parser = argparse.ArgumentParser(prog='Get-Channel', description='A wrapper for yt-dlp, specifically for downloading per-channel or per-playlist.')
parser.add_argument('link', help='YouTube channel or playlist URL. Pass as a string encased in quotes for best results.')
parser.add_argument('-a', '--age', type=int, help='The maximum age, in months, of videos to download. If 0, will check all videos regardless of age.', default=6)
args = parser.parse_args()

# output and yt-dlp install location currently hardcoded
outputRoot = os.path.join('F:\\','media','youtube','channels') # folder the playlist folder goes in
ytdlpInstall = os.path.join('F:\\','media','youtube','yt-dlp.exe')

# constants for folder and file output paths
FOLDER_PATH_TEMPLATE = os.path.join(outputRoot, r'%(channel)s__%(playlist)s')
FILE_PATH_TEMPLATE = os.path.join(FOLDER_PATH_TEMPLATE, r'%(title)s__%(id)s.%(ext)s')



# get name of output folder (does not include path to it)
print("Deducing playlist folder name...")
folderName = subprocess.run([ytdlpInstall, args.link,
                             '--simulate',                              # don't actually download the video
                             '--print', f'{FOLDER_PATH_TEMPLATE}',      # get the channel and playlist, in format used for the folder name
                             '--playlist-end', '1'],                    # only do the first video.
                             capture_output=True)                       # pipe stdout to the variable name
folderName = folderName.stdout.decode('UTF-8').replace(' ', '_').strip()
    # .stdout: get output from subprocess.
    # .decode: .stdout returns raw byte data. This converts it to a string.
    # .replace(...): change spaces to _. Mimicks what the name becomes when running ytdlp with --restrict-filenames.
    # .strip: remove ending newline character.
print("Output folder parsed as: ", folderName)

# verifying existence of output folder
if not os.path.exists(folderName):
    print("### Output folder not found. Establishing...")
    os.makedirs(folderName)
    print("Output folder created.")

# path to the archive file for this playlist or channel
archiveFile = os.path.join(folderName, "archive.txt")
if not os.path.exists(archiveFile):
    print("### Archive file for this channel/playlist not found. Establishing...")
    f = open(archiveFile, "x")
    f.close()
    print("Archive created.")
else:
    print("Archive file found: " + archiveFile)

# constructing commandline args for yt-dlp, including max age of videos to check
ytdlpArgs = ['--output', f'{FILE_PATH_TEMPLATE}', '--download-archive', f'{archiveFile}']
if args.age > 0:
    ytdlpArgs.append ('--dateafter')
    ytdlpArgs.append(f'today-{args.age}months')
    print("Only downloading videos", args.age, "months and newer.")
    print(ytdlpArgs)
else:
    print("### NOTICE: Attempting to download ALL videos from channel/playlist, regardless of age.")

print("All checks complete. Starting downloads...\n")
subprocess.run([ytdlpInstall, args.link] + ytdlpArgs)