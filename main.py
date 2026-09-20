import os
import sys
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

class WatermarkMakerApp(App):
    def build(self):
        self.selected_files = []
        
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Header Title
        header = Label(
            text="[b]Watermark Maker[/b]",
            markup=True,
            font_size='22sp',
            size_hint=(1, 0.08),
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(header)
        
        # Dashboard Action Buttons
        grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.25))
        
        btn_select_files = Button(
            text="Select Videos\n(File Manager)",
            background_color=(0.4, 0.6, 1, 1),
            halign='center'
        )
        btn_select_files.bind(on_press=self.open_file_picker)
        
        btn_select_folder = Button(
            text="Process Folder\n(/storage/emulated/0/best)",
            background_color=(0.9, 0.5, 0.6, 1),
            halign='center'
        )
        btn_select_folder.bind(on_press=self.load_folder_videos)
        
        grid.add_widget(btn_select_files)
        grid.add_widget(btn_select_folder)
        main_layout.add_widget(grid)
        
        # Watermark Input Field
        self.text_input = TextInput(
            text="@PLfolders (Tg Search)",
            multiline=False,
            size_hint=(1, 0.1),
            padding=[10, 10]
        )
        main_layout.add_widget(self.text_input)
        
        # Fixed Scrollable Log / Error Display Area
        scroll = ScrollView(size_hint=(1, 0.40))
        self.status_label = Label(
            text="Select videos or click 'Process Folder' to start...",
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1),  # Bright readable white/grey text
            halign='left',
            valign='top',
            markup=True
        )
        # Text wrapping aur height auto-adjust settings
        self.status_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value - 20, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        scroll.add_widget(self.status_label)
        main_layout.add_widget(scroll)
        
        # Start Process Button
        start_btn = Button(
            text="Start Watermarking",
            size_hint=(1, 0.12),
            background_color=(0.2, 0.7, 0.3, 1),
            font_size='18sp'
        )
        start_btn.bind(on_press=self.start_processing)
        main_layout.add_widget(start_btn)
        
        return main_layout

    def on_start(self):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE
                ])
                
                from jnius import autoclass
                from android import activity
                
                Build = autoclass('android.os.Build')
                if Build.VERSION.SDK_INT >= 30:
                    Environment = autoclass('android.os.Environment')
                    if not Environment.isExternalStorageManager():
                        Intent = autoclass('android.content.Intent')
                        Settings = autoclass('android.provider.Settings')
                        Uri = autoclass('android.net.Uri')
                        
                        intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                        intent.setData(Uri.parse(f"package:{activity.mActivity.getPackageName()}"))
                        activity.mActivity.startActivity(intent)
            except Exception as e:
                self.status_label.text = f"[color=ff5555]Permission Error: {e}[/color]"

    def open_file_picker(self, instance):
        if platform == 'android':
            try:
                from jnius import autoclass
                from android import activity
                
                Intent = autoclass('android.content.Intent')
                intent = Intent(Intent.ACTION_GET_CONTENT)
                intent.setType("video/*")
                intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, True)
                intent.addCategory(Intent.CATEGORY_OPENABLE)
                
                activity.mActivity.startActivity(Intent.createChooser(intent, "Select Videos"))
                self.status_label.text = "Opening File Manager..."
            except Exception as e:
                self.status_label.text = f"[color=ff5555]Picker Error: {e}[/color]"
        else:
            self.status_label.text = "File picker runs on Android device."

    def load_folder_videos(self, instance):
        folder_path = "/storage/emulated/0/best"
        if os.path.exists(folder_path):
            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.mp4', '.mkv', '.mov'))]
            self.selected_files = files
            if files:
                self.status_label.text = f"Found {len(files)} video(s) in /best:\n" + "\n".join([os.path.basename(f) for f in files])
            else:
                self.status_label.text = "[color=ffaa00]No video files found in /best[/color]"
        else:
            self.status_label.text = f"[color=ff5555]Folder not found: {folder_path}[/color]"

    def get_ffmpeg_cmd(self):
        if platform == 'android':
            possible_paths = [
                "/data/data/org.test.watermarkapp/files/app/ffmpeg",
                os.path.join(os.environ.get("PYTHONPATH", ""), "ffmpeg"),
                "ffmpeg"
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        return "ffmpeg"

    def start_processing(self, instance):
        if not self.selected_files:
            self.load_folder_videos(None)
            
        if not self.selected_files:
            self.status_label.text = "[color=ffaa00]No videos selected to watermark.[/color]"
            return
            
        output_dir = "/storage/emulated/0/best_WM"
        os.makedirs(output_dir, exist_ok=True)
        
        watermark_text = self.text_input.text
        total = len(self.selected_files)
        ffmpeg_bin = self.get_ffmpeg_cmd()
        
        for idx, file_path in enumerate(self.selected_files, 1):
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_dir, file_name)
            
            filter_complex = f"drawtext=text='{watermark_text}':x=10:y=10:fontsize=24:fontcolor=white"
            cmd = [
                ffmpeg_bin, "-y",
                "-i", file_path,
                "-vf", filter_complex,
                "-codec:a", "copy",
                output_path
            ]
            
            try:
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode != 0:
                    self.status_label.text = f"[color=ff5555]Error processing {file_name}:\n{res.stderr}\n\nCommand: {' '.join(cmd)}[/color]"
                    return
            except Exception as e:
                self.status_label.text = f"[color=ff5555]FFmpeg Exec Error:\n{str(e)}[/color]"
                return

        self.status_label.text = f"[color=00ff00]Success! {total} video(s) saved to /best_WM[/color]"

if __name__ == "__main__":
    WatermarkMakerApp().run()
