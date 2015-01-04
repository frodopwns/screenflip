from PyQt4.QtCore import *
from PyQt4.QtGui import *
import win32gui
import win32ui
import win32con
import sys, time

w = 346
h = 179
from_top = 905
from_left = 1572

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.setWindowTitle('Just a dialog')
        self.lineedit = QLineEdit("Write something and press Enter")
        self.lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.connect(self.lineedit, SIGNAL("returnPressed()"),
                     self.update_ui)

    def update_ui(self):
        self.browser.append(self.lineedit.text())

def capture_screen():
    hwnd = win32gui.FindWindow(None, "Chrome")
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (from_left,from_top), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, "testing0.bmp")
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    count = 0
    while count < 10:
        capture_screen()
        # Create and display the splash screen
        splash_pix = QPixmap('testing0.bmp')
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        #splash.setMask(splash_pix.mask())
        splash.move(300, from_top)
        splash.show()
        app.processEvents()

        time.sleep(2)
        count+=1

    splash.finish()
    app.exec_()