from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QComboBox
from PyQt5 import uic
import sys

class UI_movieEntry(QDialog):
    def __init__(self, db):
        super(UI_movieEntry, self).__init__()

        # Load ui file
        uic.loadUi("movieEntry.ui", self)

        # save the database connection
        self.db = db

        # define the widgets

        # Connect up actions
        self.saveButton.clicked.connect(self.saveClicked)
        self.closeButton.clicked.connect(self.closeClicked)

        # Show the window
        self.show()

    def saveClicked(self):
        book = self.bookEdit.text()
        page = self.pageEdit.text()
        format = self.mediaEdit.text()
        title = self.titleEdit.toPlainText()
        title = title.replace("\n", " / ")
        print(f"db: {self.db} - {book}/{page} - {format}: {title}")

        self.bookEdit.setText("")
        self.pageEdit.setText("")
        self.mediaEdit.setText("")
        self.titleEdit.setText("")

    def closeClicked(self):
        self.close()


# Initialize the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI_movieEntry("testdb")
    app.exec_()
