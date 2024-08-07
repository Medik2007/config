from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/pause', methods=['POST'])
def pause():
    if request.form['action'] == 'pause':
        subprocess.Popen(['playerctl', '--all-players', 'pause-play'])
        return json.dumps({'success':True})
    elif request.form['action'] == 'translate':
        subprocess.Popen(['grim', '-g', '320,1 930x900', 'img.png'])
        subprocess.Popen(['tesseract', 'img.png', 'text', '-l', 'eng'])
        translation = GoogleTranslator(source='auto', target='ru').translate(subprocess.check_output(['cat', 'text.txt'], text=True))
        print(translation)
        return json.dumps({'success':False, 'translation':translation})
    return json.dumps({'success':False})


if __name__ == "__main__":
    app.run(host='192.168.1.6')
