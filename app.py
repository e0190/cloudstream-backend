from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# Rigid CORS to allow Google's unique 'null' origin
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/search')
def search():
    query = request.args.get('q')
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id'),
                    'thumb': f"https://img.youtube.com/vi/{entry['id']}/mqdefault.jpg",
                    'url': entry.get('url')
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
