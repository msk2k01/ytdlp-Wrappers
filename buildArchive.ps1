foreach($i in (Get-ChildItem "./channels")) {
    New-Item -Path "./channels/$($i.name)/archive.txt" | Out-Null
    foreach($j in (Get-ChildItem "./channels/$($i.name)" -Exclude *.txt)) {
        $j.basename
        $id = ($j.basename).remove(0,(($j.basename).length-11))
        Add-Content -Path "./channels/$($i.name)/archive.txt" -Value "youtube $id"
    }
}

# this script will make a list of all videos currently downloaded by ID.
# yt-dlp will then skip videos in the archive.