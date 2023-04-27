#-*- encoding: utf-8 -*-

from threading import Thread
from requests.auth import HTTPDigestAuth

import requests
import json
import time
import os

pwd = os.getcwd()


def read_file():
    f = open(os.path.join(pwd, "config/ip_data.json"), 'r', encoding='UTF8')
    data = json.load(f)["data"]
    return data


def ip_start():
    thread = Thread(target=ip_checkable())
    thread.start()


def ip_checkable():
    while True:
        for i, t in enumerate(data):
            if t["ip"] == '' or t["id"] == '' or t["pwd"] == '':
                continue
            url = 'http://' + t["ip"] + '/cgi-bin/fwalarmstateget.cgi?FwModId=0&FwCgiVer=0x0001'
            auth = HTTPDigestAuth(t["id"], t["pwd"])
            target_md = 0
            if t["model"] == "3204":
                url = 'http://' + t["ip"] + '/httpapi/GetState?action=getinput&GIS_ALARM1=0'
                target_md = 1
            try:
                response = requests.get(url, auth=auth, timeout=1)
                if target_md:
                    target = target = '{"' + response.text.replace('\n\r\n', '').replace('=', '":"')+ '"}'
                else:
                    target = '{"' + response.text.replace('\r\n', '\", \"').replace('=', '":"').rstrip(', "') + '"}'
                js = json.loads(target)
            except:
                print(t["ip"]," error")
                continue
            if target_md:
                if js['GIS_ALARM1'] == '1':
                    f = open(pwd + "/Detection/" + t["name"] + "_" + t["ip"] + ".txt", 'w', encoding='UTF8')
                    f.write('Fire Alarm\n' + t["ip"] + '\n' + t["model"] + '\n'
                            + t["id"] + '\n' + t["pwd"] + '\n' + str(i))
                    f.close()
            else:
                if js['DO_STATE'] == '0x07' and js['FES_DATA1'] == '0x00000001':
                    f = open(pwd + "/Detection/" + t["name"] + "_" + t["ip"] + ".txt", 'w', encoding='UTF8')
                    f.write('Fire Alarm\n' + t["ip"] + '\n' + t["model"] + '\n'
                            + t["id"] + '\n' + t["pwd"] + '\n' + str(i))
                    f.close()
        time.sleep(3)

if __name__ == '__main__':
    print("Fire Search")
    data = read_file()
    ip_start()