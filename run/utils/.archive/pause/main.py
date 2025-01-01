from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import subprocess
import json

app = Flask(__name__)

TRANSLATE_CORDS = [subprocess.check_output(['cat', 'tmp/cords0.txt'], text=True), subprocess.check_output(['cat', 'tmp/cords1.txt'], text=True)]


def translate_screen(num):
    cords = TRANSLATE_CORDS[int(num)]
    subprocess.run(f'grim -g "{cords[:-1]}" tmp/img{num}.png', shell=True)
    subprocess.run(f'tesseract tmp/img{num}.png tmp/text{num} -l spa', shell=True)
    text = subprocess.check_output(['cat', f'tmp/text{num}.txt'], text=True)
    if text:
        return GoogleTranslator(source='auto', target='en').translate(subprocess.check_output(['cat', f'tmp/text{num}.txt'], text=True))
    return ''

def playerctl(player, act):
    subprocess.run(f'playerctl --player={player} {act}', shell=True)
    return json.dumps({'success':True})


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/pause', methods=['POST'])
def pause():
    if   request.form['act'] == 'browser-pause': return playerctl('firefox', 'pause')
    elif request.form['act'] == 'browser-play':  return playerctl('firefox', 'play')
    elif request.form['act'] == 'spotify-pause': return playerctl('spotify', 'pause')
    elif request.form['act'] == 'spotify-play':  return playerctl('spotify', 'play')
    elif request.form['act'] == 'poweroff': subprocess.run('poweroff', shell=True)
    elif request.form['act'] == 'reboot': subprocess.run('reboot', shell=True)
    elif request.form['act'] == 'sleep': subprocess.run('systemctl suspend', shell=True)
    return json.dumps({'success':False})

if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.6')






#elif request.form['act'] == 'translate':
#    subprocess.run('playerctl --all-players pause', shell=True)
#    translation = ''
#    translation += translate_screen('0')
#    translation += translate_screen('1')
#    if not translation: translation = 'Error: No translation'
#    return json.dumps({'success':True, 'translation':translation})
