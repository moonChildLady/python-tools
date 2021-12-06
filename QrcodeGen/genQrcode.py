import io
import sys
import qrcode
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QFileDialog, QDialog


'''Demo'''
class qrcodeGUI(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.setFixedSize(600, 400)
		self.setWindowTitle('QR Code Gen')
		self.grid = QGridLayout()
		# 	--Label
		self.content_label = QLabel('Content:')
		self.size_label = QLabel('Size:')
		self.version_label = QLabel('Version:')
		self.margin_label = QLabel('Margin:')
		self.rendering_label = QLabel('Render:')
		self.show_label = QLabel()
		#scable
		self.show_label.setScaledContents(True)
		#display size
		self.show_label.setMaximumSize(200, 200)
		# border
		self.content_edit = QLineEdit()
		self.content_edit.setText('QR Code')
		# button
		self.generate_button = QPushButton('Generate')
		self.save_button = QPushButton('Save')
		
		self.version_combobox = QComboBox()
		for i in range(1, 41):
			self.version_combobox.addItem('%s' % str(i))
		self.size_combobox = QComboBox()
		for i in range(8, 40, 2):
			self.size_combobox.addItem('%s * %s' % (str(i*29), str(i*29)))
		
		self.margin_spinbox = QSpinBox()

		self.grid.addWidget(self.rendering_label, 0, 0, 1, 1)
		self.grid.addWidget(self.show_label, 0, 0, 5, 5)
		self.grid.addWidget(self.content_label, 0, 5, 1, 1)
		self.grid.addWidget(self.content_edit, 0, 6, 1, 3)
		self.grid.addWidget(self.version_label, 1, 5, 1, 1)
		self.grid.addWidget(self.version_combobox, 1, 6, 1, 1)
		self.grid.addWidget(self.size_label, 2, 5, 1, 1)
		self.grid.addWidget(self.size_combobox, 2, 6, 1, 1)
		self.grid.addWidget(self.margin_label, 3, 5, 1, 1)
		self.grid.addWidget(self.margin_spinbox, 3, 6, 1, 1)
		self.grid.addWidget(self.generate_button, 4, 5, 1, 2)
		self.grid.addWidget(self.save_button, 5, 5, 1, 2)
		self.setLayout(self.grid)
		self.generate_button.clicked.connect(self.genQrcode)
		self.save_button.clicked.connect(self.saveQrcode)
		self.margin_spinbox.valueChanged.connect(self.genQrcode)
		self.genQrcode()
	#gen code
	def genQrcode(self):
		content = self.content_edit.text()
		try:
			margin = int(self.margin_spinbox.text())
		except:
			margin = 0
		size = int(self.size_combobox.currentText().split('*')[0])
		qr = qrcode.QRCode(version=1,
						   error_correction=qrcode.constants.ERROR_CORRECT_L,
						   box_size=size//29,
						   border=margin)
		qr.add_data(content)
		self.qr_img = qr.make_image()
		fp = io.BytesIO()
		self.qr_img.save(fp, 'BMP')
		qimg = QtGui.QImage()
		qimg.loadFromData(fp.getvalue(), 'BMP')
		qimg_pixmap = QtGui.QPixmap.fromImage(qimg)
		self.show_label.setPixmap(qimg_pixmap)
	# save
	def saveQrcode(self):
		filename = QFileDialog.getSaveFileName(self, 'Save', './qrcode.png', 'All(*)')
		if filename[0] != '':
			self.qr_img.save(filename[0])
			QDialog().show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = qrcodeGUI()
	gui.show()
	sys.exit(app.exec_())