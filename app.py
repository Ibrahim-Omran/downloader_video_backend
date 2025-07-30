from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import traceback

app = Flask(__name__)
CORS(app)

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'cookiefile': 'cookies.txt',  # لو عندك ملف كوكيز
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'format': 'bestvideo+bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            video_formats = [
                {
                    'format_id': f.get('format_id'),
                    'ext': f.get('ext'),
                    'quality': f.get('format_note'),
                    'url': f.get('url'),
                    'filesize': f.get('filesize'),
                    'resolution': f"{f.get('width')}x{f.get('height')}" if f.get('width') else None,
                }
                for f in formats if f.get('vcodec') != 'none'
            ]
            return {
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': video_formats,
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'source': info.get('webpage_url'),
            }
        except Exception as e:
            print(traceback.format_exc())
            return {'error': str(e)}

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    info = get_video_info(url)

    if 'error' in info:
        return jsonify({'error': info['error']}), 500

    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
