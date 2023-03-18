#! /usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QDialog, \
    QApplication, QLabel, QComboBox, QTableWidget, \
    QTableWidgetItem, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import sys
import os
from fpdf import FPDF
from datetime import datetime, date

version = "2.0"
prog_path = os.path.dirname(os.path.abspath(__file__))


class Title_report (FPDF):
    def __init__(self, recordCount):
        super().__init__("P", "mm", "Letter")
        self.record_count = recordCount
        self.first_page = True
        self.set_fill_color(220,220,220)
        self.fill = False
        self.add_page()

    def page_break_needed(self,titles):
        number_lines = len(titles.split("\n"))
        # 279.5mm = height of an 11 in page
        # 20mm = an estimate of the size of the footer
        page_left = 279.5 - self.get_y() - 20
        if (number_lines * 6) > page_left:
            return True
        return False

    def header(self):
        self.image(prog_path + '/MovieDB.JPG',170,10,20)
        self.set_font('Times', 'B',15)
        self.cell(80)
        self.cell(30,10,'Movies by Title',0,0,'C')
        self.ln()
        self.set_font('Times', 'B', 10)
        self.cell(15, 10, "Book",0,0,'R')
        self.cell(15, 10, "Page",0,0,'R')
        self.cell(15, 10, "Fmt",0,0,'L')
        self.cell(0, 10, "Title",0,0,'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(40,10,f"{date.today()}",0,0,'L')
        self.cell(40,10,f"page {self.page_no()}",0,0,'C')
        self.cell(0, 10, f"total entries: {self.record_count}")

    def detail(self, row):
        titles = "\n".join((row['title'].split("/")))
        if self.first_page:
            self.set_font('Arial', 'B', 15)
            self.cell(45,15," ",0,0,'L',False)
            self.cell(0,15,"#",0,0,'L',False)
            self.ln(15)
            self.first_page = False
            self.character = '#'
        else:
            start_char = row['sort_title'][:1]
            if start_char.lower() in "abcdefghijklmnopqrstuvwxyz":
                if start_char.lower() != self.character:
                    if self.page_break_needed(titles + '\n\n\n'):
                        self.add_page()
                    self.character = start_char.lower()
                    self.set_font('Arial', 'B', 15)
                    self.cell(45, 15, " ",0,0,'L')
                    self.cell(0, 15, self.character.upper(),0,0,'L')
                    self.ln(15)

        if self.page_break_needed(titles):
            self.add_page()
        self.set_font('Arial','',10)
        self.cell(15,5,str(row['book']),0,0,'R',self.fill)
        self.cell(15,5,str(row['page']),0,0,'R',self.fill)
        self.cell(15,5,str(row['format']),0,0,'L',self.fill)
        self.multi_cell(0,5,titles,0,'L',self.fill)
        self.fill = not self.fill


class Detail_report (FPDF):
    def __init__(self, recordCount):
        super().__init__("P", "mm", "Letter")
        self.record_count = recordCount
        self.first_page = True
        self.set_fill_color(220,220,220)
        self.fill = False
        self.add_page()

    def page_break_needed(self,titles):
        number_lines = len(titles.split("\n"))
        # 279.5mm = height of an 11 in page
        # 20mm = an estimate of the size of the footer
        page_left = 279.5 - self.get_y() - 20
        if (number_lines * 6) > page_left:
            return True
        return False

    def header(self):
        self.image(prog_path + '/MovieDB.JPG',170,10,20)
        self.set_font('Times', 'B',15)
        self.cell(80)
        self.cell(30,10,'Movies with Additional Detail',0,0,'C')
        self.ln()
        self.set_font('Times', 'B', 10)
        self.cell(15, 10, "Book",0,0,'R')
        self.cell(15, 10, "Page",0,0,'R')
        self.cell(15, 10, "Fmt",0,0,'L')
        self.cell(0, 10, "Title",0,0,'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(40,10,f"{date.today()}",0,0,'L')
        self.cell(40,10,f"page {self.page_no()}",0,0,'C')
        self.cell(0, 10, f"total entries: {self.record_count}")

    def detail(self, row):
        titles = "\n".join((row['title'].split("/")))
        if row["actors"]:
            actors = "\n".join((row["actors"].split("/")))
        if row["description"]:
            description = "\n".join((row["description"].split("/")))
        if self.first_page:
            self.set_font('Arial', 'B', 15)
            self.cell(45,15," ",0,0,'L',False)
            self.cell(0,15,"#",0,0,'L',False)
            self.ln(15)
            self.first_page = False
            self.character = '#'
        else:
            start_char = row['sort_title'][:1]
            if start_char.lower() in "abcdefghijklmnopqrstuvwxyz":
                if start_char.lower() != self.character:
                    if self.page_break_needed(titles + '\n\n\n'):
                        self.add_page()
                    self.character = start_char.lower()
                    self.set_font('Arial', 'B', 15)
                    self.cell(45, 15, " ",0,0,'L')
                    self.cell(0, 15, self.character.upper(),0,0,'L')
                    self.ln(15)

        if self.page_break_needed(titles):
            self.add_page()
        self.set_font('Arial','',10)
        self.cell(15,5,str(row['book']),0,0,'R',self.fill)
        self.cell(15,5,str(row['page']),0,0,'R',self.fill)
        self.cell(15,5,str(row['format']),0,0,'L',self.fill)
        self.multi_cell(0,5,titles,0,'L',self.fill)
        if row["actors"]:
            self.ln(0)
            self.cell(55,5,"- ",0,0,'R')
            self.multi_cell(0,5,actors,0,'L',self.fill)
        if row["description"]:
            self.ln(0)
            self.cell(55,5,"- ",0,0,'R')
            self.multi_cell(0,5,description,0,'L',self.fill)
        self.fill = not self.fill


class Book_report (FPDF):
    def __init__(self, recordCount):
        super().__init__("P", "mm", "Letter")
        self.record_count = recordCount
        self.book_number = 1
        self.add_page()

    def page_break_needed(self,titles):
        number_lines = len(titles.split("\n"))
        # 279.5mm = height of an 11 in page
        # 20mm = an estimate of the size of the footer
        page_left = 279.5 - self.get_y() - 20
        if (number_lines * 6) > page_left:
            return True
        return False

    def header(self):
        self.image(prog_path + '/MovieDB.JPG',170,10,20)
        self.set_font('Times', 'B',15)
        self.cell(80)
        self.cell(30,10,f'Movies - Book {self.book_number}',0,0,'C')
        self.ln()
        self.set_font('Times', 'B', 10)
        self.cell(15, 10, "Book",0,0,'R')
        self.cell(15, 10, "Page",0,0,'R')
        self.cell(15, 10, "Fmt",0,0,'L')
        self.cell(0, 10, "Title",0,0,'L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(40,10,f"{date.today()}",0,0,'L')
        self.cell(40,10,f"page {self.page_no()}",0,0,'C')
        self.cell(0, 10, f"total entries: {self.record_count}")

    def detail(self, row):
        titles = "\n".join((row['title'].split("/")))
        if row['book'] != self.book_number:
            self.book_number = row['book']
            self.add_page()
        self.set_font('Arial','',10)
        self.cell(15,5,str(row['book']),0,0,'R')
        self.cell(15,5,str(row['page']),0,0,'R')
        self.cell(15,5,str(row['format']),0,0,'L')
        self.multi_cell(0,5,titles,0,'L',False)


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
            cur = self.db.cursor()
            sql = f"SELECT * FROM movies WHERE book={self.parent.olddata[0]} AND page={self.parent.olddata[1]} AND format=\"{self.parent.olddata[2]}\" AND title=\"{self.parent.olddata[3]}\";"
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) == 1:
                row = rows[0]
                self.bookEdit.setText(str(row["book"]))
            self.pageEdit.setText(str(row["page"]))
            self.mediaEdit.setText(row["format"])
            title = row["title"].replace(" / ", "\n")
            if row["actors"]:
                actors = row["actors"].replace(" / ", "\n")
            else:
                actors = ""
            if row["description"]:
                description = row["description"].replace(" / ", "\n")
            else:
                description = ""
            self.titleEdit.setText(title)
            self.actorsEdit.setText(actors)
            self.descriptionEdit.setText(description)
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
        actors = self.actorsEdit.toPlainText()
        actors = actors.replace("\n", " / ")
        description = self.descriptionEdit.toPlainText()
        description = description.replace("\n", " / ")
        cur = self.db.cursor()
        if self.parent.editing:
            oldtitle = self.parent.olddata[3].replace("\n", " / ")
            update = f"UPDATE movies SET book={book}, page={page}, format=\"{format}\", title=\"{title}\", actors=\"{actors}\", description=\"{description}\" WHERE book={self.parent.olddata[0]} AND page={self.parent.olddata[1]} AND format=\"{self.parent.olddata[2]}\" AND title=\"{oldtitle}\";"
            cur.execute(update)
            self.db.commit()
            self.close()
        else:
            insert = f"INSERT INTO movies (book, page, format, title, actors, description) VALUES ({book}, {page}, \"{format}\", \"{title}\", \"{actors}\", \"{description}\");"
            cur.execute(insert)
            self.bookEdit.setText("")
            self.pageEdit.setText("")
            self.mediaEdit.setText("")
            self.titleEdit.setText("")
            self.actorsEdit.setText("")
            self.descriptionEdit.setText("")
            self.bookEdit.setFocus()
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
        # column 5 (title) fills out the width

        def onResize(event):
            print("resize")

        #self.resize.connect(self.onResize)

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
                for i in range(6):
                    data.append(self.tableWidget.item(row, i).text())
                for i in range(3,6):
                    data[i] = data[i].replace("\n", " / ")
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
                    if self.tableWidget.item(rows[0], i):
                        self.olddata.append(self.tableWidget.item(rows[0], i).text())
                    else:
                        self.olddata.append("")
                    self.olddata[i] = self.olddata[i].replace("\n", " / ")
                self.editing = True
                self.UI_movie = UI_movieEntry(self)
                self.show()
                self.UI_movie.exec()
                self.loadData()
                self.setRecordCount()

    def loadData(self):
        ct = self.setRecordCount()
        if self.sortByTitle:  # set the display order
            sql = "SELECT *, replace(replace(replace(title,'The ',''),'A ',''),'An ','') as sort_title from movies order by sort_title, book, page"
        else:
            sql = "SELECT * FROM movies ORDER BY book, page, title"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.tableWidget.setRowCount(ct)
        self.tableWidget.setColumnCount(4) # possibly 6? (2 hidden)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        rowCount = 0
        for row in rows:
            item = QTableWidgetItem(str(row["book"]))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(rowCount, 0, item)
            item = QTableWidgetItem(str(row["page"]))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(rowCount, 1, item)
            item = QTableWidgetItem(row["format"])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(rowCount, 2, item)
            title = row["title"].replace(" / ", "\n")
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
        record_count = self.setRecordCount()
        ''' Generate the Movies sorted by title report '''
        report = Title_report(record_count)
        output_file = "MovieDB.Title.pdf"
        sql = "SELECT *, replace(replace(replace(title,'The ',''),'A ',''),'An ','') as sort_title from movies order by sort_title, book, page"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            report.detail(row)
        report.output(output_file)

        ''' Generate the Movies with Details report '''
        report = Detail_report(record_count)
        output_file = "MovieDB.Detail.pdf"
        for row in rows:
            report.detail(row)
        report.output(output_file)

        ''' Generate the Movies by Book and Page report '''
        report = Book_report(record_count)
        output_file = "MovieDB.Books.pdf"
        sql = "SELECT * FROM movies ORDER BY book, page, title"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            report.detail(row)
        report.output(output_file)
        self.statusbar.showMessage("Reports saved to MovieDB.<report>.pdf")


# Initialize the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
