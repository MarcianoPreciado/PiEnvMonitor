import time
import board
import busio
import adafruit_mcp9808
import adafruit_veml7700
import socket

configFile = open('NetConfig.txt','r')
settings = configFile.readlines()
HOST = settings[0][:-1]
PORT = int(settings[1])

i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp9808 = adafruit_mcp9808.MCP9808(i2c_bus)
veml7700 = adafruit_veml7700.VEML7700(i2c_bus)


while True:
    tempC = mcp9808.temperature
    tempF = tempC * 9 / 5 + 32
    light = veml7700.light
    lux = veml7700.lux
    dataString = '{0:d},{1:.2f},{2:.2f},{3:.2f},{4:.2f}'.format(int(time.time()), tempC, tempF, light,lux)

    dataStringBytes = dataString.encode("ascii")
    print(dataStringBytes)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(dataStringBytes)
        data = s.recv(1024) # TODO is this timeout reasonable
    # TODO something about this while loop
    time.sleep(5)
