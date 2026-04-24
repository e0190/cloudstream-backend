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
    ydl_opts = {'format': 'worstaudio/best', 'quiet': True, 'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Limit to 2 results to prevent Google from cutting off the long text string
            info = ydl.extract_info(f"ytsearch2:{query} official audio", download=False)
            results = []
            for entry in info.get('entries', []):
                if not entry: continue
                
                # Inline Image
                thumb_url = f"https://img.youtube.com/vi/{entry['id']}/default.jpg"
                img_b64 = base64.b64encode(requests.get(thumb_url).content).decode('utf-8')

                results.append({
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'id': entry.get('id'),
                    'img_data': f"data:image/jpeg;base64,{img_b64}"
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_audio/<vid_id>')
def get_audio(vid_id):
    ydl_opts = {'format': 'wa[ext=m4a]/worstaudio/best', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
            # Fetch and convert to base64 inline string
            audio_raw = requests.get(info['url']).content
            audio_b64 = base64.b64encode(audio_raw).decode('utf-8')
            return jsonify({"audio_data": f"data:audio/mp4;base64,{audio_b64}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
