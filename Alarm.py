#!/usr/bin/env python3
import os
import time

import cv2
from ctypes import *

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from scapy.all import *

global table_Count
table_Count = 0
pwd = os.getcwd()
protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
try:
    os.mkdir('./Detection')
except:
    pass

try:
    os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
except:
    pass

try:
    os.system('taskkill /f /im Truen_GetHttp_thread.exe')
except:
    pass

light_dll = WinDLL(pwd+'/lib/Ux64_dllc.dll')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.soundCheck = 0

        self.event = threading.Event()

        # 메인 화면 설정
        self.setGeometry(300, 250, 1350, 600)  # x, y, w, h
        self.setFixedSize(1350, 600)
        self.setWindowTitle('Alarm Viewer')

        # QButton 위젯 폰트
        font = QtGui.QFont("맑은 고딕", 9)
        font.setBold(True)

        fontT = QtGui.QFont("맑은 고딕", 16)
        fontT.setBold(True)

        fontS = QtGui.QFont("맑은 고딕", 12)
        fontS.setBold(True)

        # 메인 화면 아이콘 설정
        self.setWindowIcon(QIcon(pwd+'/img/exelogo_inv.png'))

        # 배경 색상
        p = QPalette()
        p.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(p)

        # Seyeon IP 추가 버튼
        self.button0 = QPushButton('시작', self)
        # self.button0.clicked.connect(self.seyeon_ip_open)
        self.button0.clicked.connect(self.start_status)
        self.button0.clicked.connect(self.start)
        self.button0.setFont(font)
        self.button0.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button0.setGeometry(10, 10, 100, 50)
        self.button0.toggle()
        self.button0.setCheckable(True)
        self.button0.clicked.connect(self.start_status)

        # Truen IP 추가 버튼
        self.button1 = QPushButton('정지', self)
        # self.button1.clicked.connect(self.truen_ip_open)
        self.button1.setFont(font)
        self.button1.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button1.clicked.connect(self.stop_alarm)
        self.button1.clicked.connect(self.stop_status)
        self.button1.setGeometry(115, 10, 100, 50)
        self.button1.setDisabled(True)
        self.button1.clicked.connect(self.stop_status)

        # 시작 버튼
        # self.button2 = QPushButton('시작', self)
        # self.button2.clicked.connect(self.start_status)
        # self.button2.clicked.connect(self.start)
        # self.button2.setFont(font)
        # self.button2.setStyleSheet("color: white;"
        #                            "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
        #                            "border: 1px solid black;"
        #                            "border-radius: 20px;")
        # self.button2.setGeometry(610, 150, 100, 50)
        # self.button2.toggle()
        # self.button2.setCheckable(True)
        # self.button2.clicked.connect(self.start_status)

        # 저장 버튼
        self.button3 = QPushButton('저장 후 리셋', self)
        self.button3.clicked.connect(self.reset_table)
        self.button3.setFont(font)
        self.button3.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button3.setGeometry(490, 10, 100, 50)

        # 종료 버튼
        # self.button4 = QPushButton('정지', self)
        #
        # self.button4.setGeometry(610, 210, 100, 50)
        #
        # self.button4.toggle()
        # self.button4.setFont(font)
        # self.button4.clicked.connect(self.stop_alarm)
        # self.button4.clicked.connect(self.stop_status)
        # self.button4.setStyleSheet("color: white;"
        #                            "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
        #                            "border: 1px solid black;"
        #                            "border-radius: 20px;")
        # self.button4.setDisabled(True)
        # self.button4.clicked.connect(self.stop_status)

        # Alarm label
        self.Alarm = QLabel('Alarm Option', self)
        self.Alarm.move(400, 5)
        self.Alarm.setFont(font)

        # Sound ON radioButton
        self.rad1 = QRadioButton('Sound ON', self)
        self.rad1.move(400, 20)
        self.rad1.setFont(font)
        self.rad1.clicked.connect(self.sound_on)

        # Sound OFF radioButton
        self.rad2 = QRadioButton('Sound OFF', self)
        self.rad2.move(400, 40)
        self.rad2.setFont(font)
        self.rad2.setChecked(True)
        self.rad2.clicked.connect(self.sound_off)

        # Status check
        self.Status = QPushButton('STOP',self)
        self.Status.setGeometry(220,10,90,50)
        self.Status.setFont(font)
        self.Status.setStyleSheet("background-color:Red;"
                                  "color:white;"
                                  "border-color: 1px solid red;"
                                  "border-radius: 20px;")
        self.Status.setDisabled(True)

        # Table
        self.table = QTableWidget(self)
        self.table.setRowCount(100)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['시간', '이름', 'IP', '알람내용'])
        self.table.setFont(font)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 140)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 120)
        self.table.setGeometry(10, 70, 580, 505)
        self.table.setStyleSheet("color: black;"
                                 "background-color: white;"
                                 "border: 2px solid rgb(31,31,31);"
                                 "border-radius: 8px;")

        self.Print_L = QLabel(' . . . ', self)
        self.Print_L.setGeometry(10,570,730,20)
        self.Print_L.setFont(font)

        # QDialog 설정
        self.dialog = QDialog()
        self.dialog.setPalette(p)

        # Popup Dialog
        self.dialog2 = QDialog()
        self.dialog2.setWindowTitle('Alarm Popup')
        self.dialog2.setWindowIcon(QIcon(pwd + '/img/exelogo_inv.png'))
        self.dialog2.resize(850, 850)
        self.video_viewer_label = QLabel(self.dialog2)
        self.video_viewer_label.setGeometry(QRect(10, 10, 800, 800))


        #2023-04-20 add

        self.model = QLabel('Camera Lists',self)
        self.model.setFont(fontT)
        self.model.setGeometry(630, 30, 150, 20)

        #카메라 리스트
        nm_list = ['NM0', 'NM1', 'NM2', 'NM3', 'NM4', 'NM5', 'NM6', 'NM7', 'NM8', 'NM9', 'NM10', 'NM11', 'NM12', 'NM13',
                   'NM14', 'NM15']
        ip_list = ['IP0', 'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8', 'IP9', 'IP10', 'IP11', 'IP12', 'IP13',
                   'IP14', 'IP15']
        id_list = ['ID0', 'ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'ID8', 'ID9', 'ID10', 'ID11', 'ID12', 'ID13',
                   'ID14', 'ID15']
        ps_list = ['PS0', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9', 'PS10', 'PS11', 'PS12', 'PS13',
                   'PS14', 'PS15']
        md_list = ['md0','md1','md2','md3','md4','md5','md6','md7','md8','md9','md10','md11','md12','md13',
                   'md14','md15']
        st_list = ['st0','st1','st2','st3','st4','st5','st6','st7','st8','st9','st10','st11','st12','st13','st14','st15']

        #카메라 리스트 작성란
        for i in range(0,16):
            nm_list = QLineEdit(self)
            nm_list.setGeometry(630, 90+30*i, 70, 30)

            md_list = QComboBox(self)
            md_list.setFont(font)
            md_list.addItem('8020')
            md_list.addItem('3204')
            md_list.setGeometry(700, 90+30*i, 70, 30)

            ip_list = QLineEdit(self)
            ip_list.setFont(font)
            ip_list.setGeometry(770, 90 + 30 * i, 100, 30)

            id_list = QLineEdit(self)
            id_list.setFont(font)
            id_list.setGeometry(870, 90+30*i,70,30)

            ps_list = QLineEdit(self)
            ps_list.setFont(font)
            ps_list.setGeometry(940, 90 + 30 * i, 70, 30)

            st_list = QPushButton(self)
            st_list.setText('ON')
            st_list.setDisabled(True)
            st_list.setFont(font)
            st_list.setGeometry(1010, 90+30*i, 70, 30)
            st_list.setStyleSheet("background-color:White;"
                                      "color:Black;"
                                  "border: 1px solid Black;")

        #카메라 리스트 인덱스 라벨
        self.namel = QLabel('이름',self)
        self.namel.setFont(fontT)
        self.namel.setGeometry(630, 55, 50, 40)

        self.modell = QLabel('모델명', self)
        self.modell.setFont(fontT)
        self.modell.setGeometry(700, 55, 70, 40)

        self.ipl = QLabel('IP', self)
        self.ipl.setFont(fontT)
        self.ipl.setAlignment(Qt.AlignCenter)
        self.ipl.setGeometry(790, 55, 70, 40)

        self.idl = QLabel('ID', self)
        self.idl.setFont(fontT)
        self.idl.setAlignment(Qt.AlignCenter)
        self.idl.setGeometry(870, 55, 70, 40)

        self.psl = QLabel('PASS', self)
        self.psl.setFont(fontT)
        self.psl.setAlignment(Qt.AlignCenter)
        self.psl.setGeometry(940, 55, 70, 40)

        self.stl = QLabel('Status', self)
        self.stl.setFont(fontT)
        self.stl.setAlignment(Qt.AlignCenter)
        self.stl.setGeometry(1010,55,70,40)

        #로그인 메뉴
        self.login = QLineEdit(self)
        self.login.setFont(font)
        self.login.setGeometry(800,5,80,30)

        self.login2 = QPushButton('LogIn',self)
        self.login2.setFont(font)
        self.login2.setGeometry(880,5,50,30)

        self.login3 = QPushButton('save',self)
        self.login3.setFont(font)
        self.login3.setGeometry(930,5,50,30)

        #알람설정 & 테스트 모드 라벨
        self.onoff = QLabel('알람 설정',self)
        self.onoff.setFont(fontT)
        self.onoff.setGeometry(1090, 55, 200, 40)

        self.onoff = QLabel('Test Mode', self)
        self.onoff.setFont(fontT)
        self.onoff.setGeometry(1220, 55, 200, 40)

        alarmon = ['alarmon0','alarmon1','alarmon2','alarmon3','alarmon4','alarmon5','alarmon6','alarmon7','alarmon8'
            ,'alarmon9','alarmon10','alarmon11','alarmon12','alarmon13','alarmon14','alarmon15']
        alarmoff = ['alarmoff0','alarmoff1','alarmoff2','alarmoff3','alarmoff4','alarmoff5','alarmoff6','alarmoff7'
            ,'alarmoff8','alarmoff9','alarmoff10','alarmoff11','alarmoff12','alarmoff13','alarmoff14','alarmoff15']
        test = ['test0','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10','test11'
            ,'test12','test13','test14','test15']
        #알람설정 & 테스트 모드 버튼
        for i in range(0,16):
            alarmon[i] = QPushButton('ON',self)
            alarmon[i].setGeometry(1090, 95 + 30*i, 50, 30)
            alarmon[i].setFont(font)

            alarmoff[i] = QPushButton('OFF', self)
            alarmoff[i].setGeometry(1140, 95 + 30*i, 50, 30)
            alarmoff[i].setFont(font)

            test[i] = QPushButton(self)
            test[i].setText('ON')
            test[i].setGeometry(1220, 95 + 30 * i, 100, 30)
            test[i].setFont(font)

        #알람 모두 활성화/비활성화 버튼
        self.allon = QPushButton('ON',self)
        self.allon.setFont(font)
        self.allon.setGeometry(1090, 27, 50, 30)
        self.alloff = QPushButton('OFF', self)
        self.alloff.setFont(font)
        self.alloff.setGeometry(1140, 27, 50, 30)

        #알람 모두 활성화/비활성화 라벨
        self.allalarm = QLabel('전체 제어',self)
        self.allalarm.setFont(fontS)
        self.allalarm.setGeometry(1090, 0, 100, 40)

    def start_status(self):
        font = QtGui.QFont("맑은 고딕", 9)
        font.setBold(True)
        self.Status.setText('START')
        self.Status.setFont(font)
        self.Status.setStyleSheet("background-color: Green;"
                                  "color:white;"
                                  "border-color: 1px solid Green;"
                                  "border-radius: 20px;")
    def stop_status(self):
        font = QtGui.QFont("맑은 고딕", 9)
        font.setBold(True)
        self.Status.setText('STOP')
        self.Status.setFont(font)
        self.Status.setStyleSheet("background-color:Red;"
                                  "color:white;"
                                  "border-color: 1px solid red;"
                                  "border-radius: 20px;")
    def sound_on(self):
        self.soundCheck = 1

    def sound_off(self):
        self.soundCheck = 0

    # 버튼 이벤트 함수
    def seyeon_ip_open(self):
        # 버튼 추가
        ############## LINE ###############

        nm_list = ['NM0', 'NM1', 'NM2', 'NM3', 'NM4', 'NM5', 'NM6', 'NM7', 'NM8', 'NM9', 'NM10', 'NM11', 'NM12', 'NM13',
              'NM14', 'NM15']
        ip_list = ['IP0', 'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8', 'IP9', 'IP10', 'IP11', 'IP12', 'IP13',
              'IP14', 'IP15']
        id_list = ['ID0', 'ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'ID8', 'ID9', 'ID10', 'ID11', 'ID12', 'ID13',
              'ID14', 'ID15']
        ps_list = ['PS0', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9', 'PS10', 'PS11', 'PS12', 'PS13',
              'PS14', 'PS15']

        ##############NAME 텍스트 값 불러오기###############
        name_read = []
        try:
            self.seyeon_read_file(name_read, 'NAME')
        except:
            pass
        ###############################################
        ##############iplist 텍스트 값 불러오기###############
        ip_read = []
        try:
            self.seyeon_read_file(ip_read, 'iplist')
        except:
            pass
        ###############################################

        my_font = QtGui.QFont("Arial", 11)
        my_font.setBold(True)
        explain1 = QLabel('NAME                      IP                             ID                        '
                          'PASS', self.dialog)
        explain1.setFont(my_font)
        explain1.setStyleSheet("color: black;")
        explain1.move(22, 64)

        button_font = QtGui.QFont("Calibri", 11)
        button_font.setBold(True)

        try:
            name = QLineEdit(name_read[0], self.dialog)
        except:
            name = QLineEdit('', self.dialog)
        name.resize(130, 25)
        name.move(20, 20)

        k = 0
        for i in range(0, 16):

            try:
                nm_list[i] = QLineEdit(ip_read[k], self.dialog)
            except:
                nm_list[i] = QLineEdit('', self.dialog)
            nm_list[i].resize(130, 25)
            nm_list[i].move(20, 85 + 25 * i)
            try:
                ip_list[i] = QLineEdit(ip_read[k + 1], self.dialog)
            except:
                ip_list[i] = QLineEdit('', self.dialog)
            ip_list[i].resize(130, 25)
            ip_list[i].move(150, 85 + 25 * i)
            try:
                id_list[i] = QLineEdit(ip_read[k + 2], self.dialog)
            except:
                id_list[i] = QLineEdit('', self.dialog)
            id_list[i].resize(110, 25)
            id_list[i].move(280, 85 + 25 * i)
            try:
                ps_list[i] = QLineEdit(ip_read[k + 3], self.dialog)
            except:
                ps_list[i] = QLineEdit('', self.dialog)
            ps_list[i].setEchoMode(QLineEdit.Password)
            ps_list[i].resize(110, 25)
            ps_list[i].move(390, 85 + 25 * i)
            k += 4

        save_button = QPushButton('SAVE', self.dialog)
        save_button.resize(100, 26)
        save_button.move(170, 20)
        save_button.setFont(my_font)
        save_button.clicked.connect(lambda: self.seyeon_save_and_dialog_close(name, nm_list, ip_list, id_list, ps_list))
        save_button.setStyleSheet("color: white;"
                            "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                            "border: 1px solid black;"
                            "border-radius: 20px;")
        #######load버튼############
        # LoadB = QPushButton('LOAD', self.dialog)
        # LoadB.resize(100,26)
        # LoadB.move(320,20)
        # LoadB.setFont(myFont)
        # LoadB.clicked.connect(lambda: self.Load_Seyeon(Name, nmlist, iplist, id_list, PS))
        # LoadB.setStyleSheet("color: white;"
        #                 "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
        #                 "border: 1px solid black;"
        #                 "border-radius: 20px;")

        # QDialog 세팅
        self.dialog.setWindowTitle('9302/8020')
        self.dialog.setWindowIcon(QIcon(pwd+'/img/exelogo_inv.png'))
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setFixedSize(520, 500)
        self.dialog.show()

    def truen_ip_open(self):
        # 버튼 추가
        ############## LINE ###############

        nm_list = ['NM0', 'NM1', 'NM2', 'NM3', 'NM4', 'NM5', 'NM6', 'NM7', 'NM8', 'NM9', 'NM10', 'NM11', 'NM12', 'NM13',
              'NM14', 'NM15']
        ip_list = ['IP0', 'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8', 'IP9', 'IP10', 'IP11', 'IP12', 'IP13',
              'IP14', 'IP15']
        id_list = ['ID0', 'ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'ID8', 'ID9', 'ID10', 'ID11', 'ID12', 'ID13',
              'ID14', 'ID15']
        ps_list = ['PS0', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9', 'PS10', 'PS11', 'PS12', 'PS13',
              'PS14', 'PS15']
        # ST = ['ST0', 'ST1', 'ST2', 'ST3', 'ST4', 'ST5', 'ST6', 'ST7', 'ST8', 'ST9', 'ST10', 'ST11', 'ST12',
        #       'ST13', 'ST14', 'ST15']

        ##############NAME 텍스트 값 불러오기###############
        name_read = []
        try:
            self.read_file(name_read, 'NAME')

        except:
            pass
        ###############################################
        ##############IP 텍스트 값 불러오기###############
        ip_read = []
        try:
            self.read_file(ip_read, 'IP')
        except:
            pass
        ###############################################

        my_font = QtGui.QFont("Arial", 11)
        my_font.setBold(True)
        explain1 = QLabel('NAME                      IP                             ID                        '
                          'PASS', self.dialog)
        explain1.setFont(my_font)
        explain1.move(22, 64)

        button_font = QtGui.QFont("Calibri", 11)
        button_font.setBold(True)

        try:
            name = QLineEdit(name_read[0], self.dialog)
        except:
            name = QLineEdit('', self.dialog)
        name.resize(130, 25)
        name.move(20, 20)

        k = 0
        for i in range(0, 16):

            try:
                nm_list[i] = QLineEdit(ip_read[k], self.dialog)
            except:
                nm_list[i] = QLineEdit('', self.dialog)
            # NM[i].setAlignment(Qt.AlignCenter)
            nm_list[i].resize(130, 25)
            nm_list[i].move(20, 85 + 25 * i)
            try:
                ip_list[i] = QLineEdit(ip_read[k + 1], self.dialog)
            except:
                ip_list[i] = QLineEdit('', self.dialog)
            # LE[i].setAlignment(Qt.AlignCenter)
            ip_list[i].resize(130, 25)
            ip_list[i].move(150, 85 + 25 * i)
            try:
                id_list[i] = QLineEdit(ip_read[k + 2], self.dialog)
            except:
                id_list[i] = QLineEdit('', self.dialog)
            # ID[i].setAlignment(Qt.AlignCenter)
            id_list[i].resize(110, 25)
            id_list[i].move(280, 85 + 25 * i)
            try:
                ps_list[i] = QLineEdit(ip_read[k + 3], self.dialog)
            except:
                ps_list[i] = QLineEdit('', self.dialog)
            ps_list[i].setEchoMode(QLineEdit.Password)
            # PS[i].setAlignment(Qt.AlignCenter)
            ps_list[i].resize(110, 25)
            ps_list[i].move(390, 85 + 25 * i)
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

        save_button = QPushButton('SAVE', self.dialog)
        save_button.resize(100, 26)
        save_button.move(170, 20)
        save_button.setFont(my_font)
        save_button.clicked.connect(lambda: self.save_and_dialog_close(name, nm_list, ip_list, id_list, ps_list))
        save_button.setStyleSheet("color: white;"
                            "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                            "border: 1px solid black;"
                            "border-radius: 20px;")
        # StartB.clicked.connect(lambda: self.Start(Name, NM, IP, ID, PS, ST))
        ##################load버튼##################
        # LoadB = QPushButton('LOAD', self.dialog)
        # LoadB.resize(100,26)
        # LoadB.move(320,20)
        # LoadB.setFont(myFont)
        # LoadB.clicked.connect(lambda: self.Load_Name(Name, NM, IP, ID, PS))
        # LoadB.setStyleSheet("color: white;"
        #                 "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
        #                 "border: 1px solid black;"
        #                 "border-radius: 20px;")

        # btnDialog = QPushButton("OK", self.dialog)
        # btnDialog.move(100, 100)
        # btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('X3204')
        self.dialog.setWindowIcon(QIcon(pwd+'/img/exelogo_inv.png'))
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setFixedSize(520, 500)
        self.dialog.show()

    def seyeon_read_file(self, FILE, Case):
        if Case == 'NAME':
            f = open(pwd+"/config/Seyeon_NAME_Save.txt", 'r', encoding='UTF8')
            t = f.read()
            FILE.append(t)
            f.close()
        elif Case == 'IP':
            f = open(pwd+"/config/Seyeon_IP_Save.txt", 'r', encoding='UTF8')
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                FILE.append(line)
            f.close()

    def read_file(self, FILE, Case):
        if Case == 'NAME' :
            f = open(pwd+"/config/Truen_NAME_Save.txt", 'r', encoding='UTF8')
            t = f.read()
            FILE.append(t)
            f.close()
        elif Case == 'IP' :
            f = open(pwd+"/config/Truen_IP_Save.txt", 'r', encoding='UTF8')
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                FILE.append(line)
            f.close()

    def start(self):
        try:
            os.system('taskkill /f /im Truen_GetHttp_thread.exe')
            os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
        except:
            self.Print_L.setText("Not process")

        ### Truen 프로토콜 실행 ###
        subprocess.Popen(pwd+"/Thread/Truen_GetHttp_thread.exe", shell=True)
        self.Print_L.setText('Truen IP search start')
        time.sleep(1)

        # ### Seyeon 프로토콜 실행 ###
        subprocess.Popen(pwd+'/Thread/Seyeon_GetHttp_thread.exe', shell=True)
        self.Print_L.setText('Seyeon IP search start')

        self.event = threading.Event()
        self.button0.setDisabled(True)
        self.button1.setEnabled(True)
        self.Print_L.setText('searching . . .')
        self.detection_checking()

    def detection_checking(self):
        filenames = os.listdir("Detection")
        for filename in filenames:
            self.Print_L.setText('Detect')
            full_filename = os.path.join("Detection", filename)
            # name#
            nm = full_filename[10:full_filename.find('_')]
            # IP#
            nm2 = full_filename[full_filename.find('192.'):full_filename.find('.txt')]
            f = open(full_filename, 'r', encoding='UTF8')
            object_list = f.read().split("\n")
            object_name, object_ip, object_maker, object_id, object_pas = object_list
            f.close()
            self.write_table(nm, nm2, object_in=object_name)
            try:
                self.alarm_controller(red=2, sound=self.soundCheck)
                time.sleep(2)
                self.alarm_controller(red=0, sound=0)
            except:
                self.Print_L.setText('Alarm controller error')
                pass
            try :
                threading.Thread(self.show_dialog(object_ip, object_maker, object_id, object_pas)).start()
                os.remove(full_filename)
            except:
                self.Print_L.setText('Pop up error')
                pass
        if self.event.is_set():
            return
        #QTimer.singleShot(1000, self.table.show())

        threading.Timer(5,self.detection_checking).start()
        
    def show_dialog(self, ip, maker, id, pas):
        self.show_image(ip, maker, id, pas)
        return

    def show_image(self, ip, maker, id, pas):
        register = id+':'+pas+'@'+ip
        if 'Sey' in maker:
            connector = 'rtsp://'+register+'/cam0_1'
        else:
            connector = 'rtsp://'+register+'/video1'
        cap = cv2.VideoCapture(connector)
        width, height, channel = 800, 800, 3
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        second = 3
        count = 0
        self.dialog2.show()
        while fps*second > count:
            count+=1
            ret, img = cap.read()
            img = cv2.resize(img, (width, height))
            bgr2rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qt_img = QImage(bgr2rgb.data,
                                  width, height, width * channel,
                                  QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            self.video_viewer_label.setPixmap(pixmap)
            if cv2.waitKey(fps) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        self.dialog2.close()

    def write_table(self, name, ip_in, object_in):
        global table_Count
        # 표에 데이터 삽입
        now = datetime.now()
        now_datetime = now.strftime('%m-%d %H:%M:%S')

        item1 = QTableWidgetItem(now_datetime)
        item1.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 0, item1)

        item2 = QTableWidgetItem(name)
        item2.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 1, item2)

        item3 = QTableWidgetItem(ip_in)
        item3.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 2, item3)

        item4 = QTableWidgetItem(object_in)
        item4.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 3, item4)
        table_Count += 1

        self.table.reset()

        index = self.table.model().index(table_Count, 0)
        self.table.scrollTo(index)
        if table_Count > 99:
            table_Count = 0
            self.write_txt()
            self.reset_table()

    def reset_table(self):
        global table_Count
        self.write_txt()
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['시간', '이름', 'IP', '알람내용'])
        table_Count = 0

    def write_txt(self):
        folder = pwd+"/LogData"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        now = datetime.now()
        now_time = now.strftime('%m%d_%H_%M_%S')
        
        path = pwd+"/LogData/" + "Alarm_Data_" + now_time + ".txt"

        self.Print_L.setText("Save : " + path)

        writer = open(path, 'w', newline='')

        txt = ""
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    txt += item.text() + " "
                else:
                    txt += ''
            txt += '\n'
        writer.write(txt)
        self.isChanged = False
        writer.close()

    ########################################################
    def seyeon_save_and_dialog_close(self, name_list, nm_list, ip_list, id_list, pas_list):

        f = open(pwd+"/config/Seyeon_NAME_Save.txt", 'w', encoding='UTF8')
        f.write(name_list.text())
        f.close()

        f = open(pwd+"/config/Seyeon_IP_Save.txt", 'w', encoding='UTF8')
        for i in range(16):
            f.write(nm_list[i].text() + '\n')
            f.write(ip_list[i].text() + '\n')
            f.write(id_list[i].text() + '\n')
            f.write(pas_list[i].text() + '\n')
        f.close()

        self.dialog.close()

    def save_and_dialog_close(self, name_list, nm_list, ip_list, id_list, pas_list):

        f = open(pwd+"/config/Truen_NAME_Save.txt", 'w', encoding='UTF8')
        f.write(name_list.text())
        f.close()

        f = open(pwd+"/config/Truen_IP_Save.txt", 'w', encoding='UTF8')
        for i in range(0, 16):
            f.write(nm_list[i].text() + '\n')
            f.write(ip_list[i].text() + '\n')
            f.write(id_list[i].text() + '\n')
            f.write(pas_list[i].text() + '\n')
        f.close()
        self.dialog.close()

    def load_seyeon(self, name_list, nm_list, ip_list, id_list, pas_list):
        dial = QFileDialog.getOpenFileNames(self, 'open file', '~')

    def load_name(self, name_list, nm_list, ip_list, id_list, pas_list):
        dial = QFileDialog.getOpenFileNames(self, 'open file', '~')

        dial2 = QDialog()

    def stop_alarm(self):
        try:
            os.system('taskkill /f /im Truen_GetHttp_thread.exe')
            os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
            self.event.set()
            self.button0.setEnabled(True)
            self.button1.setDisabled(True)
            self.alarm_controller(red=0, sound=0)
        except:
            self.Print_L.setText('There is no process to stop.')
        self.Print_L.setText('All process to stop.')


    def ligth_status_check(self):
        state = light_dll['Usb_Qu_Getstate']()
        if state == 0x1:
            return 0
        elif state == 0x2:
            return 1
        elif state == 0x4:
            return 2
        elif state == 0x8:
            return 3
        else:
            self.Print_L.setText("Not Connect Usb")
        return 10

    class ArrayStruct(Structure):
        _fields_ = [("char_t", POINTER(c_char))]

    def alarm_controller(self, red, yellow=0, green=0, blue=0, white=0, sound=0):
        c_index = self.ligth_status_check()
        if c_index == 10:
            return
        c_type = 0

        c_char_t = self.ArrayStruct()
        c_char_t.char_t = (c_char * 6)(red, yellow, green, blue, white, sound)
        usb_qu_write = light_dll['Usb_Qu_write'](c_index, c_type, c_char_t.char_t)
        return usb_qu_write


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())