#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Video Compression Tool - Using FFmpeg and HEVC Encoding
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import json
import re
import winreg

class VideoCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Compression Tool")
        self.root.geometry("700x800")
        self.root.resizable(False, False)

        self.input_file = ""
        self.output_file = ""
        self.output_dir = self.get_downloads_folder()
        self.is_compressing = False

        self.setup_ui()
        self.check_ffmpeg()

    def get_downloads_folder(self):
        """Get the user's Downloads folder path from registry"""
        try:
            # Open registry path
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            )
            # Read Downloads folder path
            downloads_path, _ = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')
            winreg.CloseKey(key)
            return downloads_path
        except Exception:
            # If reading fails, return default path
            return os.path.join(os.path.expanduser('~'), 'Downloads')

    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'],
                         capture_output=True,
                         check=True,
                         creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror("Error",
                "FFmpeg not found!\nPlease install FFmpeg and add it to system PATH.")
            self.compress_btn['state'] = 'disabled'

    def setup_ui(self):
        """Setup user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        title_frame.pack(fill='x')
        title_label = tk.Label(title_frame,
                              text="Video Compression Tool",
                              font=('Arial', 14, 'bold'),
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=12)

        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=15)
        main_frame.pack(fill='both', expand=True)

        # File selection area
        file_frame = tk.LabelFrame(main_frame, text="Select Video File",
                                   font=('Arial', 9), padx=10, pady=8)
        file_frame.pack(fill='x', pady=(0, 10))

        self.file_label = tk.Label(file_frame,
                                   text="No file selected",
                                   fg='gray',
                                   wraplength=600,
                                   justify='left')
        self.file_label.pack(anchor='w', pady=(0, 10))

        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(fill='x')

        select_btn = tk.Button(btn_frame,
                              text="Select File",
                              command=self.select_file,
                              bg='#3498db', fg='white',
                              font=('Arial', 9),
                              cursor='hand2',
                              padx=15, pady=5)
        select_btn.pack(side='left', padx=(0, 10))

        self.info_label = tk.Label(btn_frame, text="", fg='#27ae60', font=('Arial', 9))
        self.info_label.pack(side='left')

        # Output directory selection
        output_frame = tk.LabelFrame(main_frame, text="Output Directory",
                                     font=('Arial', 9), padx=10, pady=8)
        output_frame.pack(fill='x', pady=(0, 10))

        self.output_label = tk.Label(output_frame,
                                     text=f"Default save to: {self.output_dir}",
                                     fg='black',
                                     wraplength=600,
                                     justify='left',
                                     font=('Arial', 9))
        self.output_label.pack(anchor='w', pady=(0, 10))

        output_btn_frame = tk.Frame(output_frame)
        output_btn_frame.pack(fill='x')

        output_btn = tk.Button(output_btn_frame,
                              text="Select Output Directory",
                              command=self.select_output_dir,
                              bg='#3498db', fg='white',
                              font=('Arial', 9),
                              cursor='hand2',
                              padx=15, pady=5)
        output_btn.pack(side='left', padx=(0, 10))

        reset_output_btn = tk.Button(output_btn_frame,
                                     text="Reset to Default",
                                     command=self.reset_output_dir,
                                     font=('Arial', 9),
                                     cursor='hand2',
                                     padx=15, pady=5)
        reset_output_btn.pack(side='left')

        # Compression quality selection
        quality_frame = tk.LabelFrame(main_frame, text="Compression Quality Settings",
                                     font=('Arial', 9), padx=10, pady=8)
        quality_frame.pack(fill='x', pady=(0, 10))

        self.quality_var = tk.StringVar(value="high")

        qualities = [
            ("High Quality (CRF 28, 1080p, 96kbps) - Visually lossless, 90-95% compression", "high"),
            ("Medium Quality (CRF 32, 1080p, 64kbps) - Slight loss, 95-97% compression", "medium"),
            ("High Compression (CRF 36, 720p, 48kbps) - Noticeable loss, 97-99% compression", "small")
        ]

        for text, value in qualities:
            rb = tk.Radiobutton(quality_frame,
                              text=text,
                              variable=self.quality_var,
                              value=value,
                              font=('Arial', 9),
                              anchor='w',
                              justify='left')
            rb.pack(anchor='w', pady=3)

        # Custom settings
        custom_frame = tk.LabelFrame(main_frame, text="Custom Settings (Optional)",
                                    font=('Arial', 9), padx=10, pady=8)
        custom_frame.pack(fill='x', pady=(0, 10))

        # Tip text
        tip_label = tk.Label(custom_frame,
                           text="Tip: These settings will override the presets above. Lower values = Higher quality = Larger file size",
                           fg='#e67e22',
                           font=('Arial', 8),
                           wraplength=600)
        tip_label.pack(anchor='w', pady=(0, 5))

        # CRF
        crf_frame = tk.Frame(custom_frame)
        crf_frame.pack(fill='x', pady=5)
        crf_label = tk.Label(crf_frame, text="CRF Value (18-36):", width=18, anchor='w', font=('Arial', 9))
        crf_label.pack(side='left')
        self.crf_var = tk.StringVar(value="")
        tk.Entry(crf_frame, textvariable=self.crf_var, width=10, font=('Arial', 9)).pack(side='left', padx=5)
        crf_help = tk.Label(crf_frame, text="Video quality (18=Very high, 28=High, 36=Low)", fg='gray', font=('Arial', 8))
        crf_help.pack(side='left')

        # Width
        width_frame = tk.Frame(custom_frame)
        width_frame.pack(fill='x', pady=5)
        width_label = tk.Label(width_frame, text="Target Width:", width=18, anchor='w', font=('Arial', 9))
        width_label.pack(side='left')
        self.width_var = tk.StringVar(value="")
        tk.Entry(width_frame, textvariable=self.width_var, width=10, font=('Arial', 9)).pack(side='left', padx=5)
        width_help = tk.Label(width_frame, text="Resolution (1920=1080p, 1280=720p, leave blank=keep)", fg='gray', font=('Arial', 8))
        width_help.pack(side='left')

        # Audio bitrate
        audio_frame = tk.Frame(custom_frame)
        audio_frame.pack(fill='x', pady=5)
        audio_label = tk.Label(audio_frame, text="Audio Bitrate:", width=18, anchor='w', font=('Arial', 9))
        audio_label.pack(side='left')
        self.audio_var = tk.StringVar(value="")
        tk.Entry(audio_frame, textvariable=self.audio_var, width=10, font=('Arial', 9)).pack(side='left', padx=5)
        audio_help = tk.Label(audio_frame, text="Audio quality (128k=High, 96k=Medium, 64k=Low)", fg='gray', font=('Arial', 8))
        audio_help.pack(side='left')

        # Status display
        self.status_label = tk.Label(main_frame, text="", fg='#7f8c8d', font=('Arial', 9))
        self.status_label.pack(anchor='w', pady=(5, 10))

        # Button area
        btn_container = tk.Frame(main_frame)
        btn_container.pack(fill='x', pady=(0, 10))

        self.compress_btn = tk.Button(btn_container,
                                     text="Start Compression",
                                     command=self.start_compression,
                                     bg='#27ae60', fg='white',
                                     font=('Arial', 11, 'bold'),
                                     cursor='hand2',
                                     padx=40, pady=12)
        self.compress_btn.pack(side='left', padx=(0, 10))

        self.cancel_btn = tk.Button(btn_container,
                                   text="Cancel",
                                   command=self.cancel_compression,
                                   bg='#e74c3c', fg='white',
                                   font=('Arial', 11),
                                   cursor='hand2',
                                   padx=40, pady=12,
                                   state='disabled')
        self.cancel_btn.pack(side='left')

        # Version number (same row as buttons, right aligned)
        version_label = tk.Label(btn_container, text="v1.0.1",
                               fg='#95a5a6',
                               font=('Arial', 8))
        version_label.pack(side='right', padx=(0, 10))

    def select_file(self):
        """Select video file"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.mkv *.avi *.mov *.flv *.wmv *.webm"),
                ("All Files", "*.*")
            ]
        )

        if filename:
            self.input_file = filename
            self.file_label.config(text=filename, fg='black')

            # Get file size
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            self.info_label.config(text=f"File size: {size_mb:.1f} MB")

    def select_output_dir(self):
        """Select output directory"""
        dirname = filedialog.askdirectory(title="Select Output Directory")

        if dirname:
            self.output_dir = dirname
            self.output_label.config(text=dirname, fg='black')

    def reset_output_dir(self):
        """Reset output directory to default"""
        self.output_dir = self.get_downloads_folder()
        self.output_label.config(text=f"Default save to: {self.output_dir}", fg='black')

    def get_compression_params(self):
        """Get compression parameters"""
        # Custom settings take priority
        crf = self.crf_var.get().strip()
        width = self.width_var.get().strip()
        audio = self.audio_var.get().strip()

        if crf or width or audio:
            # Use custom settings
            if not crf:
                crf = "28"
            if not audio:
                audio = "96k"

            scale = f"-vf scale={width}:-1" if width else ""
            suffix = "custom"
        else:
            # Use preset
            quality = self.quality_var.get()

            if quality == "high":
                crf = "28"
                scale = ""
                audio = "96k"
                suffix = "high_quality"
            elif quality == "medium":
                crf = "32"
                scale = ""
                audio = "64k"
                suffix = "medium"
            else:  # small
                crf = "36"
                scale = "-vf scale=1280:720"
                audio = "48k"
                suffix = "small"

        return crf, scale, audio, suffix

    def start_compression(self):
        """Start compression"""
        if not self.input_file:
            messagebox.showwarning("Warning", "Please select a video file first!")
            return

        # Generate output filename
        dir_name = self.output_dir

        base_name = os.path.splitext(os.path.basename(self.input_file))[0]

        crf, scale, audio, suffix = self.get_compression_params()

        self.output_file = os.path.join(dir_name, f"{base_name}_compressed_{suffix}.mp4")

        # Confirm start
        result = messagebox.askyesno(
            "Confirm Compression",
            f"Input file: {self.input_file}\n\n"
            f"Output file: {self.output_file}\n\n"
            f"CRF: {crf}\n"
            f"Audio: {audio}\n\n"
            f"Start compression?"
        )

        if not result:
            return

        # Disable button, show loading animation
        self.compress_btn.config(text="Compressing...", state='disabled')
        self.cancel_btn['state'] = 'normal'
        self.is_compressing = True

        # Update status
        self.status_label.config(text="Compressing, please wait...", fg='#3498db')

        # Execute compression in new thread
        thread = threading.Thread(target=self.compress_video,
                                 args=(crf, scale, audio))
        thread.daemon = True
        thread.start()

    def compress_video(self, crf, scale, audio):
        """Execute video compression"""
        try:
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', self.input_file,
                '-c:v', 'libx265',
                '-preset', 'medium',
                '-crf', crf
            ]

            if scale:
                cmd.extend(scale.split())

            cmd.extend([
                '-tag:v', 'hvc1',
                '-c:a', 'aac',
                '-b:a', audio,
                '-y',
                self.output_file
            ])

            # Execute compression
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            self.current_process = process
            stdout, stderr = process.communicate()

            if not self.is_compressing:
                # User cancelled
                return

            if process.returncode == 0:
                # Compression successful
                original_size = os.path.getsize(self.input_file) / (1024 * 1024)
                compressed_size = os.path.getsize(self.output_file) / (1024 * 1024)
                ratio = (1 - compressed_size / original_size) * 100

                self.root.after(0, lambda: self.compression_complete(
                    original_size, compressed_size, ratio
                ))
            else:
                error_msg = stderr.decode('utf-8', errors='ignore')
                self.root.after(0, lambda: self.compression_failed(error_msg))

        except Exception as e:
            self.root.after(0, lambda: self.compression_failed(str(e)))

    def compression_complete(self, original_size, compressed_size, ratio):
        """Compression complete"""
        self.status_label.config(text="Compression complete!", fg='#27ae60')

        self.compress_btn.config(text="Start Compression", state='normal')
        self.cancel_btn['state'] = 'disabled'
        self.is_compressing = False

        messagebox.showinfo(
            "Compression Complete",
            f"Compression successful!\n\n"
            f"Original size: {original_size:.1f} MB\n"
            f"Compressed: {compressed_size:.1f} MB\n"
            f"Compression ratio: {ratio:.1f}%\n\n"
            f"Output file:\n{self.output_file}"
        )

    def compression_failed(self, error):
        """Compression failed"""
        self.status_label.config(text="Compression failed", fg='#e74c3c')

        self.compress_btn.config(text="Start Compression", state='normal')
        self.cancel_btn['state'] = 'disabled'
        self.is_compressing = False

        messagebox.showerror("Compression Failed", f"An error occurred during compression:\n\n{error}")

    def cancel_compression(self):
        """Cancel compression"""
        if hasattr(self, 'current_process'):
            self.current_process.terminate()
            self.is_compressing = False

            self.status_label.config(text="Cancelled", fg='#e74c3c')

            self.compress_btn.config(text="Start Compression", state='normal')
            self.cancel_btn['state'] = 'disabled'

            # Delete incomplete output file
            if self.output_file and os.path.exists(self.output_file):
                try:
                    os.remove(self.output_file)
                except:
                    pass

def main():
    root = tk.Tk()
    app = VideoCompressor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
