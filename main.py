import os
import glob
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class WatermarkApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.title_label = Label(text="Video Watermarker", font_size=24)
        self.status_label = Label(text="Status: Ready", font_size=16)
        self.wm_input = TextInput(text="@PLfolders (Tg Search)", multiline=False, size_hint=(1, 0.2), font_size=18)
        self.start_btn = Button(text="Start Watermarking", size_hint=(1, 0.3))
        self.start_btn.bind(on_press=self.start_processing)
        
        layout.add_widget(self.title_label)
        layout.add_widget(self.wm_input)
        layout.add_widget(self.status_label)
        layout.add_widget(self.start_btn)
        return layout

    def start_processing(self, instance):
        self.status_label.text = "Processing..."
        Clock.schedule_once(self.process_videos, 0.5)

    def process_videos(self, dt):
        WATERMARK_TEXT = self.wm_input.text
        INPUT_FOLDER = "/storage/emulated/0/best"
        OUTPUT_FOLDER = "/storage/emulated/0/best_WM"
        FONT = "/system/fonts/DroidSans.ttf"
        
        if not os.path.exists(INPUT_FOLDER):
            self.status_label.text = "Error: /best folder not found!"
            return

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        files = glob.glob(os.path.join(INPUT_FOLDER, "*.mp4")) + glob.glob(os.path.join(INPUT_FOLDER, "*.mkv"))
        
        if not files:
            self.status_label.text = "No videos found in /best"
            return

        x = "if(lt(mod(t*60\\\\,2*(w-tw))\\\\,w-tw)\\\\,mod(t*60\\\\,2*(w-tw))\\\\,2*(w-tw)-mod(t*60\\\\,2*(w-tw)))"
        y = "if(lt(mod(t*45\\\\,2*(h-th))\\\\,h-th)\\\\,mod(t*45\\\\,2*(h-th))\\\\,2*(h-th)-mod(t*45\\\\,2*(h-th)))"
        
        total = len(files)
        for i, v in enumerate(files, 1):
            name = os.path.basename(v)
            out = os.path.join(OUTPUT_FOLDER, f"WM_{name}")
            self.status_label.text = f"Processing [{i}/{total}]: {name}"
            f = f"drawtext=fontfile={FONT}:text='{WATERMARK_TEXT}':fontcolor=white@1.0:fontsize=20:x={x}:y={y}"
            cmd = ["ffmpeg", "-y", "-i", v, "-vf", f, "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-c:a", "copy", out]
            try:
                subprocess.run(cmd, check=True)
            except Exception as e:
                self.status_label.text = f"Error on video {i}"
                return

        self.status_label.text = "Done! Check /best_WM"

if __name__ == "__main__":
    WatermarkApp().run()
