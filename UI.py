from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton, QMessageBox, QTextEdit, QLineEdit, QPlainTextEdit
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtCore import QTimer, QCoreApplication

from AX1 import Arm
import Algorithms
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import serial
from serial import Serial


class ManualControl(QWidget):
    def __init__(self, ser):
        super().__init__()
        self.setWindowTitle("Manual AX-1 Control")
        self.setStyleSheet("background-color: black;")

        # Setting up the serial connection
        self.ser = ser

        # Creating the main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Creating the sliders
        self.sliders = []
        self.slider_values = []
        slider_labels = ["Rotation", "Mid Section", "Base", "Gripper"]
        for label_text in slider_labels:
            slider_layout = QHBoxLayout()
            main_layout.addLayout(slider_layout)

            # Creating the label
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            slider_layout.addWidget(label)

            # Creating the slider
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 180)
            slider.setValue(90)
            slider.setFixedWidth(200)  # Set a fixed width for all sliders
            slider.valueChanged.connect(self.serial_send)
            slider_layout.addWidget(slider)

            # Creating the text box
            text_box = QLineEdit()
            text_box.setStyleSheet("color: white;")
            text_box.setFixedWidth(50)  # Set a fixed width for all text boxes
            text_box.setReadOnly(True)
            slider_layout.addWidget(text_box)

            self.sliders.append(slider)
            self.slider_values.append(text_box)

    def serial_send(self, value):
        positions = [180 - slider.value() for slider in self.sliders]
        pos_string = ','.join(str(pos) for pos in positions) + '\n'
        self.ser.write(pos_string.encode())
        print(pos_string)

        for slider, value in zip(self.sliders, self.slider_values):
            value.setText(str(slider.value()))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.arm = None
        self.moves = ""

        self.setWindowTitle("AX-1 Pegs Game Control")
        self.setGeometry(100, 100, 400, 450)

        self.label_com = QLabel("COM Port:", self)
        self.label_com.setGeometry(20, 20, 80, 30)
        self.edit_com = QLineEdit(self)
        self.edit_com.setGeometry(110, 20, 100, 30)
        self.edit_com.setText("COM5")  # Set default text to "COM5"

        self.button_connect = QPushButton("Connect", self)
        self.button_connect.setGeometry(220, 20, 80, 30)
        self.button_connect.clicked.connect(self.connect_to_arm)


        self.button_com_ports = QPushButton("?", self)
        self.button_com_ports.setGeometry(310, 20, 30, 30)
        self.button_com_ports.clicked.connect(self.show_com_ports)


        self.label_status = QLabel("Status: Disconnected", self)
        self.label_status.setGeometry(20, 70, 150, 30)
        self.label_status.setStyleSheet("color: red")  # Set text color to red initially


        self.check_boxes = []
        self.moves_label = QLabel("Game Board:", self)
        self.moves_label.setGeometry(20, 120, 100, 30)

        x = 120
        for i in range(7):
            check_box = QCheckBox(self)
            check_box.setGeometry(x, 120, 30, 30)
            check_box.stateChanged.connect(self.update_moves)
            self.check_boxes.append(check_box)
            x += 40

        self.button_show_moves = QPushButton("Show Moves", self)
        self.button_show_moves.setGeometry(20, 180, 120, 30)
        self.button_show_moves.clicked.connect(self.show_moves)

        self.button_send = QPushButton("Send to Arm", self)
        self.button_send.setGeometry(160, 180, 120, 30)
        self.button_send.clicked.connect(self.send_moves)
        self.button_send.setEnabled(False)

        self.text_output = QTextEdit(self)
        self.text_output.setGeometry(20, 230, 360, 150)

        self.button_manual_control = QPushButton("Manual Control", self)
        self.button_manual_control.setGeometry(20, 400, 360, 30)

        self.button_manual_control.clicked.connect(self.open_manual_control)

    def show_com_ports(self):
        com_ports = QSerialPortInfo.availablePorts()
        com_port_names = [port.portName() for port in com_ports]
        com_port_text = "\n".join(com_port_names)

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Available COM Ports")

        text_label = QLabel("Available Ports:", msg_box)
        text_label.setStyleSheet("font-weight: bold;")
        

        plain_text_edit = QPlainTextEdit(msg_box)
        plain_text_edit.setPlainText(com_port_text)
        plain_text_edit.setReadOnly(True)
        plain_text_edit.setMinimumWidth(300)
        plain_text_edit.setMinimumHeight(200)
        plain_text_edit.setStyleSheet(
            "background-color: #f0f0f0; color: #333333; font-family: Arial; font-size: 12px; padding: 5px;"
        )

        button_box = msg_box.addButton(QMessageBox.Ok)
        button_box.setStyleSheet("width: 100px;")

        layout = msg_box.layout()
        layout.addWidget(text_label, 0, 0, 1, layout.columnCount())
        layout.addWidget(plain_text_edit, 1, 0, 1, layout.columnCount())
        layout.addWidget(button_box, 2, 0, 1, layout.columnCount())

        msg_box.exec()










    def connect_to_arm(self):
        com_port = self.edit_com.text()
        if not com_port:
            QMessageBox.warning(self, "Error", "Please select COM port")
            return

        try:
            self.arm = Arm(com_port)
            print("Connected to Arm")

            self.button_connect.setEnabled(False)
            self.label_status.setText("Status: Connected")
            self.label_status.setStyleSheet("color: green")  # Set text color to green
            self.button_send.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_moves(self, state):
        self.moves = ""
        for check_box in self.check_boxes:
            if check_box.isChecked():
                self.moves += "X"
            else:
                self.moves += "o"

    def show_moves(self):
        if not self.moves:
            QMessageBox.warning(self, "Error", "Please check the boxes relating to the game board")
            return

        try:
            solution = Algorithms.pegsSolution(self.moves)
            moves_text = "\n".join(str(move) for move in solution)
            self.text_output.clear()
            self.text_output.append(moves_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def send_moves(self):
        if not self.arm:
            QMessageBox.warning(self, "Error", "AX-1 is not connected - Select COM port and connect")
            return

        if not self.moves:
            QMessageBox.warning(self, "Error", "Please select moves")
            return

        try:
            solution = Algorithms.pegsSolution(self.moves)

            for move in solution:
                self.arm.robot_make_move(move)
                QCoreApplication.processEvents()
                QTimer.singleShot(500, QCoreApplication.processEvents)  # Delay to allow GUI update

            self.arm.end()
            print("Moves executed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_manual_control(self):
        if not self.arm:
            QMessageBox.warning(self, "Error", "AX-1 is not connected - Select COM port and connect")
            return

        self.manual_control_window = ManualControl(self.arm.ser)  # Pass the serial connection
        self.manual_control_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
