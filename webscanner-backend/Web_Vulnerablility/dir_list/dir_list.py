import requests

target_url = "http://example.com/path"  # 目标URL

def check_directory_traversal(url):
    payloads = ["../", "../../", "../../../"]  # 用于测试的目录遍历载荷
    for payload in payloads:
        test_url = url + payload
        response = requests.get(test_url)
        if response.status_code == 200:
            print(f"[Vulnerable] Directory Traversal found: {test_url}")
            return '目录遍历漏洞'
            break
        else:
            print(f"Not vulnerable: {test_url}")
    return False
