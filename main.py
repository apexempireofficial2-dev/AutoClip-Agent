import os
import time
import feedparser
from processor import cut_video

SEEN_FILE = "seen_videos.txt"
CHANNELS_FILE = "channels.txt"
CHECK_INTERVAL = 3600  # Har 1 ghante me check karega

def load_seen_videos():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_seen_video(video_id):
    with open(SEEN_FILE, "a") as f:
        f.write(video_id + "\n")

def check_channels():
    if not os.path.exists(CHANNELS_FILE):
        print("Error: channels.txt file nahi mili!")
        return

    with open(CHANNELS_FILE, "r") as f:
        channels = [line.strip() for line in f if line.strip()]

    seen_videos = load_seen_videos()

    for channel_id in channels:
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        print(f"Checking channel ID: {channel_id}")

        feed = feedparser.parse(rss_url)

        if not feed.entries:
            print(f"Koi video nahi mili ya URL galat hai: {channel_id}")
            continue

        latest_video = feed.entries[0]
        video_id = latest_video.id.split(":")[-1]
        video_url = latest_video.link
        video_title = latest_video.title

        if video_id not in seen_videos:
            print(f"\n[!] Nayi Video Mili: {video_title}")
            print(f"Downloading & Clipping...")

            output_file = f"clip_{video_id}.mp4"
            cut_video(video_url, start_time=0, end_time=165, output_filename=output_file)

            save_seen_video(video_id)
            print(f"Done! Saved as {output_file}\n")
        else:
            print(f"No new video for channel {channel_id}.")

def run_loop():
    print("AutoClip Agent Started Successfully...")
    while True:
        try:
            check_channels()
        except Exception as e:
            print(f"Error aaya: {e}")

        print(f"Waiting for {CHECK_INTERVAL} seconds before next check...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_loop()
