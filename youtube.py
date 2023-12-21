import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import argparse
from pytube import YouTube
import os

def download_video(url, output_title, output_path='output/'):
    try:
        # Create YouTube object
        yt = YouTube(url)

        # Get the highest resolution progressive stream with an MP4 extension
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # Set the output path
        os.makedirs(output_path, exist_ok=True)

        # Manually set the output title from the command line argument
        sanitized_title = "".join(c for c in output_title if c.isalnum() or c.isspace())
        output_file = os.path.join(output_path, f"{sanitized_title}.mp4")

        # Download the video
        print(f"Downloading: {yt.title}")
        video_stream.download(output_path, filename=f"{sanitized_title}.mp4")

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
