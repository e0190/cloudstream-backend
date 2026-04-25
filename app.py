from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
# Wide-open CORS is strictly required for the Google iframe to talk to Render
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def health():
    return jsonify({"status": "Render engine is awake!"}), 200

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify([])

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'nocheckcertificate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # "official audio" acts as a shield against age-restricted blocks
            info = ydl.extract_info(f"ytsearch5:{query} official audio", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id'),
                    'thumb': f"https://i.ytimg.com/vi/{entry['id']}/mqdefault.jpg",
                    'url': entry.get('url') # The raw stream link
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render assigns the port automatically
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
