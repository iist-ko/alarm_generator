#-*- encoding: utf-8 -*-

from threading import Thread
from requests.auth import HTTPDigestAuth

import requests
import json
import time

NM = ['nm0','nm1','nm2','nm3','nm4','nm5','nm6','nm7','nm8','nm9','nm10','nm11','nm12','nm13','nm14','nm15']
IP = ['IP0','IP1','IP2','IP3','IP4','IP5','IP6','IP7','IP8','IP9','IP10','IP11','IP12','IP13','IP14','IP15']
ID = ['ID0', 'ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'ID8', 'ID9', 'ID10', 'ID11', 'ID12', 'ID13',
              'ID14', 'ID15']
PS = ['PS0', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9', 'PS10', 'PS11', 'PS12', 'PS13',
              'PS14', 'PS15']

IP_READ=[]

def Read_file(FILE):
    f = open("Seyeon_IP_Save.txt", 'r', encoding='UTF8')
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n', '')
        FILE.append(line)
    # print(FILE)
    f.close()

def IP_Start(IP, ID, PAS):
    bThread = True
    thread = Thread(target=IP_Checkable(IP, ID, PAS))
    thread.start()


def IP_Checkable(IP, ID, PAS):
    while True:
        for t in range(0, 16):
            if IP[t] == '' or ID[t] == '' or PAS[t] == '':
                continue
            try:
                response = requests.get('http://' + IP[t] + '/cgi-bin/fwalarmstateget.cgi?FwModId=0&FwCgiVer=0x0001',
                                        auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                target = '{"' + response.text.replace('\r\n', '\", \"').replace('=', '":"').rstrip(', "') + '"}'
                js = json.loads(target)
            except:
                continue
            if js['DO_STATE'] == '0x07' and js['FES_DATA1'] == '0x00000001':
                f = open("./Detection/"+NM[t]+"_"+IP[t] + ".txt", 'w', encoding='UTF8')
                f.write('Fire Alarm')
                f.close()
        time.sleep(0.5)

if __name__ == '__main__':
    Read_file(IP_READ)
    k = 0
    for i in range(0, 16):
        NM[i] = IP_READ[k]
        IP[i] = IP_READ[k + 1]
        ID[i] = IP_READ[k + 2]
        PS[i] = IP_READ[k + 3]
        k += 4
        #print('k')
    print(IP)
    print(ID)
    print(PS)
    IP_Start(IP=IP,ID=ID,PAS=PS)