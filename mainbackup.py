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

def resize_to_1080p(clip):
    return clip.resize(height=1080)

def make_music_video(song_file, clips_folder, output_folder):
    video_files = os.listdir(clips_folder)
    random.shuffle(video_files)

    clips = []
    for video_file in video_files:
        video_path = os.path.join(clips_folder, video_file)
        clip = VideoFileClip(video_path)
        # Resize the clip to 1080p
        clip = resize_to_1080p(clip)
        clips.append(clip)

    # Concatenate all the clips to create the final video
    final_clip = concatenate_videoclips(clips, method="compose")

    # Load the background music
    background_music = AudioFileClip(song_file)
    song_duration = background_music.duration

    # Set the audio of the final video with the background music
    final_clip = final_clip.set_audio(background_music)

    # Crop the final video to match the duration of the audio
    final_clip = final_clip.subclip(0, song_duration)

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



###


import os
import random

import cv2
from moviepy.editor import VideoFileClip



def delete_clips(clips_folder):
    for clip_file in os.listdir(clips_folder):
        clip_path = os.path.join(clips_folder, clip_file)
        cap = cv2.VideoCapture(clip_path)
        cap.release()  # Release the VideoCapture object
        os.remove(clip_path)  # Now you can safely delete the file

def export_clips(song_bpm, videos_folder, song_duration):
    beats_per_minute = song_bpm
    beats_per_second = beats_per_minute / 60
    clip_duration = 2 / beats_per_second  # Duration of each clip in seconds (2 beats)

    if not os.path.exists(videos_folder):
        print(f"Videos folder '{videos_folder}' does not exist.")
        return

    if not os.path.exists("G:\\Python\\PROJEKT\\CLIPS"):
        os.makedirs("G:\\Python\\PROJEKT\\CLIPS")

    # Load all the available video files
    video_files = [video_file for video_file in os.listdir(videos_folder) if video_file.endswith('.mp4')]
    num_videos = len(video_files)

    # Calculate the total number of clips required to cover the whole song duration
    total_clips_required = int(song_duration / clip_duration)

    # Calculate the number of clips each video should export
    clips_per_video = total_clips_required // num_videos
    remaining_clips = total_clips_required % num_videos

    clips_counter = 0

    # Keep track of the used time segments to avoid overlap
    used_time_segments = set()

    for video_file in video_files:
        video_path = os.path.join(videos_folder, video_file)
        video = VideoFileClip(video_path)
        video_duration = video.duration

        # Calculate the number of clips to render from this video
        clips_from_this_video = clips_per_video + 1 if remaining_clips > 0 else clips_per_video
        remaining_clips -= 1

        for _ in range(clips_from_this_video):
            # Ensure there is enough remaining time in the video for a new clip
            if video_duration >= clip_duration:
                # Calculate the maximum start time for this video segment to avoid overlapping
                max_start_time = video_duration - clip_duration

                # Keep trying to find a random start time that is not used and does not overlap
                found_valid_start_time = False
                start_time = 0

                while not found_valid_start_time:
                    start_time = random.uniform(0, max_start_time)
                    end_time = start_time + clip_duration

                    # Check if the current segment overlaps with any previously used segments
                    overlap = any(start_time < end and end_time > start for start, end in used_time_segments)

                    if not overlap:
                        # If there is no overlap, mark the segment as used and exit the loop
                        used_time_segments.add((start_time, end_time))
                        found_valid_start_time = True

                # Export the clip without sound
                clip = video.subclip(start_time, end_time)
                clip = clip.without_audio()

                clip_filename = f"output_clip{clips_counter}.mp4"
                clip_file_path = os.path.join("G:\\Python\\PROJEKT\\CLIPS", clip_filename)
                clip.write_videofile(clip_file_path, codec='libx264', audio=False)
                print(f"Exported clip: {clip_file_path}")

                # Close the clip after exporting to terminate the FFMPEG process for this clip
                clip.close()

                clips_counter += 1

        # Close the video after exporting all clips from this video to terminate the FFMPEG process
        video.close()

if __name__ == "__main__":
    # Example usage of export_clips method
    song_file = r"G:\Python\PROJEKT\SONGS\Z KONOPI 187.mp3"
    bpm = 156
    videos_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    song_duration = 180  # In seconds (e.g., 3 minutes)
    export_clips(bpm, videos_folder, song_duration)



############

import os
import random

import cv2
from moviepy.editor import VideoFileClip



def delete_clips(clips_folder):
    for clip_file in os.listdir(clips_folder):
        clip_path = os.path.join(clips_folder, clip_file)
        cap = cv2.VideoCapture(clip_path)
        cap.release()  # Release the VideoCapture object
        os.remove(clip_path)  # Now you can safely delete the file

def export_clips(song_bpm, videos_folder, song_duration):
    beats_per_minute = song_bpm
    beats_per_second = beats_per_minute / 60
    clip_duration = 2 / beats_per_second  # Duration of each clip in seconds (2 beats)

    if not os.path.exists(videos_folder):
        print(f"Videos folder '{videos_folder}' does not exist.")
        return

    if not os.path.exists("G:\\Python\\PROJEKT\\CLIPS"):
        os.makedirs("G:\\Python\\PROJEKT\\CLIPS")

    # Load all the available video files
    video_files = [video_file for video_file in os.listdir(videos_folder) if video_file.endswith('.mp4')]
    num_videos = len(video_files)

    # Calculate the total number of clips required to cover the whole song duration
    total_clips_required = int(song_duration / clip_duration)

    # Calculate the number of clips each video should export
    clips_per_video = total_clips_required // num_videos
    remaining_clips = total_clips_required % num_videos

    clips_counter = 0

    # Keep track of the used time segments to avoid overlap
    used_time_segments = set()

    for video_file in video_files:
        video_path = os.path.join(videos_folder, video_file)
        video = VideoFileClip(video_path)
        video_duration = video.duration

        # Calculate the number of clips to render from this video
        clips_from_this_video = clips_per_video + 1 if remaining_clips > 0 else clips_per_video
        remaining_clips -= 1

        for _ in range(clips_from_this_video):
            # Ensure there is enough remaining time in the video for a new clip
            if video_duration >= clip_duration:
                # Calculate the maximum start time for this video segment to avoid overlapping
                max_start_time = video_duration - clip_duration

                # Keep trying to find a random start time that is not used and does not overlap
                found_valid_start_time = False
                start_time = 0

                while not found_valid_start_time:
                    start_time = random.uniform(0, max_start_time)
                    end_time = start_time + clip_duration

                    # Check if the current segment overlaps with any previously used segments
                    overlap = any(start_time < end and end_time > start for start, end in used_time_segments)

                    if not overlap:
                        # If there is no overlap, mark the segment as used and exit the loop
                        used_time_segments.add((start_time, end_time))
                        found_valid_start_time = True

                # Export the clip without sound
                clip = video.subclip(start_time, end_time)
                clip = clip.without_audio()

                clip_filename = f"output_clip{clips_counter}.mp4"
                clip_file_path = os.path.join("G:\\Python\\PROJEKT\\CLIPS", clip_filename)
                clip.write_videofile(clip_file_path, codec='libx264', audio=False)
                print(f"Exported clip: {clip_file_path}")

                # Close the clip after exporting to terminate the FFMPEG process for this clip
                clip.close()

                clips_counter += 1

        # Close the video after exporting all clips from this video to terminate the FFMPEG process
        video.close()


if __name__ == "__main__":
    # Example usage of export_clips method
    bpm = 30
    videos_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    song_duration = 20  # In seconds (e.g., 3 minutes)
    export_clips(bpm, videos_folder, song_duration)
    print("done exporting clips")


###################


import os
import random

import cv2
from moviepy.editor import VideoFileClip



def delete_clips(clips_folder):
    for clip_file in os.listdir(clips_folder):
        clip_path = os.path.join(clips_folder, clip_file)
        cap = cv2.VideoCapture(clip_path)
        cap.release()  # Release the VideoCapture object
        os.remove(clip_path)  # Now you can safely delete the file

def export_clips(song_bpm, videos_folder, song_duration):
    beats_per_minute = song_bpm
    beats_per_second = beats_per_minute / 60
    clip_duration = 2 / beats_per_second  # Duration of each clip in seconds (2 beats)

    if not os.path.exists(videos_folder):
        print(f"Videos folder '{videos_folder}' does not exist.")
        return

    if not os.path.exists("G:\\Python\\PROJEKT\\CLIPS"):
        os.makedirs("G:\\Python\\PROJEKT\\CLIPS")

    # Load all the available video files
    video_files = [video_file for video_file in os.listdir(videos_folder) if video_file.endswith('.mp4')]
    num_videos = len(video_files)

    # Calculate the total number of clips required to cover the whole song duration
    total_clips_required = int(song_duration / clip_duration)

    # Calculate the number of clips each video should export
    clips_per_video = total_clips_required // num_videos
    remaining_clips = total_clips_required % num_videos

    clips_counter = 0

    # Keep track of the used time segments to avoid overlap
    used_time_segments = set()

    for video_file in video_files:
        video_path = os.path.join(videos_folder, video_file)
        video = VideoFileClip(video_path)
        video_duration = video.duration

        # Calculate the number of clips to render from this video
        clips_from_this_video = clips_per_video + 1 if remaining_clips > 0 else clips_per_video
        remaining_clips -= 1

        for _ in range(clips_from_this_video):
            # Ensure there is enough remaining time in the video for a new clip
            if video_duration >= clip_duration:
                # Calculate the maximum start time for this video segment to avoid overlapping
                max_start_time = video_duration - clip_duration

                # Keep trying to find a random start time that is not used and does not overlap
                found_valid_start_time = False
                start_time = 0

                while not found_valid_start_time:
                    start_time = random.uniform(0, max_start_time)
                    end_time = start_time + clip_duration

                    # Check if the current segment overlaps with any previously used segments
                    overlap = any(start_time < end and end_time > start for start, end in used_time_segments)

                    if not overlap:
                        # If there is no overlap, mark the segment as used and exit the loop
                        used_time_segments.add((start_time, end_time))
                        found_valid_start_time = True

                # Export the clip without sound
                clip = video.subclip(start_time, end_time)
                clip = clip.without_audio()

                clip_filename = f"output_clip{clips_counter}.mp4"
                clip_file_path = os.path.join("G:\\Python\\PROJEKT\\CLIPS", clip_filename)
                clip.write_videofile(clip_file_path, codec='libx264', audio=False)
                print(f"Exported clip: {clip_file_path}")

                # Close the clip after exporting to terminate the FFMPEG process for this clip
                clip.close()

                clips_counter += 1

        # Close the video after exporting all clips from this video to terminate the FFMPEG process
        video.close()


if __name__ == "__main__":
    # Example usage of export_clips method
    bpm = 30
    videos_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    song_duration = 20  # In seconds (e.g., 3 minutes)
    export_clips(bpm, videos_folder, song_duration)
    print("done exporting clips")

#####################
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

from package.downloadyt import download_videos_from_file

def export_clips(song_bpm, clips_folder, song_duration, video_folder):
    beats_per_minute = song_bpm
    beats_per_second = beats_per_minute / 60
    clip_duration = 2 / beats_per_second
    total_clips_required = int(song_duration / clip_duration)

    if not os.path.exists(clips_folder):
        os.makedirs(clips_folder)

    video_files = [video_file for video_file in os.listdir(video_folder) if video_file.endswith('.mp4')]

    for idx, video_file in enumerate(video_files):
        video_path = os.path.join(video_folder, video_file)
        video_title = video_file[:-4]

        video_clip = VideoFileClip(video_path)
        num_clips_from_video = total_clips_required // len(video_files)

        for clip_idx in range(num_clips_from_video):
            clip_start_time = clip_idx * clip_duration
            clip_end_time = (clip_idx + 1) * clip_duration
            clip = video_clip.subclip(clip_start_time, clip_end_time)

            clip_file_path = os.path.join(clips_folder, f"clip_{idx + 1}_{clip_idx + 1}.mp4")
            clip.write_videofile(clip_file_path, codec='libx264', audio=False)

            print(f"Exported clip {idx + 1}_{clip_idx + 1} from {video_title}")

        video_clip.close()

if __name__ == "__main__":
    file_path = "G:\\Python\\PROJEKT\\linksyt.txt"
    video_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    clips_folder = "G:\\Python\\PROJEKT\\CLIPS"
    song_bpm = 120
    song_duration = 240  # In seconds (e.g., 4 minutes)

    download_videos_from_file(file_path, video_folder)
    export_clips(song_bpm, clips_folder, song_duration, video_folder)

    print("Done exporting clips")


################



import os
from moviepy.video.io.VideoFileClip import VideoFileClip

from package.downloadyt import download_videos_from_file

def export_clips(song_bpm, clips_folder, song_duration, video_folder):
    beats_per_minute = song_bpm
    beats_per_second = beats_per_minute / 60
    clip_duration = 2 / beats_per_second
    total_clips_required = int(song_duration / clip_duration)

    if not os.path.exists(clips_folder):
        os.makedirs(clips_folder)

    video_files = [video_file for video_file in os.listdir(video_folder) if video_file.endswith('.mp4')]

    for idx, video_file in enumerate(video_files):
        video_path = os.path.join(video_folder, video_file)
        video_title = video_file[:-4]

        video_clip = VideoFileClip(video_path)
        num_clips_from_video = total_clips_required // len(video_files)

        for clip_idx in range(num_clips_from_video):
            clip_start_time = clip_idx * clip_duration
            clip_end_time = (clip_idx + 1) * clip_duration

            # Check if the clip_end_time exceeds the video duration
            if clip_end_time > video_clip.duration:
                break  # Don't export clips that are too close to the end

            clip = video_clip.subclip(clip_start_time, clip_end_time)

            clip_file_path = os.path.join(clips_folder, f"clip_{idx + 1}_{clip_idx + 1}.mp4")
            clip.write_videofile(clip_file_path, codec='libx264', audio=False)

            print(f"Exported clip {idx + 1}_{clip_idx + 1} from {video_title}")

        video_clip.close()

if __name__ == "__main__":
    file_path = "G:\\Python\\PROJEKT\\linksyt.txt"
    video_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    clips_folder = "G:\\Python\\PROJEKT\\CLIPS"
    song_bpm = 120
    song_duration = 240  # In seconds (e.g., 4 minutes)

    download_videos_from_file(file_path, video_folder)
    export_clips(song_bpm, clips_folder, song_duration, video_folder)

    print("Done exporting clips")
##########





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

def resize_to_1080p(clip):
    return clip.resize(height=1080)

def make_music_video(song_file, clips_folder, output_folder):
    video_files = os.listdir(clips_folder)
    random.shuffle(video_files)

    clips = []
    for video_file in video_files:
        video_path = os.path.join(clips_folder, video_file)
        clip = VideoFileClip(video_path)
        # Resize the clip to 1080p
        clip = resize_to_1080p(clip)
        clips.append(clip)

    # Concatenate all the clips to create the final video
    final_clip = concatenate_videoclips(clips, method="compose")

    # Load the background music
    background_music = AudioFileClip(song_file)
    song_duration = background_music.duration

    # Set the audio of the final video with the background music
    final_clip = final_clip.set_audio(background_music)

    # Crop the final video to match the duration of the audio
    final_clip = final_clip.subclip(0, song_duration)

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
