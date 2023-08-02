import os
import random
import moviepy.editor as mp

def delete_clips(clips_folder):
    if not os.path.exists(clips_folder):
        print(f"Clips folder '{clips_folder}' does not exist.")
        return

    for clip_file in os.listdir(clips_folder):
        if clip_file.endswith('.mp4'):
            clip_path = os.path.join(clips_folder, clip_file)
            os.remove(clip_path)
            print(f"Deleted clip: {clip_path}")

def export_clips(song_bpm, videos_folder, song_duration):
    beats_per_minute = song_bpm
    beats_per_second = beats_per_minute / 60
    clip_duration = 2 / beats_per_second  # Duration of each clip in seconds (2 beats)

    if not os.path.exists(videos_folder):
        print(f"Videos folder '{videos_folder}' does not exist.")
        return

    if not os.path.exists("G:\\Python\\PROJEKT\\CLIPS"):
        os.makedirs("G:\\Python\\PROJEKT\\CLIPS")

    # Calculate the total number of clips required to cover the whole song duration
    total_clips_required = int(song_duration / clip_duration)
    num_videos = len(os.listdir(videos_folder))

    clips_per_video = total_clips_required // num_videos
    remaining_clips = total_clips_required % num_videos

    clips_counter = 0
    video_clips = {}  # Dictionary to keep track of exported clips for each video

    for video_file in os.listdir(videos_folder):
        if video_file.endswith('.mp4'):
            video_path = os.path.join(videos_folder, video_file)
            # Pick a video to export clips from
            video = mp.VideoFileClip(video_path)
            video_duration = video.duration

            # Calculate the number of clips to render from this video
            clips_from_this_video = clips_per_video + 1 if remaining_clips > 0 else clips_per_video
            remaining_clips -= 1

            video_clips[video_path] = []

            for _ in range(clips_from_this_video):
                # Ensure there is enough remaining time in the video for a new clip
                if video_duration >= clip_duration:
                    # Calculate the clip start and end times without overlapping
                    start_time = random.uniform(0, video_duration - clip_duration)
                    end_time = start_time + clip_duration

                    # Check if the current clip overlaps with any previously exported clips from this video
                    while any(start_time < end and end_time > start for start, end in video_clips[video_path]):
                        start_time = random.uniform(0, video_duration - clip_duration)
                        end_time = start_time + clip_duration

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
                    video_clips[video_path].append((start_time, end_time))

            # Close the video after exporting all clips from this video to terminate the FFMPEG process
            video.close()

if __name__ == "__main__":
    # Example usage of export_clips method
    bpm = 30
    videos_folder = "G:\\Python\\PROJEKT\\VIDEOS"
    song_duration = 180  # In seconds (e.g., 3 minutes)
    export_clips(bpm, videos_folder, song_duration)
