from flask import Flask, render_template, redirect, url_for, Response
import subprocess
import time

app = Flask(__name__)

# Путь к вашим скриптам
SCAN_SCRIPT_PATH = "/home/skan_rsd/scan.sh"
SCAN_ADF_SCRIPT_PATH = "/home/skan_rsd/skan_adf.sh"

def run_script_and_stream_output(script_path):
    """Функция для запуска скрипта и отправки его вывода через SSE"""
    process = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            yield f"data: {output.decode('utf-8')}\n\n"
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return Response(run_script_and_stream_output(SCAN_SCRIPT_PATH), content_type='text/event-stream')

@app.route('/scan_adf')
def scan_adf():
    return Response(run_script_and_stream_output(SCAN_ADF_SCRIPT_PATH), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
