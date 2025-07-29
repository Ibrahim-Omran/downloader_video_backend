
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'forcejson': True,
            'skip_download': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        return jsonify({
            'title': info.get('title', 'video'),
            'url': info.get('url'),
            'thumbnail': info.get('thumbnail'),
            'filesize': info.get('filesize_approx', 0),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
