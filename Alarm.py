#!/usr/bin/env python3
#coding: UTF-8
import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
from requests.auth import HTTPDigestAuth
from scapy.all import *
from multiprocessing import Process, Queue
import datetime
import csv
import threading,time
from serial import Serial
import ctypes

try:
    arduino = Serial('COM3', 9600)
except:
    try : arduino = Serial('COM4', 9600)
    except :
        try : arduino = Serial('COM5', 9600)
        except : pass

global table_Count
table_Count = 0

protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
try :
    os.mkdir('./Detection')
except :
    pass

try :
    os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
except :
    pass

try :
    os.system('taskkill /f /im Truen_GetHttp_thread.exe')
except :
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(500, 250, 740, 410)  # x, y, w, h
        self.setWindowTitle('Alarm status')

        # QButton 위젯 생성
        Font = QtGui.QFont("Calibri", 11)
        Font.setBold(True)
        
        self.setWindowIcon(QIcon('logo.jpg'))

        p = QPalette()
        p.setColor(QPalette.Background,QColor(255,255,255))
        self.setPalette(p)
        
        self.button0 = QPushButton('Seyeon IP', self)
        self.button0.clicked.connect(self.Seyeon_IP_open)
        self.button0.setFont(Font)
        self.button0.setStyleSheet("color: White;"
	                               "background-color: rgb(255, 0, 0);"
	                               "border: 2px solid rgb(255, 0, 0);")
        self.button0.setGeometry(10, 10, 100, 50)
        self.button1 = QPushButton('Truen IP', self)
        self.button1.clicked.connect(self.IP_open)
        self.button1.setFont(Font)
        self.button1.setStyleSheet("color: White;"
	                               "background-color: rgb(255, 0, 0);"
	                               "border: 2px solid rgb(255, 0, 0);")
        self.button1.setGeometry(115, 10, 100, 50)
        self.button2 = QPushButton('Start', self)
        self.button2.clicked.connect(self.Start)
        self.button2.setFont(Font)
        self.button2.setStyleSheet("color: White;"
	                               "background-color: rgb(255, 0, 0);"
	                               "border: 2px solid rgb(255, 0, 0);")
        self.button2.setGeometry(220, 10, 100, 50)
        self.button2.toggle()
        self.button2.setCheckable(True)
        self.button3 = QPushButton('Reset', self)
        self.button3.clicked.connect(self.ResetTable)
        self.button3.setFont(Font)
        self.button3.setStyleSheet("color: White;"
	                               "background-color: rgb(255, 0, 0);"
	                               "border: 2px solid rgb(255, 0, 0);")
        self.button3.setGeometry(325, 10, 100, 50)

        # 카메라
        # self.frm1 = QLabel(self)
        # self.frm1.setFrameShape(QFrame.Panel)
        # self.frm1.setGeometry(10, 70, 480, 360)
        # self.frm2 = QLabel(self)
        # self.frm2.setFrameShape(QFrame.Panel)
        # self.frm2.setGeometry(491, 70, 240, 179)
        # self.frm3 = QLabel(self)
        # self.frm3.setFrameShape(QFrame.Panel)
        # self.frm3.setGeometry(491, 250, 240, 180)

        # Table
        self.table = QTableWidget(self)
        self.table.setRowCount(100)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['시간', '이름', 'IP', '알람내용', '확인메모'])
        self.table.setFont(Font)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 140)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 140)
        self.table.setGeometry(10, 70, 721, 328)
        self.table.setStyleSheet("color: black;"
	                             "background-color: white;"
	                             "border: 2px solid rgb(255, 0, 0);"
                                 "")

        # QDialog 설정
        self.dialog = QDialog()

    # 버튼 이벤트 함수
    def Seyeon_IP_open(self):
        # 버튼 추가
        ############## LINE ###############

        NM = ['NM0', 'NM1', 'NM2', 'NM3', 'NM4', 'NM5', 'NM6', 'NM7', 'NM8', 'NM9', 'NM10', 'NM11', 'NM12', 'NM13',
              'NM14', 'NM15']
        IP = ['IP0', 'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8', 'IP9', 'IP10', 'IP11', 'IP12', 'IP13',
              'IP14', 'IP15']
        ID = ['ID0', 'ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'ID8', 'ID9', 'ID10', 'ID11', 'ID12', 'ID13',
              'ID14', 'ID15']
        PS = ['PS0', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9', 'PS10', 'PS11', 'PS12', 'PS13',
              'PS14', 'PS15']
        # ST = ['ST0', 'ST1', 'ST2', 'ST3', 'ST4', 'ST5', 'ST6', 'ST7', 'ST8', 'ST9', 'ST10', 'ST11', 'ST12',
        #       'ST13', 'ST14', 'ST15']

        ##############NAME 텍스트 값 불러오기###############
        NAME_Read = []
        try:
            self.Seyeon_Read_file(NAME_Read, 'NAME')

            # print(NAME_Read)
        except:
            pass
        ###############################################
        ##############IP 텍스트 값 불러오기###############
        IP_Read = []
        try:
            self.Seyeon_Read_file(IP_Read, 'IP')
        except:
            pass
        ###############################################

        myFont = QtGui.QFont("Arial", 11)
        myFont.setBold(True)
        Explain1 = QLabel('NAME                      IP                             ID                        '
                          'PASS', self.dialog)
        Explain1.setFont(myFont)
        Explain1.move(22, 64)

        Button_Font = QtGui.QFont("Calibri", 11)
        Button_Font.setBold(True)

        try:
            Name = QLineEdit(NAME_Read[0], self.dialog)
        except:
            Name = QLineEdit('', self.dialog)
        Name.resize(130, 25)
        Name.move(20, 20)

        k = 0
        for i in range(0, 16):

            try:
                NM[i] = QLineEdit(IP_Read[k], self.dialog)
            except:
                NM[i] = QLineEdit('', self.dialog)
            # NM[i].setAlignment(Qt.AlignCenter)
            NM[i].resize(130, 25)
            NM[i].move(20, 85 + 25 * i)
            try:
                IP[i] = QLineEdit(IP_Read[k + 1], self.dialog)
            except:
                IP[i] = QLineEdit('', self.dialog)
            # LE[i].setAlignment(Qt.AlignCenter)
            IP[i].resize(130, 25)
            IP[i].move(150, 85 + 25 * i)
            try:
                ID[i] = QLineEdit(IP_Read[k + 2], self.dialog)
            except:
                ID[i] = QLineEdit('', self.dialog)
            # ID[i].setAlignment(Qt.AlignCenter)
            ID[i].resize(110, 25)
            ID[i].move(280, 85 + 25 * i)
            try:
                PS[i] = QLineEdit(IP_Read[k + 3], self.dialog)
            except:
                PS[i] = QLineEdit('', self.dialog)
            PS[i].setEchoMode(QLineEdit.Password)
            # PS[i].setAlignment(Qt.AlignCenter)
            PS[i].resize(110, 25)
            PS[i].move(390, 85 + 25 * i)
            # ST[i] = QLineEdit('', self.dialog)
            # ST[i].resize(60, 25)
            # ST[i].move(500, 85 + 25 * i)
            k += 4

        # SaveB = QPushButton('SAVE', self)
        # SaveB.resize(100, 26)
        # SaveB.move(170, 20)
        # SaveB.setFont(myFont)
        # SaveB.clicked.connect(lambda: self.Save_text(Name, NM, IP, ID, PS))
        #
        # StartB = QPushButton('START', self)
        # StartB.resize(100, 26)
        # StartB.move(271, 20)
        # StartB.setFont(myFont)
        # StartB.clicked.connect(lambda: self.Start(IP, ID, PS, ST))
        
        SaveB = QPushButton('SAVE', self.dialog)
        SaveB.resize(100, 26)
        SaveB.move(170, 20)
        SaveB.setFont(myFont)
        SaveB.clicked.connect(lambda: self.Seyeon_Save_and_dialog_close(Name, NM, IP, ID, PS))
        SaveB.setStyleSheet("color: White;"
	                               "background-color: rgb(255, 0, 0);"
	                               "border: 2px solid rgb(255, 0, 0);")
        # StartB.clicked.connect(lambda: self.Start(Name, NM, IP, ID, PS, ST))

        # btnDialog = QPushButton("OK", self.dialog)
        # btnDialog.move(100, 100)
        # btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('Seyeon')
        self.dialog.setWindowIcon(QIcon('logo.png'))
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(520, 500)
        self.dialog.show()

    def IP_open(self):
        # 버튼 추가
        ############## LINE ###############

        NM = ['NM0', 'NM1', 'NM2', 'NM3', 'NM4', 'NM5', 'NM6', 'NM7', 'NM8', 'NM9', 'NM10', 'NM11', 'NM12', 'NM13',
              'NM14', 'NM15']
        IP = ['IP0', 'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8', 'IP9', 'IP10', 'IP11', 'IP12', 'IP13',
              'IP14', 'IP15']
        ID = ['ID0', 'ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'ID8', 'ID9', 'ID10', 'ID11', 'ID12', 'ID13',
              'ID14', 'ID15']
        PS = ['PS0', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9', 'PS10', 'PS11', 'PS12', 'PS13',
              'PS14', 'PS15']
        # ST = ['ST0', 'ST1', 'ST2', 'ST3', 'ST4', 'ST5', 'ST6', 'ST7', 'ST8', 'ST9', 'ST10', 'ST11', 'ST12',
        #       'ST13', 'ST14', 'ST15']

        ##############NAME 텍스트 값 불러오기###############
        NAME_Read = []
        try:
            self.Read_file(NAME_Read, 'NAME')

            # print(NAME_Read)
        except:
            pass
        ###############################################
        ##############IP 텍스트 값 불러오기###############
        IP_Read = []
        try:
            self.Read_file(IP_Read, 'IP')
        except:
            pass
        ###############################################

        myFont = QtGui.QFont("Calibri", 11)
        myFont.setBold(True)
        Explain1 = QLabel('NAME                      IP                             ID                        '
                          'PASS', self.dialog)
        Explain1.setFont(myFont)
        Explain1.move(22, 64)


        Button_Font = QtGui.QFont("Calibri", 10)
        Button_Font.setBold(True)

        try:
            Name = QLineEdit(NAME_Read[0], self.dialog)
        except:
            Name = QLineEdit('', self.dialog)
        Name.resize(130, 25)
        Name.move(20, 20)

        k = 0
        for i in range(0, 16):

            try:
                NM[i] = QLineEdit(IP_Read[k], self.dialog)
            except:
                NM[i] = QLineEdit('', self.dialog)
            # NM[i].setAlignment(Qt.AlignCenter)
            NM[i].resize(130, 25)
            NM[i].move(20, 85 + 25 * i)
            try:
                IP[i] = QLineEdit(IP_Read[k + 1], self.dialog)
            except:
                IP[i] = QLineEdit('', self.dialog)
            # LE[i].setAlignment(Qt.AlignCenter)
            IP[i].resize(130, 25)
            IP[i].move(150, 85 + 25 * i)
            try:
                ID[i] = QLineEdit(IP_Read[k + 2], self.dialog)
            except:
                ID[i] = QLineEdit('', self.dialog)
            # ID[i].setAlignment(Qt.AlignCenter)
            ID[i].resize(110, 25)
            ID[i].move(280, 85 + 25 * i)
            try:
                PS[i] = QLineEdit(IP_Read[k + 3], self.dialog)
            except:
                PS[i] = QLineEdit('', self.dialog)
            PS[i].setEchoMode(QLineEdit.Password)
            # PS[i].setAlignment(Qt.AlignCenter)
            PS[i].resize(110, 25)
            PS[i].move(390, 85 + 25 * i)
            # ST[i] = QLineEdit('', self.dialog)
            # ST[i].resize(60, 25)
            # ST[i].move(500, 85 + 25 * i)
            k += 4

        # SaveB = QPushButton('SAVE', self)
        # SaveB.resize(100, 26)
        # SaveB.move(170, 20)
        # SaveB.setFont(myFont)
        # SaveB.clicked.connect(lambda: self.Save_text(Name, NM, IP, ID, PS))
        #
        # StartB = QPushButton('START', self)
        # StartB.resize(100, 26)
        # StartB.move(271, 20)
        # StartB.setFont(myFont)
        # StartB.clicked.connect(lambda: self.Start(IP, ID, PS, ST))

        SaveB = QPushButton('SAVE', self.dialog)
        SaveB.resize(100, 26)
        SaveB.move(170, 20)
        SaveB.setFont(myFont)
        SaveB.clicked.connect(lambda: self.Save_and_dialog_close(Name, NM, IP, ID, PS))
        SaveB.setStyleSheet("color: White;"
	                               "background-color: rgb(255, 0, 0);"
	                               "border: 2px solid rgb(255, 0, 0);")
        # StartB.clicked.connect(lambda: self.Start(Name, NM, IP, ID, PS, ST))

        # btnDialog = QPushButton("OK", self.dialog)
        # btnDialog.move(100, 100)
        # btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('Truen')
        self.dialog.setWindowIcon(QIcon('logo.jpg'))
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(520, 500)
        self.dialog.show()

    def Seyeon_Read_file(self,FILE,Case):
        if Case == 'NAME':
            f = open("Seyeon_NAME_Save.txt", 'r', encoding='UTF8')
            t = f.read()
            FILE.append(t)
            f.close()
        elif Case == 'IP':
            f = open("Seyeon_IP_Save.txt", 'r', encoding='UTF8')
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                FILE.append(line)
            # print(FILE)
            f.close()

    def Read_file(self,FILE,Case):
        if Case == 'NAME' :
            f = open("NAME_Save.txt", 'r', encoding='UTF8')
            t = f.read()
            FILE.append(t)
            f.close()
        elif Case == 'IP' :
            f = open("IP_Save.txt", 'r', encoding='UTF8')
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                FILE.append(line)
            #print(FILE)
            f.close()

    def Start(self):
        try:
            os.system('taskkill /f /im Truen_GetHttp_thread.exe')
            os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
        except:
            print('실행')

        print('start')
        t = 0
        k = 0
        ### IP 등등 넣어야함 ###
        FILE = []
        f = open("IP_Save.txt", 'r', encoding='UTF8')
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            FILE.append(line)
        f.close()
        #print('1')
        ### Truen 프로토콜 실행 ###
        for i in range(0, len(FILE), 4):
            if FILE[i] == '' or FILE[i] == '':
                print('pass')
                continue
            print(FILE[i])
            print(FILE[i + 1])
            print(FILE[i + 2])
            print(FILE[i + 3])
            Truen_thread ="Truen_GetHttp_thread.exe "+FILE[i]+" "+FILE[i+1]+" "+FILE[i+2]+" "+FILE[i+3]
            subprocess.Popen(Truen_thread, shell=False)
            time.sleep(1)
            print('thread start')
        print('thread end')
        ######
        FILE_Seyeon = []
        f2 = open("Seyeon_IP_Save.txt", 'r', encoding='UTF8')
        lines = f2.readlines()
        for line in lines:
            line = line.replace('\n', '')
            FILE_Seyeon.append(line)
        f2.close()
        print('1')
        # ### Seyeon 프로토콜 실행 ###
        # try:
        #     os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
        # except:
        #     print('정지할 프로세스가 없습니다')

        subprocess.Popen('Seyeon_GetHttp_thread.exe', shell=True)
        ###### 210 220 163 81

        self.detection_checking()

    def detection_checking(self):
        print('kk')
        filenames = os.listdir("Detection")
        for filename in filenames:
            full_filename = os.path.join("Detection", filename)
            #name#
            nm = full_filename[10:full_filename.find('_')]
            #IP#
            nm2 = full_filename[full_filename.find('192.'):full_filename.find('.txt')]
            #print(nm)
            #print(nm2)
            f = open(full_filename, 'r', encoding='UTF8')
            object = f.read()
            f.close()
            #print(full_filename)
            #print(object)
            self.Write_Table(nm, nm2, Object=object)
            try:
                arduino.write(b'y')
            except:
                pass

            try :
                os.remove(full_filename)
            except :
                pass
        #QTimer.singleShot(1000, self.table.show())
        threading.Timer(4,self.detection_checking).start()

    def Write_Table(self,name,Ip,Object):
        global table_Count
        # 표에 데이터 삽입
        #print('table')
        #print(table_Count)
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%m-%d %H:%M:%S')
        item1 = QTableWidgetItem(nowDatetime)
        item1.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 0, item1)
        #print('table2')
        item2 = QTableWidgetItem(name)
        item2.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 1, item2)
        #print('table3')
        item3 = QTableWidgetItem(Ip)
        item3.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 2, item3)
        #print('table4')
        item4 = QTableWidgetItem(Object)
        item4.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 3, item4)
        table_Count += 1
        #######update#######
        #print('update')
        # self.table.repaint()
        self.table.reset()
        ####################
        index = self.table.model().index(table_Count, 0)
        self.table.scrollTo(index)
        if table_Count > 99:
            table_Count = 0
            #self.WriteCsv()
            #self.ResetTable()
            self.table
        ##############################
    # Dialog 닫기 이벤트

    ########################################################
    # get http

    def ResetTable(self):
        global table_Count
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['시간', '이름', 'IP', '알람내용', '확인메모'])
        table_Count = 0

    def WriteCsv(self):
        Folder = "./ExcelData"
        if not os.path.isdir(Folder):
            os.mkdir(Folder)
        now = datetime.datetime.now()
        Nowtime = now.strftime('%m%d_%H_%M_%S')
        path = "./ExcelData/"+"Alarm_Data_"+Nowtime+".csv"
        print("saving", path)

        f = open(path, 'w', newline='')

        writer = csv.writer(f)
        for row in range(self.table.rowCount()):
            rowdata = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    rowdata.append(item.text())
                else:
                    rowdata.append('')
            writer.writerow(rowdata)
        self.isChanged = False
        f.close()

    ########################################################
    def Seyeon_Save_and_dialog_close(self,NAME, NM, IP, ID, PAS):

        f = open("Seyeon_NAME_Save.txt", 'w', encoding='UTF8')
        f.write(NAME.text())
        f.close()

        f = open("Seyeon_IP_Save.txt", 'w', encoding='UTF8')
        for i in range(0, 16):
            f.write(NM[i].text() + '\n')
            f.write(IP[i].text() + '\n')
            f.write(ID[i].text() + '\n')
            f.write(PAS[i].text() + '\n')
        f.close()
        #f = open("IP.txt",'w',encoding='UTF8')
        # for i in range(0,16):
        #     f.write(IP[i].text() + '\n')
        self.dialog.close()

    def Save_and_dialog_close(self,NAME, NM, IP, ID, PAS):

        f = open("NAME_Save.txt", 'w', encoding='UTF8')
        f.write(NAME.text())
        f.close()

        f = open("IP_Save.txt", 'w', encoding='UTF8')
        for i in range(0, 16):
            f.write(NM[i].text() + '\n')
            f.write(IP[i].text() + '\n')
            f.write(ID[i].text() + '\n')
            f.write(PAS[i].text() + '\n')
        f.close()
        f = open("IP.txt",'w',encoding='UTF8')
        # for i in range(0,16):
        #     f.write(IP[i].text() + '\n')
        self.dialog.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())