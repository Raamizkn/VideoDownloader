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

def downloadvid(url, save_path, download_id):
    """Download video with progress tracking"""
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        def progress_hook(d):
            if d['status'] == 'downloading':
                # Handle fragment-based progress (common for YouTube)
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
                
                # If we have speed and ETA, we can add those too
                if '_speed_str' in d:
                    active_downloads[download_id]['speed'] = d['_speed_str']
                if '_eta_str' in d:
                    active_downloads[download_id]['eta'] = d['_eta_str']

            elif d['status'] == 'finished':
                active_downloads[download_id]['progress'] = 100
                active_downloads[download_id]['status'] = 'completed'

        # Define download options with speed optimizations
        ydl_opts = {
            # Use 'best' instead of 'bestvideo+bestaudio' to avoid ffmpeg merging requirement
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'nocheckcertificate': True,
            'cachedir': False,
            # Speed optimizations
            'concurrent_fragment_downloads': 5, # Reduced slightly for better stability without ffmpeg
            'buffersize': 1024 * 1024, # 1MB buffer
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
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
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    download_id = str(uuid.uuid4())
    active_downloads[download_id] = {
        'status': 'downloading',
        'progress': 0,
        'url': url,
        'title': 'Fetching info...',
        'filename': None,
        'error': None
    }
    
    thread = threading.Thread(target=downloadvid, args=(url, DOWNLOADS_DIR, download_id))
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


