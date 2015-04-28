import socket
import requests
import socks
import stem.process
import hashlib
import os
import scraper
import random
import string

PANEL_URL = "http://localhost/login.php"
PORT = 5000
MAPFILE = "map.txt"


def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

def loadProxy():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", PORT)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo
    
def randomPass():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def send():
    fingerprints = scraper.scrapeNodes()
    loadProxy()

    file = open(MAPFILE, mode="a")
    
    for fp in fingerprints:
        global tor_process
        print("Testing " + fp)
        
        try:
            tor_process = stem.process.launch_tor_with_config(
                config = {
                    'SocksPort': str(PORT),
                    'ExitNodes': fp,
                },
            )
                  
            password = randomPass()
                        
            data = {
                "user": "admin",
                "password": password
            }
            
            requests.get(PANEL_URL, data=data, timeout=10)
            
            file.write(fp + "=" + password + os.linesep)
            
            print("Completed " + fp)
            
            tor_process.kill()
        except Exception as e: 
            print(str(e))
            tor_process.kill()
            
    file.close()
if __name__ == "__main__":
    send()