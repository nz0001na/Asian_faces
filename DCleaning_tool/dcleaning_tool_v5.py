#!/usr/bin/env python
# -*- coding: utf-8 -*-

# update:
# add shortcut

import sys
import os
import csv
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from PyQt4 import QtGui

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setGeometry(50, 50, 1200, 650)
        self.setWindowTitle("Data Cleaning")
        self.setWindowIcon(QIcon("data_cleaning.jpg"))

        # Select Button
        gbox_select = QGroupBox(parent=self)
        gbox_select.setGeometry(0, 0, 1000, 60)
        gbox_select.setTitle("Select")

        btSelectFolder = QPushButton()
        # btSelectFolder.initStyleOption(self, QStyleOptionButton.Flat)
        btSelectFolder.setText("Select DataSet")
        btSelectFolder.clicked.connect(self.select_folder_clicked)

        self.folder_path = QLineEdit(parent=self)
        # self.folder_path.hide()

        grid_select = QGridLayout()
        grid_select.addWidget(btSelectFolder, 1, 1)
        grid_select.addWidget(self.folder_path, 1, 2)
        gbox_select.setLayout(grid_select)

        # subjects list Folders
        gbox_sujects = QGroupBox(parent=self)
        gbox_sujects.setTitle("Subjects")
        gbox_sujects.setGeometry(0, 60, 200, 590)

        self.tv_subjects = QTableView(parent=self)
        self.tv_subjects.resizeColumnsToContents()
        grid_subjects = QGridLayout()
        grid_subjects.addWidget(self.tv_subjects, 1, 1)
        gbox_sujects.setLayout(grid_subjects)

        # set the table model of subjects
        self.model_subjects = QStandardItemModel(0, 2)
        self.model_subjects.setHorizontalHeaderLabels(['ID', 'Status'])
        self.tv_subjects.setModel(self.model_subjects)
        # self.tv_subjects.hideColumn(0)
        # self.tv_subjects.hideColumn(1)
        self.tv_subjects.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tv_subjects.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_subjects.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_subjects.verticalHeader().setVisible(True)
        # self.tv_subjects.setFocusPolicy(Qt.TabFocus)

        # load references pictures group
        gbox_Target_images = QGroupBox(parent=self)
        gbox_Target_images.setGeometry(200, 60, 400, 530)
        gbox_Target_images.setTitle("Target Subject")
        self.l1 = QLabel()
        self.l1.setAlignment(Qt.AlignCenter)
        self.l2 = QLabel()
        self.l2.setAlignment(Qt.AlignCenter)
        self.l3 = QLabel()
        self.l3.setAlignment(Qt.AlignCenter)
        self.l4 = QLabel()
        self.l4.setAlignment(Qt.AlignCenter)
        grid_target = QGridLayout()
        grid_target.addWidget(self.l1, 1, 1)
        grid_target.addWidget(self.l2, 1, 2)
        grid_target.addWidget(self.l3, 2, 1)
        grid_target.addWidget(self.l4, 2, 2)
        gbox_Target_images.setLayout(grid_target)

        # load clean images
        gbox_clean_image = QGroupBox(parent=self)
        gbox_clean_image.setGeometry(600, 60, 400, 530)
        gbox_clean_image.setTitle("Cleaning Image")
        self.l5 = QLabel()
        self.l5.setAlignment(Qt.AlignCenter)
        grid_clean = QGridLayout()
        grid_clean.addWidget(self.l5, 1, 2)
        gbox_clean_image.setLayout(grid_clean)

        # define invisible variable
        self.label_id = QLabel()
        self.label_id.setAlignment(Qt.AlignLeft)
        self.label_id.setText('Subject ID:')
        self.subject_id = QLineEdit(parent=self)
        self.subject_id.setReadOnly(True)
        # self.subject_id.hide()
        self.label_name = QLabel()
        self.label_name.setAlignment(Qt.AlignLeft)
        self.label_name.setText('Image Name:')
        self.image_name = QLineEdit(parent=self)
        self.image_name.setReadOnly(True)
        # self.image_name.hide()
        self.label_number = QLabel()
        self.label_number.setAlignment(Qt.AlignLeft)
        self.label_number.setText('Image Number:')
        self.order = QLineEdit(parent=self)
        self.order.setReadOnly(True)
        # self.order.hide()
        grid_clean.addWidget(self.label_id, 2, 1)
        grid_clean.addWidget(self.subject_id, 2, 2)
        grid_clean.addWidget(self.label_name, 3, 1)
        grid_clean.addWidget(self.image_name, 3, 2)
        grid_clean.addWidget(self.label_number, 4, 1)
        grid_clean.addWidget(self.order, 4, 2)
        gbox_clean_image.setLayout(grid_clean)

        # load buttons group
        gbox_button = QGroupBox(parent=self)
        gbox_button.setTitle("buttons")
        gbox_button.setGeometry(200, 590, 800, 60)
        b_prev = QPushButton()
        b_prev.setText("Previous")
        b_prev.clicked.connect(self.previous_clicked)
        # b_keep = QPushButton()
        # b_keep.setText("Keep")
        # b_keep.clicked.connect(self.keep_clicked)
        b_remove = QPushButton()
        b_remove.setText("Remove")
        b_remove.clicked.connect(self.remove_clicked)
        b_next = QPushButton()
        b_next.setText("Next")
        b_next.clicked.connect(self.next_clicked)
        grid_button = QGridLayout()
        grid_button.addWidget(b_prev, 1, 1)
        # grid_button.addWidget(b_keep, 1, 2)
        grid_button.addWidget(b_remove, 1, 2)
        grid_button.addWidget(b_next, 1, 3)
        gbox_button.setLayout(grid_button)

        # load image list
        gbox_list = QGroupBox(parent=self)
        gbox_list.setTitle("Image List")
        gbox_list.setGeometry(1000, 0, 200, 650)

        self.tv_images = QTableView(parent=self)
        grid_list = QGridLayout()
        grid_list.addWidget(self.tv_images, 1, 1)

        btsave = QPushButton()
        btsave.setText("Save Result")
        btsave.clicked.connect(self.save_clicked)
        grid_list.addWidget(btsave, 2, 1)
        gbox_list.setLayout(grid_list)

        # set the table model of image list
        self.model_image = QStandardItemModel(0, 2)
        self.model_image.setHorizontalHeaderLabels(['Name', 'Status'])
        self.tv_images.setModel(self.model_image)
        # self.tv_images.hideColumn(0)
        # self.tv_images.hideColumn(1)
        self.tv_images.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tv_images.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_images.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_images.verticalHeader().setVisible(True)


        self.connect(QShortcut(QKeySequence(Qt.Key_Left), self), SIGNAL('activated()'),
                     self.tvsubject_focus)
        self.connect(QShortcut(QKeySequence(Qt.Key_Right), self), SIGNAL('activated()'),
                     self.tvimage_focus)
        self.connect(QShortcut(QKeySequence(Qt.Key_Escape), self), SIGNAL('activated()'),
                     self.remove_clicked)
        self.connect(QShortcut(QKeySequence(Qt.Key_F1), self), SIGNAL('activated()'),
                     self.save_clicked)

    def tvsubject_focus(self):
        self.tv_subjects.setFocus()

    def tvimage_focus(self):
        self.tv_images.setFocus()

    # Select DataSet
    def select_folder_clicked(self):
        dataset_path = QFileDialog.getExistingDirectory(self, 'Select DataSet')

        if dataset_path == '':
            print 'Not to select folder'
        else:
            self.folder_path.setText(dataset_path)

            # create result folder
            result_path = "clean_result/"
            if (os.path.exists(result_path) == False):
                os.mkdir(result_path)

            # get all folders in selected path
            subjects = []
            if (os.path.exists(dataset_path)):
                subjects = os.listdir(dataset_path)
                # print subjects

            subject_list = []
            if (os.path.exists("subject_list.csv")):
                t = csv.reader(open("subject_list.csv"))
                for row in t:
                    subject_list.append(row)
                # print 'b'
            else:
                for s in subjects:
                    item = [str(s), 'uncleaned!']
                    subject_list.append(item)
                t = open("subject_list.csv", "wb")  # , encoding='utf8'
                file_r = csv.writer(t)
                file_r.writerows(subject_list)
            # print subject_list

            # columns = len(subject_list[0])
            self.model_subjects = QStandardItemModel(len(subject_list), 2)
            # self.model_subjects.setHorizontalHeaderLabels(pair_list[0])
            self.model_subjects.setHorizontalHeaderLabels(['ID', 'Status'])
            for row in range(len(subject_list)):
                for column in range(2):
                    item = QStandardItem(subject_list[row][column])
                    self.model_subjects.setItem(row, column, item)
            self.tv_subjects.setModel(self.model_subjects)
            # self.tv_subjects.selectRow(current_order - 1)
            self.tv_subjects.selectionModel().selectionChanged.connect(self.Subject_Selection_Changed)

            # recover to null
            self.l1.clear()
            self.l2.clear()
            self.l3.clear()
            self.l4.clear()
            self.l5.clear()
            self.subject_id.clear()
            self.image_name.clear()
            self.order.clear()
            self.model_image.clear()


    # change subjects
    def Subject_Selection_Changed(self):
        selection = self.tv_subjects.selectionModel().selectedRows()
        index = selection[0]
        subject_id = str(self.model_subjects.data(index).toString())
        self.subject_id.setText(str(subject_id))

        # load target images
        target_path = "target_images/" + subject_id
        target_images = []
        if (os.path.exists(target_path)):
            target_images = os.listdir(target_path)
        # print target_images

        # Scaled Image
        q_image = QPixmap(target_path + "/" + target_images[0])
        qImageSize = q_image.size()
        qLabelSize = self.l1.size()
        dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
        dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
        if (dWidthRatio > dHeightRatio):
            qScaledImage = q_image.scaledToWidth(qLabelSize.width())
        else:
            qScaledImage = q_image.scaledToHeight(qLabelSize.height())
        self.l1.setPixmap(qScaledImage)
        self.l1.show()
        # self.l1.setPixmap(QPixmap(target_path + "\\" + target_images[0]))

        q_image = QPixmap(target_path + "/" + target_images[1])
        qImageSize = q_image.size()
        qLabelSize = self.l2.size()
        dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
        dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
        if (dWidthRatio > dHeightRatio):
            qScaledImage = q_image.scaledToWidth(qLabelSize.width())
        else:
            qScaledImage = q_image.scaledToHeight(qLabelSize.height())
        self.l2.setPixmap(qScaledImage)
        self.l2.show()
        #    self.l2.setPixmap(QPixmap(target_path + "\\" + target_images[1]))

        q_image = QPixmap(target_path + "/" + target_images[2])
        qImageSize = q_image.size()
        qLabelSize = self.l3.size()
        dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
        dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
        if (dWidthRatio > dHeightRatio):
            qScaledImage = q_image.scaledToWidth(qLabelSize.width())
        else:
            qScaledImage = q_image.scaledToHeight(qLabelSize.height())
        self.l3.setPixmap(qScaledImage)
        self.l3.show()
        # self.l3.setPixmap(QPixmap(target_path + "\\" + target_images[2]))


        q_image = QPixmap(target_path + "/" + target_images[3])
        qImageSize = q_image.size()
        qLabelSize = self.l4.size()
        dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
        dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
        if (dWidthRatio > dHeightRatio):
            qScaledImage = q_image.scaledToWidth(qLabelSize.width())
        else:
            qScaledImage = q_image.scaledToHeight(qLabelSize.height())
        self.l4.setPixmap(qScaledImage)
        self.l4.show()
        # self.l4.setPixmap(QPixmap(target_path + "\\" + target_images[3]))

        # self.l1.setScaledContents(True)
        # self.l2.setScaledContents(True)
        # self.l3.setScaledContents(True)
        # self.l4.setScaledContents(True)

        # load clean images list
        clean_images = []
        clean_id_path = self.folder_path.text() + "/" + subject_id
        if (os.path.exists(clean_id_path)):
            clean_images = os.listdir(clean_id_path)

        # create result file
        result_file = "clean_result/" + subject_id + '.csv'
        image_list = []
        if (os.path.exists(result_file)):
            t = csv.reader(open(result_file))
            for row in t:
                image_list.append(row)
            # print 'p'
        else:
            for s in clean_images:
                item = [str(s), '?']
                image_list.append(item)
            # t = open(result_file, "wb")  # , encoding='utf8'
            # file_r = csv.writer(t)
            # file_r.writerows(image_list)
        # print image_list

        # set first image
        current_order = 1
        self.order.setText(str(current_order))

        q_image = QPixmap(clean_id_path + "/" + clean_images[0])
        qImageSize = q_image.size()
        qLabelSize = self.l5.size()
        dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
        dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
        if (dWidthRatio > dHeightRatio):
            qScaledImage = q_image.scaledToWidth(qLabelSize.width())
        else:
            qScaledImage = q_image.scaledToHeight(qLabelSize.height())
        self.l5.setPixmap(qScaledImage)
        self.l5.show()
        # self.l5.setScaledContents(True)
        self.image_name.setText(clean_images[0])

        # initial image list
        self.model_image = QStandardItemModel(len(image_list), 2)
        # self.model.setHorizontalHeaderLabels(pair_list[0])
        self.model_image.setHorizontalHeaderLabels(['Name', 'Status'])
        for row in range(len(image_list)):
            for column in range(2):
                item = QStandardItem(image_list[row][column])
                self.model_image.setItem(row, column, item)
        self.tv_images.setModel(self.model_image)
        self.tv_images.selectRow(current_order - 1)
        self.tv_images.selectionModel().selectionChanged.connect(self.Image_Selection_Changed)
        self.model_image.setItem(current_order - 1, 1, QStandardItem(str("keep")))


    # define change images
    def Image_Selection_Changed(self):
        selection = self.tv_images.selectionModel().selectedRows()
        index = selection[0]
        selected_order = index.row()
        self.model_image.setItem(selected_order, 1, QStandardItem(str("keep")))
        self.order.setText(str(selected_order + 1))

        image_name = str(self.model_image.data(index).toString())
        self.image_name.setText(image_name)
        # print image_name
        folder_path = self.folder_path.text()
        subject_id = self.subject_id.text()


        q_image = QPixmap(folder_path + "/" +subject_id + "/" + image_name)
        qImageSize = q_image.size()
        qLabelSize = self.l5.size()
        dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
        dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
        if (dWidthRatio > dHeightRatio):
            qScaledImage = q_image.scaledToWidth(qLabelSize.width())
        else:
            qScaledImage = q_image.scaledToHeight(qLabelSize.height())
        self.l5.setPixmap(qScaledImage)
        self.l5.show()
        # self.l5.setPixmap(QPixmap(folder_path + "\\" +subject_id + "\\" + image_name))
        # self.l5.setScaledContents(True)



    # define save table function- test if finished
    def save_clicked(self):
        self.tvsubject_focus()

        result_list = []
        # item = ['Image Name', 'Status']
        # result_list.append(item)

        subject_id = self.subject_id.text()
        path = "clean_result/" + subject_id + '.csv'
        model = self.tv_images.model()
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
        t = open(path, "wb") #, encoding='utf8'
        file_r = csv.writer(t)
        file_r.writerows(result_list)

        subject_list = []
        if (os.path.exists("subject_list.csv")):
            t = csv.reader(open("subject_list.csv"))
            for row in t:
                subject_list.append(row)

        flag = 0 # indicate status, 1:uncleaned, 0:ok
        for row in result_list:
            if row[1] == '?':
                flag = 1
        subject_list2 = []
        for s in subject_list:
            item = []
            if s[0] == subject_id:
                if flag == 0:  # cleaned
                    item = [subject_id, 'OK']
                if flag == 1:  # cleaning...
                    item = [subject_id, 'cleaning...']
                subject_list2.append(item)
            else:
                subject_list2.append(s)

        t = open("subject_list.csv", "wb")  # , encoding='utf8'
        file_r = csv.writer(t)
        file_r.writerows(subject_list2)

        # reload subjects list
        self.model_subjects = QStandardItemModel(len(subject_list2), 2)
        self.model_subjects.setHorizontalHeaderLabels(['ID', 'Status'])
        for row in range(len(subject_list2)):
            for column in range(2):
                item = QStandardItem(subject_list2[row][column])
                self.model_subjects.setItem(row, column, item)
        self.tv_subjects.setModel(self.model_subjects)
        # self.tv_subjects.selectRow(current_order - 1)
        self.tv_subjects.selectionModel().selectionChanged.connect(self.Subject_Selection_Changed)

        #finish saving, pop message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Save Successfully!")
        retval = msg.exec_()


    # define function: previous button clicked
    def previous_clicked(self):
        current_order = int(self.order.text())
        # folder_path = self.folder_path.text()
        if current_order == 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("This is already the first one")
            retval = msg.exec_()
        else:
            pre_order = current_order - 1
            self.order.setText(str(pre_order))
            self.tv_images.selectRow(pre_order-1)

            # load clean images list
            clean_images = []
            clean_id_path = self.folder_path.text() + "/" + self.subject_id.text()
            if (os.path.exists(clean_id_path)):
                clean_images = os.listdir(clean_id_path)

            image = clean_id_path + "/" + clean_images[pre_order-1]
            q_image = QPixmap(image)
            qImageSize = q_image.size()
            qLabelSize = self.l5.size()
            dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
            dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
            if (dWidthRatio > dHeightRatio):
                qScaledImage = q_image.scaledToWidth(qLabelSize.width())
            else:
                qScaledImage = q_image.scaledToHeight(qLabelSize.height())
            self.l5.setPixmap(qScaledImage)
            self.l5.show()
            # self.l5.setScaledContents(True)


    # define function: two images are same person
    # def keep_clicked(self):
    #     current_order = int(self.order.text())
    #     self.model_image.setItem(current_order-1, 1, QStandardItem(str("keep")))

    # define fuction: two images are different parson
    def remove_clicked(self):
        current_order = int(self.order.text())
        self.model_image.setItem(current_order - 1, 1, QStandardItem(str("remove")))


    # define function: next button is clicked
    def next_clicked(self):
        current_order = int(self.order.text())

        # load clean images list
        clean_images = []
        clean_id_path = self.folder_path.text() + "/" + self.subject_id.text()
        if (os.path.exists(clean_id_path)):
            clean_images = os.listdir(clean_id_path)

        length = len(clean_images)
        if current_order == length:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("This is already the last one")
            retval = msg.exec_()
        else:
            post_order = current_order + 1
            self.order.setText(str(post_order))
            self.tv_images.selectRow(post_order - 1)

            image = clean_id_path + "/" + clean_images[post_order-1]
            q_image = QPixmap(image)
            qImageSize = q_image.size()
            qLabelSize = self.l5.size()
            dWidthRatio = 1.0 * qImageSize.width() / qLabelSize.width()
            dHeightRatio = 1.0 * qImageSize.height() / qLabelSize.height()
            if (dWidthRatio > dHeightRatio):
                qScaledImage = q_image.scaledToWidth(qLabelSize.width())
            else:
                qScaledImage = q_image.scaledToHeight(qLabelSize.height())
            self.l5.setPixmap(qScaledImage)
            self.l5.show()
            # self.l5.setPixmap(QPixmap(image))
            # self.l5.setScaledContents(True)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
