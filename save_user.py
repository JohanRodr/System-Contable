from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QApplication, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
import sys
import json
import os

class SaveUserWindow(QWidget):
    closed = Signal()

    def __init__(self, client_data=None, save_callback=None, row=None):
        super().__init__()
        self.setWindowTitle("Contribuyente - Insertar")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: white;")
        self.client_data = client_data
        self.save_callback = save_callback
        self.row = row

        layout = QVBoxLayout()

        labels = [
            "Tipo de Empresa:", "Código:", "Nombre:", "Nombre Corto:", "Número R.I.F.:",
            "Número N.I.T:", "Tipo de Contribuyente:", "Dirección:",
            "Ciudad:", "Municipio:", "Estado:", "Zona Postal:",
            "Teléfonos:", "Número de FAX:", "Código Contribuyente:"
        ]

        self.entries = {}
        for label_text in labels:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            font = QFont("Helvetica", 12)
            font.setBold(True)
            label.setFont(font)
            label.setStyleSheet("color: black;")
            h_layout.addWidget(label)

            if label_text == "Tipo de Contribuyente:":
                combo_box = QComboBox()
                combo_box.addItems(["Formal", "Ordinarios", "Especial", "Entes Públicos"])
                combo_box.setFont(QFont("Helvetica", 12))
                h_layout.addWidget(combo_box)
                self.entries[label_text] = combo_box
            elif label_text == "Tipo de Empresa:":
                self.combo_tipo_empresa = QComboBox()
                self.combo_tipo_empresa.addItems(["Empresa", "Cliente"])
                self.combo_tipo_empresa.setFont(QFont("Helvetica", 12))
                self.combo_tipo_empresa.currentIndexChanged.connect(self.on_tipo_empresa_changed)
                h_layout.addWidget(self.combo_tipo_empresa)
                self.entries[label_text] = self.combo_tipo_empresa
            else:
                entry = QLineEdit()
                entry.setFont(QFont("Helvetica", 12))
                entry.setStyleSheet("background-color: white; color: black;")
                h_layout.addWidget(entry)
                self.entries[label_text] = entry

            layout.addLayout(h_layout)

            if label_text == "Tipo de Empresa:":
                empresa_layout = QHBoxLayout()
                self.label_empresa = QLabel("Seleccionar Empresa:")
                self.label_empresa.setFont(QFont("Helvetica", 12))
                self.label_empresa.setStyleSheet("color: black;")
                self.label_empresa.hide()

                self.combo_empresa = QComboBox()
                self.combo_empresa.setFont(QFont("Helvetica", 12))
                self.combo_empresa.hide()

                empresa_layout.addWidget(self.label_empresa)
                empresa_layout.addWidget(self.combo_empresa)
                layout.addLayout(empresa_layout)

        button_grabar = QPushButton("Grabar")
        font = QFont("Helvetica", 15)
        font.setBold(True)
        button_grabar.setFont(font)
        button_grabar.setFixedWidth(200)
        button_grabar.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
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
        button_grabar.clicked.connect(self.grabar)
        layout.addWidget(button_grabar, alignment=Qt.AlignCenter)

        button_salir = QPushButton("Salir")
        button_salir.setFont(font)
        button_salir.setFixedWidth(200)
        button_salir.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
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
        button_salir.clicked.connect(self.close)
        layout.addWidget(button_salir, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        if self.client_data:
            self.load_client_data()

    def on_tipo_empresa_changed(self):
        if self.combo_tipo_empresa.currentText() == "Cliente":
            self.label_empresa.show()
            self.combo_empresa.show()
            self.load_empresas()
        else:
            self.label_empresa.hide()
            self.combo_empresa.hide()

    def load_empresas(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            contribuyentes_path = os.path.join(script_dir, "contribuyentes.json")
            with open(contribuyentes_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                empresas = [client["Nombre:"] for client in data if client.get("Tipo de Empresa:") == "Empresa"]
                self.combo_empresa.clear()
                self.combo_empresa.addItems(empresas)
        except (FileNotFoundError, json.JSONDecodeError):
            self.combo_empresa.clear()

    def load_client_data(self):
        for label, widget in self.entries.items():
            if isinstance(widget, QLineEdit):
                widget.setText(self.client_data.get(label, ""))
            elif isinstance(widget, QComboBox):
                index = widget.findText(self.client_data.get(label, ""), Qt.MatchFixedString)
                if index >= 0:
                    widget.setCurrentIndex(index)

    def grabar(self):
        data = {}
        for label, widget in self.entries.items():
            if isinstance(widget, QLineEdit):
                data[label] = widget.text()
            elif isinstance(widget, QComboBox):
                data[label] = widget.currentText()

        if self.combo_tipo_empresa.currentText() == "Cliente":
            if not self.combo_empresa.currentText():
                QMessageBox.warning(self, "Error", "Debe seleccionar una empresa asociada para el cliente.")
                return
            data["Empresa Asociada:"] = self.combo_empresa.currentText()

        if self.save_callback and self.row is not None:
            self.save_callback(data, self.row)
        else:
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                contribuyentes_path = os.path.join(script_dir, "contribuyentes.json")
                with open(contribuyentes_path, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list):
                        existing_data = []
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = []

            existing_data.append(data)

            with open(contribuyentes_path, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4)

            if data["Tipo de Empresa:"] == "Empresa":
                self.create_empresa_folders(data["Nombre:"])

        print("Datos grabados")
        self.clear_fields()
        self.client_data = None
        self.row = None

    def create_empresa_folders(self, empresa_name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, 'INFORMES CONTADORES/EMPRESAS', empresa_name.upper())
        os.makedirs(base_path, exist_ok=True)

    def clear_fields(self):
        for widget in self.entries.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SaveUserWindow()
    window.show()
    sys.exit(app.exec())
