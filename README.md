# Video Compressor / 视频压缩工具 / ビデオ圧縮ツール

[English](#english) | [中文](#中文) | [日本語](#日本語)

---

## English

### Overview
A simple and efficient GUI application for video compression using FFmpeg and HEVC (H.265) encoding. This tool provides an easy-to-use interface for compressing videos with customizable quality settings.

### Features
- **User-friendly GUI** - Built with Python Tkinter
- **HEVC (H.265) Encoding** - Modern compression for smaller file sizes
- **Quality Presets** - Three built-in compression levels:
  - **High Quality**: CRF 28, 1080p, 96kbps audio (90-95% compression)
  - **Medium Quality**: CRF 32, 1080p, 64kbps audio (95-97% compression)
  - **Small Size**: CRF 36, 720p, 48kbps audio (97-99% compression)
- **Custom Settings** - Advanced options for CRF value, resolution, and audio bitrate
- **Real-time Progress** - Monitor compression status and statistics
- **Batch Processing Ready** - Process videos one at a time with detailed feedback

### System Requirements
- **Operating System**: Windows (tested on Windows 10/11)
- **Python**: 3.6 or higher
- **FFmpeg**: Must be installed and available in system PATH
- **Dependencies**: No external Python packages required (uses standard library only)

### Installation

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Install FFmpeg**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Add FFmpeg to your system PATH, or use a package manager:
     ```bash
     # Windows (with Chocolatey)
     choco install ffmpeg

     # Windows (with Scoop)
     scoop install ffmpeg
     ```

3. **Download this application**
   - **Option 1**: Download the pre-compiled executable from [Releases](https://github.com/kiririto/video-compressor/releases)
   - **Option 2**: Clone the repository and run from source:
     ```bash
     git clone https://github.com/kiririto/video-compressor.git
     cd video-compressor
     python video_compressor.py
     ```

### Usage

1. Launch the application (double-click the .exe or run the Python script)
2. Click "选择视频文件" (Select Video File) to choose your input video
3. (Optional) Click "选择输出目录" (Select Output Folder) to change the output location
4. Choose a quality preset or enter custom settings
5. Click "开始压缩" (Start Compression) to begin
6. Monitor the compression progress in the status area
7. When complete, find your compressed video in the output directory

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 中文

### 概述
一个简单高效的视频压缩 GUI 应用程序,使用 FFmpeg 和 HEVC (H.265) 编码。该工具提供易用的界面,支持自定义质量设置进行视频压缩。

### 功能特性
- **友好的图形界面** - 基于 Python Tkinter 构建
- **HEVC (H.265) 编码** - 现代压缩技术,文件更小
- **质量预设** - 三种内置压缩级别:
  - **高质量**: CRF 28, 1080p, 96kbps 音频 (压缩 90-95%)
  - **中等质量**: CRF 32, 1080p, 64kbps 音频 (压缩 95-97%)
  - **小体积**: CRF 36, 720p, 48kbps 音频 (压缩 97-99%)
- **自定义设置** - 高级选项可调整 CRF 值、分辨率和音频比特率
- **实时进度** - 监控压缩状态和统计信息
- **批处理支持** - 逐个处理视频,并提供详细反馈

### 系统要求
- **操作系统**: Windows (已在 Windows 10/11 上测试)
- **Python**: 3.6 或更高版本
- **FFmpeg**: 必须已安装并添加到系统 PATH
- **依赖项**: 无需额外的 Python 包(仅使用标准库)

### 安装说明

1. **安装 Python**
   - 从 [python.org](https://www.python.org/downloads/) 下载
   - 安装时务必勾选 "Add Python to PATH"

2. **安装 FFmpeg**
   - 从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载
   - 将 FFmpeg 添加到系统 PATH,或使用包管理器:
     ```bash
     # Windows (使用 Chocolatey)
     choco install ffmpeg

     # Windows (使用 Scoop)
     scoop install ffmpeg
     ```

3. **下载本应用**
   - **方式 1**: 从 [Releases](https://github.com/kiririto/video-compressor/releases) 下载预编译的可执行文件
   - **方式 2**: 克隆仓库并从源码运行:
     ```bash
     git clone https://github.com/kiririto/video-compressor.git
     cd video-compressor
     python video_compressor.py
     ```

### 使用方法

1. 启动应用程序(双击 .exe 或运行 Python 脚本)
2. 点击"选择视频文件"选择输入视频
3. (可选)点击"选择输出目录"更改输出位置
4. 选择质量预设或输入自定义设置
5. 点击"开始压缩"开始处理
6. 在状态区域监控压缩进度
7. 完成后,在输出目录中找到压缩后的视频

### 许可证
本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 日本語

### 概要
FFmpeg と HEVC (H.265) エンコーディングを使用したシンプルで効率的な動画圧縮 GUI アプリケーションです。カスタマイズ可能な品質設定で動画を圧縮できる使いやすいインターフェースを提供します。

### 機能
- **使いやすい GUI** - Python Tkinter で構築
- **HEVC (H.265) エンコーディング** - ファイルサイズを小さくする最新の圧縮技術
- **品質プリセット** - 3つの組み込み圧縮レベル:
  - **高品質**: CRF 28, 1080p, 96kbps オーディオ (90-95% 圧縮)
  - **中品質**: CRF 32, 1080p, 64kbps オーディオ (95-97% 圧縮)
  - **小サイズ**: CRF 36, 720p, 48kbps オーディオ (97-99% 圧縮)
- **カスタム設定** - CRF値、解像度、オーディオビットレートの詳細オプション
- **リアルタイム進捗** - 圧縮状況と統計情報を監視
- **バッチ処理対応** - 詳細なフィードバック付きで動画を1つずつ処理

### システム要件
- **OS**: Windows (Windows 10/11 でテスト済み)
- **Python**: 3.6 以上
- **FFmpeg**: システム PATH にインストール済みであること
- **依存関係**: 追加の Python パッケージ不要(標準ライブラリのみ使用)

### インストール

1. **Python のインストール**
   - [python.org](https://www.python.org/downloads/) からダウンロード
   - インストール時に「Add Python to PATH」を必ずチェック

2. **FFmpeg のインストール**
   - [ffmpeg.org](https://ffmpeg.org/download.html) からダウンロード
   - システム PATH に FFmpeg を追加するか、パッケージマネージャーを使用:
     ```bash
     # Windows (Chocolatey を使用)
     choco install ffmpeg

     # Windows (Scoop を使用)
     scoop install ffmpeg
     ```

3. **このアプリケーションをダウンロード**
   - **方法1**: [Releases](https://github.com/kiririto/video-compressor/releases) からコンパイル済み実行ファイルをダウンロード
   - **方法2**: リポジトリをクローンしてソースから実行:
     ```bash
     git clone https://github.com/kiririto/video-compressor.git
     cd video-compressor
     python video_compressor.py
     ```

### 使い方

1. アプリケーションを起動(.exe をダブルクリックまたは Python スクリプトを実行)
2. 「选择视频文件」(動画ファイルを選択)をクリックして入力動画を選択
3. (オプション)「选择输出目录」(出力フォルダを選択)をクリックして出力場所を変更
4. 品質プリセットを選択するか、カスタム設定を入力
5. 「开始压缩」(圧縮開始)をクリックして処理を開始
6. ステータスエリアで圧縮進捗を監視
7. 完了後、出力ディレクトリで圧縮された動画を確認

### ライセンス
このプロジェクトは MIT ライセンスの下で公開されています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

---

## Contributing / 贡献 / 貢献

Issues and pull requests are welcome! / 欢迎提交问题和拉取请求! / Issue と Pull Request を歓迎します!

## Author / 作者 / 作者

kiririto - [GitHub](https://github.com/kiririto)
