import base64
import hashlib
import requests
from os import getenv
from dotenv import load_dotenv

# load env file
load_dotenv()

def generate_salt():
    # replace %s with id and mail from env file
    authsalt = getenv('APIAUTHSALT') % (getenv('ID'), getenv('MAIL'))
    authsaltmd5 = hashlib.md5()
    authsaltmd5.update(authsalt.encode("utf-8"))
    # hexdigest needed for string type
    authsaltmd5 = authsaltmd5.hexdigest()
    #decode needed for string type 
    return base64.b64encode(authsaltmd5.encode("utf-8")).decode()


api_base = "https://api.easyname.com"
custom_header = {'Accept': 'application/json', 'X-User-ApiKey': f"{getenv('APIKEY')}", 'X-User-Authentication': f"{generate_salt()}"}

def get_domains():
    domain_response = requests.get(f"{api_base}/domain", headers=custom_header).json()
    domains = domain_response
    return domains
