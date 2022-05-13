import json
import sys
import random
import time
import serial.tools.list_ports
import requests

from Adafruit_IO import *

AIO_FEED_ID = ["led","humid","temp","buzzer","gas",]	# Adafruit IO feed Id
AIO_USERNAME = "HoangDat3430"	# Adafruit IO username
AIO_KEY = "aio_cisL76s2koJLxpV3ZWi0wAfBZ77P"	# Adafruit IO api key


def connected(client):
    print("Successfully connected...")
    for i in AIO_FEED_ID:
        client.subscribe(i)


def subscribe(client , userdata , mid , granted_qos):
    print("Successfully subscribed...")


def disconnected(client):
    print("Disconnected...")
    sys.exit (1)


def message(client , feed_id , payload):
    print("Sent: "  + payload)
    json_payload = json.loads(payload)
    ser.write((str(json_payload["data"]) + "#").encode())


client = MQTTClient(AIO_USERNAME,AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


# Accessing to micro:bit's serial device
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len (ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort :
            splitPort = strPort.split (" ")
            commPort = (splitPort[0])
    return commPort


ser = serial.Serial(port = "COM6", baudrate = 115200)

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")

    splitData = data.split(":")
    if splitData[0] == "TEMP":
        json = '"name":"{}","data":"{}"'.format("Test temp", splitData[1])
        json = '{' + json + '}'
        client.publish("temp", json)
    elif splitData[0] == "HUMID":
        json = '"name":"{}","data":"{}"'.format("Test humid", splitData[1])
        json = '{' + json + '}'
        client.publish("humid", json)
    elif splitData[0] == "GAS":
        json = '"name":"{}","data":"{}"'.format("Test gas", splitData[1])
        json = '{' + json + '}'
        client.publish("gas", json)

mess = ""

def readSerial():
    bytesToRead = ser.inWaiting()
    if(bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while("#" in mess) and ("!" in mess):
            start = mess.find ("!")
            end = mess.find ("#")
            processData(mess[start:end + 1])
            if(end == len(mess)):
                mess = ""
            else:
                mess = mess[end + 1:]


while True:
    readSerial()
    time.sleep(5)

    # apikey = 'd3bcd430a04cb83bc5bd73e385a9030f'
    # cityname = 'ho chi minh'

    # Fetch Current weather api
    # url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cityname + '&appid=' + apikey
    # response = requests.get(url)
    #
    # tempval = str(round(response.json()["main"]["temp"] - 273.15, 2))
    # humidval = response.json()["main"]["humidity"]
    # pressval = response.json()["main"]["pressure"]
    # visibilityval = str(round(response.json()["visibility"] / 1000, 2))
    # windval = response.json()["wind"]["speed"]

    # Fetch Weather forecast api
    # url1 = 'https://api.openweathermap.org/data/2.5/air_pollution?lat=' + str(response.json()["coord"]["lat"]) + '&lon=' + str(response.json()["coord"]["lon"]) + '&appid=' + apikey
    # response1 = requests.get(url1)
    #
    # airval = response1.json()["list"][0]["main"]["aqi"]

    # Publish data to Dashboard
    # client.publish("mdp-temp", tempval)
    # client.publish("mdp-humid", humidval)
    # client.publish("mdp-press", pressval)
    # client.publish("mdp-visible", visibilityval)
    # client.publish("mdp-wind", windval)
    # client.publish("mdp-air", airval)

