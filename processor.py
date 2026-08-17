import subprocess
import os

def cut_video(input_url, start_time, end_time, output_filename="output.mp4"):
    temp_input = "temp_source.mp4"

    # Download video using yt-dlp
    download_cmd = f"yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]' -o '{temp_input}' '{input_url}'"
    os.system(download_cmd)

    # Cut video using FFmpeg
    ffmpeg_cmd = (
        f"ffmpeg -i {temp_input} -ss {start_time} -to {end_time} "
        f"-c:v libx264 -c:a aac {output_filename} -y"
    )
    subprocess.run(ffmpeg_cmd, shell=True)

    if os.path.exists(temp_input):
        os.remove(temp_input)

    print(f"Video clipped successfully: {output_filename}")
    return output_filename
