from transcriber import Transcriber
from lebroniest import Lebroniest
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_lebroniest', methods=['POST'])
def get_lebroniest():
    transcriber = Transcriber()
    file = request.files['file']
    transcription = transcriber.transcribe(file)
    lebroniest = Lebroniest(transcription)
    result = lebroniest.calculate_lebroniest()
    return jsonify(result)
@app.route('/download', methods=['POST'])
def download():
    from ytmp3 import YTtoMP3
    ytmp3 = YTtoMP3()
    url = request.get_json()['url']
    output_file = ytmp3.download_youtube_mp3(url)
    return jsonify({'output_file': output_file})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
