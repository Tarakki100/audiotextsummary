from flask import Flask, request, render_template
import requests
import os
import json


import assemblyai as aai


aai.settings.api_key = "cece6023f8f44cef8548adf06f6d2ff0"


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    # Check if the post request has the file part
    if 'audio_file' not in request.files:
        return 'No file part'
    
    audio_file = request.files['audio_file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if audio_file.filename == '':
        return 'No selected file'

    # Save the uploaded audio file
    if audio_file:
        filename = 'uploaded_audio.wav'  # Change the file extension based on the audio format

        audio_file.save(os.path.join('static/uploads', filename))
        # You can also transcribe a local file by passing in a file path
        FILE_URL = 'static/uploads/uploaded_audio.wav'

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(FILE_URL)

        if transcript.status == aai.TranscriptStatus.error:
            print(transcript.error)
        else:
            print(transcript.text)

        texts=transcript.text
        url = "https://api.edenai.run/v2/text/summarize"

        payload = {
            "response_as_dict": True,
            "attributes_as_list": False,
            "show_original_response": False,
            "output_sentences": 3,
            "providers": "openai",
            "text": texts,
            "language": "en"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjc1Zjc2YmQtYzc4Zi00MTNiLWFkMzQtYTA4NjM2ZmMyMDY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.66CaJTUHK3_yOo7gx71O03TmVVSlC4mo3_zgy4Uslvg"
        }

        response = requests.post(url, json=payload, headers=headers)
       
        response_json = json.loads(response.text)
        print(response_json["openai"]["result"])
        summary=response_json["openai"]["result"]
        output= summary
        
       
        return render_template('output.html', filename=output,originaltext= texts, filenames= filename)

if __name__ == '__main__':
    app.run(debug=True)
