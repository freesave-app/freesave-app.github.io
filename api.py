from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
# CORS সেটিংস যাতে ব্রাউজার ডাউনলোড ব্লক না করে
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    quality = request.args.get('quality', '720') # কোয়ালিটি হ্যান্ডেল করার জন্য
    
    if not video_url:
        return jsonify({"success": False, "error": "URL missing"}), 400

    # yt-dlp এর জন্য শক্তিশালী কনফিগারেশন
    ydl_opts = {
        # টিকটক স্লাইডশো এবং ফেসবুকের জন্য সেরা ফরম্যাট সিলেকশন
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'allowed_extractors': ['default', 'youtube', 'facebook', 'instagram', 'tiktok', 'threads', 'capcut'],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # সরাসরি ভিডিও ইউআরএল খুঁজে বের করা
            download_link = info.get('url')
            
            # যদি টিকটক স্লাইডশো হয়, তবে প্রথম ইমেজ বা ভিডিওটি নেবে
            if not download_link and 'entries' in info:
                download_link = info['entries'][0].get('url')
            
            title = info.get('title', 'Video_' + str(os.urandom(4).hex()))

        # রেসপন্স তৈরি করা
        result = {
            "success": True,
            "title": title,
            "url": download_link, # তোর সেভ পেজে 'url' হিসেবে ডাটা যায়
            "download_link": download_link
        }
        
        # ব্রাউজারকে ডাউনলোডের অনুমতি দেওয়ার জন্য স্পেশাল হেডার যোগ করা
        response = make_response(jsonify(result))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        
        return response

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Render বা পোর্টে চালানোর জন্য
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
