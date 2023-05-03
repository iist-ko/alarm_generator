#-*- encoding: utf-8 -*-

from threading import Thread
from requests.auth import HTTPDigestAuth

import requests
import json
import time
import os

pwd = os.getcwd()


def read_json():
    f = open(os.path.join(pwd, "config/ip_data.json"), 'r', encoding='utf-8')
    j_data = json.load(f)
    f.close()
    return j_data["data"]


def ip_start():
    thread = Thread(target=ip_checkable)
    thread.start()


def ip_checkable():
    while True:
        for t in range(len(ip_data)):
            name_, model_, _ip, _id, _pwd = ip_data[t]
            if _ip == '' or _id == '' or _pwd == '':
                continue
            auth = HTTPDigestAuth(_id, _pwd)
            url = f'http://{_ip}/cgi-bin/fwalarmstateget.cgi?FwModId=0&FwCgiVer=0x0001'
            target2 = 'DO_STATE'
            target3 = 'FES_DATA1'
            if model_ == "3204":
                url = f'http://{_ip}/httpapi/GetState?action=getinput&GIS_ALARM1=0'
                target2 = 'GIS_ALARM1'
            try:
                response = requests.get(url, auth=auth, timeout=0.4)
                target = '{"' + response.text.replace('\r\n', '\", \"').replace('=', '":"').rstrip(', "') + '"}'
                if model_ == "3204":
                    target = '{"' + response.text.replace('\n\r\n', '').replace('=', '":"') + '"}'
                js = json.loads(target)
            except:
                print(_ip, "error")
                ip_data[t] = ('', '', '', '', '')
                continue

            if model_ != "3204":
                if js[target2] == '0x07' and js[target3] == '0x00000001':
                    f = open(pwd + "/Detection/" + name_ + "_" + _ip + ".txt", 'w', encoding='UTF8')
                    f.write('Fire Alarm\n' + _ip + '\n' + model_ + '\n' + _id + '\n' + _pwd + '\n' + str(t))
                    f.close()
            else:
                if js[target2] == '1':
                    f = open(pwd + "/Detection/" + name_ + "_" + _ip + ".txt", 'w', encoding='UTF8')
                    f.write('Fire Alarm\n' + _ip + '\n' + model_ + '\n' + _id + '\n' + _pwd + '\n' + str(t))
                    f.close()
        time.sleep(3)

if __name__ == '__main__':
    data_read = read_json()
    ip_data = []
    for data in data_read:
        name, model, ip_, id_, pwd_ = data.values()
        ip_data.append((name, model, ip_, id_, pwd_))
    ip_start()
