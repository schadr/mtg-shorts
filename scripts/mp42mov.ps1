# This file converts all mp4 files in a folder into mov's ussing ffmpeg
param(
    [string]$Folder = "."
)
Push-Location $Folder

try {
    Get-Childitem *.mp4 | foreach-object -Parallel { ffmpeg -i $_.Name -f mov $_.Name.Replace('.mp4','.mov').Replace('.mp4','.mov') } -ThrottleLimit 3
}
finally {
    Pop-Location
}