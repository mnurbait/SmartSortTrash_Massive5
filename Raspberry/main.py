import RPi.GPIO as GPIO
import time
import requests
from telegram.ext import Updater, CommandHandler

# PIN Raspberry Pi
relay_pin = 3
ldr_pin = 4
GPIO_TRIGGER = 24
GPIO_ECHO = 18
GPIO_TRIGGER1 = 5
GPIO_ECHO1 = 6
GPIO_TRIGGER2 = 23
GPIO_ECHO2 = 25
GPIO_TRIGGER3 = 20
GPIO_ECHO3 = 21

# Inisialisasi PIN Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(ldr_pin, GPIO.IN)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)

# Konfigurasi Telegram dan Ubidots
TOKEN = "BBFF-b32P69OKzT4ga5tFQR7JXnZ0Az8K5E"
DEVICE_LABEL = "massive5"
VARIABLE_LABEL_1 = "sensor1"
VARIABLE_LABEL_2 = "sensor2"
VARIABLE_LABEL_3 = "sensor3"
VARIABLE_LABEL_4 = "sensor4"

# Fungsi untuk mengirimkan notifikasi ke bot Telegram
def send_notification_to_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"text": message, "chat_id": chat_id}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Notification sent to Telegram successfully.")
        else:
            print("Failed to send notification to Telegram. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending notification to Telegram:", str(e))

# Fungsi untuk volume tempat sampah menggunakan ultrasonik
def distance(trigger_pin, echo_pin):
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(echo_pin) == 0:
        StartTime = time.time()

    while GPIO.input(echo_pin) == 1:
        StopTime = time.time()

#perhitungan kapasitas
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    distance = (1 - distance / 50) * 100

    return distance

# Fungsi untuk mengirim data ke Ubidots
def send_data_to_ubidots(variable_label, value):
    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{variable_label}/values"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    payload = {"value": value}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            print("Data sent to Ubidots successfully.")
        else:
            print("Failed to send data to Ubidots. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending data to Ubidots:", str(e))

if __name__ == '__main__':
    try:
        while True:
            ldr_value = GPIO.input(ldr_pin)
            if ldr_value == GPIO.LOW:
                GPIO.output(relay_pin, GPIO.HIGH)
                print("Relay ON")
            else:
                GPIO.output(relay_pin, GPIO.LOW)
                print("Relay OFF")

            dist1 = distance(GPIO_TRIGGER, GPIO_ECHO)
            print("Kapasitas Terukur 1 = %.1f " % dist1)
            send_data_to_ubidots(VARIABLE_LABEL_1, dist1)

            dist2 = distance(GPIO_TRIGGER1, GPIO_ECHO1)
            print("Kapasitas Terukur 2 = %.1f " % dist2)
            send_data_to_ubidots(VARIABLE_LABEL_2, dist2)

            dist3 = distance(GPIO_TRIGGER2, GPIO_ECHO2)
            print("Kapasitas Terukur 3 = %.1f " % dist3)
            send_data_to_ubidots(VARIABLE_LABEL_3, dist3)

            dist4 = distance(GPIO_TRIGGER3, GPIO_ECHO3)
            print("Kapasitas Terukur 4 = %.1f " % dist4)
            send_data_to_ubidots(VARIABLE_LABEL_4, dist4)

            if dist1 >= 90:
                message = "Sampah organik terisi penuhi! Berkut adalah lokasi tempat sampah : Link Gmaps"
                send_notification_to_telegram(message, "Your_Telegram_Bot_Token", "Your_Chat_ID")

            if dist2 >= 90:
                message = "Sampah plastik terisi penuh! Berkut adalah lokasi tempat sampah : Link Gmaps"
                send_notification_to_telegram(message, "Your_Telegram_Bot_Token", "Your_Chat_ID")

            if dist3 >= 90:
                message = "Sampah logam terisi penuh! Berkut adalah lokasi tempat sampah : Link Gmaps"
                send_notification_to_telegram(message, "Your_Telegram_Bot_Token", "Your_Chat_ID")

            if dist4 >= 90:
                message = "Sampah B3 terisi penuh! Berkut adalah lokasi tempat sampah : Link Gmaps"
                send_notification_to_telegram(message, "Your_Telegram_Bot_Token", "Your_Chat_ID")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
