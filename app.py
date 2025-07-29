from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # إعداد yt-dlp
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
        'no_warnings': True,
        'format': 'best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        # تمكين التعامل مع Instagram
        'cookiesfrombrowser': ('chrome',),  # لازم تشيلها لو مش عندك كوكيز
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title"),
                "url": info.get("url"),
                "thumbnail": info.get("thumbnail"),
                "ext": info.get("ext"),
                "duration": info.get("duration")
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
