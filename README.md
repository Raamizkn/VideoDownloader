# YouTube Video Downloader

A modern web-based YouTube video downloader with a beautiful user interface.

## Features

- Modern, responsive web interface
- Download YouTube videos in best quality
- Real-time download progress tracking
- Multiple simultaneous downloads
- Custom save path support
- YouTube-inspired red color scheme

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:8080
```

3. Enter a YouTube video URL and click "Download Video"

4. Watch the progress in real-time!

## How It Works

- The frontend is a modern HTML/CSS/JavaScript interface
- The backend uses Flask to handle API requests
- Downloads are processed using `yt-dlp` (youtube-dl fork)
- Videos are saved to the `downloads/` folder by default
- You can specify a custom save path if desired

## Project Structure

```
VideoDownloader/
├── app.py              # Flask backend server
├── youtube.py          # Original CLI script (preserved)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Frontend HTML
├── static/
│   ├── css/
│   │   └── style.css  # Frontend styles
│   └── js/
│       └── main.js    # Frontend JavaScript
└── downloads/         # Default download folder (created automatically)
```

## Deployment

### Deploy to Render (Recommended)

Render is perfect for this application as it supports long-running processes and persistent storage.

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add a persistent disk (optional but recommended):
   - Name: `downloads-disk`
   - Mount Path: `/opt/render/project/src/downloads`
   - Size: 1 GB

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed deployment instructions.

### Local Development

The original `youtube.py` script is preserved for CLI usage. For web interface:

```bash
python app.py
```

Then visit `http://localhost:8080`

## Notes

- The original `youtube.py` script is preserved for CLI usage
- The web interface uses the same download logic
- Downloads are processed asynchronously
- Progress is tracked in real-time via polling

## License

MIT

