# This file converts all MOV files in a folder into mp4's ussing ffmpeg
# rotate ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

param(
    [string]$Folder = "."
)
Push-Location $Folder

try {
    Get-Childitem *.mov | foreach-object -Parallel { ffmpeg -i $_.Name -vf "transpose=1" -qscale 0 $_.Name.Replace('.MOV','.mp4').Replace('.mov','.mp4') } -ThrottleLimit 3
}
finally {
    Pop-Location
}