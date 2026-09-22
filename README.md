# Douyin Translator

A Python-based tool that detects Chinese text in Douyin videos, translates it into Vietnamese using Google Gemini, and renders Vietnamese subtitles directly onto the video.

> **Current version:** `v1.0.0`
> **Status:** MVP

## ✨ Features

* 🔍 **Chinese OCR**

  * Detect Chinese text directly from video frames.
  * Track text regions across frames.
  * Filter low-quality and irrelevant OCR results.
  * Normalize and merge detected text regions.

* 🤖 **AI Translation**

  * Translate Chinese text into Vietnamese using Google Gemini.
  * Batch translation for better efficiency.
  * Translation cache to avoid translating the same text repeatedly.

* 🎬 **Subtitle Rendering**

  * Automatically cover the original Chinese text.
  * Render Vietnamese translations into the detected text regions.
  * Automatically wrap and resize text to fit the available area.
  * Preserve the original video's audio.

* 🛠️ **Pipeline**

  * Complete OCR → Translation → Subtitle → Rendering pipeline.
  * Re-render existing translation data without running OCR or translation again.
  * Windows `.bat` launcher for easier execution.

## 🧩 Pipeline

```text
Douyin Video
     │
     ▼
┌─────────────┐
│   PaddleOCR │
│ Chinese OCR │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Text Tracker│
│   Filter    │
│  Normalize  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Google      │
│ Gemini API  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Drawbox     │
│ Drawtext    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    FFmpeg   │
└──────┬──────┘
       │
       ▼
 Vietnamese
 Subtitled Video
```

## 📁 Project Structure

```text
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
├── input/
│
├── output/
│
└── test/
```

## ⚙️ Requirements

### Operating System

* Windows 10 / 11

### Python

* Python `3.11.x`

### Main Dependencies

* Python
* PaddleOCR
* PaddlePaddle
* Google Gemini API
* OpenCV
* Pillow
* FFmpeg
* python-dotenv

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/vietanh146/douyin-translator.git
cd douyin-translator
```

### 2. Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install FFmpeg

Download and install FFmpeg, then make sure the executable path matches the configuration in:

```text
config.py
```

The current configuration uses:

```text
D:\Tools\ffmpeg\bin\ffmpeg.exe
```

If FFmpeg is installed somewhere else, update `FFMPEG_PATH` in `config.py`.

## 🔑 Gemini API Key

The translation step requires a Google Gemini API key.

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is intentionally excluded from Git through `.gitignore`.

> Never commit your API key to GitHub.

## ▶️ Usage

### Using `run.bat`

The easiest way to run the application is:

```text
run.bat
```

The launcher provides the available processing options.

The main pipeline is:

```text
Video
  ↓
OCR
  ↓
Gemini Translation
  ↓
Subtitle Generation
  ↓
FFmpeg Rendering
  ↓
Translated Video
```

### Using Python directly

You can also run:

```powershell
python main.py
```

Then provide the path to the input video when prompted.

## 📂 Output

Each processed video gets its own project directory under `output/`.

Example:

```text
output/
└── cat01/
    ├── ocr.json
    ├── translated.json
    │
    ├── drawtext/
    │   ├── text_000.txt
    │   └── ...
    │
    ├── drawtext_render/
    │   ├── text_000.txt
    │   └── ...
    │
    ├── drawbox_filter.txt
    ├── drawtext_filter.txt
    │
    └── cat01_translated.mp4
```

### Intermediate files

The generated files are intentionally kept so that individual stages can be inspected or re-rendered without repeating the entire pipeline.

For example:

```text
ocr.json
```

contains detected text regions.

```text
translated.json
```

contains the Vietnamese translations.

```text
drawbox_filter.txt
```

contains the FFmpeg filter used to cover the original text.

```text
drawtext_filter.txt
```

contains the FFmpeg filter used to render the Vietnamese subtitles.

## 🔄 Re-render Existing Translation

If OCR and translation have already been completed, the existing translation can be rendered again without repeating those steps.

Example:

```powershell
python main.py path\to\video.mp4 --render
```

This is useful when adjusting subtitle rendering without consuming additional translation requests.

## 🧪 Testing

The project contains tests for individual components and pipeline stages.

Examples include:

```text
OCR
Video OCR
Text tracking
Text filtering
Text normalization
Translation
Translation cache
Subtitle rendering
Video pipeline
```

Run the relevant test scripts from the project root.

Example:

```powershell
python -m test.test_video_pipeline
```

## 📌 Current Limitations

This project is currently focused on **visual Chinese text translation**.

The following features are **not implemented yet**:

* ❌ Speech-to-text subtitles
* ❌ Audio translation
* ❌ Automatic voice dubbing
* ❌ Full GUI application
* ❌ Standalone `.exe` distribution
* ❌ Automatic Douyin downloading from URL

The `audio/` directory is reserved for future development and does not represent a currently implemented audio translation feature.

## 🗺️ Roadmap

### v1.0.0

* [x] Chinese OCR
* [x] Text tracking
* [x] OCR filtering
* [x] Text normalization
* [x] Gemini translation
* [x] Translation cache
* [x] Vietnamese subtitle rendering
* [x] Original text masking
* [x] FFmpeg rendering
* [x] End-to-end pipeline
* [x] Windows launcher

### Future

* [ ] GUI
* [ ] Subtitle customization
* [ ] Better OCR filtering
* [ ] Watermark detection/filtering
* [ ] Performance optimization
* [ ] Speech-to-text
* [ ] Audio translation
* [ ] Voice generation
* [ ] Standalone executable
* [ ] More input sources

## 🤝 Contributing

Contributions, ideas, bug reports, and improvements are welcome.

If you find a bug or have an idea for a new feature, feel free to open an issue.

## 📄 License

License information will be added in a future release.

## 👤 Author

**Viet Anh**

GitHub:

https://github.com/vietanh146

Project:

https://github.com/vietanh146/douyin-translator
