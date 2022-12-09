import requests
from requests.auth import HTTPDigestAuth
from scapy.all import *

protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}

# if len(sys.argv) != 5:
#     print("Insufficient Argument")
#     sys.exit(0)

nm = sys.argv[1]
ip = sys.argv[2]
id = sys.argv[3]
pas = sys.argv[4]

# nm = '트루엔테스트'
# ip = '192.168.0.245'
# id = 'admin'
# pas = 'root'

def showPacket(packet):
    global Ip
    src_ip = packet[0][1].src
    dst_ip = packet[0][1].dst
    proto = packet[0][1].proto

    if proto in protocols:

        if src_ip == Ip :
            data = ('%s' % (packet[TCP].payload))
            data2 = str('\\xdd\\xcc\\xbb\\xaa')

            if data.find(data2)!=-1:
                object = data[131:133]
                if object == '07' or object == '01':
                    f = open("./Detection/"+nm+"_"+Ip+".txt", 'w', encoding='UTF8')
                    f.write('test')
                    f.close()
                    #print('test')
                elif object == '04':
                    f = open("./Detection/"+nm+"_"+Ip + ".txt", 'w', encoding='UTF8')
                    f.write('smoke')
                    f.close()
                    #print('smoke')
                elif object == '02':
                    f = open("./Detection/"+nm+"_"+Ip + ".txt", 'w', encoding='UTF8')
                    f.write('fire')
                    f.close()
                    #print('fire')
        if proto == 1:
            print("TYPE: [%d], CODE[%d]" % (packet[0][2].type, packet[0][2].code))

def sniffing(filter, IP):
    global Ip
    Ip = IP
    sniff(filter=filter, prn=showPacket, count=0)

def thread_1(IP,ID,PAS):
    try :
        response = requests.get('http://'+IP, auth=HTTPDigestAuth(ID, PAS),timeout=1)
    except :
        print('pass t1')
    response = requests.get('http://'+IP+'/httpapi/IISTEvent', auth=HTTPDigestAuth(ID, PAS))
    ## 킨 상태에서만 패킷 확인이 가능하다 ##

    print(response.content)
    print('End Response')
    response.text
    print(response)

def thread_2(IP,ID,PAS):
    try:
        response = requests.get('http://'+IP,auth=HTTPDigestAuth(ID, PAS),timeout=1)
    except:
        print('out')
        sys.exit(0)
    try:
        sniffing('tcp', IP)
    except:
        print('out')
        sys.exit(0)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

if __name__ == "__main__":

    createFolder('Detection')
    threads = []
    try :
        t1 = threading.Thread(target=thread_1, args=(ip, id, pas,))
        #t1 = threading.Thread(target=thread_1, args=(IP,ID,PAS,))
        t1.start()
        threads.append(t1)
        print('t1 start')
    except :
        print('pass t1t1')
        sys.exit(0)
        pass

    try :
        t2 = threading.Thread(target=thread_2, args=(ip,id,pas,))
        #t2 = threading.Thread(target=thread_2, args=(IP,))
        t2.start()
        threads.append(t2)
        print('t2 start')
    except :
        print('pass t2t2')
        sys.exit(0)
        pass

    try:
        for t in threads:
            t.join()
    except :
        sys.exit(0)
        pass

    print("end of main")