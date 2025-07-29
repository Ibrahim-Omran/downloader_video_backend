import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from yt_dlp import YoutubeDL

app = Flask(__name__)
CORS(app)

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def get_video_info_and_download(url, format_ext='mp4'):
    try:
        uid = str(uuid.uuid4())
        filename = f"{uid}.{format_ext}"
        output_path = os.path.join(DOWNLOADS_DIR, filename)

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': format_ext,
            'quiet': True,
            'noplaylist': True,
            'skip_download': False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            return {
                "title": info.get("title", "No title"),
                "url": f"{request.host_url}download/{filename}",
                "thumbnail": info.get("thumbnail", ""),
                "filesize": info.get("filesize") or info.get("filesize_approx") or 0
            }

    except Exception as e:
        print("Error:", e)
        return None

@app.route('/get_video_url', methods=['POST'])
def get_video():
    data = request.get_json()
    url = data.get("url")
    format_ext = data.get("format", "mp4")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = get_video_info_and_download(url, format_ext=format_ext)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to process video"}), 500

@app.route('/download/<filename>')
def serve_video(filename):
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
