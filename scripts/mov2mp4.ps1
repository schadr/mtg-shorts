# This file converts all MOV files in a folder into mp4's ussing ffmpeg

Get-Childitem *.mov | foreach-object -Parallel { ffmpeg -i $_.Name -qscale 0 $_.Name.Replace('.MOV','.mp4').Replace('.mov','.mp4') } -ThrottleLimit 3