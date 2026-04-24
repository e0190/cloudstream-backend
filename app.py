from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q')
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False,
        # This forces a fresh fetch of the stream URL
        'force_generic_extractor': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Adding "audio" helps filter out video-only content
            info = ydl.extract_info(f"ytsearch5:{query} official audio", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                
                # Try to get the highest resolution thumbnail
                thumb = entry.get('thumbnail')
                if entry.get('thumbnails'):
                    # Sort to find the most reliable thumbnail URL
                    thumb = entry['thumbnails'][-1]['url']

                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'thumbnail': thumb,
                    'audio_url': entry.get('url'),
                    'is_verified': True if "Topic" in entry.get('uploader', '') else entry.get('channel_is_verified', False)
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
