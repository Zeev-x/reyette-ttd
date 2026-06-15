from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import threading
import os
import yt_dlp


# =========================
# LOGGER ANTI ERROR
# =========================
class DummyLogger:
    def debug(self, msg): 
        pass
    def warning(self, msg): 
        pass
    def error(self, msg): 
        pass


class TikTokLayout(BoxLayout):

    # =========================
    # SAFE LOG
    # =========================
    def add_log(self, text):
        def update(dt):
            current = self.ids.log.text or ""
            self.ids.log.text = current + str(text) + "\n"
        Clock.schedule_once(update)

    def clear_log(self):
        self.ids.log.text = ""

    # =========================
    # FIX URL (AUTO CLEAN)
    # =========================
    def fix_url(self, url):
        url = url.strip()

        if url.startswith("m/"):
            url = "https://www.tiktok.com/" + url[2:]

        if not url.startswith("http"):
            url = "https://" + url

        return url

    # =========================
    # DOWNLOAD TRIGGER
    # =========================
    def download_tiktok(self):
        threading.Thread(target=self._download_tiktok, daemon=True).start()

    # =========================
    # CORE DOWNLOAD
    # =========================
    def _download_tiktok(self):
        url = self.fix_url(self.ids.url.text)

        if not url:
            self.add_log("❌ URL kosong!")
            return

        os.makedirs("downloads/tiktok", exist_ok=True)

        self.add_log("=== DOWNLOAD TIKTOK ===")
        self.add_log(url)

        try:
            ydl_opts = {
                # 🔥 MAX QUALITY MODE
                'format': 'bestvideo+bestaudio/best',

                # merge jadi mp4
                'merge_output_format': 'mp4',

                # output file
                'outtmpl': '/storage/emulated/0/downloads/tiktokDLR/%(title)s.%(ext)s',

                # header biar tidak ditolak server
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0'
                },

                # 🔥 prioritas kualitas
                'format_sort': [
                    'res:1080',
                    'res:720',
                    'ext:mp4:m4a',
                    'vcodec:h264',
                    'acodec:aac'
                ],

                # safety
                'noplaylist': True,

                # silent mode
                'quiet': True,
                'no_warnings': True,
                'logger': DummyLogger(),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.add_log("✅ Download selesai!")

        except Exception as e:
            self.add_log(f"❌ Error: {str(e)}")


# =========================
# APP
# =========================
class TikTokApp(App):
    def build(self):
        return TikTokLayout()


if __name__ == "__main__":
    TikTokApp().run()
