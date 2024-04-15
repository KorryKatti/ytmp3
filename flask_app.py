from flask import Flask, render_template, request, send_file
import yt_dlp as youtube_dl
import os

app = Flask(__name__)

def clear_directory(directory):
    """Clears all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Ensure that the 'lol' directory exists
if not os.path.exists('./lol'):
    os.makedirs('./lol')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form['youtube_url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': './lol/%(title)s.%(ext)s'  # Set the download directory to /lol
    }
    # Clear the 'lol' directory before downloading the next file
    clear_directory('./lol')
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            audio_path = ydl.prepare_filename(info)
            # Manually change the extension to mp3
            audio_path = os.path.splitext(audio_path)[0] + '.mp3'
            print("Audio file path:", audio_path)  # Print the audio file path for debugging
            if os.path.exists(audio_path):
                print("Audio file downloaded successfully:", audio_path)
                return send_file(audio_path, as_attachment=True)
            else:
                print("Error: Audio file not found at:", audio_path)
                return "Error: Audio file not found", 404
    except youtube_dl.utils.ExtractorError as e:
        print("ExtractorError:", e)
        return "Error: Unable to download audio from the provided URL", 500

@app.route('/arc-sw.js')
def serve_js():
    return send_file('arc-sw.js')

if __name__ == '__main__':
    app.run(debug=True, port=5678)
