#! /usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import sys
import os

prog_path = os.path.dirname(os.path.abspath(__file__))

class UI_movieEntry(QDialog):
    def __init__(self, parent):
        super(UI_movieEntry, self).__init__(parent)
        self.parent = parent
        self.db = parent.conn
        self.setModal(True)

        # Load UI file
        uic.loadUi(prog_path+"/movieEntry.ui", self)

        # Define the Actions
        self.closeButton.clicked.connect(self.closeMovieEntry)
        self.saveButton.clicked.connect(self.saveMovieEntry)

        # if editing, show the previous data
        if self.parent.editing:
            self.bookEdit.setText(self.parent.olddata[0])
            self.pageEdit.setText(self.parent.olddata[1])
            self.mediaEdit.setText(self.parent.olddata[2])
            title = self.parent.olddata[3].replace(" / ", "\n")
            self.titleEdit.setText(title)
            self.closeButton.setText("Cancel")

        # Show the setWindow
        self.show()

    def closeMovieEntry(self):
        self.close()

    def saveMovieEntry(self):
        book = self.bookEdit.text()
        page = self.pageEdit.text()
        format = self.mediaEdit.text()
        title = self.titleEdit.toPlainText()
        title = title.replace("\n", " / ")
        cur = self.db.cursor()
        if self.parent.editing:
            oldtitle = self.parent.olddata[3].replace("\n", " / ")
            update = f"UPDATE movies SET book={book}, page={page}, format=\"{format}\", title=\"{title}\" WHERE book={self.parent.olddata[0]} AND page={self.parent.olddata[1]} AND format=\"{self.parent.olddata[2]}\" AND title=\"{oldtitle}\";"
            cur.execute(update)
            self.db.commit()
            self.close()
        else:
            cur.execute(f"INSERT INTO movies (book, page, format, title) VALUES ({book}, {page}, \"{format}\", \"{title}\");")
            self.bookEdit.setText("")
            self.pageEdit.setText("")
            self.mediaEdit.setText("")
            self.titleEdit.setText("")
            self.db.commit()

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi(prog_path+"/MovieDB.ui", self)

        # set up the table dimensions
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 50)
        self.tableWidget.setColumnWidth(3, 500)


        # Open the database
        self.conn = sqlite3.connect('MovieDB.sqlite')
        self.conn.row_factory = sqlite3.Row

        # define the local variables needed
        self.pagect = 0
        self.linect = 0
        self.sortByTitle = True

        # define the widgets
        '''
            searchTerm
            sortOrder
            TableWidget
            addMovie
            deleteMovie
            printButton
            movieCount
            statusbar
        '''

        # Connect up actions
        self.tableWidget.itemDoubleClicked.connect(self.editEntry)
        self.addMovie.clicked.connect(self.addMovieClicked)
        self.deleteMovie.clicked.connect(self.deleteMovieClicked)
        self.sortOrder.currentIndexChanged.connect(self.sortOrderChanged)
        self.searchTerm.textChanged.connect(self.searchChanged)
        self.clearSearch.clicked.connect(self.clearSearchClicked)
        self.printButton.clicked.connect(self.printReports)

        # load the table
        self.loadData()

        # Show the window
        self.show()

    def addMovieClicked(self):
        self.editing = False  # We're adding movies, not editing already existing ones
        self.UI_movie = UI_movieEntry(self)
        self.show()
        self.UI_movie.exec()
        self.loadData()
        self.setRecordCount()

    def deleteMovieClicked(self):
        sel = self.tableWidget.selectedItems()
        if sel:
            rows = sorted(list(set([r.row() for r in sel])), reverse=True)
            cur = self.conn.cursor()
            for row in rows:
                data = []
                for i in range(4):
                    data.append(self.tableWidget.item(row, i).text())
                data[3] = data[3].replace("\n", " / ")
                sql = f"DELETE FROM movies WHERE book={data[0]} and page={data[1]} and title=\"{data[3]}\";"
                cur.execute(sql)
            self.conn.commit()
            self.loadData()

    def searchChanged(self):
        searchText = self.searchTerm.text()
        items = self.tableWidget.findItems(searchText, Qt.MatchContains)
        if items:
            item = items[0]
            self.tableWidget.setCurrentItem(item)

    def clearSearchClicked(self):
        self.searchTerm.setText("")

    def sortOrderChanged(self):
        selected = self.sortOrder.currentIndex()
        if (selected == 1 and self.sortByTitle) or (selected == 0 and not self.sortByTitle):
            self.sortByTitle = not self.sortByTitle
        self.loadData()

    def editEntry(self, entryClicked):
        sel = self.tableWidget.selectedItems()
        if sel:
            rows = list(set([r.row() for r in sel]))
            if len(rows) == 1:
                self.olddata = []
                for i in range(4):
                    self.olddata.append(self.tableWidget.item(rows[0], i).text())
                self.olddata[3] = self.olddata[3].replace("\n", " / ")
                self.editing = True
                self.UI_movie = UI_movieEntry(self)
                self.show()
                self.UI_movie.exec()
                self.loadData()
                self.setRecordCount()

    def loadData(self):
        ct = self.setRecordCount()
        if self.sortByTitle:  # set the display order
            sql = "SELECT * from movies order by replace(replace(replace(title,'The ',''),'A ',''),'An ',''), book, page"
        else:
            sql = "SELECT * FROM movies ORDER BY book, page, title"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        self.tableWidget.setRowCount(ct)
        rowCount = 0
        for row in rows:
            title = row["title"].replace(" / ", "\n")
            item = QTableWidgetItem(str(row["book"]))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(rowCount, 0, item)
            item = QTableWidgetItem(str(row["page"]))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(rowCount, 1, item)
            item = QTableWidgetItem(row["format"])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(rowCount, 2, item)
            item = QTableWidgetItem(title)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(rowCount, 3, item)
            self.tableWidget.resizeRowToContents(rowCount)
            rowCount += 1

    def setRecordCount(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM movies")
        recs = cur.fetchone()[0]
        self.movieCount.setText(str(recs))
        return recs

    def printReports(self):
        self.moviesByTitle()
        self.moviesByBook()
        self.statusbar.showMessage("Reports saved to movieList.txt and bookList.txt")

    def reportHeader(self, output, firstCall=False):
    	''' Create the page header for the movie report, sorted by title.

    	    Use a local static variable (reportHeader.pagect) to number the pages.
    		The firstCall parameter, set to True, will cause page numbering
    		to begin at one again, so that multiple reports can be generated
    		using the same header routine.
    	'''
    	if firstCall:  # Start of a new report. Set page number to 1
    		self.pagect = 1
    	else:
    		self.pagect += 1

    	print("\n" * 3, file=output)
    	print(" " * 4, f"     Movies, sorted by title           pg {self.pagect:4d}\n", file=output)
    	print("     Bk Pg  fmt     Title", file=output)
    	return 6 # number of lines consumed


    def bookHeader(self, output, firstCall=False):
    	''' Create the page header for the movie report, sorted by book and page.

    	    Use a local static variable (bookHeader.pagect) to number the pages.
    		The firstCall parameter, set to True, will cause page numbering
    		to begin at one again, so that multiple reports can be generated
    		using the same header routine.
    	'''
    	if firstCall:
    		self.pagect = 1
    	else:
    		self.pagect += 1

    	print("\n" * 3, file=output)
    	print(" " * 4, f"     Movies, sorted by book and page          pg {self.pagect:4d}\n", file=output)
    	print("     Bk Pg  fmt     Title", file=output)
    	return 6


    def reportDetail(self, output, header, row, firstCall=False):
    	''' Create a report detail line, accounting for page overflows.

    		Use 56 lines as a complete page.
    		The firstCall parameter, when True, will initialize a new report.

    		output is the open file to write to.
    		header is the function to call to generate a new page header.
    		row is the SQLite3 row object to write to the report.
    	'''
    	if firstCall:  # Start a new report. Set line count to 0
    		self.linect = header(output, firstCall=True)

    	if self.linect > 56:
    		print("\f", file=output)  # formfeed to next page
    		self.linect = header(output)

    	titles = row['title'].split("/")
    	print(f"     {row['book']:2d} {row['page']:2d} ({row['format']:4s})   {titles[0]}", file=output)
    	if len(titles) > 1:
    		for title in titles[1:]:
    			print(f"                 + {title}", file=output)
    	self.linect += len(titles)


    def moviesByTitle(self):
    	''' Generate the Movies sorted by title report, save in movieList.txt '''
    	with open("movieList.txt", "w") as out:
            c = self.conn.cursor()
            first = True
            for row in c.execute("SELECT * from movies order by replace(replace(replace(title,'The ',''),'A ',''),'An ',''), book, page"):
                self.reportDetail(out, self.reportHeader, row, firstCall=first)
                first = False
            print(f"\n     Movie count: {self.setRecordCount()}", file=out)


    def moviesByBook(self):
    	''' Generate the Movies by book, page report, save in bookList.txt '''
    	with open("bookList.txt", "w") as out:
            c = self.conn.cursor()
            first = True
            for row in c.execute("SELECT * from movies order by book, page"):
                self.reportDetail(out, self.bookHeader, row, firstCall=first)
                first=False
            print(f"\n     Movie count: {self.setRecordCount()}", file=out)


# Initialize the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
