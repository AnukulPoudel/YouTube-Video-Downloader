'''
YouTube Video Downloader
Author: Anukul Poudel
'''

#import the package
from pytube import YouTube
import tempfile
import os
import subprocess

def download(url):
    #Set the URL
    yt = YouTube(url)

    #Get the title
    title = yt.title
    print(f"Tile: {title}")

    #Get thumbnail URL
    print(f"Thumbnail URL: {yt.thumbnail_url}")

    # Filter video streams with file extension "mp4" and is DASH/adaptive
    adaptive_video_streams = yt.streams.filter(adaptive=True,file_extension='mp4',only_video=True)

    # Filter audio streams with file extension "mp4"
    adaptive_audio_streams = yt.streams.filter(adaptive=True,only_audio=True,file_extension='mp4')

    #Selects best Audio and Video Quality
    # print("\nBest Video Quality: ")
    print(f"res: {adaptive_video_streams[0].resolution}")

    # print("\nBest Audio Quality: ")
    print(f"res: {adaptive_audio_streams[-1].abr}")

    #downloading in system's temporary storage

    # Create a temporary directory to save the video
    temp_dir = tempfile.mkdtemp()

    #print temp-dir
    # print(temp_dir)

    audio_stream = adaptive_audio_streams[-1]
    audio_filename = f"{title}_A"
    audio_stream.download(filename=audio_filename,output_path=temp_dir)

    video_stream = adaptive_video_streams[0]
    video_filename = f"{title}_V"
    video_stream.download(filename=video_filename,output_path=temp_dir)


    #combining both audio and video 
    def combine_audio_video(input_video, input_audio, output_video):
        # FFmpeg command to combine audio and video
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-i', input_audio,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            output_video
        ]

        # Run the FFmpeg command
        subprocess.run(cmd)

    output_video_path = f"{title}.mp4"
    input_audio_path = f"{os.path.join(temp_dir, title)}_A"
    input_video_path = f"{os.path.join(temp_dir, title)}_V"

    combine_audio_video(input_audio_path, input_video_path, output_video_path)

url = 'https://www.youtube.com/watch?v=_w6PCHutmb4'
download(url)