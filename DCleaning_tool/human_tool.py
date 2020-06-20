#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from PyQt4 import QtGui

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setGeometry(300, 100, 1000, 600)
        self.setWindowTitle("Human Recognition")
        self.setWindowIcon(QIcon("1.jpg"))

        gbox = QGroupBox(parent=self)
        gbox.setGeometry(0, 0, 600, 100)
        gbox.setTitle("Select")
        # btSelectFile = QPushButton()
        # btSelectFile.setText("Select pair list")
        # btSelectFile.clicked.connect(self.select_file_clicked)
        btSelectFolder = QPushButton()
        # btSelectFolder.initStyleOption(self, QStyleOptionButton.Flat)
        btSelectFolder.setText("Select Samples")
        btSelectFolder.clicked.connect(self.select_folder_clicked)
        # self.file_path = QLineEdit(parent=self)
        # self.file_path.hide()
        self.folder_path = QLineEdit(parent=self)
        self.folder_path.hide()
        grid = QGridLayout()
        # grid1.addWidget(btSelectFile, 1, 1)
        grid.addWidget(btSelectFolder, 1, 1)
        # grid1.addWidget(self.file_path, 2, 1)
        grid.addWidget(self.folder_path, 1, 2)
        gbox.setLayout(grid)

        # load pictures group
        gbox1 = QGroupBox(parent=self)
        gbox1.setGeometry(0, 100, 600, 400)
        gbox1.setTitle("pictures")
        self.l1 = QLabel()
        self.l1.setAlignment(Qt.AlignCenter)
        self.l2 = QLabel()
        self.l2.setAlignment(Qt.AlignCenter)
        grid1 = QGridLayout()
        grid1.addWidget(self.l1, 1, 1)
        grid1.addWidget(self.l2, 1, 2)
        gbox1.setLayout(grid1)

        # load buttons group2
        gbox2 = QGroupBox(parent=self)
        gbox2.setTitle("buttons")
        gbox2.setGeometry(0, 500, 600, 100)
        b1 = QPushButton()
        b1.setText("Previous Pair")
        b1.clicked.connect(self.previous_clicked)
        b2 = QPushButton()
        b2.setText("Same Person")
        # b1.move(50, 400)
        b2.clicked.connect(self.same_clicked)
        b3 = QPushButton()
        b3.setText("Different Person")
        b3.clicked.connect(self.diff_clicked)
        # QObject.connect(b2, SIGNAL("clicked()"), b2_clicked)
        b4 = QPushButton()
        b4.setText("Next Pair")
        b4.clicked.connect(self.next_clicked)
        grid2 = QGridLayout()
        grid2.addWidget(b1, 1, 1)
        grid2.addWidget(b2, 1, 2)
        grid2.addWidget(b3, 1, 3)
        grid2.addWidget(b4, 1, 4)

        self.order = QLineEdit(parent=self)
        self.order.hide()
        self.length = QLineEdit(parent=self)
        self.length.hide()
        grid2.addWidget(self.order, 2, 1)
        grid2.addWidget(self.length, 2, 2)
        gbox2.setLayout(grid2)

        # group3: pairs list
        gbox3 = QGroupBox(parent=self)
        gbox3.setTitle("Pair List")
        gbox3.setGeometry(600, 0, 400, 600)
        self.tv = QTableView(parent=self)
        grid3 = QGridLayout()
        grid3.addWidget(self.tv, 1, 1)
        btsave = QPushButton()
        btsave.setText("Save Result")
        btsave.clicked.connect(self.save_clicked)
        grid3.addWidget(btsave, 2, 1)
        gbox3.setLayout(grid3)
        # set the table model
        # columns = len(pair_list[0])
        self.model = QStandardItemModel(0, 4)
        self.model.setHorizontalHeaderLabels(['number', 'query name', 'target name', 'result']) # 'flag',
        # for row in range(len(pair_list)):
        #     for column in range(columns):
        #         item = QStandardItem(pair_list[row][column])
        #         self.model.setItem(row, column, item)
        self.tv.setModel(self.model)
        # self.tv.hideColumn(0)
        self.tv.hideColumn(1)
        self.tv.hideColumn(2)
        # self.tv.hideColumn(3)
        self.tv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tv.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv.verticalHeader().setVisible(False)
        # self.tv.resizeColumnsToContents()
        # define function of selection changed
        # self.tv.selectionModel().selectionChanged.connect(self.selection_Changed)


    def select_file_clicked(self):
        absolute_path = QFileDialog.getOpenFileName(self, 'Open file', '.', "CSV Files (*.csv)")
        self.file_path.setText(absolute_path)
        # if absolute_path:
        #     cur_path = QDir('.')
        #     relative_path = cur_path.relativeFilePath(absolute_path)
        print absolute_path

    def select_folder_clicked(self):
        sample_path = QFileDialog.getExistingDirectory(self, 'Select Samples')
        self.folder_path.setText(sample_path)

        # list_path = self.file_path.text()
        pair_list = []
        current_order = 1
        if sample_path is not None:
            t = csv.reader(open(sample_path + '/samples_list.csv'))
            for row in t:
                if row[0] == 'number':
                    continue
                pair_list.append(row)

            qry_name = pair_list[current_order - 1][1]
            trg_name = pair_list[current_order - 1][2]
            image1 = sample_path + '/' + qry_name
            image2 = sample_path + '/' + trg_name
            self.l1.setPixmap(QPixmap(image1))
            self.l1.setScaledContents(True)
            self.l1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.l2.setPixmap(QPixmap(image2))
            self.l2.setScaledContents(True)
            self.l2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.order.setText(str(current_order))
            self.length.setText(str(len(pair_list)))

            columns = len(pair_list[0])
            self.model = QStandardItemModel(len(pair_list), 4)
            # self.model.setHorizontalHeaderLabels(pair_list[0])
            self.model.setHorizontalHeaderLabels(['number', 'query name', 'target name', 'result']) # 'flag',
            for row in range(len(pair_list)):
                for column in range(4):
                    item = QStandardItem(pair_list[row][column])
                    self.model.setItem(row, column, item)
            self.tv.setModel(self.model)
            self.tv.selectRow(current_order - 1)
            self.tv.selectionModel().selectionChanged.connect(self.selection_Changed)

        print sample_path

    # define save table function
    def save_clicked(self):
        result_list = []
        item = ['number', 'qry_name', 'trg_name', 'exp_result'] # 'flag',
        result_list.append(item)

        path = self.folder_path.text()
        model = self.tv.model()
        for row in range(model.rowCount()):
            item = []
            for col in range(model.columnCount()):
                index = model.index(row, col)
                # a = model.data(index)
                # b = a.toString()
                # d = str(b)
                d = str(model.data(index).toString())
                item.append(d)
            result_list.append(item)
        t = open(path + "/samples_list.csv", "wb") #, encoding='utf8'
        file_r = csv.writer(t)
        file_r.writerows(result_list)

        #finish saving, pop message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Save Successfully!")
        retval = msg.exec_()

    def selection_Changed(self):
        selection = self.tv.selectionModel().selectedRows()
        index = selection[0]
        selected_order = index.row()
        self.order.setText(str(selected_order + 1))
        pair_list = []
        t = csv.reader(open(self.folder_path.text() + "/samples_list.csv"))
        for row in t:
            if row[0] == 'number':
                continue
            pair_list.append(row)
        qry_name = pair_list[selected_order][1]
        trg_name = pair_list[selected_order][2]
        image1 = self.folder_path.text() + '/' + qry_name
        image2 = self.folder_path.text() + '/' + trg_name
        self.l1.setPixmap(QPixmap(image1))
        self.l2.setPixmap(QPixmap(image2))
        # print "selection changed"

    # define function: previous button clicked
    def previous_clicked(self):
        current_order = int(self.order.text())
        sample_path = self.folder_path.text()
        if current_order == 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("This is already the first one")
            retval = msg.exec_()
        else:
            pre_order = current_order - 1
            self.order.setText(str(pre_order))
            self.tv.selectRow(pre_order-1)
            pair_list = []
            t = csv.reader(open(sample_path + "/samples_list.csv"))
            for row in t:
                if row[0] == 'number':
                    continue
                pair_list.append(row)
            qry_name = pair_list[pre_order - 1][1]
            trg_name = pair_list[pre_order - 1][2]
            image1 = sample_path + '/' + qry_name
            image2 = sample_path + '/' + trg_name
            self.l1.setPixmap(QPixmap(image1))
            self.l2.setPixmap(QPixmap(image2))

    # define function: two images are same person
    def same_clicked(self):
        current_order = int(self.order.text())
        self.model.setItem(current_order-1, 3, QStandardItem(str(1)))

    # define fuction: two images are different parson
    def diff_clicked(self):
        current_order = int(self.order.text())
        self.model.setItem(current_order - 1, 3, QStandardItem(str(-1)))

    # define function: next button is clicked
    def next_clicked(self):
        current_order = int(self.order.text())
        length = int(self.length.text())
        sample_path = self.folder_path.text()
        if current_order == length:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("This is already the last one")
            retval = msg.exec_()
        else:
            post_order = current_order + 1
            self.order.setText(str(post_order))
            self.tv.selectRow(post_order - 1)
            pair_list = []
            t = csv.reader(open(sample_path + "/samples_list.csv"))
            for row in t:
                if row[0] == 'number':
                    continue
                pair_list.append(row)
            qry_name = pair_list[post_order - 1][1]
            trg_name = pair_list[post_order - 1][2]
            image1 = sample_path + '/' + qry_name
            image2 = sample_path + '/' + trg_name
            self.l1.setPixmap(QPixmap(image1))
            self.l2.setPixmap(QPixmap(image2))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
