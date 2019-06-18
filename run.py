import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from download_ebook_ui import *
from download_ebook import *


class mwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mwindow, self).__init__(parent)
        self.setupUi(self)
        self.actionsybz.triggered.connect(self.sybz)
        self.actiongy.triggered.connect(self.gy)

    def slot1(self):
        # 清空eboo_temp目录
        for root, dirs, files in os.walk(os.path.join(basedir, 'ebook_temp'), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        d = DownloadEbook()
        base_url = self.lineEdit.text()
        base_url = re.split(r'\d{0,5}.jpg', base_url)[0]
        with open('config.txt', 'w') as f:
            f.write(base_url)
        for i in range(d.thread_num):
            t=threading.Thread(target=d.download_img, args=(base_url,self))
            t.setDaemon(True)
            t.start()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)

    def slot2(self):
        d = DownloadEbook()
        with open('config.txt', 'r') as f:
            base_url = f.read()
        d.get_L()
        for i in range(d.thread_num):
            t=threading.Thread(target=d.download_img, args=(base_url,self))
            t.setDaemon(True)
            t.start()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)

    def slot3(self):
        d = DownloadEbook()
        pdf_name = 'output.pdf'
        d.rea(pdf_name, self)

    def sybz(self):
        os.system(os.path.join(basedir, 'help', 'index.html'))

    def gy(self):
        QMessageBox.information(self, "关于", "软件版本：V1.0\n制作者：程鹏",
                                QMessageBox.Yes)


if __name__ == '__main__':
    '''
    主函数
    '''
    path = os.path.join(basedir, 'ebook_temp')
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    app = QApplication(sys.argv)
    myWin = mwindow()
    myWin.show()
    sys.exit(app.exec_())
