from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import requests
import base64

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('q')
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch3:{query} official audio", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                
                # Convert Thumbnail to Base64
                thumb_url = f"https://img.youtube.com/vi/{entry['id']}/mqdefault.jpg"
                img_b64 = ""
                try:
                    img_b64 = "data:image/jpeg;base64," + base64.b64encode(requests.get(thumb_url).content).decode('utf-8')
                except: pass

                # Get Audio URL
                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'thumbnail': img_b64,
                    'id': entry.get('id')
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_audio/<vid_id>')
def get_audio(vid_id):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
            # Fetch the actual audio bytes and send as a Data URI
            audio_data = requests.get(info['url']).content
            b64_audio = "data:audio/mpeg;base64," + base64.b64encode(audio_data).decode('utf-8')
            return jsonify({"audio": b64_audio})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
