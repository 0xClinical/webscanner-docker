# -*- coding=utf8 -*-
# 导入Flask库
from flask_cors import CORS
from flask import Flask, jsonify
from flask import request
from flask import render_template
import plotly.graph_objs as go
from keras_preprocessing.sequence import pad_sequences
from threading import Thread
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import label_data
import flask
import json
from Web_Vulnerablility.scan_endpoint import scanweb,read_list_from_database
from static.Tools.SQL.SQL_op import SQL
from phishing import classify

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # 允许所有来源访问/api/*端点
global graph
graph = tf.compat.v1.get_default_graph()


def prepare_url(url):
    urlz = label_data.main()

    samples = []
    labels = []
    for k, v in urlz.items():
        samples.append(k)
        labels.append(v)

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


# 写好的数据库连接函数，
# 传入的是table，数据表的名称，
# 返回值是数据表中所有的数据，以元祖的格式返回
# 模拟已知的漏洞列表（可以根据实际情况进行修改）
sql1 = SQL()
counter = sql1.selectSQL(sql1.cursor)[0]
vulnerabilities = {
    'XSS': '跨站脚本攻击（Cross-Site Scripting）',
    'SQLI': 'SQL 注入攻击（SQL Injection）',
    'RCE': '远程命令执行（Remote Code Execution）'
}

client_proxy = {
    "Internet Explorer 11": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Default": ""
}

scan_mode = {
    "全面扫描": 2,
    "快速扫描": 1,
    "SQL注入扫描": 3,
    "XSS扫描": 4,
    "暴力破解扫描": 5,
    "远程代码执行扫描": 6,
    "文件漏洞扫描": 7
}


shared_data = {

}


# 启动服务器后运行的第一个函数，显示对应的网页内容
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')

# 假设我们有一个简单的用户数据库
users = {"admin@1","123456"}
scan_results = []
# 对登录的用户名和密码进行判断
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    '''
    if email in users and users[email] == password:
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401
        '''
    return jsonify({'status': 'success', 'message': 'Login successful'}), 200



@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users:
        return jsonify({'status': 'fail', 'message': 'User already exists'}), 409
    else:
        users[email] = password
        return jsonify({'status': 'success', 'message': 'Registration successful'}), 201

# 显示教师首页的函数，可以显示首页里的信息
@app.route('/api/scan', methods=['POST'])
def start_scan():
    data = request.get_json()
    url = data.get('url')
    config = data.get('config')

    # 假设我们有一个扫描函数 `perform_scan`
    results = perform_scan(url, config)
    scan_results.append({'url': url, 'results': results})
    return jsonify({'status': 'success', 'url': url, 'results': results}), 200


@app.route('/api/vulInfo', methods=['POST'])
def vul_info():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        return jsonify({'status': 'success', 'results': scan_results}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401


@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    data = read_list_from_database()

    return jsonify(data), 200


@app.route('/api/check-url', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')

    # 假设我们有一个钓鱼网站检测函数 `is_phishing_url`
    is_phishing = classify.url_detect(url)

    return jsonify({'isPhishing': is_phishing}), 200


@app.route('/api/check-image', methods=['POST'])
def check_image():
    image = request.files.get('image')

    # 假设我们有一个钓鱼图片检测函数 `is_phishing_image`
    is_phishing = is_phishing_image(image)

    return jsonify({'isPhishing': is_phishing}), 200


@app.route('/api/saveInfo', methods=['POST'])
def save_info():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        # 假设我们有一个保存设置的函数 `save_user_info`
        save_user_info(email, data)
        return jsonify({'status': 'success', 'message': 'Information saved'}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401
def is_phishing_image(image):
    # 这里添加检测钓鱼图片的逻辑
    # 这是一个示例逻辑，实际检测应更加复杂
    return False


def perform_scan(url, config):
    results = []
    # 这里添加漏洞扫描的逻辑
    scan_results = scanweb(url,config)
    for item in scan_results:
        results.append({'type': item[0], 'url': item[1]})
    # 这是一个示例逻辑，实际扫描应更加复杂
    return results


def save_user_info(email, data):
    # 这里添加保存用户设置的逻辑
    # 这是一个示例逻辑，实际保存应更加复杂
    pass

# 主函数
if __name__ == '__main__':
    # app.debug = True
    app.run()
