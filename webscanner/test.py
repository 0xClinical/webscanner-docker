# -*- coding=utf8 -*-
# 导入Flask库
from flask import Flask
from flask import request
from flask import render_template
import plotly.graph_objs as go
import numpy as np
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences

from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import label_data
import flask
import json
global graph
graph = tf.compat.v1.get_default_graph()
model_pre = ''#'G:\\Model\\pishing-url-detection-main\\bi-lstmchar256256128.h5'
model = load_model(model_pre)


def prepare_url(url):
    urlz = label_data.main()

    samples = []
    labels = []
    for k, v in urlz.items():
        samples.append(k)
        labels.append(v)

    # print(len(samples))
    # print(len(labels))

    maxlen = 128
    max_words = 20000

    tokenizer = Tokenizer(num_words=max_words, char_level=True)
    tokenizer.fit_on_texts(samples)
    sequences = tokenizer.texts_to_sequences(url)
    '''
    创建一个Tokenizer对象，并使用样本数据samples对其进行训练，以便后续可以使用这个Tokenizer对象对文本数据进行编码和处理。训练过程中会构建词汇表和统计词频等信息，以供后续使用。
    '''
    word_index = tokenizer.word_index
    # print('Found %s unique tokens.' % len(word_index))

    url_prepped = pad_sequences(sequences, maxlen=maxlen)
    return url_prepped

urlz = []
url = "http://jkiiytgbfb.com/pconfirm3.htm"
urlz.append(url)
print(url)

# Process and prepare the URL.
url_prepped = prepare_url(urlz)
data = {"success": False}
# classify the URL and make the prediction.
with graph.as_default():
    model =tf.keras.Sequential()
    model.call = tf.function(model.call)
    prediction = model.predict(url_prepped)
print(prediction)

data["predictions"] = []

if (prediction > 0.50).all():
    result = "URL is probably malicious."
else:
    result = "URL is probably NOT malicious."
print(result)
