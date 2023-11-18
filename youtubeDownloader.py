'''
YouTube Video Downloader
Author: Anukul Poudel
'''

# import the package
from pytube import YouTube
import tempfile
import os
import subprocess

# check if there exixts resolution higher than 720 if yes returns 1 else 0
def check_resolutions(yt):
    '''checks if there exixts resolution higher than 720 if yes returns 1 else 0'''
    # Filter video streams with mime_type "video/mp4" and resolution higher than 720p
    filtered_streams = [stream for stream in yt.streams if stream.mime_type == 'video/mp4' and 'video' in stream.type and stream.resolution and int(stream.resolution[:-1]) > 720]

    # Check if there are resolutions greater than 720p
    return 1 if filtered_streams else 0

# combining both audio and video 
def combine_audio_video(input_video, input_audio, output_video):
    '''combining both audio and video'''
    # FFmpeg command to combine audio and video using FFmpeg
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

# display's progress percentage the first one is of audio and second one is of video
def on_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize_mb
    bytes_downloaded = total_size - bytes_remaining/(1024*1024)
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Download Progress: {percentage:.2f}%")
    # print(f'{bytes_downloaded} / {total_size}')

# download's video
def download(url):
    '''Downloads the video from URL'''
    # Set the URL
    yt = YouTube(url)

    # Get the title
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
    # print(f"res: {adaptive_video_streams[0].resolution}")

    # print("\nBest Audio Quality: ")
    # print(f"res: {adaptive_audio_streams[-1].abr}")

    # If result is 1 download audio and video seperately and combine using FFmpeg (DASH)
    # If 0 then download progressively
    result = check_resolutions(yt=yt)

    if result == 1:
        
        # Notifying user that there exists higher resulution video and that we are using DASH and FFmpeg
        print('Since the maximum quality of the video is greater than 720')
        print('using DASH or adaptive to download single best audio and video seperately and using FFmpeg to combining them.')

        # Downloading in system's temporary storage

        # Create a temporary directory to save the video
        temp_dir = tempfile.mkdtemp()

        # Print temp-dir
        # print(temp_dir)

        audio_stream = adaptive_audio_streams[-1]
        audio_filename = f"{title}_A"
        # Register the on_progress_callback
        print('Audio: ')
        yt.register_on_progress_callback(on_progress_callback)
        audio_stream.download(filename=audio_filename,output_path=temp_dir)

        video_stream = adaptive_video_streams[0]
        video_filename = f"{title}_V"
        # Register the on_progress_callback
        print('Video: ')
        yt.register_on_progress_callback(on_progress_callback)
        video_stream.download(filename=video_filename,output_path=temp_dir)

        # Combine audio and video
        output_video_path = f"{title}.mp4"
        input_audio_path = f"{os.path.join(temp_dir, title)}_A"
        input_video_path = f"{os.path.join(temp_dir, title)}_V"

        combine_audio_video(input_audio_path, input_video_path, output_video_path)
    else:
        # If the condition jummps here it means that the resolution of the video is not larger than 720
        print('Since the maximum quality of the video is not greater than 720')
        print("using progressive to download best video and audio.")
        # Set highest resolution
        videoaudio_stream = yt.streams.get_highest_resolution()

        # Showing download progress
        yt.register_on_progress_callback(on_progress_callback)

        # Download video
        videoaudio_stream.download()

url = 'https://www.youtube.com/watch?v=oIkhgagvrjI'
download(url)
