#!/usr/bin/env python3
import os

from ctypes import *

from PyQt5 import QtGui
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

        # 윈도우 설정
        self.setGeometry(500, 250, 740, 410)  # x, y, w, h
        self.setFixedSize(740, 410)
        self.setWindowTitle('Alarm Viewer')

        # QButton 위젯 생성
        Font = QtGui.QFont("맑은 고딕", 9)
        Font.setBold(True)

        self.setWindowIcon(QIcon(pwd+'/img/exelogo_inv.png'))

        p = QPalette()
        p.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(p)

        self.button0 = QPushButton('9302/8020 등록', self)
        self.button0.clicked.connect(self.Seyeon_IP_open)
        self.button0.setFont(Font)
        self.button0.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button0.setGeometry(10, 10, 100, 50)

        self.button1 = QPushButton('3204 등록', self)
        self.button1.clicked.connect(self.IP_open)
        self.button1.setFont(Font)
        self.button1.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button1.setGeometry(115, 10, 100, 50)

        self.button2 = QPushButton('시작', self)
        self.button2.clicked.connect(self.Start)
        self.button2.setFont(Font)
        self.button2.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button2.setGeometry(410, 10, 100, 50)
        self.button2.toggle()
        self.button2.setCheckable(True)

        self.button3 = QPushButton('저장 후 리셋', self)
        self.button3.clicked.connect(self.ResetTable)
        self.button3.setFont(Font)
        self.button3.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button3.setGeometry(625, 10, 100, 50)

        self.button4 = QPushButton('정지', self)
        self.button4.setGeometry(520, 10, 100, 50)

        self.button4.toggle()
        self.button4.setFont(Font)
        self.button4.clicked.connect(self.StopAlarm)
        self.button4.setStyleSheet("color: white;"
                                   "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                   "border: 1px solid black;"
                                   "border-radius: 20px;")
        self.button4.setDisabled(True)

        self.Alarm = QLabel('Alarm Option', self)
        self.Alarm.move(600, 120)
        self.Alarm.setFont(Font)

        self.rad1 = QRadioButton('Sound ON', self)
        self.rad1.move(600, 150)
        self.rad1.setFont(Font)
        self.rad1.clicked.connect(self.SoundOn)
        self.rad2 = QRadioButton('Sound OFF', self)
        self.rad2.move(600, 180)
        self.rad2.setFont(Font)
        self.rad2.setChecked(True)
        self.rad2.clicked.connect(self.SoundOff)
        self.Status = QLabel('STOP',self)
        self.Status.move(650,320)
        self.Status.setFont(Font)
        self.Status.setStyleSheet("color:Red;")
        self.button2.clicked.connect(self.startstatus)
        self.button4.clicked.connect(self.stopstatus)

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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['시간', '이름', 'IP', '알람내용'])
        self.table.setFont(Font)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 140)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 120)
        self.table.setGeometry(10, 70, 580, 328)
        self.table.setStyleSheet("color: black;"
                                 "background-color: white;"
                                 "border: 2px solid rgb(31,31,31);"
                                 "border-radius: 8px;")

        # QDialog 설정
        self.dialog = QDialog()
        self.dialog2 = QDialog()

        p = QPalette()
        p.setColor(QPalette.Background, QColor(255, 255, 255))
        self.dialog.setPalette(p)
    def startstatus(self):
        Font = QtGui.QFont("맑은 고딕", 9)
        Font.setBold(True)
        self.Status.setText('START')
        self.Status.setFont(Font)
        self.Status.setStyleSheet("color:blue;")
    def stopstatus(self):
        Font = QtGui.QFont("맑은 고딕", 9)
        Font.setBold(True)
        self.Status.setText('STOP')
        self.Status.setFont(Font)
        self.Status.setStyleSheet("color:red;")
    def SoundOn(self):
        self.soundCheck = 1

    def SoundOff(self):
        self.soundCheck = 0

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
        Explain1.setStyleSheet("color: black;")
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
        SaveB.setStyleSheet("color: white;"
                            "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                            "border: 1px solid black;"
                            "border-radius: 20px;")
        # StartB.clicked.connect(lambda: self.Start(Name, NM, IP, ID, PS, ST))
        #######load버튼############
        # LoadB = QPushButton('LOAD', self.dialog)
        # LoadB.resize(100,26)
        # LoadB.move(320,20)
        # LoadB.setFont(myFont)
        # LoadB.clicked.connect(lambda: self.Load_Seyeon(Name, NM, IP, ID, PS))
        # LoadB.setStyleSheet("color: white;"
        #                 "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
        #                 "border: 1px solid black;"
        #                 "border-radius: 20px;")

        # btnDialog = QPushButton("OK", self.dialog)
        # btnDialog.move(100, 100)
        # btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('9302/8020')
        self.dialog.setWindowIcon(QIcon(pwd+'/img/exelogo_inv.png'))
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setFixedSize(520, 500)
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
        SaveB.clicked.connect(lambda: self.Save_and_dialog_close(Name, NM, IP, ID, PS))
        SaveB.setStyleSheet("color: white;"
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

    def Seyeon_Read_file(self, FILE, Case):

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


    def Read_file(self,FILE,Case):
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

    def Start(self):
        try:
            os.system('taskkill /f /im Truen_GetHttp_thread.exe')
            os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
        except:
            print("Not process")

        ### Truen 프로토콜 실행 ###

        subprocess.Popen(pwd+"/Thread/Truen_GetHttp_thread.exe", shell=True)
        time.sleep(1)
        print('Truen IP search start')

        # ### Seyeon 프로토콜 실행 ###

        subprocess.Popen(pwd+'/Thread/Seyeon_GetHttp_thread.exe', shell=True)
        print('Seyeon IP search start')

        self.event = threading.Event()
        self.button2.setDisabled(True)
        self.button4.setEnabled(True)
        self.detection_checking()

    def detection_checking(self):
        print('searching . . .')
        filenames = os.listdir("Detection")
        for filename in filenames:
            full_filename = os.path.join("Detection", filename)
            # name#
            nm = full_filename[10:full_filename.find('_')]
            # IP#
            nm2 = full_filename[full_filename.find('192.'):full_filename.find('.txt')]
            f = open(full_filename, 'r', encoding='UTF8')
            object = f.read()
            f.close()
            self.Write_Table(nm, nm2, Object=object)
            try:
                self.alarm_controll(red=2, sound=self.soundCheck)
                time.sleep(2)
                self.alarm_controll(red=0, sound=0)
            except:
                pass
            try :
                os.remove(full_filename)
            except:
                pass

        if self.event.is_set():
            return
        #QTimer.singleShot(1000, self.table.show())
        threading.Timer(4,self.detection_checking).start()
        
    def showdialog(self):

        self.dialog2.setWindowTitle('Alarm Popup')
        self.dialog2.setWindowIcon(QIcon(pwd+'/img/exelogo_inv.png'))
        # self.dialog2.setWindowModality(Qt.ApplicationModal)
        self.dialog2.resize(520, 500)
        log = QLabel('IP', self.dialog2)
        log.move(170, 20)
        self.dialog2.show()
        time.sleep(2)
        self.dialog2.close()

    def Write_Table(self, name, Ip, Object):
        global table_Count
        # 표에 데이터 삽입
        now = datetime.now()
        nowDatetime = now.strftime('%m-%d %H:%M:%S')

        item1 = QTableWidgetItem(nowDatetime)
        item1.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 0, item1)

        item2 = QTableWidgetItem(name)
        item2.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 1, item2)

        item3 = QTableWidgetItem(Ip)
        item3.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 2, item3)

        item4 = QTableWidgetItem(Object)
        item4.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(table_Count, 3, item4)
        table_Count += 1

        self.table.reset()

        index = self.table.model().index(table_Count, 0)
        self.table.scrollTo(index)
        if table_Count > 99:
            table_Count = 0
            self.WriteTxT()
            self.ResetTable()

    def ResetTable(self):
        global table_Count
        self.WriteTxT()
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['시간', '이름', 'IP', '알람내용'])
        table_Count = 0

    def WriteTxT(self):
        Folder = pwd+"/LogData"
        if not os.path.isdir(Folder):
            os.mkdir(Folder)
        now = datetime.now()
        Nowtime = now.strftime('%m%d_%H_%M_%S')
        
        path = pwd+"/LogData/" + "Alarm_Data_" + Nowtime + ".txt"

        print("saving", path)

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
    def Seyeon_Save_and_dialog_close(self, NAME, NM, IP, ID, PAS):

        f = open(pwd+"/config/Seyeon_NAME_Save.txt", 'w', encoding='UTF8')
        f.write(NAME.text())
        f.close()

        f = open(pwd+"/config/Seyeon_IP_Save.txt", 'w', encoding='UTF8')
        for i in range(0, 16):
            f.write(NM[i].text() + '\n')
            f.write(IP[i].text() + '\n')
            f.write(ID[i].text() + '\n')
            f.write(PAS[i].text() + '\n')
        f.close()

        self.dialog.close()

    def Save_and_dialog_close(self, NAME, NM, IP, ID, PAS):

        f = open(pwd+"/config/Truen_NAME_Save.txt", 'w', encoding='UTF8')
        f.write(NAME.text())
        f.close()

        f = open(pwd+"/config/Truen_IP_Save.txt", 'w', encoding='UTF8')
        for i in range(0, 16):
            f.write(NM[i].text() + '\n')
            f.write(IP[i].text() + '\n')
            f.write(ID[i].text() + '\n')
            f.write(PAS[i].text() + '\n')
        f.close()
        self.dialog.close()

    def Load_Seyeon(self, Name, NM, IP, ID, PS):
        dial = QFileDialog.getOpenFileNames(self, 'open file', '~')

    def Load_Name(self, Name, NM, IP, ID, PS):
        dial = QFileDialog.getOpenFileNames(self, 'open file', '~')

        dial2 = QDialog()

    def StopAlarm(self):
        try:
            os.system('taskkill /f /im Truen_GetHttp_thread.exe')
            os.system('taskkill /f /im Seyeon_GetHttp_thread.exe')
            self.event.set()
            self.button2.setEnabled(True)
            self.button4.setDisabled(True)
            self.alarm_controll(red=0, sound=0)
        except:
            print('정지할 프로세스가 없습니다')

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
            print("Not Connect Usb")
        return

    class ArrayStruct(Structure):
        _fields_ = [("char_t", POINTER(c_char))]

    def alarm_controll(self, red, yellow=0, green=0, blue=0, white=0, sound=0):
        C_index = self.ligth_status_check()
        C_type = 0

        c_char_t = self.ArrayStruct()
        c_char_t.char_t = (c_char * 6)(red, yellow, green, blue, white, sound)
        Usb_Qu_write = light_dll['Usb_Qu_write'](C_index, C_type, c_char_t.char_t)
        return Usb_Qu_write


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())