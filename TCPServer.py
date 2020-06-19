from absl import app, flags, logging
import socket

# import thread module
from _thread import *
import threading

from absl import logging

from random import randint

import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

print_lock = threading.Lock()

addr_rasp = []
images = []

addr_aff = []


def parse_message_received(data):
    return data.split(";")


def send_to(socketT, exist, data):
    if exist:
        socketT.send(data.encode('utf-8'))
    else:
        print("Category not recognize")


def message_received(data, c):
    message = parse_message_received(data)
    if len(message) > 1:
        if message[1] == "YOLO":  # Message from YOLO
            if message[0] != "0":
                logging.info('YOLO Client send image cat {}'.format(message[2]))
                id_img = str(randint(1, 1000))
                message_to_send = id_img + ";" + message[2] + ";" + message[3] + ";"
                add_image([id_img, message[2], message[3]])
                socket, exist = get_address(message[2])
                send_to(socket, exist, message_to_send)
            else:
                c.send(("OK;").encode('utf-8'))
        elif message[1] == "AFF":
            # Message to Display
            c.send(("OK;").encode('utf-8'))
            if message[0] == "0":
                logging.info("Display client has been added")
                add_aff_address(c)
        elif message[1] == "RASP":
            # Message from RASP
            c.send(("OK;").encode('utf-8'))
            if message[0] == "0":
                logging.info("Device : {} added".format(message[3]))
                add_rasp_address(message[3], c)
            else:
                image = get_image(message[0])
                image_to_send = image[0] + ";" + image[1] + ";" + message[2] + ";" + image[2] + ";"
                logging.info(
                    "DEVICE SEND : ID:{} , PRIMARY CAT : {} , SECONDARY CAT : {} ".format(image[0], image[1], message[2]))
                for socketT in addr_aff:
                    send_to(socketT, True, image_to_send)


def add_rasp_address(cat, socketT):
    rasp = [cat, socketT]
    addr_rasp.append(rasp)


def get_address(cat):
    for rasp_addr in addr_rasp:
        if cat in rasp_addr:
            return rasp_addr[1], True
    return "", False


def add_aff_address(socketT):
    addr_aff.append(socketT)


def add_image(data):
    images.append(data)


def get_image(id_img):
    data = []
    for image in images:
        if image[0] == id_img:
            data = image
    return data


# thread function
def threaded(c):
    while True:
        # data received from client
        try:
            data = c.recv(3000000)
            # reverse the given string from client
            message_received(data.decode('utf-8'), c)
            # send back reversed string to client

        except ConnectionAbortedError:
            c.close()
            logging.info("Connexion closed")
            break
        # connection closed
    c.close()


def main(_argv):
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    logging.info("Socket binded at {}:{}".format(host, port))

    # put the socket into listening mode
    s.listen(5)
    logging.info("Socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        # lock acquired by client
        # print_lock.acquire()
        logging.info("New connection, connected to {}:{}".format(addr[0], addr[1]))

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
