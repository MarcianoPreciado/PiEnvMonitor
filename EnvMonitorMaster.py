#!/usr/bin/env/python3

import sys
import socket
import selectors 
import types

sel = selectors.DefaultSelector()

def logData(time, label, data):
    logString = '%11d'%time
    for item in data:
        logString = logString + ',{}'.format(item)
    print(logData)
    
    # Write to file for remote data from this source
    filename = label + '.csv'
    f = open(filename, a+)
    f.write(logString)
    f.close()
    # TODO log to net file that data was saved

def getCommas(string):
    indicies = []
    remaining = string
    i = 0
    while ',' in remaining:
        indicies[i] = remaining.index(',')
        remaining = remaining[indicies[i]+1:]
        i = i + 1
    return indicies

def parsePacket(data):
    msg = str(data.outb)
    inds = getCommas(msg)
    timestamp = msg[:inds[0]]
    label     = msg[inds[0]+1:inds[1]]
    tempC     = msg[inds[1]+1:inds[2]]
    tempF     = msg[inds[2]+1:inds[3]]
    ambient   = msg[inds[3]+1:inds[4]]
    lux       = msg[inds[4]+1:]
    
    data = (tempC,tempf,ambient,lux)
    logData(timestamp, label, data)

def accept_wrapper(sock):
    conn, addr = sock.accept()
    # TODO log to master net log
    # print('accepted connection from',addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'b', outb=b'b')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            # TODO log to master net log
            # print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            parsePacket(data)
            # print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


configFile = open('NetConfig.txt', 'r')
settings = configFile.readlines()
HOST = settings[0][:-1]
PORT = int(settings[1])

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST,PORT))
lsock.listen()
print('listening on', (HOST,PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt")
finally:
    sel.close()
