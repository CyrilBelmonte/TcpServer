# Import socket module
import socket
import sys
import numpy as np
import time
import threading

from absl import app, flags, logging
from absl.flags import FLAGS

import myTools.cnn_model as cnn

flags.DEFINE_string('ip', '127.0.0.1', 'default ip')
flags.DEFINE_integer('port', 12346, 'default port')

np.set_printoptions(threshold=sys.maxsize)

info = []


def parse_message_received(data):
    parse = data.split(";")
    return parse


def get_img(data):
    tmp_data = data.split(" ")
    print(tmp_data[1:-1])
    return


def main(_argv):
    logging.info('load cat modem')

    dog_1 = time.time()
    dog_model = cnn.get_inception_v2_dog()
    dog_2 = time.time()
    logging.info('dog model load in {:.2f}ms'.format((dog_2 - dog_1)))

    logging.info('Initialization connection at {}:{}'.format(FLAGS.ip, FLAGS.port))
    time_c_1 = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((FLAGS.ip, FLAGS.port))
    time_c_2 = time.time()
    logging.info('Connected to {}:{} in {:.3f}ms'.format(FLAGS.ip, FLAGS.port, (time_c_2 - time_c_1)))

    message = "0;RASP;127.0.0.1;DOG;"
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
            if len(message_parsed) == 4:
                logging.info('\t image {}'.format(message_parsed[0]))
                img = eval('np.array(' + message_parsed[2] + ')')
                process = ThreadCAT(message_parsed[0], img, dog_model, s)
                process.start()
            if data.decode('utf-8') == "close":
                break
        except (ConnectionResetError, ConnectionRefusedError):
            logging.info("Server close the connexion or not online")
            break
    # close the connection
    s.close()


class ThreadCAT(threading.Thread):
    def __init__(self, id_img, img, model, s):
        threading.Thread.__init__(self)
        self.id_img = id_img
        self.img = img
        self.model = model
        self.s = s

    def run(self):
        cnn.thread_for_cnn(self.id_img, self.img, self.model, self.s)


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
