# YouTube-Video-Downloader
This script selects and downloads the best quality of both video and audio available and merges them togetheir and saves them in the current directory.

Pre-requisities:
==========================
```
-Python
-Pytube
-FFmpeg
```
How this works:
==========================
This script works in following way:
```
1. It takes a url of a YT video in function name download
2. The function then,
   i. Prints the title and the thumbnail image`s url
   ii. Check if the video resulution is greater than 720,
       if yes it uses DASH to download best of both audio and video in temporary storage of OS and combine them using FFmpeg and save the combined video in the current working directory
       if not uses progressive to download the best video
   iii. It displays the current progress of download.
   iv. If the video is downloading in DASH then the video will not be available until the FFmpeg is finished combining them.
   v. If the video is progressive than we can see the video as soon as it starts downloading.
```
Things to add:
==========================
```
1. downloading Subtitle/Caption
2. downloading Playlists
3. downloading Channel`s video
4. A good looking UI
```
