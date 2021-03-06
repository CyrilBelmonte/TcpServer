import numpy as np
import tensorflow as tf
import pandas as pd
import sys

import threading

np.set_printoptions(threshold=sys.maxsize)
from myTools import image_tools as img_t

info = []


def get_inception_v2_cat():
    model = tf.keras.models.load_model("./resources/inceptionV2_cat_breed_finetuned_v1.h5")
    return model


def get_inception_v2_dog():
    model = tf.keras.models.load_model("./resources/inceptionV2_dog_breed120_finetuned_v2.h5")
    return model


def get_more_cat(model, img):
    prediction = model.predict(img)
    arg = np.argmax(prediction)
    labels = pd.read_csv(".\\resources\\cats.csv")
    list_label = list(set(labels['breed']))
    list_label.sort()
    return list_label[arg], prediction[0][arg]


def get_more_dog(model, img):
    prediction = model.predict(img)
    arg = np.argmax(prediction)
    labels = pd.read_csv(".\\resources\\labels_dog_breeds.csv")
    list_label = list(set(labels['breed']))
    list_label.sort()
    return list_label[arg], prediction[0][arg]


def thread_for_cnn(id_img, img, model, s):
    label, prob = get_more_dog(model, img)
    message = '{};RASP;{};'.format(id_img, label)
    print("Send to server : ", message)
    s.send(message.encode('utf-8'))
    return [id_img, label, prob]


"""
def get_more_data(img, model_cat, model_dog, outputs, class_names):
    boxes, objectness, classes, nums = outputs
    boxes, objectness, classes, nums = boxes[0], objectness[0], classes[0], nums[0]
    wh = np.flip(img.shape[0:2])
    process_s = []
    for i in range(nums):
        x1y1 = tuple((np.array(boxes[i][0:2]) * wh).astype(np.int32))
        x2y2 = tuple((np.array(boxes[i][2:4]) * wh).astype(np.int32))

        if class_names[int(classes[i])] == "cat" or class_names[int(classes[i])] == "dog":
            x1, y1 = x1y1
            x2, y2 = x2y2
            img_crop = img[y1:y1 + (y2 - y1), x1:x1 + (x2 - x1)]

            img_to_cnn = img_t.load_img_opencv(img_crop)
            if class_names[int(classes[i])] == "cat":
                process = ThreadCat(i, "cat", model_cat, img_to_cnn)
                process_s.append(process)
            else:
                process = ThreadDog(i, "dog", model_dog, img_to_cnn)
                process_s.append(process)
    for process in process_s:
        process.start()
        process.join()
    return info


class ThreadCat(threading.Thread):
    def __init__(self, i, class_t, model, img):
        threading.Thread.__init__(self)
        self.i = i
        self.class_t = class_t
        self.model = model
        self.img = img

    def run(self):
        thread_for_cnn(self.i, self.class_t, self.model, self.img)


class ThreadDog(threading.Thread):
    def __init__(self, i, class_t, model, img):
        threading.Thread.__init__(self)
        self.i = i
        self.class_t = class_t
        self.model = model
        self.img = img

    def run(self):
        thread_for_cnn(self.i, self.class_t, self.model, self.img)
"""
