
# -*- coding: utf-8 -*-

import requests
import json
import time
import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
import requests
import random
import json
from hashlib import md5

hander = RotatingFileHandler("./logs/server.log",
                             encoding="UTF-8",
                             maxBytes=1024 * 1024 * 10,
                             backupCount=10)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler(), hander],
)

log = logging.getLogger("utils")

# Set your own appid/appkey.
appid = '20180913000206313'
appkey = '2OVyXCP2sBdBLLEsq2Nf'

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def connect(origin_text:str, from_lang:str, to_lang:str):
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    query = origin_text

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    log.info(json.dumps(result, indent=4, ensure_ascii=False))
    log.info(result['trans_result'])
    return result['trans_result'][0]['dst']


def re_write(text:str):
    log.info(text)
    ans = text
    langs = ["zh","jp","en","de","pt","zh"]
    
    for i in range(len(langs)-1):
        ans = connect(ans, langs[i], langs[i+1])
        time.sleep(1)
    return ans

if __name__ == "__main__":
    re_write("我是中国人")