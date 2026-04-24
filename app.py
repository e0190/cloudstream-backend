from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import yt_dlp

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
                    'thumb': f"https://i.ytimg.com/vi/{entry['id']}/mqdefault.jpg"
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stream/<vid_id>')
def stream(vid_id):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
        return redirect(info['url'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
