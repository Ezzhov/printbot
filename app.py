from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

# Путь к вашему скрипту
SCAN_SCRIPT_PATH = "/home/skan_rsd/scan.sh"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    try:
        # Запускаем скрипт для сканирования
        subprocess.run([SCAN_SCRIPT_PATH], check=True)
        return render_template('index.html', message="Сканирование завершено успешно!")
    except subprocess.CalledProcessError:
        return render_template('index.html', message="Ошибка при сканировании.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
