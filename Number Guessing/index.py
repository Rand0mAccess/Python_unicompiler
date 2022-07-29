from PyQt5.QtWidgets import *
from PyQt5 import uic
from os import path
import sys, random
import win32com.client as wincl

speak = wincl.Dispatch("SAPI.SpVoice")
ui,_ = uic.loadUiType("main.ui")

class MainApp(QMainWindow, ui):
  def __init__(self,parent=None):
    super(MainApp,self).__init__(parent)
    QMainWindow.__init__(self)
    self.setupUi(self)
    self.Action_Button()
    self.UI()
    self.Answer = 0
    self.count = 0

  def UI(self):
    style = open("stylesheet.css","r")
    style = style.read()
    self.setStyleSheet(style)

  def Action_Button(self):
    self.pushButton.clicked.connect(self.start_game)
    self.pushButton_2.clicked.connect(self.check_answer)
    self.pushButton_3.clicked.connect(self.reset_game)
    self.pushButton_4.clicked.connect(self.quit_game)

  def start_game(self):
    low_range = self.lineEdit.text()
    high_range = self.lineEdit_2.text()
    if low_range=="" or high_range=="":
      speak.Speak("Data Error, Enter Low and High Number")
      QMessageBox.warning(self,"Data Error","Please Fill the low and High Value")
    else:
      speak.Speak("Game Started, Guess the Number Between "+str(low_range)+" and "+str(high_range))
      self.Answer = random.randint(int(low_range),int(high_range))

  def check_answer(self):
    guess_number = self.lineEdit_3.text()
    low_range = self.lineEdit.text()
    high_range = self.lineEdit_2.text()
    if guess_number == "":
      speak.Speak("Data Error, Enter the Number")
      QMessageBox.warning(self, "Data Error", "Please Enter the Number")
    else:
      if int(guess_number)>self.Answer:
        self.count += 1
        speak.Speak("Wrong number! Guess Less than this")
        self.label_4.setText("Guess Less than this")
        self.lineEdit_3.setText("")
        if int(guess_number)>self.Answer and self.Answer%2==0:
          speak.Speak("Hint: Number is Even")
          self.label_4.setText("Wrong number! Hint: Number is Even")
        elif int(guess_number)>self.Answer and self.Answer%2!=0:
          speak.Speak("Hint: Number is Odd")
          self.label_4.setText("Wrong number! Hint: Number is Odd")

      elif int(guess_number)<self.Answer:
        self.count += 1
        speak.Speak("Wrong number! Guess Higher than this")
        self.label_4.setText("Guess Higher than this")
        self.lineEdit_3.setText("")


      elif int(guess_number) == self.Answer:
        speak.Speak("Yeah!, You Guessed the Number")
        self.label_4.setText("Congratulations! You Guessed the Number")

      else:
        speak.Speak("Error, Number is not between "+str(low_range)+" and "+str(high_range))
        self.lineEdit_3.setText("")

    self.label_5.setText("You Tried : "+str(self.count)+" Times")


  def reset_game(self):
    self.lineEdit.setText("")
    self.lineEdit_2.setText("")
    self.lineEdit_3.setText("")
    self.label_4.setText("")
    self.label_5.setText("")
    self.Answer = 0
    self.count = 0

  def quit_game(self):
    speak.Speak("Quitting Game.....")
    exit()


def main():
  app = QApplication(sys.argv)
  window = MainApp()
  window.show()
  app.exec_()

if __name__ == "__main__":
  main()