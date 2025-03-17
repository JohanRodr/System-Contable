from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QApplication, QLineEdit, QHBoxLayout, QLabel, QPushButton, QAbstractItemView, QScrollArea, QAbstractScrollArea
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
import json
import sys
import os
import shutil
from save_user import SaveUserWindow

class ClientListWindow(QWidget):
    window_closed = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Contribuyentes")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        search_label.setFont(QFont("Helvetica", 14))
        self.search_bar = QLineEdit()
        self.search_bar.setFont(QFont("Helvetica", 14))
        self.search_bar.textChanged.connect(self.filter_clients)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_bar)
        layout.addLayout(search_layout)

        button_layout = QHBoxLayout()

        delete_button = QPushButton("Eliminar")
        delete_button.setFont(QFont("Helvetica", 14))
        delete_button.clicked.connect(self.delete_client)
        button_layout.addWidget(delete_button)

        edit_button = QPushButton("Ver/Editar")
        edit_button.setFont(QFont("Helvetica", 14))
        edit_button.clicked.connect(self.edit_client)
        button_layout.addWidget(edit_button)

        view_clients_button = QPushButton("Ver Clientes")
        view_clients_button.setFont(QFont("Helvetica", 14))
        view_clients_button.clicked.connect(self.view_clients)
        button_layout.addWidget(view_clients_button)

        exit_button = QPushButton("Salir")
        exit_button.setFont(QFont("Helvetica", 14))
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.selected_empresa = None
        self.previous_view = None
        self.load_clients()

    def load_clients(self):
        try:
            with open("contribuyentes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []

                self.all_clients = data
                self.filtered_clients = [client for client in data if client.get("Tipo de Empresa:") == "Empresa"]

                headers = ["Nombre:", "Número R.I.F.:"]
                self.table_widget.setColumnCount(len(headers))
                self.table_widget.setHorizontalHeaderLabels(headers)
                self.table_widget.setRowCount(len(self.filtered_clients))

                header_font = QFont("Helvetica", 16)
                self.table_widget.horizontalHeader().setFont(header_font)
                self.table_widget.horizontalHeader().setStretchLastSection(True)
                self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                cell_font = QFont("Helvetica", 16)
                for row, client in enumerate(self.filtered_clients):
                    if isinstance(client, dict):
                        item_nombre = QTableWidgetItem(client.get("Nombre:", ""))
                        item_nombre.setFont(cell_font)
                        item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable)
                        self.table_widget.setItem(row, 0, item_nombre)

                        item_rif = QTableWidgetItem(client.get("Número R.I.F.:", ""))
                        item_rif.setFont(cell_font)
                        item_rif.setFlags(item_rif.flags() & ~Qt.ItemIsEditable)
                        self.table_widget.setItem(row, 1, item_rif)
                    else:
                        self.table_widget.setItem(row, 0, QTableWidgetItem("Datos de cliente inválidos."))
        except (FileNotFoundError, json.JSONDecodeError):
            self.table_widget.setRowCount(1)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No se encontraron datos de contribuyentes."))

    def filter_clients(self):
        search_text = self.search_bar.text().lower()
        filtered_clients = [client for client in self.filtered_clients if any(search_text in str(value).lower() for value in client.values())]

        self.table_widget.setRowCount(len(filtered_clients))
        cell_font = QFont("Helvetica", 18)
        for row, client in enumerate(filtered_clients):
            if isinstance(client, dict):
                item_nombre = QTableWidgetItem(client.get("Nombre:", ""))
                item_nombre.setFont(cell_font)
                item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row, 0, item_nombre)

                item_rif = QTableWidgetItem(client.get("Número R.I.F.:", ""))
                item_rif.setFont(cell_font)
                item_rif.setFlags(item_rif.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row, 1, item_rif)
            else:
                self.table_widget.setItem(row, 0, QTableWidgetItem("Datos de cliente inválidos."))

    def delete_client(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if selected_rows:
            for index in sorted(selected_rows, reverse=True):
                selected_empresa = self.filtered_clients[index.row()].get("Nombre:", "")
                self.all_clients = [client for client in self.all_clients if client.get("Nombre:") != selected_empresa]
                self.all_clients = [client for client in self.all_clients if client.get("Empresa Asociada:") != selected_empresa]
                self.table_widget.removeRow(index.row())
                self.delete_empresa_folder(selected_empresa)
                self.delete_empresa_invoices(selected_empresa)
            self.save_clients()
            self.load_clients()

    def delete_empresa_folder(self, empresa_name):
        base_path = f'INFORMES CONTADORES/EMPRESAS/{empresa_name.upper()}'
        if os.path.exists(base_path):
            shutil.rmtree(base_path)

    def delete_empresa_invoices(self, empresa_name):
        try:
            with open("facturas.json", "r", encoding="utf-8") as file:
                invoices = json.load(file)
                invoices = [invoice for invoice in invoices if invoice.get("Empresa") != empresa_name]
            with open("facturas.json", "w", encoding="utf-8") as file:
                json.dump(invoices, file, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_clients(self):
        try:
            with open("contribuyentes.json", "w", encoding="utf-8") as file:
                json.dump(self.all_clients, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    def edit_client(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            if self.selected_empresa:
                clients = [client for client in self.all_clients if client.get("Empresa Asociada:") == self.selected_empresa]
                client_data = clients[selected_row]
            else:
                client_data = self.filtered_clients[selected_row]
            self.edit_window = SaveUserWindow(client_data, self.save_edited_client, selected_row)
            self.edit_window.show()
            self.edit_window.closed.connect(self.load_clients)

    def save_edited_client(self, client_data, row):
        if self.selected_empresa:
            clients = [client for client in self.all_clients if client.get("Empresa Asociada:") == self.selected_empresa]
            client_index = self.all_clients.index(clients[row])
            self.all_clients[client_index] = client_data
        else:
            user_index = self.filtered_clients.index(self.filtered_clients[row])
            self.all_clients[user_index] = client_data
        self.save_clients()
        self.load_clients()

    def view_clients(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            self.selected_empresa = self.filtered_clients[selected_row].get("Nombre:", "")
            clients = [client for client in self.all_clients if client.get("Empresa Asociada:") == self.selected_empresa]

            self.previous_view = self.table_widget.rowCount(), [self.table_widget.item(row, 0).text() for row in range(self.table_widget.rowCount())]

            headers = ["Nombre:", "Número R.I.F.:"]
            self.table_widget.setColumnCount(len(headers))
            self.table_widget.setHorizontalHeaderLabels(headers)
            self.table_widget.setRowCount(len(clients))

            cell_font = QFont("Helvetica", 16)
            for row, client in enumerate(clients):
                if isinstance(client, dict):
                    item_nombre = QTableWidgetItem(client.get("Nombre:", ""))
                    item_nombre.setFont(cell_font)
                    item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable)
                    self.table_widget.setItem(row, 0, item_nombre)

                    item_rif = QTableWidgetItem(client.get("Número R.I.F.:", ""))
                    item_rif.setFont(cell_font)
                    item_rif.setFlags(item_rif.flags() & ~Qt.ItemIsEditable)
                    self.table_widget.setItem(row, 1, item_rif)
                else:
                    self.table_widget.setItem(row, 0, QTableWidgetItem("Datos de cliente inválidos."))

    def closeEvent(self, event):
        if self.previous_view:
            row_count, items = self.previous_view
            self.table_widget.setRowCount(row_count)
            for row, item in enumerate(items):
                item_nombre = QTableWidgetItem(item)
                item_nombre.setFont(QFont("Helvetica", 16))
                item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row, 0, item_nombre)
            self.previous_view = None
            self.selected_empresa = None
            event.ignore()
        else:
            self.window_closed.emit()
            super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientListWindow()
    window.show()
    sys.exit(app.exec())
