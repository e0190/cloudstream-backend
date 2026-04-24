from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # This tells the browser to allow Google to talk to Render

@app.route('/search')
def search():
    query = request.args.get('q')
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Adding "topic" usually forces high-quality verified album art
            info = ydl.extract_info(f"ytsearch5:{query} topic", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'thumbnail': entry.get('thumbnail'),
                    'audio_url': entry.get('url'),
                    'is_verified': entry.get('channel_is_verified', False)
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return "Online", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
