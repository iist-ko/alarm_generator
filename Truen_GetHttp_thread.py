import requests
from requests.auth import HTTPDigestAuth
from scapy.all import *
from scapy.layers.inet import TCP
import threading
import time

protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}

# if len(sys.argv) != 5:
#     print("Insufficient Argument")
#     sys.exit(0)

# nm = sys.argv[1].replace('\n', '')
# ip = sys.argv[2].replace('\n', '')
# id = sys.argv[3].replace('\n', '')
# pas = sys.argv[4].replace('\n', '')

nm = '트루엔테스트'
ip = '192.168.0.179'
id = 'admin'
pas = 'root'

def showPacket(packet):
    global Ip
    try:
        src_ip = packet[0][1].src
        dst_ip = packet[0][1].dst
        proto = packet[0][1].proto
    except:
        proto = 'Null'
    if proto in protocols:
        if src_ip == Ip :

            data = f'{packet[TCP].payload}'

            data2 = str('\\xdd\\xcc\\xbb\\xaa')

            # if data.find(data2)!=-1:
            if data.find(data2) != -1:
                object = data[131:133]
                if object == '07' or object == '01':
                    f = open("./Detection/"+nm+"_"+Ip+".txt", 'w', encoding='UTF8')
                    f.write('test')
                    print('test')
                    f.close()
                    #print('test')
                elif object == '04':
                    f = open("./Detection/"+nm+"_"+Ip + ".txt", 'w', encoding='UTF8')
                    f.write('smoke')
                    print('smoke')
                    f.close()
                    #print('smoke')
                elif object == '02':
                    f = open("./Detection/"+nm+"_"+Ip + ".txt", 'w', encoding='UTF8')
                    f.write('fire')
                    print('fire')
                    f.close()
                    #print('fire')
        if proto == 1:
            print("TYPE: [%d], CODE[%d]" % (packet[0][2].type, packet[0][2].code))

def sniffing(filter, IP):
    global Ip
    Ip = IP
    print("sniff", Ip)
    sniff(filter=filter, prn=showPacket, count=0)

def thread_1(IP,ID,PAS):
    try :
        print('thread_1:response1')
        response = requests.get('http://'+IP, auth=HTTPDigestAuth(ID, PAS),timeout=1)
    except :
        print('pass t1', IP)
        return

    print('thread_1:response2')
    response = requests.get('http://'+IP+'/httpapi/IISTEvent', auth=HTTPDigestAuth(ID, PAS))
    ## 킨 상태에서만 패킷 확인이 가능하다 ##

    print(response.content)
    print('End Response')
    response.text
    print(response)

def thread_2(IP,ID,PAS):
    try:
        print('thread_2:response1')
        response = requests.get('http://'+IP,auth=HTTPDigestAuth(ID, PAS),timeout=3)
    except:
        print('out t2_1', IP)
        return
    sniffing('tcp', IP)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

if __name__ == "__main__":

    createFolder('Detection')
    print(ip, id, pas)
    threads = []
    try :
        t1 = threading.Thread(target=thread_1, args=(ip, id, pas,))
        # t1 = threading.Thread(target=thread_1, args=(IP,ID,PAS,))
        t1.start()
        threads.append(t1)
        print('t1 start')
    except :
        print('pass t1t1', ip)
        sys.exit(0)
        pass

    try :
        t2 = threading.Thread(target=thread_2, args=(ip,id,pas,))
        #t2 = threading.Thread(target=thread_2, args=(IP,))
        t2.start()
        threads.append(t2)
        print('t2 start')
    except :
        print('pass t2t2', ip)
        sys.exit(0)
        pass

    try:
        for t in threads:
            t.join()
    except :
        print("join error ", ip)
        sys.exit(0)
        pass

    print("end of main")