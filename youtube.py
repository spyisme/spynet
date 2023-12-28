import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import argparse
from pytube import YouTube
import os 
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    # Your custom progress bar or print statement goes here
    print(f"Downloading... {bytes_downloaded/total_size:.1%} done", end='\r')

def download_video(url, output_title, output_path='output/'):
    try:
        # Create YouTube object with on_progress callback
        yt = YouTube(url, on_progress_callback=on_progress)

        # Get the lowest resolution progressive stream with an MP4 extension
        video_stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()

        # Set the output path
        output_file = os.path.join(output_path, f"{output_title}.mp4")

        # Download the video
        print(f"Downloading: {yt.title}")
        video_stream.download(output_path, filename=f"{output_title}.mp4")

        print(f"Video saved as: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Video Downloader")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("title", help="Title for the downloaded video")
    args = parser.parse_args()

    video_url = args.url
    output_title = args.title

    download_video(video_url, output_title)
