@echo off
set /p url="Community Tab URL: "
set /p folder="Destination Folder: "
cmd /K python export_community_content.py -d"%folder%" "%url%"
pause
