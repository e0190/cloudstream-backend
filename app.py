from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
# Rigid CORS setup to allow Google Apps Script specifically
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/search')
def search():
    query = request.args.get('q')
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We search for official audio to keep it verified
            info = ydl.extract_info(f"ytsearch5:{query} official audio", download=False)
            results = []
            for entry in info.get('entries', []):
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id')
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/thumb/<vid_id>')
def thumb(vid_id):
    # Proxy the image so the browser doesn't block i.ytimg.com
    url = f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg"
    r = requests.get(url)
    return Response(r.content, content_type="image/jpeg")

@app.route('/stream/<vid_id>')
def stream(vid_id):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
            audio_url = info['url']
        
        # Pipe the audio data directly
        def generate():
            with requests.get(audio_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=8192):
                    yield chunk
        return Response(generate(), content_type="audio/mpeg")
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
