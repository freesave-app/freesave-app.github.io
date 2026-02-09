import yt_dlp, os
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url: return "URL missing", 400
    
    clean_url = video_url.split('?')[0]
    output_file = 'video.mp4'
    if os.path.exists(output_file): os.remove(output_file)
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_file,
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([clean_url])
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 
