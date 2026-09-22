# Douyin Translator

A Python-based tool that detects Chinese text in Douyin videos, translates it into Vietnamese using Google Gemini, and renders the translated subtitles directly onto the video.

> **Version:** `v1.0.0`  
> **Status:** MVP

## ✨ Features

- 🔍 Chinese text detection with PaddleOCR
- 🧠 Text tracking, filtering, normalization, and merging
- 🤖 Vietnamese translation using Google Gemini
- ⚡ Batch translation with translation cache
- 🎬 Automatic masking of original Chinese text
- 📝 Vietnamese subtitle rendering with automatic text wrapping and resizing
- 🔊 Preserves the original video's audio
- 🔄 Re-render subtitles without running OCR or translation again
- 🪟 Windows `.bat` launcher

## 🔄 Pipeline

```text
Douyin Video
     ↓
PaddleOCR
     ↓
Text Tracking / Filtering
     ↓
Gemini Translation
     ↓
Subtitle Generation
     ↓
Drawbox + Drawtext
     ↓
FFmpeg
     ↓
Vietnamese Subtitled Video

📁 Project Structure
douyin-translator/
│
├── main.py
├── config.py
├── requirements.txt
├── run.bat
│
├── core/
│   ├── video.py
│   ├── models.py
│   └── serializer.py
│
├── ocr/
│   ├── detector.py
│   ├── tracker.py
│   ├── filter.py
│   ├── normalizer.py
│   ├── merger.py
│   ├── timing.py
│   └── video_ocr.py
│
├── translator/
│   ├── translator.py
│   ├── mock_translator.py
│   ├── gemini_translator.py
│   └── cache.py
│
├── subtitle/
│   └── renderer.py
│
├── audio/
│   └── speech_to_text.py
│
└── test/

audio/ is reserved for future audio-related features and is not part of the current MVP.

⚙️ Requirements
Windows 10 / 11
Python 3.11.x
FFmpeg
Google Gemini API key

Python dependencies are listed in requirements.txt.

🚀 Installation
1. Clone the repository
git clone https://github.com/vietanh146/douyin-translator.git
cd douyin-translator
2. Create a virtual environment
py -3.11 -m venv .venv
.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure FFmpeg

Set the FFmpeg path in config.py:

FFMPEG_PATH = r"D:\Tools\ffmpeg\bin\ffmpeg.exe"

Change this path if FFmpeg is installed elsewhere.

🔑 Gemini API Key

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

▶️ Usage
Using run.bat

Run:

run.bat

The launcher starts the processing workflow.

Using Python directly
python main.py

Then enter the path to the video when prompted.

You can also provide the video path directly:

python main.py path\to\video.mp4
📂 Output

Each video gets its own directory under output/.

Example:

output/
└── cat01/
    ├── ocr.json
    ├── translated.json
    ├── drawtext/
    │   ├── text_000.txt
    │   ├── text_001.txt
    │   └── ...
    ├── drawtext_render/
    ├── drawbox_filter.txt
    ├── drawtext_filter.txt
    └── cat01_translated.mp4

The output/ directory is generated automatically and is not included in the repository.

✏️ Manual Subtitle Editing

One useful feature of the project is the ability to manually correct subtitles before rendering.

After translation, Vietnamese subtitle text is stored in:

output/<video_name>/drawtext/

For example:

output/
└── cat01/
    └── drawtext/
        ├── text_000.txt
        ├── text_001.txt
        └── text_002.txt

You can open and edit these files directly.

For example:

Original:
Tôi đã ăn rất no rồi

Edited:
Tôi no rồi :v

After editing, render the video again:

python main.py path\to\video.mp4 --render

This does not run OCR or Gemini translation again.

drawtext/
     ↓
DrawTextRenderer
     ↓
drawtext_render/
     ↓
FFmpeg
     ↓
Translated Video

Important: Edit files inside drawtext/.
Do not manually edit drawtext_render/, because those files are generated again during rendering.

This allows subtitle corrections without consuming additional Gemini translation requests.

🧪 Testing

The project contains tests for the main components and processing pipeline.

Example:

python -m test.test_video_pipeline

Other tests cover:

OCR
Video OCR
Text tracking
Text filtering
Text normalization
Translation
Translation cache
Subtitle rendering
📌 Current Limitations

The current MVP focuses on visual Chinese text translation.

Not implemented yet:

❌ Speech-to-text
❌ Audio translation
❌ Automatic voice dubbing
❌ GUI
❌ Standalone .exe
❌ Automatic Douyin URL downloading
🗺️ Future Development

Possible future improvements:

 GUI
 Better OCR filtering
 Watermark detection
 Subtitle customization
 Performance optimization
 Speech-to-text
 Audio translation
 Voice generation
 Standalone executable
👤 Author

Viet Anh

GitHub: vietanh146

Project: douyin-translator
