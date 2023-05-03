import os
import threading

import cv2
import json
import requests
import winsound

from ctypes import *
from PyQt5 import QtGui
from copy import deepcopy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from scapy.all import *
from requests.auth import HTTPDigestAuth

pwd = os.getcwd()
protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
try:
    os.mkdir('./Detection')
except:
    pass

try:
    os.system('taskkill /f /im GetHttp_thread.exe')
except:
    pass

light_dll = WinDLL(pwd + '/lib/Ux64_dllc.dll')

version = "2.1.230503"


def data2dic(txt, model):
    data_dic = {}
    if model == '3204':
        data = txt.rsplit('\n\r\n')[0].split('=')
        data_dic[data[0]] = data[1]
    else:
        data = list(txt.split('\r\n\r\n'))[2:4]
        for i in data:
            k = i.strip(' ').strip(';').split(';\r\n')
            for j in k:
                p = j.split('=')
                data_dic[p[0]] = p[1]
    return data_dic


def ligth_status_check():
    state = light_dll['Usb_Qu_Getstate']()
    if state == 0x1:
        return 0
    elif state == 0x2:
        return 1
    elif state == 0x4:
        return 2
    elif state == 0x8:
        return 3
    return 10


def read_json():
    f = open(os.path.join(pwd, "config/ip_data.json"), 'r', encoding='utf-8')
    j_data = json.load(f)
    f.close()
    return j_data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # font set
        self.table_Count = 0
        self.c_index = 10
        self.font_k9 = QtGui.QFont("맑은 고딕", 9)
        self.font_k13 = QtGui.QFont("맑은 고딕", 13)
        self.font_k12 = QtGui.QFont("맑은 고딕", 12)
        self.font_ecam12 = QtGui.QFont("cambria", 12)
        self.font_ecal9 = QtGui.QFont("calibri", 9)
        self.font_ecam9 = QtGui.QFont("cambria", 9)
        self.font_Tcam = QtGui.QFont("cambria",10)

        self.video_viewer_label = None
        self.popup_dialog = QDialog()
        self.dialog = QDialog()
        self.alarm_table = QTableWidget(self)
        self.table_off_list = [QPushButton('OFF') for _ in range(100)]

        self.Print_L = QLabel(' . . . ', self)
        self.running_status = QPushButton('STOP', self)
        self.alarm_radoff = QRadioButton('Sound OFF', self)
        self.alarm_radon = QRadioButton('Sound ON', self)
        # self.alarm_label = QLabel('Alarm Option', self)
        self.save_reset = QPushButton('SAVE RESET', self)
        self.start_button = QPushButton('START', self)
        self.stop_button = QPushButton('STOP', self)

        self.area_name = QLineEdit(self)
        self.alarm_status = QLabel('STATUS', self)
        self.pwd_label = QLabel('PASS', self)
        self.id_label = QLabel('ID', self)
        self.ip_label = QLabel('IP', self)
        self.model_label = QLabel('MODEL', self)
        # self.right_label = QLabel('Camera Lists', self)
        self.name_label = QLabel('NAME', self)
        self.login = QPushButton('LOGIN', self)
        self.save = QPushButton('SAVE', self)
        self.all_onoff_label = QLabel('ALARM', self)
        self.test_label = QLabel('TEST', self)

        self.nm_list = [QLineEdit(self) for _ in range(16)]
        self.ip_list = [QLineEdit(self) for _ in range(16)]
        self.id_list = [QLineEdit(self) for _ in range(16)]
        self.ps_list = [QLineEdit(self) for _ in range(16)]
        self.st_list = [QLineEdit('N/A', self) for _ in range(16)]
        self.md_list = [QComboBox(self) for _ in range(16)]
        self.alarm_on_list = [QPushButton('ON', self) for _ in range(16)]
        self.alarm_off_list = [QPushButton('OFF', self) for _ in range(16)]
        self.test_list = [QPushButton('ON', self) for _ in range(16)]
        self.all_off_button = QPushButton('ALL OFF', self)
        self.all_on_button = QPushButton('ALL ON', self)
        self.state = 10

        self.process_apply = "stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), " \
                             "stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
        self.process_dis = "stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(90, 97, 101, 255), " \
                           "stop:0.935961 rgba(62, 71, 78, 255), stop:1 rgba(240, 240, 240, 255));"
        self.alarm_apply = 'darkgray'
        self.alarm_dis = 'gray'

        self.soundCheck = 0
        self.event = threading.Event()

        self.setup_ui()
        self.setup_back()

    def setup_ui(self):
        # set main window
        self.setGeometry(300, 250, 1350, 600)  # x, y, w, h
        self.setFixedSize(1350, 600)
        self.setWindowTitle(f'Alarm Viewer - {version}')
        self.setStyleSheet("background-color:#edeef0")
        # self.setStyleSheet("background-color:gray;")

        # set fonts
        self.font_k9.setBold(True)

        self.font_k13.setBold(True)

        self.font_k12.setBold(True)

        self.font_ecam12.setBold(True)

        # font_ecal9 = QtGui.QFont("calibri", 9)

        self.font_ecal9.setBold(True)

        self.font_Tcam.setBold(True)

        # set Main windown icon
        self.setWindowIcon(QIcon(pwd + '/img/exelogo_inv.png'))

        # Background color
        p = QPalette()
        p.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(p)

        # Start Button
        self.start_button.setFont(self.font_ecam9)
        self.start_button.setStyleSheet("color: white;"
                                        "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                        f"{self.process_dis}"
                                        "border: 1px solid black;border-radius: 20px;")
        self.start_button.setGeometry(10, 10, 100, 50)
        self.start_button.toggle()
        self.start_button.setDisabled(True)

        # Stop Button
        self.stop_button.setFont(self.font_ecam9)
        self.stop_button.setStyleSheet("color: white;"
                                       "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                       f"{self.process_dis}"
                                       "border: 1px solid black;border-radius: 20px;")

        self.stop_button.setGeometry(115, 10, 100, 50)
        self.stop_button.setDisabled(True)

        # Save Button
        self.save_reset.setFont(self.font_ecam9)
        self.save_reset.setStyleSheet("color: white;"
                                      "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1,"
                                      "stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), "
                                      "stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));"
                                      "border: 1px solid black;border-radius: 20px;")
        self.save_reset.setGeometry(490, 10, 100, 50)

        # Alarm label

        # self.alarm_label.setGeometry(400, 10, 80, 9)
        # self.alarm_label.setFont(self.font_ecal9)

        # Sound ON radioButton
        self.alarm_radon.setGeometry(390, 15, 100, 25)
        self.alarm_radon.setFont(self.font_ecal9)

        # Sound OFF radioButton
        self.alarm_radoff.setGeometry(390, 40, 100, 20)
        self.alarm_radoff.setFont(self.font_ecal9)
        self.alarm_radoff.setChecked(True)   # off Default set

        # Status check
        self.running_status.setGeometry(280, 10, 90, 50)
        self.running_status.setFont(self.font_ecam12)
        self.running_status.setStyleSheet("background-color:#cccc33;color:white;border-color: 1px solid red;"
                                          "border-radius: 20px;")
        self.running_status.setDisabled(True)

        # Table
        self.alarm_table.setRowCount(100)
        self.alarm_table.setColumnCount(5)
        self.alarm_table.setHorizontalHeaderLabels(['Time', 'Name', 'IP', 'Alarm', 'Alarm OFF'])
        self.alarm_table.setFont(self.font_ecal9)
        self.alarm_table.setAlternatingRowColors(True)
        self.alarm_table.setColumnWidth(0, 140)
        self.alarm_table.setColumnWidth(1, 100)
        self.alarm_table.setColumnWidth(2, 100)
        self.alarm_table.setColumnWidth(3, 110)
        self.alarm_table.setColumnWidth(4, 80)
        for i in range(100):
            self.table_off_list[i].setObjectName(str(i))
            self.table_off_list[i].setStyleSheet("color: black;"
                                                 "background-color: white;")
            self.table_off_list[i].setFont(self.font_ecal9)
            self.table_off_list[i].setDisabled(True)
        self.alarm_table.setGeometry(10, 70, 580, 505)
        self.alarm_table.setStyleSheet("color: black;"
                                       "border-color: black;")

        # Status label
        self.Print_L.setGeometry(10, 570, 730, 20)
        self.Print_L.setFont(self.font_k9)

        # QDialog setting
        self.dialog.setPalette(p)

        # Popup Dialog
        self.popup_dialog.setWindowTitle('Alarm Popup')
        self.popup_dialog.setWindowIcon(QIcon(pwd + '/img/exelogo_inv.png'))
        self.popup_dialog.resize(850, 850)

        self.video_viewer_label = QLabel(self.popup_dialog)
        self.video_viewer_label.setGeometry(QRect(10, 10, 800, 800))

        # 2023-04-20 add

        # ======================= Right Page Start ===========================

        # 카메라 리스트 작성란
        for i in range(0, 16):
            # config list set field
            self.nm_list[i].setFont(self.font_ecam9)
            self.nm_list[i].setGeometry(630, 70 + 32 * i, 90, 30)
            self.nm_list[i].setPlaceholderText("카메라 이름")
            self.nm_list[i].setStyleSheet("box-shadow: inset 5px 5px 5px -5px #333;"
                                          "background-color:white;")

            self.md_list[i].setFont(self.font_k9)
            self.md_list[i].addItem('SELECT')
            self.md_list[i].addItem('8020')
            self.md_list[i].addItem('3204')
            self.md_list[i].setGeometry(720, 70 + 32 * i, 70, 30)
            self.md_list[i].setStyleSheet("background-color: white;"
                                          "color:Black;"
                                          "Border:0.5px solid black;"
                                          "box-shadow: inset 5px 5px 5px -5px #333;")

            self.ip_list[i].setFont(self.font_ecam9)
            self.ip_list[i].setGeometry(790, 70 + 32 * i, 100, 30)
            self.ip_list[i].setPlaceholderText("IP 입력")
            self.ip_list[i].setStyleSheet("box-shadow: inset 5px 5px 5px -5px #333;"
                                          "background-color:white;")

            self.id_list[i].setFont(self.font_ecam9)
            self.id_list[i].setGeometry(890, 70 + 32 * i, 90, 30)
            self.id_list[i].setPlaceholderText("아이디")
            self.id_list[i].setStyleSheet("box-shadow: inset 5px 5px 5px -5px #333;"
                                          "background-color:white;")

            self.ps_list[i].setFont(self.font_ecam9)
            self.ps_list[i].setEchoMode(QLineEdit.Password)
            self.ps_list[i].setPlaceholderText("비밀번호")
            self.ps_list[i].setGeometry(980, 70 + 32 * i, 70, 30)
            self.ps_list[i].setStyleSheet("box-shadow: inset 5px 5px 5px -5px #333;"
                                          "background-color:white;")

            self.st_list[i].setDisabled(True)
            self.st_list[i].setFont(self.font_ecam12)
            self.st_list[i].setGeometry(1050, 70 + 32 * i, 70, 30)
            self.st_list[i].setStyleSheet("background-color:White;"
                                          "color:darkred;"
                                          "border: 1px solid Black;"
                                          "box-shadow: inset 5px 5px 5px -5px #333;")

            # alarm on / off / test button set
            self.alarm_on_list[i].setGeometry(1150, 70 + 32 * i, 50, 30)
            self.alarm_on_list[i].setDisabled(True)
            self.alarm_on_list[i].setFont(self.font_ecam12)
            self.alarm_on_list[i].setStyleSheet(f"background-color:{self.alarm_dis};color: darkgray;")

            self.alarm_off_list[i].setGeometry(1200, 70 + 32 * i, 50, 30)
            self.alarm_off_list[i].setDisabled(True)
            self.alarm_off_list[i].setFont(self.font_ecam12)
            self.alarm_off_list[i].setStyleSheet(f"background-color:{self.alarm_dis};color: darkgrey;")

            self.test_list[i].setText('ON')
            self.test_list[i].setDisabled(True)
            self.test_list[i].setGeometry(1270, 70 + 32 * i, 70, 30)
            self.test_list[i].setFont(self.font_ecam12)
            self.test_list[i].setStyleSheet("background-color: grey; color: darkgrey;")

        # 카메라 리스트 인덱스 라벨
        self.name_label.setFont(self.font_Tcam)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setGeometry(632, 55, 80, 10)

        self.model_label.setFont(self.font_Tcam)
        self.model_label.setGeometry(730, 55, 70, 10)

        self.ip_label.setFont(self.font_Tcam)
        self.ip_label.setAlignment(Qt.AlignCenter)
        self.ip_label.setGeometry(810, 55, 70, 10)

        self.id_label.setFont(self.font_Tcam)
        self.id_label.setAlignment(Qt.AlignCenter)
        self.id_label.setGeometry(895, 55, 70, 10)

        self.pwd_label.setFont(self.font_Tcam)
        self.pwd_label.setAlignment(Qt.AlignCenter)
        self.pwd_label.setGeometry(980, 55, 70, 10)

        self.alarm_status.setFont(self.font_Tcam)
        self.alarm_status.setAlignment(Qt.AlignCenter)
        self.alarm_status.setGeometry(1050, 55, 70, 10)

        # 로그인 메뉴
        self.area_name.setFont(self.font_ecal9)
        self.area_name.setGeometry(800, 20, 150, 30)
        self.area_name.setPlaceholderText("IIST - 구역 입력")
        self.area_name.setStyleSheet("background-color:white;")

        # 로그인 버튼
        self.login.setFont(self.font_ecal9)
        self.login.setStyleSheet("color:white;"
                                 "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                 "stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), "
                                 "stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));")
        self.login.setGeometry(960, 20, 55, 30)

        # 저장 버튼
        self.save.setFont(self.font_ecal9)
        self.save.setStyleSheet("color:white;"
                                "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                "stop:0 rgba(218, 218, 218, 255), stop:0.305419 rgba(0, 7, 11, 255), "
                                "stop:0.935961 rgba(2, 11, 18, 255), stop:1 rgba(240, 240, 240, 255));")
        self.save.setGeometry(1020, 20, 55, 30)

        # 알람설정 & 테스트 모드 라벨
        self.all_onoff_label.setFont(self.font_Tcam)
        self.all_onoff_label.setGeometry(1180, 55, 200, 10)

        self.test_label.setFont(self.font_Tcam)
        self.test_label.setGeometry(1290, 55, 200, 10)

        # 알람 모두 활성화/비활성화 버튼
        self.all_on_button.setFont(self.font_Tcam)
        self.all_on_button.setGeometry(1138, 20, 60, 30)
        self.all_on_button.setDisabled(True)
        self.all_on_button.setStyleSheet("background-color:#336699;color:white;")

        self.all_off_button.setFont(self.font_Tcam)
        self.all_off_button.setGeometry(1202, 20, 60, 30)
        self.all_off_button.setDisabled(True)
        self.all_off_button.setStyleSheet("background-color:#999925;color:white;")

    def setup_back(self):
        self.start_button.clicked.connect(self.start_process)
        self.stop_button.clicked.connect(self.stop_process)

        self.alarm_radon.clicked.connect(self.sound_on)  # 소리 on
        self.alarm_radoff.clicked.connect(self.sound_off)  # 소리 off

        self.save_reset.clicked.connect(self.log_reset_table)  # 초기화 및 테이블 저장
        self.set_right()  # 오른쪽 칸들을 채워주는 함수.

        self.save.clicked.connect(lambda: self.save_right(True))  # 저장 버튼
        self.login.clicked.connect(self.login_button)

        for i in range(16):
            self.alarm_on_list[i].clicked.connect(lambda _, b=i: self.alarm_on(b))
            self.alarm_off_list[i].clicked.connect(lambda _, b=i: self.alarm_off(b))
            self.test_list[i].clicked.connect(lambda _, b=i: self.test_on_off(b))

        for i in range(100):
            self.table_off_list[i].clicked.connect(lambda _, b=self.table_off_list[i].objectName():
                                                   self.table_off_action(b))

        self.all_on_button.clicked.connect(self.alarm_all_on)
        self.all_off_button.clicked.connect(self.alarm_all_off)

    def sound_on(self):
        self.soundCheck = 1

    def sound_off(self):
        self.soundCheck = 0

    # 수정 부분
    def set_right(self):  # json파일을 읽어들어 각 인덱스에 설정값을 넣어주는 함수.
        j_data = read_json()

        self.area_name.setText(j_data["area"])
        for i, data in enumerate(j_data["data"]):
            self.nm_list[i].setText(data["name"])
            self.md_list[i].setCurrentText(data["model"])
            self.ip_list[i].setText(data["ip"])
            self.id_list[i].setText(data["id"])
            self.ps_list[i].setText(data["pwd"])

    def save_right(self, manual=False):
        dic = dict()
        dic["area"] = self.area_name.text()
        data = list()
        for i in range(16):
            if self.ip_list[i].text() != '' and self.id_list[i].text() != '' and self.ps_list[i].text() != '':
                data_i = dict()
                data_i["name"] = self.nm_list[i].text()
                data_i["model"] = self.md_list[i].currentText()
                data_i["ip"] = self.ip_list[i].text()
                data_i["id"] = self.id_list[i].text()
                data_i["pwd"] = self.ps_list[i].text()
                data.append(data_i)
            else:
                pass
        dic['data'] = data
        with open(os.path.join(pwd, "config/ip_data.json"), 'w', encoding='utf-8') as f:
            json.dump(dic, f, indent=4)
            f.close()
        if manual:
            QMessageBox.information(self, "SAVE", "DATA SAVE SUCCESS")

    def param_read(self, i, first=False):
        ip = self.ip_list[i].text()
        auth = HTTPDigestAuth(self.id_list[i].text(), self.ps_list[i].text())
        model = self.md_list[i].currentText()
        url = f'http://{ip}/admin/video_analytics2.asp'
        label = 'ALARMDISABLE'
        off_target = '1'
        if model == '3204':
            url = f'http://{ip}/httpapi/ReadParam?action=readparam&ETC_FLAMEDETECT_AlarmOutEnable=1'
            label = 'ETC_FLAMEDETECT_AlarmOutEnable'
            off_target = '0'
        try:
            response = requests.get(url, auth=auth, timeout=0.5)
            if response.status_code == 200:
                if first:
                    self.test_list[i].setEnabled(True)
                    self.test_list[i].setStyleSheet("background-color: grey;color: white;")
                data = data2dic(response.text, model)
                if data[label] == off_target:
                    self.st_list[i].setText("OFF")
                    self.st_list[i].setStyleSheet("background-color:White;"
                                                  "color:#c7c732;"
                                                  "border: 1px solid Black;"
                                                  "box-shadow: inset 5px 5px 5px -5px #333;")
                    self.alarm_on_list[i].setStyleSheet(f"background-color:{self.alarm_apply};color: white;")
                    self.alarm_on_list[i].setEnabled(True)
                    self.alarm_off_list[i].setStyleSheet(f"background-color:{self.alarm_dis};color: darkgray;")
                    self.alarm_off_list[i].setDisabled(True)
                else:
                    self.st_list[i].setText("ON")
                    self.st_list[i].setStyleSheet("background-color:White;"
                                                  "color:#6699CC;"
                                                  "border: 1px solid Black;"
                                                  "box-shadow: inset 5px 5px 5px -5px #333;")
                    self.alarm_off_list[i].setStyleSheet(f"background-color:{self.alarm_apply};color: white;")
                    self.alarm_off_list[i].setEnabled(True)
                    self.alarm_on_list[i].setStyleSheet(f"background-color:{self.alarm_dis};color: darkgray;")
                    self.alarm_on_list[i].setDisabled(True)
            else:
                self.st_list[i].setText("FAIL")
                self.st_list[i].setStyleSheet("background-color:White;"
                                              "color:darkred;"
                                              "border: 1px solid Black;"
                                              "box-shadow: inset 5px 5px 5px -5px #333;")
        except:
            self.st_list[i].setText("FAIL")
            self.st_list[i].setStyleSheet("background-color:White;"
                                          "color:darkred;"
                                          "border: 1px solid Black;"
                                          "box-shadow: inset 5px 5px 5px -5px #333;")
            self.alarm_off_list[i].setStyleSheet(f"background-color:{self.alarm_dis};color: darkgray;")
            self.alarm_off_list[i].setDisabled(True)
            self.alarm_on_list[i].setStyleSheet(f"background-color:{self.alarm_dis};color: darkgray;")
            self.alarm_on_list[i].setDisabled(True)
            self.test_list[i].setStyleSheet("background-color: grey;color: darkgrey;")
            self.test_list[i].setDisabled(True)

            print('Wrong IP')

    def login_button(self):
        self.start_button.setStyleSheet("color: white;"
                                        "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                        f"{self.process_apply}"
                                        "border: 1px solid black;border-radius: 20px;")
        self.start_button.setEnabled(True)
        for i in range(16):
            if self.ip_list[i].text() != '' and self.id_list[i].text() != '' and self.ps_list[i].text() != '':
                self.param_read(i, first=True)
            else:
                pass
        self.all_on_button.setEnabled(True)
        self.all_off_button.setEnabled(True)
        self.all_on_button.setStyleSheet("background-color:#73aae1;color:white;")
        self.all_off_button.setStyleSheet("background-color:#c7c732;color:white;")

        QMessageBox.information(self, "LOGIN SUCCESS", "Login")
        self.save_right()

    def alarm_on(self, i, manual=True):
        print(i)
        # on
        ip = self.ip_list[i].text()
        auth = HTTPDigestAuth(self.id_list[i].text(), self.ps_list[i].text())
        model = self.md_list[i].currentText()

        url = f'http://{ip}/cgi-bin/admin/fwvamispecific.cgi?AlarmDisable=0&FwCgiVer=0x0001'

        if model == '3204':
            url = f'http://{ip}/httpapi/WriteParam?action=writeparam&ETC_FLAMEDETECT_AlarmOutEnable=1'

        try:
            response = requests.get(url, auth=auth, timeout=0.5)
            if response.status_code == 200:
                if manual:
                    QMessageBox.information(self, "ALARM", "ON")
                self.param_read(i)
            else:
                self.st_list[i].setText("FAIL")
                if manual:
                    QMessageBox.warning(self, "ALARM", "FAIL")
        except:
            if manual:
                QMessageBox.warning(self, "ALARM", "Wrong IP")
            # self.Param_Reload(i)
            print('Wrong IP')
        self.save_right()

    def alarm_off(self, i, manual=True):
        ip = self.ip_list[i].text()
        auth = HTTPDigestAuth(self.id_list[i].text(), self.ps_list[i].text())
        model = self.md_list[i].currentText()

        url = f'http://{ip}/cgi-bin/admin/fwvamispecific.cgi?AlarmDisable=1&FwCgiVer=0x0001'

        if model == '3204':
            url = f'http://{ip}/httpapi/WriteParam?action=writeparam&ETC_FLAMEDETECT_AlarmOutEnable=0'

        try:
            response = requests.get(url, auth=auth, timeout=0.5)
            if response.status_code == 200:
                if manual:
                    QMessageBox.information(self, "ALARM", "OFF")
                self.delete_detection()
                self.param_read(i)
            else:
                self.st_list[i].setText("FAIL")
                if manual:
                    QMessageBox.warning(self, "ALARM", "FAIL")

        except:
            if manual:
                QMessageBox.warning(self, "ALARM", "Wrong IP")
            # self.Param_Reload(i)
            print('Wrong IP')

        self.save_right()

    def alarm_all_on(self):
        for i in range(16):
            if self.ip_list[i].text() != '' and self.id_list[i].text() != '' and self.ps_list[i].text() != '' \
                    and self.st_list[i].text() != 'FAIL':
                self.alarm_on(i, manual=False)
            else:
                pass
        QMessageBox.information(self, "ALARM", "ALL_ON")
        self.save_right()

    def alarm_all_off(self):
        for i in range(16):
            if self.ip_list[i].text() != '' and self.id_list[i].text() != '' and self.ps_list[i].text() != '' \
                    and self.st_list[i].text() != 'FAIL':
                self.alarm_off(i, manual=False)
            else:
                pass
        QMessageBox.information(self, "ALARM", "ALL_OFF")
        self.save_right()

    def test_on_off(self, i):
        print(i)
        if not (self.test_list[i].text() == "ON" or self.test_list[i].text() == "OFF"):
            return
        ip = self.ip_list[i].text()
        auth = HTTPDigestAuth(self.id_list[i].text(), self.ps_list[i].text())

        model = self.md_list[i].currentText()

        button_text = self.test_list[i].text()
        if button_text == 'ON':
            target = "1"
        else:
            target = "0"

        url = f'http://{ip}/cgi-bin/admin/fwvamispecific.cgi?TestMode={target}&FwCgiVer=0x0001'

        if model == '3204':
            url = f'http://{ip}/httpapi/WriteParam?action=writeparam&ETC_FLAMEDETECT_AlarmOutTest={target}'

        try:
            response = requests.get(url, auth=auth, timeout=0.5)
            # QMessageBox.information(self, "COM", "Send")

            if response.status_code == 200:
                if button_text == 'ON':
                    self.test_list[i].setText("OFF")
                    self.test_list[i].setStyleSheet("background-color: grey;color: red;")
                    QMessageBox.information(self, "TEST", "TEST ON")
                else:
                    self.test_list[i].setText("ON")
                    self.test_list[i].setStyleSheet("background-color: grey;color: white;")
                    QMessageBox.information(self, "TEST", "TEST OFF")
            else:
                QMessageBox.warning(self, "TEST", "TEST FAIL")
        except:
            QMessageBox.warning(self, "LOGIN", "Wrong IP")
            print('Wrong IP')

        self.save_right()

    # 알람 시작 버튼
    def start_process(self):
        try:
            os.system('taskkill /f /im GetHttp_thread.exe')
        except:
            self.Print_L.setText("Not process")
        # 프로토콜 실행 #
        subprocess.Popen(pwd + "/Thread/GetHttp_thread.exe", shell=True)

        self.event = threading.Event()
        self.start_button.setDisabled(True)
        self.stop_button.setEnabled(True)
        self.Print_L.setText('searching . . .')
        self.start_button.setStyleSheet("color: white;"
                                        "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                        f"{self.process_dis}"
                                        "border: 1px solid black;border-radius: 20px;")
        self.stop_button.setStyleSheet("color: white;"
                                       "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                       f"{self.process_apply}"
                                       "border: 1px solid black;border-radius: 20px;")
        # status 변화
        self.running_status.setText('START')
        self.running_status.setFont(self.font_k9)
        self.running_status.setStyleSheet("background-color: #6699cc;"
                                          "color:white;"
                                          "border-color: 1px solid Green;"
                                          "border-radius: 20px;")
        QMessageBox.information(self, "START", "Process Start")

        self.save_right()
        self.detection_checking()

    def delete_detection(self):
        filenames = os.listdir("Detection")
        for filename in filenames:
            self.Print_L.setText('Detect')
            full_filename = os.path.join("Detection", filename)
            try:
                os.remove(full_filename)
            except WindowsError as e:
                pass

    # 알람 멈추는 버튼
    def stop_process(self):
        try:
            os.system('taskkill /f /im GetHttp_thread.exe')
            self.event.set()
            self.start_button.setEnabled(True)
            self.stop_button.setDisabled(True)
            self.alarm_controller(red=0, sound=0)
            self.delete_detection()
        except:
            self.Print_L.setText('There is no process to stop.')
        self.running_status.setText('STOP')
        self.running_status.setFont(self.font_k9)
        self.running_status.setStyleSheet("background-color:#c7c732;"
                                          "color:white;"
                                          "border-color: 1px solid red;"
                                          "border-radius: 20px;")
        self.start_button.setStyleSheet("color: white;"
                                        "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                        f"{self.process_apply}"
                                        "border: 1px solid black;border-radius: 20px;")
        self.stop_button.setStyleSheet("color: white;"
                                       "background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.995, y2:1, "
                                       f"{self.process_dis}"
                                       "border: 1px solid black;border-radius: 20px;")
        QMessageBox.information(self, "STOP", "Process Stop")
        self.save_right()
        self.Print_L.setText('All process to stop.')

    # alarm 확인 부분 - popup lock
    def detection_checking(self):
        filenames = os.listdir("Detection")
        for filename in filenames:
            if filename == '.gitkeep':
                continue
            self.Print_L.setText('Detect')
            full_filename = os.path.join("Detection", filename)
            # name#
            name, _ip = filename.rstrip(".txt").split("_")
            # IP#
            f = open(full_filename, 'r', encoding='UTF8')
            object_list = f.read().split("\n")
            object_name, object_ip, object_maker, object_id, object_pas, object_idx = object_list
            f.close()
            self.write_table(name, _ip, object_name, object_idx)
            try:
                if self.soundCheck and self.c_index == 10:
                    threading.Thread(target=winsound.PlaySound, args=["sound/fire_detect.wav",
                                                                      winsound.SND_FILENAME, ]).start()
                elif self.c_index != 10:
                    self.alarm_controller(red=2, sound=self.soundCheck)
                    time.sleep(2)
                    self.alarm_controller(red=0, sound=0)
            except:
                self.Print_L.setText('Alarm controller error')
                pass
            try:
                # threading.Thread(self.show_dialog(object_ip, object_maker, object_id, object_pas)).start()
                os.remove(full_filename)
            except:
                self.Print_L.setText('Pop up error')
                pass
        if self.event.is_set():
            return
        threading.Timer(5, self.detection_checking).start()

    # popup을 위한 함수.
    def show_dialog(self, ip, maker, id, pas):
        self.show_image(ip, maker, id, pas)
        return

    # popup - 영상 보여주기
    def show_image(self, ip, maker, id, pas):
        register = id + ':' + pas + '@' + ip
        if 'Sey' in maker:
            connector = 'rtsp://' + register + '/cam0_1'
        else:
            connector = 'rtsp://' + register + '/video1'
        cap = cv2.VideoCapture(connector)
        width, height, channel = 800, 800, 3
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        second = 3
        count = 0
        self.popup_dialog.show()
        while fps * second > count:
            count += 1
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
        self.popup_dialog.close()

    # log 부분
    def write_table(self, name, ip_in, object_in, object_idx):
        # 표에 데이터 삽입
        now = datetime.now()
        now_datetime = now.strftime('%y-%m-%d %H:%M:%S')

        item1 = QTableWidgetItem(now_datetime)
        item1.setTextAlignment(Qt.AlignCenter)
        self.alarm_table.setItem(self.table_Count, 0, item1)

        item2 = QTableWidgetItem(name)
        item2.setTextAlignment(Qt.AlignCenter)
        self.alarm_table.setItem(self.table_Count, 1, item2)

        item3 = QTableWidgetItem(ip_in)
        item3.setTextAlignment(Qt.AlignCenter)
        self.alarm_table.setItem(self.table_Count, 2, item3)

        item4 = QTableWidgetItem(object_in)
        item4.setTextAlignment(Qt.AlignCenter)
        self.alarm_table.setItem(self.table_Count, 3, item4)

        self.alarm_table.setCellWidget(self.table_Count, 4, self.table_off_list[self.table_Count])
        self.table_off_list[self.table_Count].setEnabled(True)
        self.table_off_list[self.table_Count].setStyleSheet("color: black;"
                                                            "background-color: white;")
        self.table_off_list[self.table_Count].setFont(self.font_ecal9)
        self.table_Count += 1

        self.alarm_table.update()

        index = self.alarm_table.model().index(self.table_Count, 0)
        self.alarm_table.scrollTo(index)
        if self.table_Count > 99:
            self.table_Count = 0
            self.log_write_txt()
            self.log_reset_table()

    # 기록 리셋 부분
    def log_reset_table(self):
        self.log_write_txt()
        self.alarm_table.clear()
        self.alarm_table.setHorizontalHeaderLabels(['Time', 'Name', 'IP', 'Alarm', 'Alarm OFF'])
        self.table_off_list = [QPushButton('OFF') for _ in range(100)]
        for i in range(100):
            self.table_off_list[i].setStyleSheet("color: black;"
                                                 "background-color: white;")
            self.table_off_list[i].setFont(self.font_ecal9)
            self.table_off_list[i].setDisabled(True)
            self.table_off_list[i].setObjectName(str(i))
            self.table_off_list[i].clicked.connect(lambda _, b=self.table_off_list[i].objectName():
                                                   self.table_off_action(b))

        self.table_Count = 0
        self.save_right()
        QMessageBox.information(self, "SAVE", "LOG SAVE SUCCESS")

    def table_off_action(self, object_):
        ip = self.alarm_table.item(int(object_), 2).text()
        j_data = read_json()
        for i, data in enumerate(j_data["data"]):
            if data["ip"] == ip:
                self.alarm_off(i=i)
        for i in range(100):
            try:
                t = self.alarm_table.item(i, 2).text()
            except AttributeError:
                break
            print(ip)
            if t == ip:
                self.table_off_list[i].setDisabled(True)
                self.table_off_list[i].setStyleSheet("color: lightgray;"
                                                     "background-color: white;")
                self.table_off_list[i].setFont(self.font_ecal9)

    # 로그 저장 부분
    def log_write_txt(self):
        folder = pwd + "/LogData"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        now = datetime.now()
        now_time = now.strftime('%m%d_%H_%M_%S')

        path = pwd + "/LogData/" + "Alarm_Data_" + now_time + ".txt"

        self.Print_L.setText("Save : " + path)

        writer = open(path, 'w', newline='')

        txt = ""
        for row in range(self.alarm_table.rowCount()):
            for column in range(self.alarm_table.columnCount() - 1):
                item = self.alarm_table.item(row, column)
                if item is not None:
                    txt += item.text() + " "
                else:
                    txt += ''
            txt += '\n'
        writer.write(txt)
        self.isChanged = False
        writer.close()

    ########################################################

    # 경광등 연결 상태 확인 return : 10 = fail

    # 구조체 만들어 주기
    class ArrayStruct(Structure):
        _fields_ = [("char_t", POINTER(c_char))]

    # 알람 확인해 주는 부분.
    def alarm_controller(self, red, yellow=0, green=0, blue=0, white=0, sound=0):
        self.c_index = ligth_status_check()
        if self.c_index == 10:
            return
        c_type = 0

        c_char_t = self.ArrayStruct()
        c_char_t.char_t = (c_char * 6)(red, yellow, green, blue, white, sound)
        usb_qu_write = light_dll['Usb_Qu_write'](self.c_index, c_type, c_char_t.char_t)
        return usb_qu_write


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
