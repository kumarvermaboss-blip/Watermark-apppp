import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.utils import platform

class WatermarkMakerApp(App):
    def build(self):
        self.selected_files = []
        
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        header = Label(
            text="[b]Watermark Maker[/b]",
            markup=True,
            font_size='22sp',
            size_hint=(1, 0.08)
        )
        main_layout.add_widget(header)
        
        grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.22))
        
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
        
        self.text_input = TextInput(
            text="@PLfolders (Tg Search)",
            multiline=False,
            size_hint=(1, 0.1),
            padding=[10, 10]
        )
        main_layout.add_widget(self.text_input)
        
        scroll = ScrollView(size_hint=(1, 0.42))
        self.status_label = Label(
            text="Select videos or click 'Process Folder' to start...",
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1),
            halign='left',
            valign='top',
            markup=True
        )
        self.status_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value - 20, None)),
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        scroll.add_widget(self.status_label)
        main_layout.add_widget(scroll)
        
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
        layout = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path='/storage/emulated/0', filters=['*.mp4', '*.mkv', '*.mov'])
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10, padding=5)
        select_btn = Button(text="Select Chosen File(s)")
        cancel_btn = Button(text="Cancel")
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        
        layout.add_widget(filechooser)
        layout.add_widget(btn_layout)
        
        popup = Popup(title="Choose Video Files", content=layout, size_hint=(0.95, 0.95))
        
        def on_select(btn):
            if filechooser.selection:
                self.selected_files = filechooser.selection
                self.status_label.text = f"Selected {len(self.selected_files)} file(s):\n" + "\n".join([os.path.basename(f) for f in self.selected_files])
            popup.dismiss()
            
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

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

    def start_processing(self, instance):
        if not self.selected_files:
            self.load_folder_videos(None)
            
        if not self.selected_files:
            self.status_label.text = "[color=ffaa00]No videos selected to watermark.[/color]"
            return
            
        output_dir = "/storage/emulated/0/best_WM"
        os.makedirs(output_dir, exist_ok=True)
        
        text = self.text_input.text
        total = len(self.selected_files)

        for idx, file_path in enumerate(self.selected_files, 1):
            file_name = os.path.basename(file_path)
            output_path = os.path.join(output_dir, file_name)
            
            try:
                self.status_label.text = f"Processing ({idx}/{total}): {file_name}..."
                
                # FFmpeg command for overlay watermark (No C-extensions needed)
                cmd = [
                    'ffmpeg', '-y', '-i', file_path,
                    '-vf', f"drawtext=text='{text}':x=20:y=20:fontsize=24:fontcolor=white",
                    '-c:a', 'copy', output_path
                ]
                
                subprocess.run(cmd, check=True)
                
            except Exception as e:
                self.status_label.text = f"[color=ff5555]Error processing {file_name}:\n{str(e)}[/color]"
                return

        self.status_label.text = f"[color=00ff00]Success! {total} video(s) saved to /best_WM[/color]"

if __name__ == "__main__":
    WatermarkMakerApp().run()
