import sys
import json
import requests


from PySide6 import QtWidgets, QtCore, QtGui


def translate(word):
    url = "http://fanyi.youdao.com/translate?smartresult" \
          "=dict&smartresult" \
          "=rule&smartresult" \
          "=ugc&sessionFrom" \
          "=null"
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    try:
        response = requests.post(url, data=key)
        if response.status_code != 200:
            raise Exception("Call youdao dictionary error\n")
        result = json.loads(response.text)["translateResult"][0][0]["tgt"]
        return result
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
    return ""


class Translator(QtWidgets.QMainWindow):


    QSS = """
    QWidget {
        border-style: none;
        border-radius: 10px;
        margin: 2px;
        padding: 2px;
        background: #DDEEFF;
    }
    QPlainTextEdit {
        border-style: solid;
        border-color: #AAAAAA;
        border-width: 2px;
        border-radius: 10px;
        margin: 2px;
        padding: 2px;
        background: #FFFFFF;
    }
    #BtnTranslate {
        border-style: solid;
        border-color: #AAAAAA;
        border-width: 2px;
        border-radius: 10px;
        margin: 2px;
        padding: 2px;
        background: #FFFFFF;
    }
    #BtnTranslate:hover,clicked {
        border-style: solid;
        border-color: #AAAAAA;
        border-width: 2px;
        border-radius: 10px;
        margin: 2px;
        padding: 2px;
        background: #DDFFDD;
    }
    #BtnExit{
        border-style: solid;
        border-color: #AAAAAA;
        border-width: 2px;
        border-radius: 10px;
        margin: 2px;
        padding: 2px;
        background: #FFFFFF;
    }
    #BtnExit:hover,clicked {
        border-style: solid;
        border-color: #AAAAAA;
        border-width: 2px;
        border-radius: 10px;
        margin: 2px;
        padding: 2px;
        background: #FFDDDD;
    }
    """


    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0.9)

        self.__moving = True
        self.__move_from = QtGui.QCursor.pos()
        self.__move_origin = self.pos()

        self.cw = QtWidgets.QWidget()
        self.txtInput = QtWidgets.QPlainTextEdit()
        self.txtInput.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.txtInput.setMinimumSize(QtCore.QSize(0, 0))
        self.txtInput.setMaximumSize(QtCore.QSize(65535, 65535))
        self.txtOutput = QtWidgets.QPlainTextEdit(readOnly=True)
        self.txtOutput.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.txtOutput.setMinimumSize(QtCore.QSize(0, 0))
        self.txtOutput.setMaximumSize(QtCore.QSize(65535, 65535))
        self.btnTranslate = QtWidgets.QPushButton("有道翻译")
        self.btnTranslate.setObjectName("BtnTranslate")
        self.btnTranslate.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred)
        self.btnExit = QtWidgets.QPushButton("退出")
        self.btnExit.setObjectName("BtnExit")
        self.btnExit.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred)

        self.setCentralWidget(self.cw)
        self.cw.setLayout(QtWidgets.QVBoxLayout())
        self.cw.layout().addWidget(self.txtInput, 2)
        self.cw.layout().addWidget(self.txtOutput, 2)
        self.cw.layout().addWidget(self.btnTranslate, 1)
        self.cw.layout().addWidget(self.btnExit, 1)

        self.txtInput.textChanged.connect(self.__event_txtInput_textChanged)
        self.btnTranslate.clicked.connect(self.__event_btnTranslate_clicked)
        self.btnExit.clicked.connect(self.__event_btnExit_clicked)

        self.cw.setStyleSheet(self.__class__.QSS)
        self.resize(300, 200)

        self.installEventFilter(self)


    def eventFilter(self, sender, event):
        event_type = event.type()
        if event_type == QtCore.QEvent.MouseButtonPress:
            self.__moving = True
            self.__move_from = QtGui.QCursor.pos()
            self.__move_origin = self.pos()
        elif event_type == QtCore.QEvent.MouseButtonRelease:
            self.__moving = False
        elif event_type == QtCore.QEvent.MouseMove and self.__moving:
            delta_x = QtGui.QCursor.pos().x() - self.__move_from.x()
            delta_y = QtGui.QCursor.pos().y() - self.__move_from.y()
            target_x = self.__move_origin.x() + delta_x
            target_y = self.__move_origin.y() + delta_y
            self.move(target_x, target_y)
        elif event_type == QtCore.QEvent.Enter:
            pos = self.pos()
            height = self.height()
            x = pos.x()
            y = pos.y()
            if y <= 20-height:
                self.move(x, -5)
        elif event_type == QtCore.QEvent.Leave:
            pos = self.pos()
            height = self.height()
            x = pos.x()
            y = pos.y()
            if y < 20:
                self.move(x, 20-height)
        return False


    def __event_txtInput_textChanged(self):
        trans = translate(self.txtInput.toPlainText())
        self.txtOutput.setPlainText(trans)


    def __event_btnTranslate_clicked(self):
        trans = translate(self.txtInput.toPlainText())
        self.txtOutput.setPlainText(trans)


    def __event_btnExit_clicked(self):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Translator()
    w.show()
    sys.exit(app.exec())
