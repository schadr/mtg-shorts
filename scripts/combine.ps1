# this file combines all the movie files in a folder into one mp4 file using ffmpeg and also combines all the json files into one json file adjusting relative positions
param(
    [string]$Folder = "."
)

# combine all json files
python -m src.merge_config --folder $Folder

# combine all mp4 files
# mylist.txt needs to be of the form:
# file 'file1.mp4'
# file 'file2.mp4'
Get-Childitem -File $Folder/*.mp4 | foreach-object {echo "file '$($_.Name)'"} | Out-File $Folder/mylist.txt -Encoding utf8NoBOM
Push-Location $Folder
try {
    ffmpeg -f concat -safe 0 -i mylist.txt -c copy merged.mp4
}
finally {
    Pop-Location
}