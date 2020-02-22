#!/usr/bin/env/python3

import socket

configFile = open('NetConfig.txt', 'r')
settings = configFile.readlines()
HOST = settings[0][:-1]
PORT = int(settings[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn: 
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                print(data)
