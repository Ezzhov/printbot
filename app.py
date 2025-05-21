from flask import Flask, render_template, Response
import subprocess
import time

app = Flask(__name__)

# Пути к вашим скриптам
SCAN_SCRIPT_PATH = "/home/skan_rsd/scan.sh"
SCAN_ADF_SCRIPT_PATH = "/home/skan_rsd/skan_adf.sh"
SCAN94_SCRIPT_PATH = "/home/skan_rsd/skan94.sh"  # Новый путь

def run_script_and_stream_output(script_path):
    """Функция для запуска скрипта и отправки его вывода через SSE"""
    process = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            yield f"data: {output}\n\n"
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

@app.route('/scan94')  # Новый маршрут
def scan94():
    return Response(run_script_and_stream_output(SCAN94_SCRIPT_PATH), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
