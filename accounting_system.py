import sys
import json
import os
import shutil
from datetime import datetime
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QApplication, QPushButton, QLineEdit, QDateEdit, QComboBox, QMessageBox, QFileDialog
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtCore import Qt, QDate
from save_user import SaveUserWindow
from client_list import ClientListWindow  # Importar la nueva ventana
from factura import FacturaWindow  # Importar la nueva ventana

class AddWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Añadir")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: white;")
        label = QLabel("Nueva GUI de Añadir")
        label.setFont(QFont("Helvetica", 15))
        label.setStyleSheet("color: black;")
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class AccountingSystemWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Contable")
        self.setFixedSize(800, 600)  # Ampliar la GUI
        self.setStyleSheet("background-color: white;")

        # Crear y colocar el nuevo botón "Añadir"
        button_add = QPushButton("Añadir")
        button_add.setFont(QFont("Helvetica", 12))
        button_add.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: blue;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #ddd);
            }
            QPushButton:hover {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #bbb);
            }
            QPushButton:pressed {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #ddd, stop: 1 #aaa);
            }
        """)
        button_add.clicked.connect(self.show_add_window)

        # Crear y colocar el nuevo botón "Buscar"
        button_search = QPushButton("Buscar")
        button_search.setFont(QFont("Helvetica", 12))
        button_search.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: green;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #ddd);
            }
            QPushButton:hover {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #bbb);
            }
            QPushButton:pressed {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #ddd, stop: 1 #aaa);
            }
        """)
        button_search.clicked.connect(self.show_client_list)

        # Crear y colocar el nuevo botón "Ver Factura"
        button_view_invoice = QPushButton("Ver Factura")
        button_view_invoice.setFont(QFont("Helvetica", 12))
        button_view_invoice.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: orange;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #ddd);
            }
            QPushButton:hover {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #bbb);
            }
            QPushButton:pressed {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #ddd, stop: 1 #aaa);
            }
        """)
        button_view_invoice.clicked.connect(self.show_invoice_window)

        # Crear y colocar el nuevo botón "Guardar"
        button_save = QPushButton("Guardar")
        button_save.setFont(QFont("Helvetica", 12))
        button_save.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: red;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #ddd);
            }
            QPushButton:hover {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #bbb);
            }
            QPushButton:pressed {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #ddd, stop: 1 #aaa);
            }
        """)
        button_save.clicked.connect(self.save_data)

        # Crear y colocar el nuevo botón "Subir Archivo"
        self.button_upload = QPushButton("Subir Archivo")
        self.button_upload.setFont(QFont("Helvetica", 12))
        self.button_upload.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: purple;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #ddd);
            }
            QPushButton:hover {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #fff, stop: 1 #bbb);
            }
            QPushButton:pressed {
                background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5,
                                            fx: 0.5, fy: 0.5,
                                            stop: 0 #ddd, stop: 1 #aaa);
            }
        """)
        self.button_upload.clicked.connect(self.upload_file)
        self.uploaded_file_path = ""

        # Crear el layout horizontal para los botones en la parte superior
        button_layout = QHBoxLayout()
        button_layout.addWidget(button_add)
        button_layout.addWidget(button_search)
        button_layout.addWidget(button_view_invoice)
        button_layout.addWidget(button_save)
        button_layout.addWidget(self.button_upload)

        # Crear y colocar el nuevo label "Fecha" y el selector de fecha
        label_date = QLabel("Fecha")
        font = QFont("Helvetica", 12)
        font.setBold(True)
        label_date.setFont(font)
        label_date.setStyleSheet("color: black;")
        label_date.setAlignment(Qt.AlignLeft)

        self.date_edit = QDateEdit()
        self.date_edit.setFont(QFont("Helvetica", 12))
        self.date_edit.setStyleSheet("background-color: white; color: black;")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        date_layout = QHBoxLayout()
        date_layout.addWidget(label_date)
        date_layout.addWidget(self.date_edit)
        date_layout.setContentsMargins(0, 0, 0, 0)  # Ajustar los márgenes para reducir la distancia

        # Crear y colocar el nuevo label "Empresa" y el combo box
        label_empresa = QLabel("Empresa")
        label_empresa.setFont(font)
        label_empresa.setStyleSheet("color: black;")
        label_empresa.setAlignment(Qt.AlignLeft)

        self.combo_empresa = QComboBox()
        self.combo_empresa.setFont(QFont("Helvetica", 12))
        self.combo_empresa.setStyleSheet("background-color: white; color: black;")
        self.combo_empresa.currentIndexChanged.connect(self.update_clients)

        empresa_layout = QHBoxLayout()
        empresa_layout.addWidget(label_empresa)
        empresa_layout.addWidget(self.combo_empresa)

        # Crear y colocar el nuevo label "Tipo de Transacción" y el combo box
        label_transaction_type = QLabel("Tipo de Transacción")
        label_transaction_type.setFont(font)
        label_transaction_type.setStyleSheet("color: black;")
        label_transaction_type.setAlignment(Qt.AlignLeft)

        self.combo_transaction_type = QComboBox()
        self.combo_transaction_type.setFont(QFont("Helvetica", 12))
        self.combo_transaction_type.setStyleSheet("background-color: white; color: black;")
        self.combo_transaction_type.addItems(["Compras", "Ventas"])
        self.combo_transaction_type.currentIndexChanged.connect(self.update_transaction_type)

        transaction_type_layout = QHBoxLayout()
        transaction_type_layout.addWidget(label_transaction_type)
        transaction_type_layout.addWidget(self.combo_transaction_type)

        # Crear y colocar el nuevo label "Cliente" y el combo box
        self.label_client = QLabel("Cliente")
        self.label_client.setFont(font)
        self.label_client.setStyleSheet("color: black;")
        self.label_client.setAlignment(Qt.AlignLeft)

        self.combo_client = QComboBox()
        self.combo_client.setFont(QFont("Helvetica", 12))
        self.combo_client.setStyleSheet("background-color: white; color: black;")
        self.combo_client.currentIndexChanged.connect(self.update_client_info)

        client_layout = QHBoxLayout()
        client_layout.addWidget(self.label_client)
        client_layout.addWidget(self.combo_client)

        # Crear y colocar el nuevo label "Nombre del Cliente" y el cuadro de texto
        self.label_client_name = QLabel("Nombre del Cliente:")
        self.label_client_name.setFont(font)
        self.label_client_name.setStyleSheet("color: black;")
        self.label_client_name.setAlignment(Qt.AlignLeft)

        self.entry_client_name = QLineEdit()
        self.entry_client_name.setFont(QFont("Helvetica", 12))
        self.entry_client_name.setStyleSheet("background-color: white; color: black;")

        client_name_layout = QHBoxLayout()
        client_name_layout.addWidget(self.label_client_name)
        client_name_layout.addWidget(self.entry_client_name)

        # Crear y colocar el nuevo label "RIF" y el cuadro de texto
        self.label_rif = QLabel("RIF:")
        self.label_rif.setFont(font)
        self.label_rif.setStyleSheet("color: black;")
        self.label_rif.setAlignment(Qt.AlignLeft)

        self.entry_rif = QLineEdit()
        self.entry_rif.setFont(QFont("Helvetica", 12))
        self.entry_rif.setStyleSheet("background-color: white; color: black;")

        rif_layout = QHBoxLayout()
        rif_layout.addWidget(self.label_rif)
        rif_layout.addWidget(self.entry_rif)

        # Crear y colocar el nuevo label "Número de Documento" y el cuadro de texto
        label_doc_num = QLabel("Número de Documento")
        label_doc_num.setFont(font)
        label_doc_num.setStyleSheet("color: black;")
        label_doc_num.setAlignment(Qt.AlignLeft)

        self.entry_doc_num = QLineEdit()
        self.entry_doc_num.setFont(QFont("Helvetica", 12))
        self.entry_doc_num.setStyleSheet("background-color: white; color: black;")

        doc_num_layout = QHBoxLayout()
        doc_num_layout.addWidget(label_doc_num)
        doc_num_layout.addWidget(self.entry_doc_num)

        # Crear y colocar el nuevo label "Número de Control" y el cuadro de texto
        label_control_num = QLabel("Número de Control")
        label_control_num.setFont(font)
        label_control_num.setStyleSheet("color: black;")
        label_control_num.setAlignment(Qt.AlignLeft)

        self.entry_control_num = QLineEdit()
        self.entry_control_num.setFont(QFont("Helvetica", 12))
        self.entry_control_num.setStyleSheet("background-color: white; color: black;")
        self.entry_control_num.setCursorPosition(3)  # Colocar el cursor después de "00-"

        control_num_layout = QHBoxLayout()
        control_num_layout.addWidget(label_control_num)
        control_num_layout.addWidget(self.entry_control_num)

        # Crear y colocar el nuevo label "Base imponible 16%" y el cuadro de texto
        label_base_16 = QLabel("Base imponible 16%")
        label_base_16.setFont(font)
        label_base_16.setStyleSheet("color: black;")
        label_base_16.setAlignment(Qt.AlignLeft)

        self.entry_base_16 = QLineEdit()
        self.entry_base_16.setObjectName("entry_base_16")  # Asignar nombre al QLineEdit
        self.entry_base_16.setFont(QFont("Helvetica", 12))
        self.entry_base_16.setStyleSheet("background-color: white; color: black;")
        self.entry_base_16.setValidator(QDoubleValidator(0, 1000000, 2))  # Aceptar solo números decimales
        self.entry_base_16.textChanged.connect(self.update_totals)

        base_16_layout = QHBoxLayout()
        base_16_layout.addWidget(label_base_16)
        base_16_layout.addWidget(self.entry_base_16)

        # Crear y colocar el nuevo label "IVA 16%" y el cuadro de texto
        label_iva_16 = QLabel("IVA 16%")
        label_iva_16.setFont(font)
        label_iva_16.setStyleSheet("color: black;")
        label_iva_16.setAlignment(Qt.AlignLeft)

        self.entry_iva_16 = QLineEdit()
        self.entry_iva_16.setObjectName("entry_iva_16")  # Asignar nombre al QLineEdit
        self.entry_iva_16.setFont(QFont("Helvetica", 12))
        self.entry_iva_16.setStyleSheet("background-color: white; color: black;")
        self.entry_iva_16.setReadOnly(True)  # Campo de solo lectura

        iva_16_layout = QHBoxLayout()
        iva_16_layout.addWidget(label_iva_16)
        iva_16_layout.addWidget(self.entry_iva_16)

        # Crear y colocar el nuevo label "Base imponible 8%" y el cuadro de texto
        label_base_8 = QLabel("Base imponible 8%")
        label_base_8.setFont(font)
        label_base_8.setStyleSheet("color: black;")
        label_base_8.setAlignment(Qt.AlignLeft)

        self.entry_base_8 = QLineEdit()
        self.entry_base_8.setObjectName("entry_base_8")  # Asignar nombre al QLineEdit
        self.entry_base_8.setFont(QFont("Helvetica", 12))
        self.entry_base_8.setStyleSheet("background-color: white; color: black;")
        self.entry_base_8.setValidator(QDoubleValidator(0, 1000000, 2))  # Aceptar solo números decimales
        self.entry_base_8.textChanged.connect(self.update_totals)

        base_8_layout = QHBoxLayout()
        base_8_layout.addWidget(label_base_8)
        base_8_layout.addWidget(self.entry_base_8)

        # Crear y colocar el nuevo label "IVA 8%" y el cuadro de texto
        label_iva_8 = QLabel("IVA 8%")
        label_iva_8.setFont(font)
        label_iva_8.setStyleSheet("color: black;")
        label_iva_8.setAlignment(Qt.AlignLeft)

        self.entry_iva_8 = QLineEdit()
        self.entry_iva_8.setObjectName("entry_iva_8")  # Asignar nombre al QLineEdit
        self.entry_iva_8.setFont(QFont("Helvetica", 12))
        self.entry_iva_8.setStyleSheet("background-color: white; color: black;")
        self.entry_iva_8.setReadOnly(True)  # Campo de solo lectura

        iva_8_layout = QHBoxLayout()
        iva_8_layout.addWidget(label_iva_8)
        iva_8_layout.addWidget(self.entry_iva_8)

        # Crear y colocar el nuevo label "Total" y el cuadro de texto
        label_total = QLabel("Total")
        label_total.setFont(font)
        label_total.setStyleSheet("color: black;")
        label_total.setAlignment(Qt.AlignLeft)

        self.entry_total = QLineEdit()
        self.entry_total.setObjectName("entry_total")  # Asignar nombre al QLineEdit
        self.entry_total.setFont(QFont("Helvetica", 12))
        self.entry_total.setStyleSheet("background-color: white; color: black;")
        self.entry_total.setReadOnly(True)  # Campo de solo lectura

        total_layout = QHBoxLayout()
        total_layout.addWidget(label_total)
        total_layout.addWidget(self.entry_total)

        self.layout = QVBoxLayout()
        self.layout.addLayout(button_layout)
        self.layout.addLayout(date_layout)
        self.layout.addLayout(empresa_layout)
        self.layout.addLayout(transaction_type_layout)
        self.layout.addLayout(client_layout)
        self.layout.addLayout(client_name_layout)
        self.layout.addLayout(rif_layout)
        self.layout.addLayout(doc_num_layout)
        self.layout.addLayout(control_num_layout)
        self.layout.addLayout(base_16_layout)
        self.layout.addLayout(iva_16_layout)
        self.layout.addLayout(base_8_layout)
        self.layout.addLayout(iva_8_layout)
        self.layout.addLayout(total_layout)
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.layout)
        self.load_users()

    def load_users(self):
        try:
            with open("contribuyentes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.users = [client for client in data if client.get("Tipo de Empresa:") == "Empresa"]
                self.combo_empresa.clear()
                self.combo_empresa.addItems([user.get("Nombre:", "").upper() for user in self.users])
        except (FileNotFoundError, json.JSONDecodeError):
            self.combo_empresa.clear()

    def update_clients(self):
        selected_user = self.combo_empresa.currentText()
        try:
            with open("contribuyentes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                clients = [client for client in data if client.get("Empresa Asociada:") == selected_user]
                self.combo_client.clear()
                self.combo_client.addItems([client.get("Nombre:", "").upper() for client in clients])
        except (FileNotFoundError, json.JSONDecodeError):
            self.combo_client.clear()

    def update_client_info(self):
        selected_client = self.combo_client.currentText()
        try:
            with open("contribuyentes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                for client in data:
                    if client.get("Nombre:").upper() == selected_client:
                        self.entry_client_name.setText(client.get("Nombre:", "").upper())
                        self.entry_rif.setText(client.get("Número R.I.F.:", ""))
                        break
        except (FileNotFoundError, json.JSONDecodeError):
            self.entry_client_name.clear()
            self.entry_rif.clear()

    def update_transaction_type(self):
        transaction_type = self.combo_transaction_type.currentText()
        if transaction_type == "Compras":
            self.label_client.setText("Proveedor")
            self.label_client.show()
            self.combo_client.show()
            self.update_clients()  # Actualizar la lista de clientes/proveedores
        else:
            self.label_client.hide()
            self.combo_client.hide()
            self.entry_client_name.clear()
            self.entry_rif.clear()
            self.combo_client.clear()  # Limpiar la lista de clientes

    def update_totals(self):
        try:
            base_16 = float(self.entry_base_16.text()) if self.entry_base_16.text() else 0
            base_8 = float(self.entry_base_8.text()) if self.entry_base_8.text() else 0
            iva_16 = base_16 * 0.16
            iva_8 = base_8 * 0.08
            total = base_16 + iva_16 + base_8 + iva_8

            self.entry_iva_16.setText(f"{iva_16:.2f}")
            self.entry_iva_8.setText(f"{iva_8:.2f}")
            self.entry_total.setText(f"{total:.2f}")
        except ValueError:
            self.entry_iva_16.clear()
            self.entry_iva_8.clear()
            self.entry_total.clear()

    def show_add_window(self):
        self.add_window = SaveUserWindow()
        self.add_window.closed.connect(self.load_users)  # Recargar usuarios cuando se cierre la ventana
        self.add_window.show()

    def show_client_list(self):
        self.client_list_window = ClientListWindow()
        self.client_list_window.window_closed.connect(self.load_users)  # Recargar usuarios cuando se cierre la ventana de lista de clientes
        self.client_list_window.show()

    def show_invoice_window(self):
        self.invoice_window = FacturaWindow()
        self.invoice_window.window_closed.connect(self.load_users)  # Recargar usuarios cuando se cierre la ventana de facturas
        self.invoice_window.show()

    def save_data(self):
        data = {
            "Fecha": self.date_edit.date().toString(Qt.ISODate),
            "Empresa": self.combo_empresa.currentText(),
            "Tipo de Transacción": self.combo_transaction_type.currentText(),
            "Cliente": self.combo_client.currentText(),
            "Nombre del Cliente": self.entry_client_name.text(),
            "RIF": self.entry_rif.text(),
            "Número de Documento": self.entry_doc_num.text(),
            "Número de Control": self.entry_control_num.text(),
            "Base imponible 16%": self.entry_base_16.text(),
            "IVA 16%": self.entry_iva_16.text(),
            "Base imponible 8%": self.entry_base_8.text(),
            "IVA 8%": self.entry_iva_8.text(),
            "Total": self.entry_total.text(),
            "Archivo": self.uploaded_file_path
        }

        try:
            # Crear la ruta de destino para el archivo
            if self.uploaded_file_path:
                fecha = self.date_edit.date().toString("yyyy-MM-dd")
                year, month, _ = fecha.split('-')
                tipo_transaccion = self.combo_transaction_type.currentText()
                dest_dir = f'C:/Users/Dell/Desktop/System Contable/INFORMES CONTADORES/EMPRESAS/{data["Empresa"]}/FACTURAS/{tipo_transaccion}/{year}/{month}'
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, os.path.basename(self.uploaded_file_path))
                shutil.copy(self.uploaded_file_path, dest_path)
                data["Archivo"] = dest_path

            with open("datos_guardados.json", "r+", encoding="utf-8") as file:
                file_data = json.load(file)
                file_data.append(data)
                file.seek(0)
                json.dump(file_data, file, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")
        except (FileNotFoundError, json.JSONDecodeError):
            with open("datos_guardados.json", "w", encoding="utf-8") as file:
                json.dump([data], file, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron guardar los datos: {e}")

        # Limpiar todos los campos excepto Nombre del Cliente y RIF después de guardar
        self.entry_doc_num.clear()
        self.entry_control_num.clear()
        self.entry_base_16.clear()
        self.entry_iva_16.clear()
        self.entry_base_8.clear()
        self.entry_iva_8.clear()
        self.entry_total.clear()
        self.uploaded_file_path = ""
        self.button_upload.setText("Subir Archivo")
        self.button_upload.clicked.disconnect()
        self.button_upload.clicked.connect(self.upload_file)

    def delete_user(self, user_name):
        try:
            with open("contribuyentes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            data = [user for user in data if user.get("Nombre:", "").upper() != user_name.upper()]
            with open("contribuyentes.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.load_users()  # Actualizar la lista de usuarios después de eliminar uno
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Seleccionar archivo", "", "Images (*.png *.xpm *.jpg *.jpeg);;PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.uploaded_file_path = file_path
            self.button_upload.setText(os.path.basename(file_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccountingSystemWindow()
    window.show()
    sys.exit(app.exec())
