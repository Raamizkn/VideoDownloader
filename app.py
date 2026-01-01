from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from yt_dlp import YoutubeDL
import threading
import uuid

app = Flask(__name__)
CORS(app)

# Store downloads directory
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), 'downloads')

# Ensure downloads directory exists
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

# Store active downloads
active_downloads = {}

def downloadvid(url, save_path, download_id):
    """Download video with progress tracking"""
    try:
        # Ensure the save directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Progress hook to track download
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d:
                    percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    active_downloads[download_id]['progress'] = round(percent, 2)
                elif '_percent_str' in d:
                    percent_str = d['_percent_str'].replace('%', '')
                    try:
                        active_downloads[download_id]['progress'] = float(percent_str)
                    except:
                        pass
            elif d['status'] == 'finished':
                active_downloads[download_id]['progress'] = 100
                active_downloads[download_id]['status'] = 'completed'
                if 'filename' in d:
                    active_downloads[download_id]['filename'] = os.path.basename(d['filename'])

        # Define download options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save file path
            'progress_hooks': [progress_hook],
        }

        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            active_downloads[download_id]['title'] = info.get('title', 'Unknown')
            active_downloads[download_id]['status'] = 'completed'
            active_downloads[download_id]['progress'] = 100

    except Exception as e:
        active_downloads[download_id]['status'] = 'error'
        active_downloads[download_id]['error'] = str(e)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    """Start a video download"""
    data = request.json
    url = data.get('url')
    custom_path = data.get('save_path', None)
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL
    if 'youtube.com' not in url and 'youtu.be' not in url:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    # Generate download ID
    download_id = str(uuid.uuid4())
    
    # Determine save path
    save_path = custom_path if custom_path else DOWNLOADS_DIR
    
    # Initialize download tracking
    active_downloads[download_id] = {
        'status': 'downloading',
        'progress': 0,
        'url': url,
        'title': 'Loading...',
        'filename': None,
        'error': None
    }
    
    # Start download in background thread
    thread = threading.Thread(target=downloadvid, args=(url, save_path, download_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'download_id': download_id,
        'status': 'started'
    })

@app.route('/api/status/<download_id>', methods=['GET'])
def get_status(download_id):
    """Get download status"""
    if download_id not in active_downloads:
        return jsonify({'error': 'Download not found'}), 404
    
    return jsonify(active_downloads[download_id])

@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    """List all active downloads"""
    return jsonify(active_downloads)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)

