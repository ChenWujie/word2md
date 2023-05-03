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
        if len(string) > 1:
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

    with open('./word_files/' + today + '_memorize.md', 'a+', encoding='utf-8') as f1, \
            open('./word_files/' + today + '_review.md', 'a+', encoding='utf-8') as f2:
        if text == 'new':
            f1.write('# {} memorize\n'.format(today))
            f2.write('# {} review\n'.format(today))
        elif '@' in text:
            if not text.endswith("。"):
                text += "。"
            string = '**' + text[:text.find('@')].strip() + '** '
            response = requests.get('https://cn.bing.com/dict/search?q={0}'.format(text.split(' ')[0]))
            us, en = '', ''
            if response.ok:
                r = response.text
                soup = BeautifulSoup(r, 'html.parser')
                us = soup.find(class_='hd_prUS b_primtxt').text
                en = soup.find(class_='hd_pr b_primtxt').text
            mean = []
            part_of_speech = ''
            for i in re.finditer(k, text):
                temp = i.group()[1: -1].split(' ')
                mean.append('*' + temp[0] + '.* ')
                part_of_speech += '*' + temp[0] + '.* ···  '
                mean.append(" ".join(temp[1:]))
            all_mean = '    '.join(mean)
            mem_result = string + en + ' ' + us + '  ' + all_mean + '\n\n'
            rev_result = string + en + ' ' + us + '  ' + part_of_speech + '\n\n'
            mem_result = mem_result.replace('（', '(')
            mem_result = mem_result.replace('）', ')')
            rev_result = rev_result.replace('（', '(')
            rev_result = rev_result.replace('）', ')')
            mem_result = mem_result.replace('【', '[')
            mem_result = mem_result.replace('】', ']')
            rev_result = rev_result.replace('【', '[')
            rev_result = rev_result.replace('】', ']')
            f1.write(mem_result)
            f2.write(rev_result)


def do(text):
    thread.start_new_thread(write_func, (text,))


if __name__ == '__main__':
    show()