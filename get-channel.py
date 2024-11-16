import argparse, subprocess, os

# global constants (commandline args parsed later in "main loop") (could be user-defined in future config file)
OUTPUT_ROOT = os.path.realpath(os.path.join('F:\\', 'media', 'youtube','channels'))
YTDLP_INSTALL = os.path.realpath(os.path.join('F:\\', 'media', 'youtube','yt-dlp.exe'))
FOLDER_NAME = r'%(channel)s__%(playlist)s'
FILE_NAME = r'%(title)s__%(id)s.%(ext)s'

# parse commandline arguments
def getArgs():
    parser = argparse.ArgumentParser(prog='Get-Channel', description='A wrapper for yt-dlp, specifically for downloading per-channel or per-playlist.')
    parser.add_argument('link', help='YouTube channel or playlist URL. Pass as a string encased in quotes.')
    parser.add_argument('-a', '--age', type=int, help='For archives that already exist, the maximum age (in months) of videos to check for download. Default is 6 months. Ignored if archive does not exist yet.', default=6)
    return parser.parse_args()

# get name of output folder (does not include path to it)
def getFolderName():
    print("[get-channel] Deducing output folder...")

    # get folder name using FOLDER_NAME as a template that includes attributes which yt-dlp detects and fills in
    result = subprocess.run([YTDLP_INSTALL, ARGS.link,
                                 '--simulate',                              # don't actually download the video
                                 '--print', f'{FOLDER_NAME}',               # use FOLDER_NAME as a template for what to return
                                 '--playlist-end', '1'],                    # only do the first video.
                                 capture_output=True)                       # pipe stdout to the variable name
    
    # .stdout:  get output from subprocess.
    # .decode:  .stdout returns raw byte data. This converts it to a string. 'replace' turns non-UTF-8 chars into �
    # .strip:   remove ending newline character and trailing spaces.
    result = result.stdout.decode('UTF-8', 'replace').strip()

    # sanitizing special characters
    result = ''.join('_' if c in ['/', '\\', '&', ' ', '�', '"', '\''] else c for c in result)
    
    # append root to folder name
    result = os.path.join(OUTPUT_ROOT, result)  

    return result

# check for existing playlist folder and its archive.txt. create if it doesn't exist.
# Return codes: 0 => both existed; 1 => folder existed, but not archive; 2 => neither folder nor archive existed.
def assertFolder(folderPath: str):
    archivePath = os.path.join(folderPath, "archive.txt")
    if os.path.exists(folderPath):
        if os.path.exists(archivePath):
            return 0
        else:
            return 1
    else:
        os.makedirs(folderPath)
        open(archivePath, 'a').close()
        print("[get-channel] Output folder and archive file created.")
        return 2

# constructing commandline args for yt-dlp, including max age of videos to check    
def makeYtdlpArgs(folderPath: str, ga: bool):
    archivePath = os.path.join(folderPath, "archive.txt")
    filePath = os.path.join(folderPath, FILE_NAME)
    result = ['--output', f'{filePath}', '--download-archive', f'{archivePath}']
    if ga:
        print("[get-channel] Downloading all videos in playlist, regardless of age.")
    else:
        result.extend(['--dateafter', f'today-{ARGS.age}months'])
        print(f'[get-channel] Downloading videos up to {ARGS.age} months old.')
    return result

###### Main execution starts here ######

ARGS = getArgs()
folder = getFolderName()

# logic to determine whether or not all files should be downloaded. Defaults to False.
getAll = False
match assertFolder(folder):
    case 0: # archive already exists
        if ARGS.age <= 0: getAll = True # if archive folder exists, but user still wants to check for all videos
    case 1:
        print("[get-channel] Output folder exists, but not associated archive.txt.")
        quit()
    case 2:
        getAll = True
    case _:
        print("[get-channel] Could not assert folder existence.")
        quit()

ytdlpArgs = makeYtdlpArgs(folder, getAll)
input("[get-channel] Press enter to begin...")
subprocess.run([YTDLP_INSTALL, ARGS.link] + ytdlpArgs)