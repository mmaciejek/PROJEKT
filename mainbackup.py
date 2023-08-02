import os
import random
import moviepy.editor as mp

def get_unique_filename(output_folder, base_filename):
    base_name, ext = os.path.splitext(base_filename)
    unique_filename = os.path.join(output_folder, f"{base_name}_music_video")
    num = 1
    while os.path.exists(f"{unique_filename}{num}.mp4"):
        num += 1
    return f"{unique_filename}{num}.mp4"

def make_music_video(song_file, clips_folder, output_folder):
    # Check if the song file exists
    if not os.path.exists(song_file):
        print(f"Song file '{song_file}' does not exist.")
        return

    # Check if the clips folder exists
    if not os.path.exists(clips_folder):
        print(f"Clips folder '{clips_folder}' does not exist.")
        return

    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the song file
    audio_clip = mp.AudioFileClip(song_file)

    # Get a list of all the video clips in the clips folder
    clip_files = [os.path.join(clips_folder, clip_file) for clip_file in os.listdir(clips_folder) if
                  clip_file.endswith('.mp4')]

    # Shuffle the list of clips to play them in random order
    random.shuffle(clip_files)

    # Create a VideoFileClip object for each clip
    clips = [mp.VideoFileClip(clip_file) for clip_file in clip_files]

    # Concatenate all the clips together
    final_clip = mp.concatenate_videoclips(clips, method="compose")

    # Set the audio of the final clip to be the song audio
    final_clip = final_clip.set_audio(audio_clip)

    # Get the base filename of the song file without the path
    song_filename = os.path.basename(song_file)

    # Generate a unique output filename
    output_filename = get_unique_filename(output_folder, song_filename)

    # Export the final video to the output folder
    final_clip.write_videofile(output_filename, codec='libx264', audio_codec='aac')

    # Close all the clips after exporting to terminate the FFMPEG process
if __name__ == "__main__":
    song_file = r"G:\Python\PROJEKT\SONGS\OHSHIIT160 tag160.mp3"
    clips_folder = r"G:\Python\PROJEKT\CLIPS"
    output_folder = r"G:\Python\PROJEKT\OUTPUT"

    make_music_video(song_file, clips_folder, output_folder)
