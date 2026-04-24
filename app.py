from flask import Flask, request, jsonify
import yt_dlp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query"}), 400

    # We use a more 'generic' extractor to avoid IP-locking some streams
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False,
        'skip_download': True,
        'allowed_extractors': ['youtube', 'youtube:search'],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Explicitly searching for the video to get fresh URLs
            search_query = f"ytsearch5:{query} official audio"
            info = ydl.extract_info(search_query, download=False)
            
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                
                # Get the best thumbnail
                thumb = entry.get('thumbnail')
                if entry.get('thumbnails'):
                    thumb = entry['thumbnails'][-1]['url']

                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'uploader_verified': entry.get('channel_is_verified', False) or "Topic" in entry.get('uploader', ""),
                    'thumbnail': thumb,
                    'audio_url': entry.get('url'),
                    'id': entry.get('id')
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
