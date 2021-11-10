# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'movieEntry.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_movieEntry(object):
    def setupUi(self, movieEntry):
        movieEntry.setObjectName("movieEntry")
        movieEntry.resize(581, 300)
        movieEntry.setModal(True)
        self.saveButton = QtWidgets.QPushButton(movieEntry)
        self.saveButton.setGeometry(QtCore.QRect(440, 250, 113, 32))
        self.saveButton.setObjectName("saveButton")
        self.closeButton = QtWidgets.QPushButton(movieEntry)
        self.closeButton.setGeometry(QtCore.QRect(300, 250, 113, 32))
        self.closeButton.setObjectName("closeButton")
        self.label = QtWidgets.QLabel(movieEntry)
        self.label.setGeometry(QtCore.QRect(50, 40, 60, 16))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(movieEntry)
        self.label_2.setGeometry(QtCore.QRect(50, 60, 60, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(movieEntry)
        self.label_3.setGeometry(QtCore.QRect(50, 100, 60, 16))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(movieEntry)
        self.label_4.setGeometry(QtCore.QRect(50, 130, 60, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.bookEdit = QtWidgets.QLineEdit(movieEntry)
        self.bookEdit.setGeometry(QtCore.QRect(120, 40, 113, 21))
        self.bookEdit.setObjectName("bookEdit")
        self.pageEdit = QtWidgets.QLineEdit(movieEntry)
        self.pageEdit.setGeometry(QtCore.QRect(120, 60, 113, 21))
        self.pageEdit.setObjectName("pageEdit")
        self.mediaEdit = QtWidgets.QLineEdit(movieEntry)
        self.mediaEdit.setGeometry(QtCore.QRect(120, 100, 113, 21))
        self.mediaEdit.setObjectName("mediaEdit")
        self.titleEdit = QtWidgets.QTextEdit(movieEntry)
        self.titleEdit.setGeometry(QtCore.QRect(120, 130, 421, 101))
        self.titleEdit.setObjectName("titleEdit")
        self.label_5 = QtWidgets.QLabel(movieEntry)
        self.label_5.setGeometry(QtCore.QRect(250, 100, 121, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(movieEntry)
        QtCore.QMetaObject.connectSlotsByName(movieEntry)

    def retranslateUi(self, movieEntry):
        _translate = QtCore.QCoreApplication.translate
        movieEntry.setWindowTitle(_translate("movieEntry", "Movie:"))
        self.saveButton.setText(_translate("movieEntry", "Save"))
        self.closeButton.setText(_translate("movieEntry", "Close"))
        self.label.setText(_translate("movieEntry", "Book:"))
        self.label_2.setText(_translate("movieEntry", "Page:"))
        self.label_3.setText(_translate("movieEntry", "Media:"))
        self.label_4.setText(_translate("movieEntry", "Title:"))
        self.label_5.setText(_translate("movieEntry", "(D, B, 3, 4, E)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    movieEntry = QtWidgets.QDialog()
    ui = Ui_movieEntry()
    ui.setupUi(movieEntry)
    movieEntry.show()
    sys.exit(app.exec_())
