from flask import Flask, render_template
import subprocess
import json

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/pause', methods=['POST'])
def pause():
    subprocess.Popen(['wtype', ' '])
    return json.dumps({'success':True})


if __name__ == "__main__":
    app.run(host='192.168.1.6')
