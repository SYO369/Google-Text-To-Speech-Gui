from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import window as ui
import text_to_speech as tos

class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
         super().__init__()
         self.setupUi(self)
         self.getLanguageList()
         self.getVoiceList()
         self.qButton_Speak.setShortcut("Ctrl+Return")
         self.qButton_Speak.clicked.connect(self.speak)
         self.qComboBox_Language.currentTextChanged.connect(self.getVoiceList)
         self.qSlider_SpeedValue.valueChanged.connect(self.updateSpeedRate)
         self.qSlider_Pitch.valueChanged.connect(self.updatePitch)

    def getLanguageList(self):
        self.qComboBox_Language.addItems(tos.LOCALE_LIST.keys())

    def getVoiceList(self):
        self.qComboBox_Voice.clear()
        self.qComboBox_Voice.addItems(tos.get_voice_list(tos.LOCALE_LIST.get(self.qComboBox_Language.currentText())))

    def updatePitch(self):
        self.qLabel_PitchValue.setText(str(self.qSlider_Pitch.value()/10))

    def updateSpeedRate(self):
        self.qLabel_SpeedValue.setText(str(self.qSlider_SpeedValue.value()/100))
    
    def speak(self):
        voice_param = tos.voice_param()
        voice_param.text = self.qTextEdit_Content.toPlainText()
        voice_param.language_code = tos.LOCALE_LIST.get(self.qComboBox_Language.currentText())
        voice_param.name = self.qComboBox_Voice.currentText()
        voice_param.pitch = self.qSlider_Pitch.value() / 10
        voice_param.speakingRate = self.qSlider_SpeedValue.value() /100
        tos.playAudio(voice_param)
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())