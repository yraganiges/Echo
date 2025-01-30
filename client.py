import socket
import pyaudio
import threading

HOST = '127.0.0.1'  # Адрес сервера
PORT = 5000          # Порт сервера

# Инициализация PyAudio
p = pyaudio.PyAudio()

# Открытие потока для воспроизведения звука
def play_audio(stream):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        stream.write(data)
    stream.stop_stream()
    stream.close()

# Открытие потока для записи звука
def record_audio(stream):
    while True:
        data = stream.read(1024)
        conn.sendall(data)

# Настройка сокета
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    conn.connect((HOST, PORT))
    print("Подключено к серверу")

    # Открытие потока для записи и воспроизведения
    stream = p.open(format=pyaudio.paInt16,
                     channels=2,
                     rate=44100,
                     input=True,
                     output=True)

    # Запуск потоков
    threading.Thread(target=play_audio, args=(stream,)).start()
    record_audio(stream)
