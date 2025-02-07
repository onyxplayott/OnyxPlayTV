import os
import subprocess
import vlc
import time
import threading

class IPTVPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()

    def play_mpd(self, mpd_url):
        self.player.set_mrl(mpd_url)
        self.player.play()
        time.sleep(1)

    def play_m3u(self, m3u_url):
        m3u_content = self.download_m3u(m3u_url)
        urls = self.parse_m3u(m3u_content)
        for url in urls:
            self.player.set_mrl(url)
            self.player.play()
            time.sleep(1)
            while self.player.is_playing():
                time.sleep(1)

    def download_m3u(self, m3u_url):
        try:
            import requests
            response = requests.get(m3u_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Failed to download M3U: {e}")
            return ""

    def parse_m3u(self, m3u_content):
        urls = []
        for line in m3u_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
        return urls

    def stop(self):
        self.player.stop()

if __name__ == "__main__":
    player = IPTVPlayer()
    try:
        while True:
            mode = input("Enter 'mpd' to play MPD or 'm3u' to play M3U: ").strip().lower()
            if mode == 'mpd':
                url = input("Enter the MPD URL: ").strip()
                player.play_mpd(url)
            elif mode == 'm3u':
                url = input("Enter the M3U URL: ").strip()
                player.play_m3u(url)
            elif mode == 'exit':
                break
            else:
                print("Invalid mode. Please enter 'mpd', 'm3u', or 'exit'.")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        player.stop()
