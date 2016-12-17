# -*- coding:utf-8 -*-
'''
Created on  
2016年12月8日   上午1:49:07
@author: yzw
'''
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cv2
import cv2.cv as cv
import configparser as parser
import shutil
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
CONFIG_FILE_PATH = "Crop.ini"  
fileTypes = ['*.jpg', '*.png', '*.bmp', '*.gif', '*.jpeg', '*.ico', '*.ppm', '*.tiff']
filenameTypes =['.jpg', '.png','.PNG', '.BMP','.bmp', '.gif', '.jpeg', '.ico', '.ppm', '.tiff']

class MainCrop(QMainWindow):
    def __init__(self,parent =None):
        QMainWindow.__init__(self,parent)
        self.setWindowTitle(u'欢迎使用智能剪切板')
        self.resize(580,388)
        self.lowther =float(10)
        self.highther =float(240)
        self.config = parser.ConfigParser()
        with open(CONFIG_FILE_PATH, 'w') as fw:
            self.config.add_section('Display')
            self.config.write(fw)
        self.config.read(CONFIG_FILE_PATH) 
        #view Picture
        self.image = QImage()
        self.picture =QLabel()
        self.setAcceptDrops(True)
        #right
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setMouseTracking(False)
        self.scrollAreaWidgetContents.setFocusPolicy(Qt.NoFocus)
        self.scrollAreaWidgetContents.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.picture.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)  
        self.setCentralWidget(self.picture) 
        #==============
        self.ModifyPanel = ModifyPanel()
        #QAction
        self.OpenAction = QAction(QIcon('images/open.png'), u"&打开...",
                                          self, shortcut=QKeySequence.Open,
                                            statusTip=u"打开文件",triggered=self.openFileEvent)
        self.CropAction =  QAction(QIcon('images/cut.png'), u"&剪切...",
                                          self, shortcut=QKeySequence.Cut,
                                            statusTip=u"智能剪切",triggered=self.intCrop)
        self.TwoAction = QAction(QIcon('images/two.png'), u"&边缘检测...",
                                          self,shortcut ='ctrl+Y',
                                            statusTip=u"边缘检测",triggered=self.twovalue)
        self.SaveAction = QAction(QIcon('images/save.png'), u"&保存...",
                                          self, shortcut=QKeySequence.Save,
                                            statusTip=u"保存修改",triggered=self.SavePic)
        self.SaveAsAction = QAction(QIcon('images/saveas1.png'), u"&另存为...",
                                          self, shortcut="Ctrl+W",
                                            statusTip=u"另存为修改",triggered=self.SaveAsPic)
        self.exitAction =QAction(QIcon('images/exit.png'), u"&退出...",
                                          self, shortcut="Ctrl+Q",
                                            statusTip=u"退出",triggered=self.close)
        self.toolBarAction = QAction(QIcon('images/check.png'), u"&工具栏...",
                                          self, shortcut="Ctrl+A",
                                            statusTip=u"显示工具栏",triggered=self.toggleToolBar)
        self.aboutAction = QAction(QIcon('images/about.png'), u"&关于...",
                                          self,statusTip=u"关于此软件",triggered=self.about)
        self.helpAction = QAction(QIcon('images/help.png'), u"&帮助...",
                                          self,statusTip=u"如何使用",triggered=self.help)
        
        self.ThresAction =QAction(QIcon('images/modify.png'), u"&阈值...",
                                          self,statusTip=u"修改阈值",triggered=self.ModifyPanel.show)
        self.cxconfigAction = QAction(QIcon('images/clear.png'), u"&重配...",
                                          self,statusTip=u"重新配置",triggered=self.cxconfig)
        self.CropAction.setEnabled(False)
        self.SaveAction.setEnabled(False)
        self.SaveAsAction.setEnabled(False)
        self.TwoAction.setEnabled(False)
        self.ThresAction.setEnabled(False)
        self.statusBar()
        self.initUi()
    def initUi(self):
        self.setWindowIcon(QIcon('images/crop.png'))
        #右键菜单
        self.contextMenu = QMenu(self)
        self.contextMenu.addAction(self.OpenAction)
        self.contextMenu.addAction(self.CropAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.TwoAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.ThresAction)
        self.contextMenu.addAction(self.cxconfigAction)
        #===============菜单，工具栏
        self.createMenuBars()
        self.createToolBars()
    def cxconfig(self):
        with open(CONFIG_FILE_PATH, 'w') as fw:
            self.config.read(CONFIG_FILE_PATH)
            self.config.remove_section('Display')
            self.config.add_section('Display')
            self.config.write(fw)
        self.picture.clear()
        self.CropAction.setEnabled(False)
        self.TwoAction.setEnabled(False)
        for filename in os.listdir(os.getcwd()):
            if os.path.splitext(filename)[1] in filenameTypes:
               os.remove(filename)
        #self.science =QGraphicsScene(self)
    def contextMenuEvent(self, event):
        self.contextMenu.exec_(event.globalPos())
    def WriteCon(self,strcon):
        self.config.set('Display', 'picname', strcon)
        self.config.write(open(CONFIG_FILE_PATH, "r+")) 
    def Qpixview(self,imagesource):
        self.image.load(imagesource)
        if self.image.width()>self.picture.width() or self.image.height()>self.picture.height():
           self.image =self.image.scaled(self.picture.size(),Qt.KeepAspectRatio, Qt.SmoothTransformation)
           self.picture.setPixmap(QPixmap(self.image))
           self.picture.setAlignment(Qt.AlignCenter)
        else:
            self.image.load(imagesource)
            self.picture.setPixmap(QPixmap(self.image))
            self.picture.setAlignment(Qt.AlignCenter)
         
    def createMenuBars(self):
    
        file =self.menuBar().addMenu(u'文件')
        file.addAction(self.OpenAction)
        file.addSeparator()
        file.addAction(self.SaveAction)
        file.addAction(self.SaveAsAction)
        file.addSeparator()
        file.addAction(self.exitAction)
        edit =self.menuBar().addMenu(u'编辑')
        edit.addAction(self.CropAction)
        edit.addAction(self.TwoAction)
        edit.addAction(self.ThresAction)
        edit.addAction(self.cxconfigAction)
        view =self.menuBar().addMenu(u'查看')
        view.addAction(self.toolBarAction)
        help =self.menuBar().addMenu(u'帮助')
        help.addAction(self.aboutAction)
        help.addAction(self.helpAction)
    def createToolBars(self):
        self.toolBar = self.addToolBar("")
        self.toolBar.addAction(self.OpenAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.CropAction)
        self.toolBar.addAction(self.TwoAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.SaveAction)
        self.toolBar.addAction(self.SaveAsAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.exitAction)  
    def openFileEvent(self):        
        picturename =QFileDialog.getOpenFileName()
        if picturename !='':
            self.WriteCon(picturename)
            self.Qpixview(picturename)
            self.CropAction.setEnabled(True)
            self.TwoAction.setEnabled(True)
            self.ThresAction.setEnabled(True)
            self.setWindowTitle(picturename)
            self.statusBar().showMessage('%s'%picturename)  
    def twovalue(self):
        if  'picname' in self.config.options('Display'): 
        #if  self.config.options('Display') == ['picname'] :
            self.config.read(CONFIG_FILE_PATH)
            if 'lowther' in self.config.options('Display'): 
                lowvalue =self.config.get('Display', 'lowther')
                highvalue =self.config.get('Display','highther')
            else :
                lowvalue =self.lowther
                highvalue =self.highther 
            self.picname =unicode(str(self.config.get('Display', 'picname')))
            self.imname_ext =str('./tem_two%s' %os.path.splitext(self.picname)[1])
            self.imname = str('./tem%s' %os.path.splitext(self.picname)[1])
            self.loadname = os.path.basename(self.picname)
            img = cv2.imread(str(self.picname).encode('gbk'))  
            img = cv2.GaussianBlur(img,(3,3),0)
            canny =cv2.Canny(img,float(lowvalue),float(highvalue))
            cv2.imwrite(self.imname_ext,canny) 
            self.Qpixview(self.imname_ext)
            if os.path.exists(self.loadname) and os.path.exists(self.imname):
                os.remove(self.loadname)
                os.remove(self.imname)
            self.SaveAction.setEnabled(False)
            self.SaveAsAction.setEnabled(True)              
    def intCrop(self):
        if  'picname' in self.config.options('Display'):
        #if  self.config.options('Display') == ['picname'] : 
            self.config.read(CONFIG_FILE_PATH)
            if 'lowther' in self.config.options('Display'): 
                lowvalue =self.config.get('Display', 'lowther')
                highvalue =self.config.get('Display','highther') 
            else:
                lowvalue =self.lowther
                highvalue =self.highther
            self.picname =str(self.config.get('Display', 'picname'))
            self.imname_ext =str('./tem%s' %os.path.splitext(self.picname)[1].encode('gbk'))
            self.imname_two =str('./tem_two%s' %os.path.splitext(self.picname)[1])
            self.loadname = str(os.path.basename(self.picname)).encode('gbk')
            img = cv2.imread(str(self.picname).encode('gbk')) 
            img_l=cv.LoadImage(str(self.picname).encode('gbk')) 
            img = cv2.GaussianBlur(img,(3,3),0)  
            canny1 = cv2.Canny(img,float(lowvalue),float(highvalue))
            img_width =img.shape[1]
            img_heigh =img.shape[0]
            white =list()
            for i in range(img_heigh):
                if 255 in canny1[i]:
                   white.append(i)
            up_pixel =white[0]
            low_pixel =white[-1]
            canny1T =canny1.T
            whiteT =list()
            for i in range(img_width):
                if 255 in canny1T[i]:
                   whiteT.append(i)
            left_pixel =whiteT[0]
            right_pixel =whiteT[-1]
            cv2.rectangle(img,(left_pixel,up_pixel),(right_pixel,low_pixel),(0,255,0),1)
            cv2.imwrite(self.imname_ext,img)
            self.Qpixview(self.imname_ext)
            cv.SetImageROI(img_l,(left_pixel,up_pixel,right_pixel-left_pixel,low_pixel-up_pixel))
            cv.SaveImage(self.loadname,img_l)
            self.SaveAction.setEnabled(True)
            self.SaveAsAction.setEnabled(True)
            if os.path.exists(self.imname_two):
                os.remove(self.imname_two)
        else:
            self.loadname =''
            self.imname_ext ='' 
    def SavePic(self):
        SavePicapp =self.intCrop()
        if os.path.exists(self.loadname):
            shutil.copy(self.loadname, self.picname)
        os.remove(self.loadname)
        os.remove(self.imname_ext)
    def SaveAsPic(self): 
        if  'picname' in self.config.options('Display'): 
        #if  self.config.options('Display') == ['picname'] :  
            self.picname =str(self.config.get('Display', 'picname')).encode('gbk')
            self.imname_two =str('./tem_two%s' %os.path.splitext(self.picname)[1])
            self.imname_ext =str('./tem%s' %os.path.splitext(self.picname)[1])
            self.loadname = os.path.basename(self.picname) 
        imgFormat = 'PNG File (*.png);;BMP File (*.bmp);;JPG File (*.jpg);;JPEG File (*.jpeg);;PPM File (*.ppm);;TIFF File(*.tiff)'            
        imgFile = QFileDialog.getSaveFileName(self, 'Save Picture',self.picname, imgFormat)
        if os.path.exists(self.imname_two):
           shutil.copy(self.imname_two,imgFile)
           os.remove(self.imname_two)
        else:
           shutil.copy(self.loadname,imgFile)
        if os.path.exists(self.loadname) and os.path.exists(self.imname_ext):
            os.remove(self.loadname)
            os.remove(self.imname_ext)
    def mouseDoubleClickEvent(self,e):  
        self.openFileEvent()
    def toggleToolBar(self):
        if self.toolBar.isHidden():
            self.toolBar.show()
            self.toolBarAction.setIcon(QIcon("images/check.png"))
        else:
            self.toolBar.hide()
            self.toolBarAction.setIcon(QIcon("images/check_no.png"))
    def dragEnterEvent(self, event):
        global fileType
        if len(event.mimeData().urls()):
            self.fileName = event.mimeData().urls()[0].toLocalFile()
            ext = QFileInfo(self.fileName).suffix()
            if "*." + ext.toUtf8().data().lower() in fileTypes:
                event.accept()
        
    def dropEvent(self, event):
        if self.fileName !='':
            self.WriteCon(self.fileName)
            self.Qpixview(self.fileName)
            self.CropAction.setEnabled(True)
            self.TwoAction.setEnabled(True)
            self.ThresAction.setEnabled(True)
            self.setWindowTitle(self.fileName)
    def about(self):
        QMessageBox.about(self, u"智能剪切板",
                                u"这是参考别人实例写的一个基于Python_2.7 + PyQt4的智能剪切板\r\n"
                                u'目前支持智能裁剪，边缘检测功能\r\n'
                                u"作者：余忠伟\r\n"
                                u"时间：2016-12")
    def help(self):
        QMessageBox.about(self, u"智能剪切板使用方法",
                                u"1,打开图片(可以从菜单栏，工具栏打开\r\n"
                                u'   以及双击，拖入等打开方式).\r\n'
                                u"2,支持大部分图片格式，gif及透明的png除外.\r\n"
                                u'3,选择智能裁剪或边缘检测功能.\r\n'
                                u"4,进行保存或另存为，保存修改的图片.\r\n"
                                u"5,如有异常，请检查配置文件里面的内容\r\n"
                                u'   是否有乱码，并修改正确.')
    def resizeEvent(self, event):
        if  'picname' in self.config.options('Display'):
        #if  self.config.options('Display') == ['picname'] :  
            self.picname =str(self.config.get('Display', 'picname'))
            self.imname_ext =str('./tem%s' %os.path.splitext(self.picname)[1])
            self.Qpixview(self.imname_ext)
    def closeEvent(self, e):
        for filename in os.listdir(os.getcwd()):
            if os.path.splitext(filename)[1] in filenameTypes:
               os.remove(filename)   
               
               
class ModifyPanel(QDialog):
    def __init__(self,parent=None):
        super(ModifyPanel, self).__init__(parent)
        lowLabel = QLabel(u"低阈值:")
        self.lowSpinBox = QSpinBox()
        lowLabel.setBuddy(self.lowSpinBox)
        self.lowSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.lowSpinBox.setRange(1,255)
        self.lowSpinBox.setValue(10)
        highLabel = QLabel(u"高阈值:")
        self.highSpinBox = QSpinBox()
        highLabel.setBuddy(self.highSpinBox)
        self.highSpinBox.setAlignment(Qt.AlignRight|
                                        Qt.AlignVCenter)
        self.highSpinBox.setRange(1,255)
        self.highSpinBox.setValue(240)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                     QDialogButtonBox.Cancel)
        layout = QGridLayout()
        layout.addWidget(lowLabel, 0, 0)
        layout.addWidget(self.lowSpinBox, 0, 1)
        layout.addWidget(highLabel, 1, 0)
        layout.addWidget(self.highSpinBox, 1, 1)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(layout)
        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)
        self.setWindowTitle(u"修改阈值")
        self.setWindowIcon(QIcon('images/modify.png'))
    def therTip(self):
       reply = QMessageBox.information(self,                         #使用infomation信息框  
                                    u"阈值",  
                                    u"阈值不合理，请重新设置",  
                                   QMessageBox.Ok )
    
    def Writether(self):
        config = parser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        config.set('Display', 'lowther',self.lowSpinBox.value())
        config.set('Display','highther',self.highSpinBox.value())
        config.write(open(CONFIG_FILE_PATH,'w'))     
    def accept(self):       
        self.Writether()
        self.close()
app =QApplication(sys.argv)
ui = MainCrop()
ui.show()
app.exec_()