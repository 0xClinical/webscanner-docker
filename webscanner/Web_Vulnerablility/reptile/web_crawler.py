import requests
from bs4 import BeautifulSoup
from queue import Queue
from urllib.parse import urljoin, urlparse


def check_url_accessible(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False


def spider1_link(url):
    links = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href and href not in links:
                    links.append(href)
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
    return links


def is_same_origin(url1, url2):
    parsed_url1 = urlparse(url1)
    parsed_url2 = urlparse(url2)
    return parsed_url1.netloc == parsed_url2.netloc


def remove_query_params(url):
    parts = url.split("?")
    clean_url = parts[0]
    return clean_url


def spider2_content(url):
    if not check_url_accessible(url):
        print(f"URL not accessible: {url}")
        return []

    base_url = url
    unvisited = Queue()
    all_links = []
    processed_links = set()

    unvisited.put(url)
    all_links.append(url)
    processed_links.add(url)

    while not unvisited.empty():
        current_url = unvisited.get()
        links = spider1_link(current_url)
        for link in links:
            absolute_url = urljoin(base_url, remove_query_params(link))  # 构建绝对URL并移除查询参数
            if is_same_origin(base_url, absolute_url) and absolute_url not in processed_links:
                unvisited.put(absolute_url)
                all_links.append(absolute_url)
                processed_links.add(absolute_url)

    return all_links