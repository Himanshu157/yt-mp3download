from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__)

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the audio download
@app.route('/download', methods=['POST'])
def download_audio():
    data = request.json
    video_url = data.get('videoUrl')
    
    if not video_url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400

    # Define the download path to the "Downloads" folder
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),  # Save to Downloads folder
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return jsonify({'success': True, 'message': 'Audio downloaded successfully to Downloads folder!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
