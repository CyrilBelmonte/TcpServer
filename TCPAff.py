# Import socket module
import socket
import sys
import numpy as np
import time
import threading
import cv2

from absl import app, flags, logging
from absl.flags import FLAGS

flags.DEFINE_string('ip', '127.0.0.1', 'default ip')
flags.DEFINE_integer('port', 12346, 'default port')

np.set_printoptions(threshold=sys.maxsize)

info = []


def print_img(id_img, cat, label):
    logging.info("\t ID: {},PRIMARY DETECTION: {}, SECONDARY DETECTION: {}".format(id_img, cat, label))


def parse_message_received(data):
    parse = data.split(";")
    return parse


def get_img(data):
    tmp_data = data.split(" ")
    print(tmp_data[1:-1])
    return


def main(_argv):
    logging.info('connexion to the server')
    logging.info('Initialization connection at {}:{}'.format(FLAGS.ip, FLAGS.port))
    time_c_1 = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((FLAGS.ip, FLAGS.port))
    time_c_2 = time.time()
    logging.info('Connected to {}:{} in {:.3f}ms'.format(FLAGS.ip, FLAGS.port, (time_c_2 - time_c_1)))

    message = "0;AFF;;;"
    send_1 = time.time()
    s.send(message.encode('utf-8'))
    send_2 = time.time()
    logging.info('Send identification message {} in {}ms'.format(message, (send_2 - send_1)))

    while True:

        try:
            data = s.recv(3000000)
            message_parsed = parse_message_received(data.decode('utf-8'))
            logging.info(
                'message {} size : {:.2f}Mb received'.format(message_parsed[0], (sys.getsizeof(data) / 1000000)))
            if len(message_parsed) == 5:
                id_img = message_parsed[0]
                logging.info('\t image {}'.format(message_parsed[0]))
                # img = eval('np.array(' + message_parsed[3] + ')')
                cat = message_parsed[1]
                label = message_parsed[2]
                process = ThreadAFF(id_img, cat, label)
                process.start()
            if data.decode('utf-8') == "close":
                break
        except (ConnectionResetError, ConnectionRefusedError):
            logging.info("Server close the connexion or not online")
            break
    # close the connection
    s.close()


class ThreadAFF(threading.Thread):
    def __init__(self, id_img, cat, label):
        threading.Thread.__init__(self)
        self.cat = cat
        self.id_img = id_img
        self.label = label

    def run(self):
        print_img(self.id_img, self.cat, self.label)


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
