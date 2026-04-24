from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import requests
import base64

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q')
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{query} official music", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                
                # Convert thumbnail to Base64 so Google can't block the URL
                thumb_url = f"https://img.youtube.com/vi/{entry['id']}/mqdefault.jpg"
                try:
                    img_data = base64.b64encode(requests.get(thumb_url).content).decode('utf-8')
                    b64_thumb = f"data:image/jpeg;base64,{img_data}"
                except:
                    b64_thumb = ""

                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id'),
                    'thumbnail': b64_thumb,
                    'audio_url': entry.get('url')
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
