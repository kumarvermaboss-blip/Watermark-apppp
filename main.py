import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

# Request Storage Permissions on Android Startup
if platform == 'android':
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

class WatermarkMakerApp(App):
    def build(self):
        self.selected_files = []
        
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Application Header
        header = Label(
            text="[b]Watermark Maker[/b]",
            markup=True,
            font_size='22sp',
            size_hint=(1, 0.08),
            color=(0.1, 0.1, 0.1, 1)
        )
        main_layout.add_widget(header)
        
        # Action Dashboard Cards
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
        
        # Watermark Text Box
        self.text_input = TextInput(
            text="@PLfolders (Tg Search)",
            multiline=False,
            size_hint=(1, 0.1),
            padding=[10, 10]
        )
        main_layout.add_widget(self.text_input)
        
        # Scrollable Status Display Box
        scroll = ScrollView(size_hint=(1, 0.35))
        self.status_label = Label(
            text="Select videos or click 'Process Folder' to start...",
            size_hint_y=None,
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            valign='top'
        )
        self.status_label.bind(texture_size=self.status_label.setter('size'))
        scroll.add_widget(self.status_label)
        main_layout.add_widget(scroll)
        
        # Execution Button
        start_btn = Button(
            text="Start Watermarking",
            size_hint=(1, 0.12),
            background_color=(0.2, 0.7, 0.3, 1),
            font_size='18sp'
        )
        start_btn.bind(on_press=self.start_processing)
        main_layout.add_widget(start_btn)
        
        return main_layout

    def open_file_picker(self, instance):
        if platform == 'android':
            from jnius import autoclass
            from android import activity
            
            Intent = autoclass('android.content.Intent')
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType("video/*")
            intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, True)
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            
            activity.mActivity.startActivityForResult(
                Intent.createChooser(intent, "Select Videos"), 1001
            )
            self.status_label.text = "Opening File Manager..."
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
                self.status_label.text = "No video files found in /best"
        else:
            self.status_label.text = f"Folder not found: {folder_path}"

    def start_processing(self, instance):
        if not self.selected_files:
            self.load_folder_videos(None)
            
        if not self.selected_files:
            self.status_label.text = "No videos selected to watermark."
            return
            
        output_dir = "/storage/emulated/0/best_WM"
        os.makedirs(output_dir, exist_ok=True)
        
        watermark_text = self.text_input.text
        total = len(self.selected_files)
        
        for idx, file_path in enumerate(self.selected_files, 1):
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_dir, file_name)
            
            filter_complex = f"drawtext=text='{watermark_text}':x=10:y=10:fontsize=24:fontcolor=white"
            cmd = [
                "ffmpeg", "-y",
                "-i", file_path,
                "-vf", filter_complex,
                "-codec:a", "copy",
                output_path
            ]
            
            try:
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode != 0:
                    self.status_label.text = f"Error processing {file_name}"
                    return
            except Exception as e:
                self.status_label.text = f"FFmpeg Error: {str(e)}"
                return

        self.status_label.text = f"Success! {total} video(s) saved to /best_WM"

if __name__ == "__main__":
    WatermarkMakerApp().run()
