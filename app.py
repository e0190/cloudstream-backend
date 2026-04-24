from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests
import io

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q')
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{query} official music", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id'),
                    'is_verified': entry.get('channel_is_verified', False)
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PROXY ROUTE FOR IMAGES
@app.route('/proxy_thumb/<vid_id>')
def proxy_thumb(vid_id):
    url = f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
    resp = requests.get(url)
    return Response(resp.content, content_type=resp.headers['Content-Type'])

# PROXY ROUTE FOR AUDIO
@app.route('/proxy_audio/<vid_id>')
def proxy_audio(vid_id):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
        url = info['url']
    
    # Streams the audio data through Render to bypass blocks
    req = requests.get(url, stream=True)
    return Response(req.iter_content(chunk_size=1024), content_type=req.headers['Content-Type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
