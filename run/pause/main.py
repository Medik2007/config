from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import subprocess
import json

app = Flask(__name__)

TRANSLATE_CORDS = [subprocess.check_output(['cat', 'cords0.txt'], text=True), subprocess.check_output(['cat', 'cords1.txt'], text=True)]
#TRANSLATE_CORDS = ["1729,752 1248x326", "1698,96 1050x337"]


def translate_screen(num):
    cords = TRANSLATE_CORDS[int(num)]
    subprocess.run(f'grim -g "{cords[:-1]}" img{num}.png', shell=True)
    subprocess.run(f'tesseract img{num}.png text{num} -l spa', shell=True)
    text = subprocess.check_output(['cat', f'text{num}.txt'], text=True)
    if text:
        return GoogleTranslator(source='auto', target='en').translate(subprocess.check_output(['cat', f'text{num}.txt'], text=True))
    return ''


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/pause', methods=['POST'])
def pause():
    if request.form['act'] == 'pause':
        subprocess.run('playerctl --all-players play-pause', shell=True)
        return json.dumps({'success':True})
    elif request.form['act'] == 'translate':
        subprocess.run('playerctl --all-players pause', shell=True)
        translation = translate_screen('0')
        if not translation:
            translation = translate_screen('1')
        print(translation)
        return json.dumps({'success':True, 'translation':translation})
    return json.dumps({'success':False})

if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.9')
