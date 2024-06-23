import requests
from colorama import init, Fore

init(autoreset=True)


def scan_remote_file_inclusion(url, file_param, file_path):
    payload = {
        file_param: file_path,
        'submit':'提交'
    }

    try:
        response = requests.get(url, params=payload)

        if response.status_code == 200 and "PHP Version" in response.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False



