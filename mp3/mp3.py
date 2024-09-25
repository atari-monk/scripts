import os
import yt_dlp

def download_youtube_as_mp3(video_url, output_folder="downloads"):
    try:
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # yt-dlp options to download audio and convert to mp3
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        print("Download and conversion to MP3 completed.")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_as_mp3(video_url)
