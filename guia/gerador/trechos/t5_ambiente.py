import time
import board
import adafruit_dht

dht = adafruit_dht.DHT11(board.D22)    # GPIO22

while True:
    try:
        print(f"{dht.temperature} °C | {dht.humidity} %")
    except RuntimeError as erro:        # falhar de vez em quando é normal
        print("tentando de novo:", erro.args[0])
    time.sleep(2)
