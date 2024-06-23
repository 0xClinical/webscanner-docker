import re
import requests
import socket
import ssl
import whois
from datetime import datetime
from urllib.parse import urlparse
import tldextract
from sklearn.preprocessing import StandardScaler

# 标准化器
scaler = StandardScaler()
def having_ip_address(url):
    # 检查URL中是否使用了IP地址
    ip_pattern = re.compile(
        r'^(http|https):\/\/(\d{1,3}\.){3}\d{1,3}')
    return 1 if ip_pattern.match(url) else -1


def url_length(url):
    # 计算URL的长度
    length = len(url)
    if length < 10:
        return -1
    elif 20 <= length <= 34:
        return 0
    else:
        return 1


def shortining_service(url):
    # 检查是否使用URL缩短服务
    shortening_services = ["bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "bit.do"]
    parsed_url = urlparse(url)
    return 1 if parsed_url.netloc in shortening_services else -1


def sslfinal_state(url):
    # 检查SSL证书的状态
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                certificate = ssock.getpeercert()
                not_after = datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
                if not_after > datetime.now():
                    return 1
                else:
                    return -1
    except:
        return 1


def domain_registration_length(url):
    # 检查域名注册时间的长度
    try:
        domain = tldextract.extract(url).registered_domain
        whois_info = whois.whois(domain)
        creation_date = whois_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        age = (datetime.now() - creation_date).days
        return 1 if age < 365 else -1
    except:
        return 1


def web_traffic(url):
    # 评估网站的流量（这里只是一个示例，实际上可以使用Alexa等服务获取流量信息）
    try:
        response = requests.get(f"https://www.alexa.com/siteinfo/{urlparse(url).hostname}")
        if response.status_code == 200:
            rank = re.search(r'Global Rank:</span> <strong class="metrics-data align-vmiddle">(\d+)</strong>',
                             response.text)
            if rank:
                rank = int(rank.group(1).replace(',', ''))
                if rank < 100000:
                    return -1
                elif rank < 1000000:
                    return 0
                else:
                    return 1
        return 1
    except:
        return 1


def get_important_features(url):
    features = {
        'having_ip_address': having_ip_address(url),
        'url_length': url_length(url),
        'shortining_service': shortining_service(url),
        'sslfinal_state': sslfinal_state(url),
        'domain_registration_length': domain_registration_length(url),
        'web_traffic': web_traffic(url)
    }

    # 将特征转换为与模型一致的格式
    feature_values = [features[feat] for feat in features.keys()]
    print("URL的特征:", feature_values)
    # 标准化特征
    return [feature_values]


