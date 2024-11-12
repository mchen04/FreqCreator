import os
from moviepy.editor import VideoFileClip

# Define folder paths
input_folder = "output_videos/videos"  # Folder where original videos are stored
output_folder = "processed_videos"  # Folder where processed videos will be saved
platforms = {
    "tiktok": 180,  # Max duration in seconds (e.g., 3 minutes)
    "facebook_reels": 60,
    "instagram_reels": 90,
    "youtube_shorts": 180,
}

def create_folders():
    """
    Checks if output folders for each platform exist; if not, creates them.
    """
    for platform in platforms.keys():
        platform_folder = os.path.join(output_folder, platform)
        os.makedirs(platform_folder, exist_ok=True)

def compress_video(input_path, output_path):
    """
    Compresses a video using MoviePy while maintaining quality.
    Adjusts bitrate to reduce file size but keeps a high-quality codec.
    """
    with VideoFileClip(input_path) as clip:
        # Use a reasonable bitrate for good quality (e.g., 1000k)
        clip.write_videofile(output_path, codec='libx264', bitrate="1000k")  # Adjust bitrate for quality

def process_videos():
    # Ensure output folders are set up
    create_folders()
    
    # Process each video in the input folder
    for video_file in os.listdir(input_folder):
        if video_file.endswith((".mp4", ".mov", ".avi")):
            video_path = os.path.join(input_folder, video_file)
            clip = VideoFileClip(video_path)

            # Trim and compress video for each platform
            for platform, max_duration in platforms.items():
                trimmed_path = os.path.join(output_folder, platform, f"{platform}_{video_file}")
                
                # Trim video to platform's max duration if needed
                if clip.duration > max_duration:
                    trimmed_clip = clip.subclip(0, max_duration)
                else:
                    trimmed_clip = clip
                
                # Save trimmed video
                trimmed_clip.write_videofile(trimmed_path, codec="libx264")
                trimmed_clip.close()

                # Compress the video
                compressed_path = os.path.join(output_folder, platform, f"compressed_{platform}_{video_file}")
                compress_video(trimmed_path, compressed_path)

                # Optional: remove the uncompressed version after compressing
                os.remove(trimmed_path)

            # Close the original clip to free memory
            clip.close()

# Run the process
process_videos()
