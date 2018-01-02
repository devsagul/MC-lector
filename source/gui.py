# -*- coding: utf-8 -*-

import os
from builtins import super
import json
import datetime

# PyQt5
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, \
                            QDialog, QTextEdit, QGridLayout, QPushButton, QWidget, QSizePolicy, \
                            QVBoxLayout, QHBoxLayout, QSplitter, QStyleFactory, QSizePolicy, QLabel, \
                            QScrollArea
from PyQt5.QtGui import QIcon, QKeyEvent, QFontMetrics, QPixmap


class LectorApp(object):
    def __init__(self, args, communicator):
        self.app = QApplication(args)
        self.chat_app = MainWindow(communicator)


class MainWindow(QMainWindow):
    def __init__(self, communicator):
        super().__init__()
        self.initUI(communicator)

    def initUI(self, communicator):
        self.populateUI(communicator)
        self.resize(1000, 480)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(480)
        self.setWindowTitle('Приложение лектора')
        self.setContentsMargins(-10,-10,-10,-10)
        self.menuBar().setVisible(False)
        self.statusBar().setVisible(False)
        self.show()

    def populateUI(self, communicator):
        self.centralWidget = CentralWidget(communicator)
        self.setCentralWidget(self.centralWidget)

    def closeEvent(self, event):
        os._exit(0)


class CentralWidget(QWidget):
    def __init__(self, communicator):
        super().__init__()
        self.initUI(communicator)
        self.setStyleSheet("QWidget {border: 0;}")

    def initUI(self, communicator):
        self.questionBlock = Questions(communicator)
        self.lectionBlock = Lection(communicator)
        layout = QHBoxLayout()
        layout.setSpacing(0)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.lectionBlock)
        self.splitter.addWidget(self.questionBlock)
        self.splitter.setHandleWidth(0)
        self.splitter.setStretchFactor(0, 5)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStyleSheet("QWidget {background-color: #78aef9;border:0;}")
        layout.addWidget(self.splitter)
        self.setContentsMargins(-10, -10, -10, -10)
        self.setLayout(layout)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

    def closeEvent(self, event):
        os.exit(0)


class Lection(QWidget):
    def __init__(self, communicator):
        super().__init__()
        self.setStyleSheet("QWidget {background-color: rgb(255,255,255);}")
        self.initUI(communicator)

    def initUI(self, communicator):
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText("ЛЕКЦИЯ")
        self.label.setStyleSheet('QWidget {font-family: "Roboto";font-Size: 24px;padding: 24px;font-weight: bold; color: #595f66}')
        layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignTop)
        self.scrollable = ScrollableAreaLecture(communicator)
        layout.addWidget(self.scrollable)
        self.setContentsMargins(-10, -10, -10, -10)
        layout.setSpacing(0)
        self.setLayout(layout)


class Questions(QWidget):
    def __init__(self, communicator):
        super().__init__()
        self.setStyleSheet("QWidget {background-color: #78aef9;padding: 24px 24px 24px 0;}")
        self.initUI(communicator)

    def initUI(self, communicator):
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText("ВОПРОСЫ")
        self.label.setStyleSheet('QWidget {font-family: "Roboto";font-Size: 24px; color: #FFFFFF;font-weight: bold;}')
        self.label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.label)
        self.scrollable = ScrollableAreaQuestions(communicator)
        layout.addWidget(self.scrollable)
        layout.setSpacing(0)
        self.setContentsMargins(-10, -10, -10, -10)
        self.setLayout(layout)


class ScrollableAreaLecture(QWidget):
    def __init__(self, communicator):
        super().__init__()
        self.c = communicator
        listBox = QVBoxLayout(self)
        self.setLayout(listBox)

        scroll = QScrollArea(self)
        self.scroll = scroll
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""QScrollBar:vertical {
                        width: 0px;
                        border-radius: 5px;
                        background-color: #333333
                      }
                      """)

        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollLayout.setSpacing(30)
        scrollLayout.addStretch()
        scrollContent.setLayout(scrollLayout)
        scroll.setWidget(scrollContent)
        self.scrollLayout = scrollLayout
        self.setContentsMargins(0, -10, -10, 0)
        self.c.recieve["sig"].connect(self.addItem)
        self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)

    def ResizeScroll(self, min, maxi):
        self.scroll.verticalScrollBar().setValue(maxi)

    def addItem(self):
        item = LectionItem(self.c.recieve["text"])
        self.scrollLayout.insertWidget(self.scrollLayout.count() - 1, item)

class LectionItem(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()
        self.timestamp = TimeStamp()
        self.text = LectionText(text)
        self.setStyleSheet('QWidget {border-bottom: 9px solid #333333;}')
        layout.addWidget(self.timestamp)
        layout.addWidget(self.text)
        layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(self.timestamp.height + self.text.textHeight)
        self.setLayout(layout)


class TimeStamp(QLabel):
    def __init__(self):
        super().__init__()
        self.setText(datetime.datetime.today().strftime("%d.%m.%Y %H:%M"))
        self.setAlignment(Qt.AlignRight)
        self.height = 16
        self.setFixedHeight(self.height)
        self.setStyleSheet('QWidget {border-bottom: 0px solid #333333;}')

class LectionText(QTextEdit):
    def __init__(self, text):
        super().__init__()
        self.append(text)
        self.setReadOnly(True)

        self.setLineWrapMode(True)
        font = self.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, text)

        self.textHeight = textSize.height() + 15

        self.setFixedHeight(self.textHeight)


class ScrollableAreaQuestions(QWidget):
    def __init__(self, communicator):
        super().__init__()
        self.c = communicator
        listBox = QVBoxLayout(self)
        self.setLayout(listBox)

        scroll = QScrollArea(self)
        self.scroll = scroll
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""QScrollBar:vertical {
                        width: 0px;
                      }
                      QWidget {border-bottom: 0px solid #333333;background-color: #FFFFFF;}
                      """)

        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollLayout.setSpacing(0)
        scrollLayout.addStretch()
        scrollContent.setLayout(scrollLayout)
        scroll.setWidget(scrollContent)
        self.scrollLayout = scrollLayout
        self.setContentsMargins(24, 0, 24, 0)
        self.c.recieveQuestion["sig"].connect(self.addItem)
        self.c.answerQuestion["sig"].connect(self.popItem)
        self.scroll.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)

    def ResizeScroll(self, min, maxi):
        self.scroll.verticalScrollBar().setValue(maxi)

    def addItem(self):
        item = QuestionItem(self.c.question["text"], self.c.question["username"])
        self.scrollLayout.insertWidget(self.scrollLayout.count() - 1, item)

    def popItem(self):
        if self.scrollLayout.count() > 1:
            widget = self.scrollLayout.takeAt(0)
            text = widget.text
            widget.setParent(None)
            self.c.send["text"] = "Ответ на вопрос:" + text
            self.c.send["sig"].emit()
        else:
            text = "Нет больше вопросов"
        self.c.tts["text"] = text
        self.c.tts["sig"].emit()


class QuestionItem(QWidget):
    def __init__(self, text, username):
        super().__init__()
        layout = QHBoxLayout()
        self.text = text
        self.message = Message(username, text)
        self.setStyleSheet('QWidget {border-bottom: 9px solid #333333;background-color: #FFFFFF}')
        layout.addWidget(self.imageHolder)
        layout.addWidget(self.message)
        layout.setSpacing(0)
        self.setContentsMargins(0, -10, 0, 0)
        self.setFixedHeight(self.message.height)
        self.setLayout(layout)


class Message(QWidget):
    def __init__(self, username, text):
        super().__init__()
        self.username = Username(username)
        self.text = QuestionText(text)
        layout = QVBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.text)
        layout.setSpacing(4)
        self.setLayout(layout)
        self.height = (self.username.height + self.text.textHeight)


class Username(QLabel):
    def __init__(self, username):
        super().__init__()
        self.setText(username)
        self.height = 16
        self.setFixedHeight(self.height)
        self.setStyleSheet('QWidget {border-bottom: 0px solid #333333; color:#333333; font-family: Roboto; font-weight: bold;padding: 3;}')


class QuestionText(QTextEdit):
    def __init__(self, text):
        super().__init__()
        self.append(text)
        self.setReadOnly(True)

        self.setLineWrapMode(True)
        font = self.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, text)

        self.textHeight = textSize.height() + 50

        self.setFixedHeight(self.textHeight)
        self.setStyleSheet('QWidget {border-bottom: 22px solid #333333;padding: 3;}')