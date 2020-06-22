#-*- coding:utf-8 -*-
# flags.py

import os
import time
import sys
import requests

# 국기 사이트가 뻗었으므로 걍 내 이미지로 하자...
POP20_CC = ('8_1 8_2 8_3 8_4 8_5 '
           '13_1 13_2 13_3 15_1').split()

BASE_URL = 'http://flupy.org/data/flags'
#BASE_URL = 'https://github.com/lih0905/Fluent_Python/raw/master/images/'

DEST_DIR = 'downloads/'

def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)
        
def get_flag(cc):
    url = '{}/{cc}.PNG'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content

def show(text):
    print(text, end=' ')
    sys.stdout.flush()

def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.PNG')
    return len(cc_list)

def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))
    
if __name__ == '__main__':
    main(download_many)
