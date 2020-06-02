# import socket programming library
import socket

# import thread module
from _thread import *
import threading

import re

print_lock = threading.Lock()

addr_rasp = []
images = []

addr_aff = []


def parse_message_received(data):
    return data.split(";")


def send_to(socketT, data):
    socketT.send(data.encode('utf-8'))


def message_received(data, c):
    message = parse_message_received(data)
    message.pop()
    if len(message) > 1:
        if message[1] == "YOLO":  # Message from YOLO
            print("YOLO send image ID :", message[0])
            message_to_send = message[0] + ";" + message[2] + ";" + message[3] + ";"
            add_image(message)
            send_to(get_address(message[2]), message_to_send)
        elif message[1] == "AFF":  # Message to Display
            if message[0] == "0":
                print("A display has been added")
                add_aff_address(c)
        elif message[1] == "RASP":  # Message from RASP
            if message[0] == "0":
                print("RASP : ", message[3], " added")
                add_rasp_address(message[3], c)
            else:
                image = get_image(message[0])
                image_to_send = image[0] + ";" + image[1] + ";" + message[1] + ";" + image[2] + ";"
                for socketT in addr_aff:
                    send_to(socketT, image_to_send)


def add_rasp_address(cat, socketT):
    rasp = [cat, socketT]
    addr_rasp.append(rasp)


def get_address(cat):
    for rasp_addr in addr_rasp:
        if cat in rasp_addr:
            return rasp_addr[1]


def add_aff_address(socketT):
    addr_aff.append(socketT)


def add_image(data):
    images.append(data)


def get_image(ID):
    data = []
    for image in images:
        if image[0] == ID:
            data = image
            images.remove(image)
    return data


# thread function
def threaded(c):
    while True:
        # data received from client
        data = c.recv(1024)
        # reverse the given string from client
        message_received(data.decode('utf-8'), c)
        # send back reversed string to client
        c.send(("ok").encode('utf-8'))
        # connection closed
    c.close()


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
