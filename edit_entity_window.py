from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QCompleter, QStyledItemDelegate
from PySide6.QtGui import QFont, QPainter
from PySide6.QtCore import Qt, Signal

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.font = QFont("Helvetica", 16)

    def paint(self, painter, option, index):
        painter.save()
        painter.setFont(self.font)
        super().paint(painter, option, index)
        painter.restore()

class EditEntityWindow(QWidget):
    entity_edited = Signal(dict)

    def __init__(self, entity, all_entities):
        super().__init__()
        self.setWindowTitle("Editar Entidad")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: white;")

        self.entity = entity
        self.all_entities = all_entities

        layout = QVBoxLayout()

        self.fields = {}
        for key, value in entity.items():
            h_layout = QHBoxLayout()
            label = QLabel(key)
            label.setFont(QFont("Helvetica", 14))
            label.setStyleSheet("color: black;")
            label.setAlignment(Qt.AlignLeft)
            h_layout.addWidget(label)

            if key == "Empresa Asociada:":
                self.combo_empresa = QComboBox()
                self.combo_empresa.setFont(QFont("Helvetica", 14))
                self.combo_empresa.setStyleSheet("""
                    QComboBox {
                        font-size: 16px;
                        background-color: white;
                        color: black;
                    }
                """)
                self.combo_empresa.setEditable(True)
                self.combo_empresa.setFixedSize(400, 30)
                self.combo_empresa.addItems([e.get("Nombre:", "") for e in self.all_entities if e.get("Tipo de Empresa:") == "Empresa"])
                completer = QCompleter([e.get("Nombre:", "") for e in self.all_entities if e.get("Tipo de Empresa:") == "Empresa"])
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setFilterMode(Qt.MatchContains)
                
                # Configurar la fuente del completer
                completer.popup().setFont(QFont("Helvetica", 16))

                self.combo_empresa.setCompleter(completer)
                self.combo_empresa.setCurrentText(value)
                self.combo_empresa.setItemDelegate(ComboBoxDelegate(self.combo_empresa))
                
                # Configurar el QLineEdit interno
                line_edit = self.combo_empresa.lineEdit()
                if line_edit:
                    line_edit.setFont(QFont("Helvetica", 16))
                    line_edit.setStyleSheet("font-size: 16px;")
                    line_edit.setFixedHeight(40)
                    line_edit.setMinimumWidth(300)

                h_layout.addWidget(self.combo_empresa)
                self.fields[key] = self.combo_empresa
            else:
                line_edit = QLineEdit(value)
                line_edit.setFont(QFont("Helvetica", 16))
                line_edit.setStyleSheet("background-color: white; color: black;")
                h_layout.addWidget(line_edit)
                self.fields[key] = line_edit

            layout.addLayout(h_layout)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.setFont(QFont("Helvetica", 12))
        save_button.clicked.connect(self.save_entity)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setFont(QFont("Helvetica", 12))
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_entity(self):
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                self.entity[key] = widget.text()
            elif isinstance(widget, QComboBox):
                self.entity[key] = widget.currentText()

        self.entity_edited.emit(self.entity)
        self.close()