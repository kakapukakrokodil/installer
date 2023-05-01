import sys
import os
import threading
from distutils.dir_util import copy_tree

from PySide6.QtWidgets import QApplication,QMainWindow, QFileDialog
from PySide6.QtCore import QTimer, QSize, Slot, Signal, QThread, QRunnable, QObject

from build import Ui_MainWindow
        
class download_signal(QObject):
    
    finished = Signal()
    
class download_dependencies(QRunnable):
    def __init__(self, other_self):
        super(download_dependencies, self).__init__()
        self.other_self = other_self
        self.signals = download_signal()
        
    @Slot()
    def run(self):
        os.system("dependencies.bat")
        self.other_self.ui.progressBar.setValue(33)
        self.signals.finished.emit()
    
class Build(QRunnable):
    def __init__(self, other_self):
        super(Build, self).__init__()
        self.other_self = other_self
        self.signals = download_signal()
        
    @Slot()
    def run(self):
        copy_tree(os.getcwd() + "/ToBuild", self.other_self.choose_path)
        self.other_self.ui.progressBar.setValue(66)
        os.system("Build " + self.other_self.choose_path)
        self.other_self.ui.progressBar.setValue(100)
        self.signals.finished.emit()
        
class apps(QMainWindow):

    def __init__(self):
        super(apps, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.setValue(0)
        self.choose_path = ''
        
        self.thread1 = QThread()
        self.thread2 = QThread()
        
        self.download = download_dependencies(self)
        self.make = Build(self)
        
        self.thread1.started.connect(self.download.run)
        self.thread2.started.connect(self.make.run)
        
        self.download.signals.finished.connect(self.thread1.terminate)
        self.make.signals.finished.connect(self.thread2.terminate)
        
        self.thread1.finished.connect(self.run_thread2)
        
        self.ui.getdir_toolbutton.clicked.connect(self.getDirectory)
        self.ui.download_button.clicked.connect(self.run_thread1)
        
    def getDirectory(self):                                                     # <-----
       dirlist = QFileDialog.getExistingDirectory(self,"Выбрать папку",".")
       self.choose_path = dirlist
       self.ui.path_edit.setText(dirlist)
       self.ui.path_label.setText("Текущий путь:")
       
    def run_thread1(self):
        self.ui.download_button.setEnabled(False)
        self.ui.getdir_toolbutton.setEnabled(False)
        self.thread1.start()
        
    def run_thread2(self):
        self.thread2.start()
       
#точка входа в программу
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    window = apps()
    window.show()
    
    sys.exit(app.exec())
    