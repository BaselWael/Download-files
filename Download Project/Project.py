import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from os import path
from PB import Spider
import Bat
from update import data
from Check import check_update
import urllib.request
import os
from PyQt5.uic import loadUiType
FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),'main.ui'))

class MainApp(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI()
        self.Buttons()

    def UI(self):
        if os.path.exists('filelist.txt'):
            self.check_filelist()
        else:
            QMessageBox.warning(self,'Error','Put the launcher in the game folder')
            QApplication.exit()
            MainApp.close()
            #self.close()



    def Buttons(self):
        self.pushButton_start.clicked.connect(self.StartButton)

    def StartButton(self):
        status = self.pushButton_start.text()
        if status== 'UPDATE':
            self.check()
            self.pushButton_start.setText('START')
            self.label_update.setText('Server is up to date')
        else:
            email = self.lineEdit_email.text()
            password = self.lineEdit_pass.text()
            if email =='' and password =='':
                QMessageBox.information(self,'No Data','من فضلك ادخل حسابك')
            else:
                Account_ID = Spider().login(email=email, password=password)
                try:
                    if Account_ID=='faild':
                        QMessageBox.warning(self,'Warrning','معلومات تسجيل الدخول خاطئه !')
                    else:
                        self.close()
                        Bat.BatFile().startPB(id=Account_ID)
                        QApplication.exit()
                        MainApp.close()
                        QApplication.processEvents()
                    QApplication.processEvents()
                except:
                    QMessageBox.warning(self,"Error","Error")
    def check_filelist(self):
        file = open('filelist.txt','r').read()
        id = data().Get_ID()[-1]
        if int(file) < int(id):
            self.pushButton_start.setText('UPDATE')
            self.progressBar.setValue(0)
        else:
            self.pushButton_start.setText('START')
    def Progress_Bar_downloadfile(self):
        names_packages = data().Get_name()
        ID = data().Get_ID()
        links = data().Get_link()
        file_name = data().Get_name_file()
        id_read = open('filelist.txt', 'r').read()
        for id, name, link, filename in zip(ID, names_packages, links, file_name):
            if int(id) > int(id_read):
                calc = int(id_read) / len(ID)
                self.progressBar.setValue(int(calc*100))
                start = self.pushButton_start.text()
                if start =='START':
                    self.progressBar.setValue(100)
                QApplication.processEvents()


    def check(self):
        names_packages = data().Get_name()
        ID = data().Get_ID()
        links = data().Get_link()
        file_name = data().Get_name_file()
        id_read = open('filelist.txt', 'r').read()
        for id, name, link, filename in zip(ID,names_packages,links,file_name):
            if int(id) > int(id_read):
                self.name = filename
                #self.label_update.setText(name +'is downloading...')
                self.download(url=link)
                print(self.name)
                print(link)
                id_change = open('filelist.txt', 'w')
                id_change.write(id)
                id_change.close()
                QApplication.processEvents()
        self.progressBar.setValue(100)


    def download(self,url = None):
        try:
            urllib.request.urlretrieve(url,sys.path[0]+'\\'+self.name)
            print('done download')
            #self.Progress_Bar_downloadfile()
            self.start_threading()
        except:
            #self.pushButton_start.setText('UPDATE')
            print('error download')
        try:
            time.sleep(1)
            Spider().Unrar(file=self.name)
        except:
            print('error unrar')
        if os.path.exists(self.name):
            os.remove(self.name)
            print('done delete')
        else:
            print("The file does not exist")

            QApplication.processEvents()
            #QApplication.processEvents()
    def start_threading(self):
        self.thread_started = Threadclass()
        self.thread_started.start()
        self.thread_started.value.connect(self.progressBar.setValue)
        self.thread_started.label.connect(self.label_update.setText)


class Threadclass(QThread):
    value = pyqtSignal(int)
    label = pyqtSignal(str)
    def __init__(self,parent=None):
        QThread.__init__(self,parent=None)
        self.isRunning = True
    def run(self):
        while self.isRunning:
            names_packages = data().Get_name()
            ID = data().Get_ID()
            links = data().Get_link()
            file_name = data().Get_name_file()
            id_read = open('filelist.txt', 'r').read()
            for id, name, link, filename in zip(ID, names_packages, links, file_name):
                if int(id) > int(id_read):
                    v = int(id_read) / len(ID)
                    c = v*100
                    self.value.emit(int(c))
                    self.label.emit(name)


    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()

def Main_():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    Main_()
