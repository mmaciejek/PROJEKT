# G:\Python\PROJEKT\main.py
from package.downloadyt import download_videos_from_file
from package.getsongbpm import get_bpm_from_mp3_name
import os
from package.exportclips import export_clips, delete_clips
from package.makemusicvideo import make_music_video
import time
from mutagen.mp3 import MP3

def main():
    # Download videos from the links in linksyt.txt
    file_path = "G:\\Python\\PROJEKT\\linksyt.txt"
    video_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    clips_folder = "G:\\Python\\PROJEKT\\CLIPS"
    output_folder = r"G:\Python\PROJEKT\OUTPUT"
    download_videos_from_file(file_path, video_folder)

    # Get BPM for each song in the SONGS folder
    songs_folder = "G:\\Python\\PROJEKT\\SONGS"
    for song_file in os.listdir(songs_folder):
        if song_file.endswith('.mp3'):
            # Get BPM
            bpm = get_bpm_from_mp3_name(song_file)
            if bpm is not None:
                print(f"The BPM of '{song_file}' is {bpm}.")

            # Get song duration
            song_path = os.path.join(songs_folder, song_file)
            audio = MP3(song_path)
            song_duration = audio.info.length

            export_clips(bpm, video_folder, song_duration)
            make_music_video(song_path, clips_folder, output_folder)

    time.sleep(1)

if __name__ == "__main__":
    main()
