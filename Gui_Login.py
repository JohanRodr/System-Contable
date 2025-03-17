import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Agregar la ruta de la carpeta Src al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Src')))
from db_connector import DatabaseConnector
from accounting_system import AccountingSystemWindow

# Inicializar la base de datos y agregar usuarios
def initialize_db():
    db = DatabaseConnector()
    db.add_user("Doriannis", "Budokai2025")
    db.add_user("user1", "password1")
    db.add_user("1", "1")
    db.close()
    print("Base de datos inicializada y usuarios añadidos.")

# Llamar a la función para inicializar la base de datos
initialize_db()

# Crear una nueva instancia de DatabaseConnector para la aplicación
db = DatabaseConnector()

def login():
    username = entry_username.text()
    password = entry_password.text()
    user = db.verify_user(username, password)
    if user:
        global accounting_window
        accounting_window = AccountingSystemWindow()
        accounting_window.show()
        window.close()
    else:
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Login Info")
        msg_box.setText("Usuario o clave incorrectos")
        msg_box.setStyleSheet("QLabel{color: black; font-size: 16px;} QPushButton{color: black; background-color: white;}")
        msg_box.exec()

# Crear la aplicación principal
app = QApplication(sys.argv)

# Crear la ventana principal
window = QWidget()
window.setWindowTitle("Login")
window.setFixedSize(380, 250)  # Establecer tamaño de la ventana
window.setStyleSheet("background-color: black;")

# Crear y colocar el título
label_title = QLabel("Sistema Contable")
label_title.setFont(QFont("Helvetica", 16))
label_title.setStyleSheet("color: white;")
label_title.setAlignment(Qt.AlignCenter)

# Crear y colocar las etiquetas y campos de entrada
label_username = QLabel("Usuario:")
label_username.setFont(QFont("Helvetica", 14))
label_username.setStyleSheet("color: white;")

entry_username = QLineEdit()
entry_username.setFont(QFont("Helvetica", 14))
entry_username.setFixedWidth(200)
entry_username.setStyleSheet("background-color: white; color: black;")

label_password = QLabel("Clave:")
label_password.setFont(QFont("Helvetica", 14))
label_password.setStyleSheet("color: white;")

entry_password = QLineEdit()
entry_password.setFont(QFont("Helvetica", 14))
entry_password.setEchoMode(QLineEdit.Password)
entry_password.setFixedWidth(200)
entry_password.setStyleSheet("background-color: white; color: black;")

# Crear y colocar el botón de login
button_login = QPushButton("Login")
button_login.setFont(QFont("Helvetica", 14))
button_login.setStyleSheet("background-color: white; color: black;")
button_login.setFixedWidth(100)
button_login.clicked.connect(login)

# Crear el layout
layout = QVBoxLayout()
layout.addWidget(label_title)

form_layout_username = QHBoxLayout()
form_layout_username.addWidget(label_username)
form_layout_username.addWidget(entry_username)
# Reducir el espaciado entre la etiqueta y el campo de entrada
form_layout_username.setContentsMargins(20, 0, 0, 0)  # Ajustar los márgenes para alinear más hacia la izquierda
layout.addLayout(form_layout_username)

form_layout_password = QHBoxLayout()
form_layout_password.addWidget(label_password)
form_layout_password.addWidget(entry_password)
form_layout_password.setContentsMargins(20, 0, 0, 0)  # Ajustar los márgenes para alinear más hacia la izquierda
layout.addLayout(form_layout_password)

layout.addWidget(button_login, alignment=Qt.AlignCenter)

window.setLayout(layout)

# Mostrar la ventana principal
window.show()

# Iniciar el bucle principal de la aplicación
sys.exit(app.exec())
