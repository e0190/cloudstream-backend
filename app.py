from flask import Flask, request, jsonify
import yt_dlp
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Ensures Google Apps Script can talk to it

@app.route('/search')
def search():
    query = request.args.get('q')
    # This configuration specifically hunts for audio-only streams
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False, # Set to False to get the real stream URL
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Add "official music" to the search to help with the "Verified" constraint
            search_query = f"ytsearch5:{query} official music"
            info = ydl.extract_info(search_query, download=False)
            results = []
            
            for entry in info['entries']:
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'uploader_verified': entry.get('uploader_id') and entry.get('channel_is_verified', False),
                    'thumbnail': entry.get('thumbnail'),
                    'audio_url': entry.get('url'), # This is the magic direct stream link
                    'channel_url': entry.get('channel_url'),
                    'duration': entry.get('duration')
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
