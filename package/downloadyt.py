from pytube import YouTube
import os

def download_videos_from_file(file_path, video_folder):
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    existing_video_titles = set()
    for video_file in os.listdir(video_folder):
        if video_file.endswith('.mp4'):
            video_title = video_file[:-4]
            existing_video_titles.add(video_title)

    with open(file_path, 'r') as file:
        video_links = file.read().strip().split('\n')

    for link in video_links:
        try:
            yt = YouTube(link)
            video_title = yt.title.replace(" ", "_")

            if video_title in existing_video_titles:
                print(f"Skipping {yt.title}. Video already downloaded.")
                continue

            video = yt.streams.filter(progressive=True, file_extension='mp4', resolution='1080p').first()

            # If there is no 1080p stream, fallback to the highest available resolution
            if not video:
                video = yt.streams.filter(progressive=True, file_extension='mp4').first()

            if video:
                print(f"Downloading: {yt.title}")
                video_file_path = os.path.join(video_folder, f"{video_title}.mp4")
                video.download(output_path=video_folder, filename=f"{video_title}.mp4")
                print("Download completed successfully.")
            else:
                print(f"Skipping {yt.title}. Could not find a compatible video stream.")
        except Exception as e:
            print(f"Error downloading {link}: {str(e)}")

            # Retry download up to 2 times
            retries = 2
            while retries > 0:
                retries -= 1
                print(f"Retrying download {2 - retries} time...")
                try:
                    video.download(output_path=video_folder, filename=f"{video_title}.mp4")
                    print("Download completed successfully.")
                    break
                except Exception as e:
                    print(f"Error downloading {link}: {str(e)}")
                    if retries == 0:
                        # If error persists after retries, delete the partially downloaded video file (if any)
                        video_file_path = os.path.join(video_folder, f"{video_title}.mp4")
                        if os.path.exists(video_file_path):
                            os.remove(video_file_path)

if __name__ == "__main__":
    file_path = "G:\\Python\\PROJEKT\\linksyt.txt"
    video_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    download_videos_from_file(file_path, video_folder)
