#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
视频压缩工具 - 使用 FFmpeg 和 HEVC 编码
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
        self.root.title("视频压缩工具")
        self.root.geometry("700x800")
        self.root.resizable(False, False)

        self.input_file = ""
        self.output_file = ""
        self.output_dir = self.get_downloads_folder()
        self.is_compressing = False

        self.setup_ui()
        self.check_ffmpeg()

    def get_downloads_folder(self):
        """从注册表获取用户的下载文件夹路径"""
        try:
            # 打开注册表路径
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            )
            # 读取 Downloads 文件夹路径
            downloads_path, _ = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')
            winreg.CloseKey(key)
            return downloads_path
        except Exception:
            # 如果读取失败，返回默认路径
            return os.path.join(os.path.expanduser('~'), 'Downloads')

    def check_ffmpeg(self):
        """检查 FFmpeg 是否安装"""
        try:
            subprocess.run(['ffmpeg', '-version'],
                         capture_output=True,
                         check=True,
                         creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror("错误",
                "未找到 FFmpeg！\n请先安装 FFmpeg 并添加到系统 PATH。")
            self.compress_btn['state'] = 'disabled'

    def setup_ui(self):
        """设置界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        title_frame.pack(fill='x')
        title_label = tk.Label(title_frame,
                              text="视频压缩工具",
                              font=('Microsoft YaHei UI', 14, 'bold'),
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=12)

        # 主容器
        main_frame = tk.Frame(self.root, padx=20, pady=15)
        main_frame.pack(fill='both', expand=True)

        # 文件选择区域
        file_frame = tk.LabelFrame(main_frame, text="选择视频文件",
                                   font=('Microsoft YaHei UI', 9), padx=10, pady=8)
        file_frame.pack(fill='x', pady=(0, 10))

        self.file_label = tk.Label(file_frame,
                                   text="未选择文件",
                                   fg='gray',
                                   wraplength=600,
                                   justify='left')
        self.file_label.pack(anchor='w', pady=(0, 10))

        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(fill='x')

        select_btn = tk.Button(btn_frame,
                              text="选择文件",
                              command=self.select_file,
                              bg='#3498db', fg='white',
                              font=('Microsoft YaHei UI', 9),
                              cursor='hand2',
                              padx=15, pady=5)
        select_btn.pack(side='left', padx=(0, 10))

        self.info_label = tk.Label(btn_frame, text="", fg='#27ae60', font=('Microsoft YaHei UI', 9))
        self.info_label.pack(side='left')

        # 输出目录选择
        output_frame = tk.LabelFrame(main_frame, text="输出目录",
                                     font=('Microsoft YaHei UI', 9), padx=10, pady=8)
        output_frame.pack(fill='x', pady=(0, 10))

        self.output_label = tk.Label(output_frame,
                                     text=f"默认保存到: {self.output_dir}",
                                     fg='black',
                                     wraplength=600,
                                     justify='left',
                                     font=('Microsoft YaHei UI', 9))
        self.output_label.pack(anchor='w', pady=(0, 10))

        output_btn_frame = tk.Frame(output_frame)
        output_btn_frame.pack(fill='x')

        output_btn = tk.Button(output_btn_frame,
                              text="选择输出目录",
                              command=self.select_output_dir,
                              bg='#3498db', fg='white',
                              font=('Microsoft YaHei UI', 9),
                              cursor='hand2',
                              padx=15, pady=5)
        output_btn.pack(side='left', padx=(0, 10))

        reset_output_btn = tk.Button(output_btn_frame,
                                     text="重置为默认",
                                     command=self.reset_output_dir,
                                     font=('Microsoft YaHei UI', 9),
                                     cursor='hand2',
                                     padx=15, pady=5)
        reset_output_btn.pack(side='left')

        # 压缩质量选择
        quality_frame = tk.LabelFrame(main_frame, text="压缩质量设置",
                                     font=('Microsoft YaHei UI', 9), padx=10, pady=8)
        quality_frame.pack(fill='x', pady=(0, 10))

        self.quality_var = tk.StringVar(value="high")

        qualities = [
            ("高质量 (CRF 28, 1080p, 96kbps) - 视觉无损，压缩率 90-95%", "high"),
            ("中等质量 (CRF 32, 1080p, 64kbps) - 轻微损失，压缩率 95-97%", "medium"),
            ("高度压缩 (CRF 36, 720p, 48kbps) - 明显损失，压缩率 97-99%", "small")
        ]

        for text, value in qualities:
            rb = tk.Radiobutton(quality_frame,
                              text=text,
                              variable=self.quality_var,
                              value=value,
                              font=('Microsoft YaHei UI', 9),
                              anchor='w',
                              justify='left')
            rb.pack(anchor='w', pady=3)

        # 自定义设置
        custom_frame = tk.LabelFrame(main_frame, text="自定义设置 (可选)",
                                    font=('Microsoft YaHei UI', 9), padx=10, pady=8)
        custom_frame.pack(fill='x', pady=(0, 10))

        # 说明文字
        tip_label = tk.Label(custom_frame,
                           text="提示：以下设置会覆盖上方预设。数值越小=质量越高=文件越大",
                           fg='#e67e22',
                           font=('Microsoft YaHei UI', 8),
                           wraplength=600)
        tip_label.pack(anchor='w', pady=(0, 5))

        # CRF
        crf_frame = tk.Frame(custom_frame)
        crf_frame.pack(fill='x', pady=5)
        crf_label = tk.Label(crf_frame, text="CRF 值 (18-36):", width=15, anchor='w', font=('Microsoft YaHei UI', 9))
        crf_label.pack(side='left')
        self.crf_var = tk.StringVar(value="")
        tk.Entry(crf_frame, textvariable=self.crf_var, width=10, font=('Microsoft YaHei UI', 9)).pack(side='left', padx=5)
        crf_help = tk.Label(crf_frame, text="视频质量 (18=极高, 28=高, 36=低)", fg='gray', font=('Microsoft YaHei UI', 8))
        crf_help.pack(side='left')

        # 宽度
        width_frame = tk.Frame(custom_frame)
        width_frame.pack(fill='x', pady=5)
        width_label = tk.Label(width_frame, text="目标宽度:", width=15, anchor='w', font=('Microsoft YaHei UI', 9))
        width_label.pack(side='left')
        self.width_var = tk.StringVar(value="")
        tk.Entry(width_frame, textvariable=self.width_var, width=10, font=('Microsoft YaHei UI', 9)).pack(side='left', padx=5)
        width_help = tk.Label(width_frame, text="分辨率 (1920=1080p, 1280=720p, 留空=保持)", fg='gray', font=('Microsoft YaHei UI', 8))
        width_help.pack(side='left')

        # 音频比特率
        audio_frame = tk.Frame(custom_frame)
        audio_frame.pack(fill='x', pady=5)
        audio_label = tk.Label(audio_frame, text="音频比特率:", width=15, anchor='w', font=('Microsoft YaHei UI', 9))
        audio_label.pack(side='left')
        self.audio_var = tk.StringVar(value="")
        tk.Entry(audio_frame, textvariable=self.audio_var, width=10, font=('Microsoft YaHei UI', 9)).pack(side='left', padx=5)
        audio_help = tk.Label(audio_frame, text="音质 (128k=高, 96k=中, 64k=低)", fg='gray', font=('Microsoft YaHei UI', 8))
        audio_help.pack(side='left')

        # 状态显示
        self.status_label = tk.Label(main_frame, text="", fg='#7f8c8d', font=('Microsoft YaHei UI', 9))
        self.status_label.pack(anchor='w', pady=(5, 10))

        # 按钮区域
        btn_container = tk.Frame(main_frame)
        btn_container.pack(fill='x', pady=(0, 10))

        self.compress_btn = tk.Button(btn_container,
                                     text="开始压缩",
                                     command=self.start_compression,
                                     bg='#27ae60', fg='white',
                                     font=('Microsoft YaHei UI', 11, 'bold'),
                                     cursor='hand2',
                                     padx=40, pady=12)
        self.compress_btn.pack(side='left', padx=(0, 10))

        self.cancel_btn = tk.Button(btn_container,
                                   text="取消",
                                   command=self.cancel_compression,
                                   bg='#e74c3c', fg='white',
                                   font=('Microsoft YaHei UI', 11),
                                   cursor='hand2',
                                   padx=40, pady=12,
                                   state='disabled')
        self.cancel_btn.pack(side='left')

        # 版本号（和按钮同一行，右对齐）
        version_label = tk.Label(btn_container, text="v1.0",
                               fg='#95a5a6',
                               font=('Microsoft YaHei UI', 8))
        version_label.pack(side='right', padx=(0, 10))

    def select_file(self):
        """选择视频文件"""
        filename = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[
                ("视频文件", "*.mp4 *.mkv *.avi *.mov *.flv *.wmv *.webm"),
                ("所有文件", "*.*")
            ]
        )

        if filename:
            self.input_file = filename
            self.file_label.config(text=filename, fg='black')

            # 获取文件大小
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            self.info_label.config(text=f"文件大小: {size_mb:.1f} MB")

    def select_output_dir(self):
        """选择输出目录"""
        dirname = filedialog.askdirectory(title="选择输出目录")

        if dirname:
            self.output_dir = dirname
            self.output_label.config(text=dirname, fg='black')

    def reset_output_dir(self):
        """重置输出目录为默认"""
        self.output_dir = self.get_downloads_folder()
        self.output_label.config(text=f"默认保存到: {self.output_dir}", fg='black')

    def get_compression_params(self):
        """获取压缩参数"""
        # 自定义优先
        crf = self.crf_var.get().strip()
        width = self.width_var.get().strip()
        audio = self.audio_var.get().strip()

        if crf or width or audio:
            # 使用自定义设置
            if not crf:
                crf = "28"
            if not audio:
                audio = "96k"

            scale = f"-vf scale={width}:-1" if width else ""
            suffix = "custom"
        else:
            # 使用预设
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
        """开始压缩"""
        if not self.input_file:
            messagebox.showwarning("警告", "请先选择视频文件！")
            return

        # 生成输出文件名
        dir_name = self.output_dir

        base_name = os.path.splitext(os.path.basename(self.input_file))[0]

        crf, scale, audio, suffix = self.get_compression_params()

        self.output_file = os.path.join(dir_name, f"{base_name}_compressed_{suffix}.mp4")

        # 确认开始
        result = messagebox.askyesno(
            "确认压缩",
            f"输入文件: {self.input_file}\n\n"
            f"输出文件: {self.output_file}\n\n"
            f"CRF: {crf}\n"
            f"音频: {audio}\n\n"
            f"开始压缩？"
        )

        if not result:
            return

        # 禁用按钮，显示加载动画
        self.compress_btn.config(text="压缩中...", state='disabled')
        self.cancel_btn['state'] = 'normal'
        self.is_compressing = True

        # 更新状态
        self.status_label.config(text="正在压缩，请稍候...", fg='#3498db')

        # 在新线程中执行压缩
        thread = threading.Thread(target=self.compress_video,
                                 args=(crf, scale, audio))
        thread.daemon = True
        thread.start()

    def compress_video(self, crf, scale, audio):
        """执行视频压缩"""
        try:
            # 构建 FFmpeg 命令
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

            # 执行压缩
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            self.current_process = process
            stdout, stderr = process.communicate()

            if not self.is_compressing:
                # 用户取消了
                return

            if process.returncode == 0:
                # 压缩成功
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
        """压缩完成"""
        self.status_label.config(text="压缩完成！", fg='#27ae60')

        self.compress_btn.config(text="开始压缩", state='normal')
        self.cancel_btn['state'] = 'disabled'
        self.is_compressing = False

        messagebox.showinfo(
            "压缩完成",
            f"压缩成功！\n\n"
            f"原始大小: {original_size:.1f} MB\n"
            f"压缩后: {compressed_size:.1f} MB\n"
            f"压缩率: {ratio:.1f}%\n\n"
            f"输出文件:\n{self.output_file}"
        )

    def compression_failed(self, error):
        """压缩失败"""
        self.status_label.config(text="压缩失败", fg='#e74c3c')

        self.compress_btn.config(text="开始压缩", state='normal')
        self.cancel_btn['state'] = 'disabled'
        self.is_compressing = False

        messagebox.showerror("压缩失败", f"压缩过程中出现错误:\n\n{error}")

    def cancel_compression(self):
        """取消压缩"""
        if hasattr(self, 'current_process'):
            self.current_process.terminate()
            self.is_compressing = False

            self.status_label.config(text="已取消", fg='#e74c3c')

            self.compress_btn.config(text="开始压缩", state='normal')
            self.cancel_btn['state'] = 'disabled'

            # 删除未完成的输出文件
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
