import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert')
def convert():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Strict "Verified Artist" Filter
            uploader = info.get('uploader', '')
            is_verified = "VEVO" in uploader or "Topic" in uploader
            
            if not is_verified:
                return jsonify({"error": "Only verified artists allowed"}), 403

            return jsonify({
                "title": info.get('title'),
                "artist": uploader.replace(" - Topic", ""),
                "cover": info.get('thumbnail'),
                "audio_url": info.get('url')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
