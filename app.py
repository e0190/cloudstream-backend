from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q')
    # Using a faster search configuration
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist', 
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Search specifically for the "Topic" (Verified) version
            info = ydl.extract_info(f"ytsearch5:{query} official audio", download=False)
            results = []
            for entry in info.get('entries', []):
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id'),
                    # Use the high-res thumbnail direct link
                    'thumbnail': f"https://img.youtube.com/vi/{entry.get('id')}/mqdefault.jpg"
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stream/<vid_id>')
def stream(vid_id):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
            url = info['url']
        
        # This pipes the audio through Render so Google doesn't see YouTube
        req = requests.get(url, stream=True)
        return Response(req.iter_content(chunk_size=4096), content_type=req.headers['Content-Type'])
    except:
        return "Stream Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
