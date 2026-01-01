const API_BASE = '';

let activeDownloads = new Map();

// DOM elements
const videoUrlInput = document.getElementById('video-url');
const savePathInput = document.getElementById('save-path');
const downloadBtn = document.getElementById('download-btn');
const statusMessage = document.getElementById('status-message');
const downloadsSection = document.getElementById('downloads-section');
const downloadsList = document.getElementById('downloads-list');

// Show status message
function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
    
    if (type === 'success' || type === 'error') {
        setTimeout(() => {
            statusMessage.style.display = 'none';
        }, 5000);
    }
}

// Validate YouTube URL
function isValidYouTubeUrl(url) {
    const patterns = [
        /^https?:\/\/(www\.)?(youtube\.com|youtu\.be)\/.+/,
        /^https?:\/\/youtube\.com\/watch\?v=[\w-]+/,
        /^https?:\/\/youtu\.be\/[\w-]+/
    ];
    return patterns.some(pattern => pattern.test(url));
}

// Start download
async function startDownload() {
    const url = videoUrlInput.value.trim();
    const savePath = savePathInput.value.trim() || null;
    const format = document.querySelector('input[name="format"]:checked').value;

    // Validate URL
    if (!url) {
        showStatus('Please enter a YouTube URL', 'error');
        return;
    }

    if (!isValidYouTubeUrl(url)) {
        showStatus('Please enter a valid YouTube URL', 'error');
        return;
    }

    // Disable button and show loading
    downloadBtn.disabled = true;
    downloadBtn.querySelector('.btn-text').style.display = 'none';
    downloadBtn.querySelector('.btn-loader').style.display = 'inline-block';
    showStatus('Starting download...', 'info');

    try {
        const response = await fetch(`${API_BASE}/api/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                save_path: savePath,
                format: format
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to start download');
        }

        // Add to active downloads
        activeDownloads.set(data.download_id, {
            id: data.download_id,
            url: url,
            status: 'downloading',
            progress: 0,
            title: 'Loading...',
            format: format
        });

        // Start polling for status
        pollDownloadStatus(data.download_id);

        // Show downloads section
        downloadsSection.style.display = 'block';
        updateDownloadsList();

        showStatus('Download started!', 'success');
        videoUrlInput.value = '';
        savePathInput.value = '';

    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        // Re-enable button
        downloadBtn.disabled = false;
        downloadBtn.querySelector('.btn-text').style.display = 'inline';
        downloadBtn.querySelector('.btn-loader').style.display = 'none';
    }
}

// Poll download status
async function pollDownloadStatus(downloadId) {
    const maxAttempts = 300; // 5 minutes max
    let attempts = 0;

    const poll = async () => {
        if (attempts >= maxAttempts) {
            activeDownloads.delete(downloadId);
            updateDownloadsList();
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/api/status/${downloadId}`);
            const data = await response.json();

            if (response.ok) {
                const currentFormat = activeDownloads.get(downloadId)?.format;
                activeDownloads.set(downloadId, {
                    id: downloadId,
                    url: data.url,
                    status: data.status,
                    progress: data.progress || 0,
                    title: data.title || 'Unknown',
                    filename: data.filename,
                    error: data.error,
                    format: data.format || currentFormat
                });

                updateDownloadsList();

                // Continue polling if still downloading
                if (data.status === 'downloading') {
                    attempts++;
                    setTimeout(poll, 1000); // Poll every second
                } else if (data.status === 'completed') {
                    showStatus(`Download completed: ${data.title}`, 'success');
                } else if (data.status === 'error') {
                    showStatus(`Download failed: ${data.error}`, 'error');
                }
            } else {
                // Download not found, remove it
                activeDownloads.delete(downloadId);
                updateDownloadsList();
            }
        } catch (error) {
            console.error('Error polling status:', error);
            attempts++;
            if (attempts < maxAttempts) {
                setTimeout(poll, 2000);
            }
        }
    };

    poll();
}

// Update downloads list UI
function updateDownloadsList() {
    if (activeDownloads.size === 0) {
        downloadsSection.style.display = 'none';
        return;
    }

    downloadsList.innerHTML = '';

    activeDownloads.forEach((download) => {
        const item = document.createElement('div');
        item.className = `download-item ${download.status}`;
        
        const statusClass = download.status === 'completed' ? 'completed' : 
                           download.status === 'error' ? 'error' : 'downloading';

        item.innerHTML = `
            <div class="download-header">
                <div class="download-title">
                    <span class="format-badge ${download.format || 'video'}">${download.format === 'audio' ? 'AUDIO' : 'VIDEO'}</span>
                    ${escapeHtml(download.title)}
                </div>
                <button class="btn-remove" onclick="removeDownload('${download.id}')">✕</button>
            </div>
            <div class="download-url">${escapeHtml(download.url)}</div>
            ${download.status === 'downloading' ? `
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${download.progress}%"></div>
                    </div>
                    <div class="progress-stats">
                        <span class="progress-text">${download.progress.toFixed(1)}%</span>
                        ${download.speed ? `<span class="download-speed">${download.speed}</span>` : ''}
                        ${download.eta ? `<span class="download-eta">ETA: ${download.eta}</span>` : ''}
                    </div>
                </div>
            ` : ''}
            <div class="download-status ${statusClass}">
                Status: ${download.status.charAt(0).toUpperCase() + download.status.slice(1)}
            </div>
            ${download.status === 'completed' && download.filename ? `
                <div class="download-actions">
                    <a href="/download/${encodeURIComponent(download.filename)}" class="btn-download-file" download>
                        Download to Computer
                    </a>
                </div>
            ` : ''}
            ${download.error ? `
                <div class="download-status error">Error: ${escapeHtml(download.error)}</div>
            ` : ''}
        `;

        downloadsList.appendChild(item);
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Remove a download from history
async function removeDownload(downloadId) {
    try {
        await fetch(`${API_BASE}/api/clear/${downloadId}`, { method: 'POST' });
        activeDownloads.delete(downloadId);
        updateDownloadsList();
    } catch (error) {
        console.error('Error removing download:', error);
    }
}

// Event listeners
downloadBtn.addEventListener('click', startDownload);

// Change button text based on format selection
document.querySelectorAll('input[name="format"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        const btnText = downloadBtn.querySelector('.btn-text');
        if (e.target.value === 'audio') {
            btnText.textContent = 'Download Audio';
        } else {
            btnText.textContent = 'Download Video';
        }
    });
});

videoUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        startDownload();
    }
});

savePathInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        startDownload();
    }
});

// Load existing downloads on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE}/api/downloads`);
        const data = await response.json();
        
        if (response.ok && Object.keys(data).length > 0) {
            Object.entries(data).forEach(([id, download]) => {
                activeDownloads.set(id, {
                    id: id,
                    url: download.url,
                    status: download.status,
                    progress: download.progress || 0,
                    title: download.title || 'Unknown',
                    filename: download.filename,
                    error: download.error,
                    format: download.format || (download.filename && (download.filename.endsWith('.m4a') || download.filename.endsWith('.webm')) ? 'audio' : 'video')
                });
                
                if (download.status === 'downloading') {
                    pollDownloadStatus(id);
                }
            });
            
            if (activeDownloads.size > 0) {
                downloadsSection.style.display = 'block';
                updateDownloadsList();
            }
        }
    } catch (error) {
        console.error('Error loading downloads:', error);
    }
});

