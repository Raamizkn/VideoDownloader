from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import yt_dlp
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

def downloadvid(url, save_path, download_id, format_type='video'):
    """Download video or audio with progress tracking"""
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    percent = (downloaded / total) * 100
                    active_downloads[download_id]['progress'] = round(percent, 1)
                elif '_percent_str' in d:
                    try:
                        p_str = d['_percent_str'].replace('%', '').strip()
                        active_downloads[download_id]['progress'] = float(p_str)
                    except:
                        pass
                if '_speed_str' in d:
                    active_downloads[download_id]['speed'] = d['_speed_str']
                if '_eta_str' in d:
                    active_downloads[download_id]['eta'] = d['_eta_str']
            elif d['status'] == 'finished':
                active_downloads[download_id]['progress'] = 100
                active_downloads[download_id]['status'] = 'completed'

        # Set format based on type
        if format_type == 'audio':
            # Prioritize m4a as it's more compatible than webm without conversion
            ydl_format = 'bestaudio[ext=m4a]/bestaudio/best'
        else:
            # Use 'best' instead of 'bestvideo+bestaudio' to avoid ffmpeg merging requirement
            ydl_format = 'best[ext=mp4]/best'

        # Define download options with speed and bot-bypass optimizations
        ydl_opts = {
            'format': ydl_format,
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'nocheckcertificate': True,
            'cachedir': False,
            'concurrent_fragment_downloads': 5,
            'buffersize': 1024 * 1024,
            # Stealth settings for Render
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            },
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            active_downloads[download_id]['title'] = info.get('title', 'Unknown')
            active_downloads[download_id]['filename'] = os.path.basename(filename)
            active_downloads[download_id]['status'] = 'completed'
            active_downloads[download_id]['progress'] = 100
            active_downloads[download_id]['format'] = format_type # Ensure format persists

    except Exception as e:
        active_downloads[download_id]['status'] = 'error'
        active_downloads[download_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format_type = data.get('format', 'video') # Default to video
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    download_id = str(uuid.uuid4())
    active_downloads[download_id] = {
        'status': 'downloading',
        'progress': 0,
        'url': url,
        'format': format_type,
        'title': 'Fetching info...',
        'filename': None,
        'error': None
    }
    
    thread = threading.Thread(target=downloadvid, args=(url, DOWNLOADS_DIR, download_id, format_type))
    thread.daemon = True
    thread.start()
    
    return jsonify({'download_id': download_id, 'status': 'started'})

@app.route('/api/status/<download_id>', methods=['GET'])
def get_status(download_id):
    if download_id not in active_downloads:
        return jsonify({'error': 'Download not found'}), 404
    return jsonify(active_downloads[download_id])

@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    return jsonify(active_downloads)

@app.route('/api/clear/<download_id>', methods=['POST'])
def clear_download(download_id):
    """Remove a download from the history"""
    if download_id in active_downloads:
        del active_downloads[download_id]
        return jsonify({'status': 'cleared'})
    return jsonify({'error': 'Not found'}), 404

@app.route('/download/<filename>')
def serve_video(filename):
    """Route to download the actual file to user's computer"""
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)


