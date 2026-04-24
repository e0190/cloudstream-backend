from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q')
    # Filter for verified: YouTube search with "official" or "topic"
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # We add "official" to help yt-dlp find verified versions
        results = ydl.extract_info(f"ytsearch5:{query} official", download=False)['entries']
        
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)
