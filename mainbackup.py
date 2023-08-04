import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

def get_unique_filename(output_folder, base_filename):
    base_name, ext = os.path.splitext(base_filename)
    unique_filename = os.path.join(output_folder, f"{base_name}_music_video")
    num = 1
    while os.path.exists(f"{unique_filename}{num}.mp4"):
        num += 1
    return f"{unique_filename}{num}.mp4"

def make_music_video(song_file, clips_folder, output_folder):
    video_files = os.listdir(clips_folder)
    random.shuffle(video_files)

    clips = []
    for video_file in video_files:
        video_path = os.path.join(clips_folder, video_file)
        clip = VideoFileClip(video_path)
        clips.append(clip)

    # Concatenate all the clips to create the final video
    final_clip = concatenate_videoclips(clips, method="compose")

    # Load the background music
    background_music = AudioFileClip(song_file)

    # Set the audio of the final video with the background music
    final_clip = final_clip.set_audio(background_music)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a unique filename for the output video
    base_filename = os.path.basename(song_file)
    output_file = get_unique_filename(output_folder, base_filename)

    # Save the final video with the unique filename and the audio merged
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # Close all the clips to release resources
    for clip in clips:
        clip.close()

if __name__ == "__main__":
    song_file = r"G:\Python\PROJEKT\SONGS\Z KONOPI 187.mp3"
    clips_folder = r"G:\Python\PROJEKT\CLIPS"
    output_folder = r"G:\Python\PROJEKT\OUTPUT"

    make_music_video(song_file, clips_folder, output_folder)
