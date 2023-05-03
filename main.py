from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtGui
import sys
import re
import requests
from bs4 import BeautifulSoup
import datetime
import _thread as thread


class MyWin(QDialog):
    def __init__(self):
        super(MyWin, self).__init__()
        uic.loadUi('word2md.ui', self)
        self.setWindowIcon(QtGui.QIcon("./cow.ico"))
        self.lineEdit.editingFinished.connect(self.textFinished_func)

    def textFinished_func(self):
        string = self.lineEdit.text()
        self.label_2.setText(string)
        self.lineEdit.clear()
        do(string)      # 网络请求异步执行，否则会闪退


def Print(string):
    with open('1.txt', 'a+') as f:
        f.write(string)


def show():
    app = QtWidgets.QApplication(sys.argv)
    myWin = MyWin()
    myWin.show()
    sys.exit(app.exec())


def write_func(text):
    k = re.compile('@.+?。')
    today = datetime.date.today().strftime('%y%m%d')
    result = ''
    with open('./word_files/' + today + '.md', 'a+', encoding='utf-8') as f:
        if text == 'new':
            f.write('# {}\n'.format(today))
        else:
            if not text.endswith("。"):
                text += "。"
            string = '**' + text.split(' ')[0] + '** '
            response = requests.get('https://cn.bing.com/dict/search?q={0}'.format(text.split(' ')[0]))
            us, en = '', ''
            if response.ok:
                r = response.text
                soup = BeautifulSoup(r, 'html.parser')
                us = soup.find(class_='hd_prUS b_primtxt').text
                en = soup.find(class_='hd_pr b_primtxt').text
            mean = []
            for i in re.finditer(k, text):
                temp = i.group()[1: -1].split(' ')
                mean.append('*' + temp[0] + '.* ')
                mean.append(temp[1])
            all_mean = ' '.join(mean)
            result = string + en + ' ' + us + ' ' + all_mean + '\n'
            f.write(result)


def do(text):
    thread.start_new_thread(write_func, (text,))


if __name__ == '__main__':
    show()