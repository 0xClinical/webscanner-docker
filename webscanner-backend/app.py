# -*- coding=utf8 -*-
# 导入Flask库
from flask_cors import CORS
from flask import Flask, jsonify
from flask import request
from flask import render_template
import flask
import json
from Web_Vulnerablility.scan_endpoint import scanweb,read_list_from_database
from static.Tools.SQL.SQL_op import SQL
from phishing import classify

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # 允许所有来源访问/api/*端点

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
