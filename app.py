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
    # We use 'worstaudio' to keep the text string small enough for Google to handle
    ydl_opts = {'format': 'ba[ext=m4a]/worstaudio/best', 'quiet': True, 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch3:{query}", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                
                # Encode Image
                thumb_url = f"https://img.youtube.com/vi/{entry['id']}/mqdefault.jpg"
                img_b64 = base64.b64encode(requests.get(thumb_url).content).decode('utf-8')

                # Encode Audio (The Secret Sauce)
                audio_raw = requests.get(entry['url']).content
                audio_b64 = base64.b64encode(audio_raw).decode('utf-8')

                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'img': f"data:image/jpeg;base64,{img_b64}",
                    'audio': f"data:audio/mp4;base64,{audio_b64}"
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
