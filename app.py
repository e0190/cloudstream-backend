from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

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
            # We search for "topic" to get the high-quality official versions
            info = ydl.extract_info(f"ytsearch5:{query} official audio", download=False)
            results = []
            for entry in info.get('entries', []):
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id'),
                    # Direct thumbnail link that usually bypasses Google's filter
                    'thumbnail': f"https://i.ytimg.com/vi/{entry.get('id')}/hqdefault.jpg"
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stream/<vid_id>')
def stream(vid_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'force_generic_extractor': False
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
            # Redirecting is more stable than proxying for home use
            return redirect(info['url'])
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
