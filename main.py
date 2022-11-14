from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.uic       import *

from random import choice
from gtts import gTTS

import speech_recognition
import pygame
import sys, os

# ----------------------------------------------------------------------------------------

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		loadUi('MainWinForm.ui', self)

		pygame.mixer.init()
		self.mixer_volume = 0.5

		self.name_folder = 'folder with voice acting'
		self.name_audio = ''

		# Инициализировать распознаватель речи
		self.sr = speech_recognition.Recognizer()

		self.create_folder()
		self.group_tools()

	def create_folder(self):
		if not os.path.exists(self.name_folder):
			os.makedirs(self.name_folder)

	def group_tools(self):
		# Запись
		self.btn_record.clicked.connect(self.connect_record)
		self.action_record.triggered.connect(self.connect_record)

		# Озвучивать
		self.btn_vocalize.clicked.connect(self.connect_vocalize)
		self.action_vocalize.triggered.connect(self.connect_vocalize)

		# Играть
		self.btn_play.clicked.connect(self.connect_play)
		self.action_play.triggered.connect(self.connect_play)

		# Пауза
		self.btn_pause.clicked.connect(self.connect_pause)
		self.action_pause.triggered.connect(self.connect_pause)
#
#		# Копирование
#		self.btn_copy.clicked.connect()
#		self.action_copy.triggered.connect()
#
#		# Очистка
#		self.btn_clear.clicked.connect()
#		self.action_clear.triggered.connect()

	def setting_plain_text(self, info: str):
		self.plainTextEdit.setPlainText(str(info))

	def getter_plain_text(self) -> str:
		return self.plainTextEdit.toPlainText()

	def connect_record(self):
		query = self.func_wiretapping()
		self.setting_plain_text(query)

	def connect_vocalize(self):
		self.name_audio = self.create_name(8) + '.mp3'
		self.func_text_synthesis(self.name_audio)
		pygame.mixer.music.load(os.path.join(self.name_folder, self.name_audio))
		pygame.mixer.music.set_volume(self.mixer_volume)
		pygame.mixer.music.play()

	def connect_play(self):
		pygame.mixer.music.unpause()

	def connect_pause(self):
		pygame.mixer.music.pause()


	def func_wiretapping(self) -> str:
		try:
			try:
				with speech_recognition.Microphone() as mic:
					self.sr.adjust_for_ambient_noise(source=mic, duration=0.5)
					audio = self.sr.listen(source=mic)
					query = self.sr.recognize_google(audio_data=audio, language='ru-RU')
				return query
			except speech_recognition.UnknownValueError:
				return 'Мда... Я вас не понимаю! :|'
		except Exception as ex:
			self.message_window('Ошибка!', f'Что-то пошло не так: {ex}!')


	def func_text_synthesis(self, name: str):
		try:
			text = self.getter_plain_text()
			speech = gTTS(text=text, lang='ru', slow=False)
			speech.save(os.path.join(self.name_folder, name))
		except Exception as ex:
			self.message_window('Ошибка!', f'Что-то пошло не так: {ex}!')


	def create_name(self, size: int) -> str:
		symbols = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
		name = ''
		for i in range(size):
			name += choice(symbols)
		return name


	def message_window(self, caption, info):
		msg = QMessageBox()
		msg.setWindowTitle(str(caption))
		msg.setText(str(info))
		msg.setIcon(QMessageBox.Warning)

		msg.exec_()

# ----------------------------------------------------------------------------------------

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
