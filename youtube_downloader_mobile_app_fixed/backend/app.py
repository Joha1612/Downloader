from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        for fmt in info.get("formats", []):
            if fmt.get("filesize") and fmt.get("ext") in ["mp4", "webm", "m4a", "mp3"]:
                formats.append({
                    "format_id": fmt["format_id"],
                    "ext": fmt["ext"],
                    "resolution": fmt.get("resolution") or f"{fmt.get('width', '')}x{fmt.get('height', '')}",
                    "filesize": round(fmt["filesize"] / (1024 * 1024), 2),
                    "url": fmt["url"],
                    "acodec": fmt.get("acodec", ""),
                    "vcodec": fmt.get("vcodec", "")
                })
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        }

@app.route('/')
def index():
    return "✅ YouTube API is Running!"

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.form.get("url")
    try:
        info = get_video_info(url)
        return jsonify({"success": True, "info": info})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
