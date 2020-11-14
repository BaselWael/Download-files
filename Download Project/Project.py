from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
from os import path
import urllib.request
import time
import pafy
import humanize


FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),'main.ui'))
class MainApp(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI()
        self.Buttons()



    def UI(self):
        self.setWindowTitle("Youtube Downloader")
        self.setFixedSize(1077,363)


    def Browse_Button(self):
        save_place = QFileDialog.getSaveFileName(self,caption="Save As",directory=".",filter="All Files(*.*)")
        save_place=str(save_place)
        line = save_place.split(",")
        edit_line = line[0]
        print(edit_line)
        final_line = edit_line[2:]
        print(final_line)
        final_line = final_line.split("'")
        print(final_line)
        self.LineBrowse.setText(final_line[0])
    def Browse_Button_youtubevidoe(self):
        save = QFileDialog.getExistingDirectory(self,"Select Download Directory")
        self.LineBrowse_2.setText(save)
        '''save_place = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        save_place = str(save_place)
        line = save_place.split(",")
        edit_line = line[0]
        print(edit_line)
        final_line = edit_line[2:]
        print(final_line)
        final_line = final_line.split("'")
        print(final_line)
        self.LineBrowse_2.setText(final_line[0])
        '''



    def Buttons(self):
        try:
           self.DownloadButton.clicked.connect(self.downloadfiles)
           self.BrowseButton.clicked.connect(self.Browse_Button)
           self.BrowseButton_2.clicked.connect(self.Browse_Button_youtubevidoe)
           self.CheckQualityButton.clicked.connect(self.check_quality)
           self.DownloadButton_2.clicked.connect(self.downloadyoutubevidoe)
        except Exception:
            QMessageBox.warning(self, "Error", "Some Thing Went Wrong")

    def Progress_Bar_downloadfile(self,blocknum , blocksize , totalsize):
        data = blocknum * blocksize
        if totalsize >0:
            percent = data * 100 / totalsize
            self.ProgressBar.setValue(percent)
            QApplication.processEvents()  #Not Responding


    def downloadfiles(self):

        url = self.LineUrl.text()
        browse = self.LineBrowse.text()
        if browse == "":
            QMessageBox.information("Please Enter Location")
        else:
            try:
                urllib.request.urlretrieve(url,browse,self.Progress_Bar_downloadfile)
                QMessageBox.information(self, "Completed", "Download Completed")
            except Exception:
                QMessageBox.warning(self,"Download Error","Download Failed")

            self.LineUrl.setText('')
            self.LineBrowse.setText('')
            self.ProgressBar.setValue(0)

    def downloadyoutubevidoe(self):
        try:
            video = self.VideoUrl.text()
            save = self.LineBrowse_2.text()
            if save == "":
                QMessageBox.information("Please Enter Location")

            else:
                url = pafy.new(video)
                st = url.videostreams
                quality = self.ComboBoxQuality.currentIndex()
                down = st[quality].download(filepath = save)
        except Exception:
            QMessageBox.information(self,"Information","Please enter the link and Location and Click Check Quality")
    def check_quality(self):
        try:
            vidoe = self.VideoUrl.text()
            url = pafy.new(vidoe)
            st = url.allstreams
            for qualityy in st:
                size = humanize.naturalsize(qualityy.get_filesize())
                add = str((qualityy.quality + "  Size : " + size))
                self.ComboBoxQuality.addItem(add)
            QMessageBox.information(self,"Successfuly","Successfuly")
        except Exception:
             QMessageBox.warning(self,"Wrong URL","Wrong URL")



def Main_():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    Main_()

