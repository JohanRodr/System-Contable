from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QApplication, QLineEdit, QHBoxLayout, QLabel, QPushButton, QAbstractItemView, QScrollArea, QAbstractScrollArea, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
import json
import sys
import os
import shutil
from edit_entity_window import EditEntityWindow

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

        self.delete_button = QPushButton("Eliminar Empresa")
        self.delete_button.setFont(QFont("Helvetica", 14))
        self.delete_button.clicked.connect(self.delete_entity)
        button_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton("Editar Empresa")
        self.edit_button.setFont(QFont("Helvetica", 14))
        self.edit_button.clicked.connect(self.edit_entity)
        button_layout.addWidget(self.edit_button)

        self.view_clients_button = QPushButton("Ver Clientes")
        self.view_clients_button.setFont(QFont("Helvetica", 14))
        self.view_clients_button.clicked.connect(self.view_clients)
        button_layout.addWidget(self.view_clients_button)

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

        self.all_clients = []
        self.filtered_clients = []
        self.selected_empresa = None
        self.previous_view = None
        self.load_clients()

    def load_clients(self):
        try:
            with open("contribuyentes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        self.all_clients = data
        self.filtered_clients = [client for client in data if client.get("Tipo de Empresa:") == "Empresa"]
        self.update_table(self.filtered_clients)

    def filter_clients(self):
        search_text = self.search_bar.text().lower()
        self.filtered_clients = [client for client in self.all_clients if any(search_text in str(value).lower() for value in client.values()) and client.get("Tipo de Empresa:") == "Empresa"]
        self.update_table(self.filtered_clients)

    def update_table(self, clients):
        headers = ["Nombre:", "Número R.I.F.:"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setRowCount(len(clients))

        header_font = QFont("Helvetica", 16)
        self.table_widget.horizontalHeader().setFont(header_font)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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

    def delete_entity(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if selected_rows:
            for index in sorted(selected_rows, reverse=True):
                if index.row() < len(self.filtered_clients):
                    selected_entity = self.filtered_clients[index.row()]
                    selected_entity_name = selected_entity.get("Nombre:", "")
                    selected_entity_rif = selected_entity.get("Número R.I.F.:", "")
                    entity_type = selected_entity.get("Tipo de Empresa:", "")

                    if self.delete_button.text() == "Eliminar Empresa":
                        print(f"Intentando eliminar empresa: {selected_entity_name} con RIF {selected_entity_rif}")

                        if entity_type == "Empresa":
                            reply = QMessageBox.question(
                                self,
                                'Eliminar Empresa',
                                f'¿Estás seguro de que deseas eliminar la empresa "{selected_entity_name}" con RIF {selected_entity_rif}? Esto también eliminará todos los clientes asociados y la carpeta de la empresa.',
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No
                            )
                            if reply == QMessageBox.Yes:
                                # Eliminar la empresa seleccionada y sus clientes asociados
                                self.all_clients = [
                                    client for client in self.all_clients
                                    if not (client.get("Nombre:") == selected_entity_name and
                                            client.get("Número R.I.F.:") == selected_entity_rif and
                                            client.get("Tipo de Empresa:") == "Empresa") and
                                    client.get("Empresa Asociada:") != selected_entity_name
                                ]
                                print(f"Empresa {selected_entity_name} y sus clientes asociados eliminados de la lista all_clients.")
                                # Eliminar la empresa de la lista filtered_clients
                                self.filtered_clients.pop(index.row())
                                print(f"Empresa {selected_entity_name} eliminada de la lista filtered_clients.")
                                # Eliminar la carpeta de la empresa
                                empresa_folder = os.path.join("C:\\Users\\Dell\\Desktop\\System Contable\\INFORMES CONTADORES\\EMPRESAS", selected_entity_name)
                                if os.path.exists(empresa_folder):
                                    shutil.rmtree(empresa_folder)
                                    print(f"Carpeta de la empresa {selected_entity_name} eliminada.")
                                # Guardar los cambios en el archivo JSON
                                self.save_clients()
                                # Actualizar la tabla
                                self.update_table(self.filtered_clients)
                        else:
                            QMessageBox.warning(self, "Eliminar", "Solo se pueden eliminar empresas desde la vista principal.")
                    elif self.delete_button.text() == "Eliminar Cliente":
                        print(f"Intentando eliminar cliente: {selected_entity_name} con RIF {selected_entity_rif}")

                        if entity_type == "Cliente" and self.selected_empresa:
                            reply = QMessageBox.question(
                                self,
                                'Eliminar Cliente',
                                f'¿Estás seguro de que deseas eliminar el cliente "{selected_entity_name}" con RIF {selected_entity_rif}?',
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No
                            )
                            if reply == QMessageBox.Yes:
                                # Eliminar solo el cliente seleccionado
                                self.all_clients = [
                                    client for client in self.all_clients
                                    if not (client.get("Nombre:") == selected_entity_name and
                                            client.get("Número R.I.F.:") == selected_entity_rif and
                                            client.get("Tipo de Empresa:") == "Cliente" and
                                            client.get("Empresa Asociada:") == self.selected_empresa)
                                ]
                                print(f"Cliente {selected_entity_name} eliminado de la lista all_clients.")
                                # Eliminar el cliente de la lista filtered_clients
                                self.filtered_clients.pop(index.row())
                                print(f"Cliente {selected_entity_name} eliminado de la lista filtered_clients.")
                                # Guardar los cambios en el archivo JSON
                                self.save_clients()
                                # Actualizar la tabla
                                self.update_table(self.filtered_clients)
                        else:
                            QMessageBox.warning(self, "Eliminar", "Solo se pueden eliminar clientes desde la vista de clientes asociados a una empresa.")
        else:
            QMessageBox.warning(self, "Eliminar", "No se seleccionaron filas para eliminar.")

    def edit_entity(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if selected_rows:
            for index in selected_rows:
                if index.row() < len(self.filtered_clients):
                    selected_entity = self.filtered_clients[index.row()]
                    selected_entity_name = selected_entity.get("Nombre:", "")
                    selected_entity_rif = selected_entity.get("Número R.I.F.:", "")
                    entity_type = selected_entity.get("Tipo de Empresa:", "")

                    if self.edit_button.text() == "Editar Empresa":
                        print(f"Intentando editar empresa: {selected_entity_name} con RIF {selected_entity_rif}")
                        self.edit_window = EditEntityWindow(selected_entity, self.all_clients)
                        self.edit_window.entity_edited.connect(self.update_entity)
                        self.edit_window.show()
                    elif self.edit_button.text() == "Editar Cliente":
                        print(f"Intentando editar cliente: {selected_entity_name} con RIF {selected_entity_rif}")
                        self.edit_window = EditEntityWindow(selected_entity, self.all_clients)
                        self.edit_window.entity_edited.connect(self.update_entity)
                        self.edit_window.show()
        else:
            QMessageBox.warning(self, "Editar", "No se seleccionaron filas para editar.")

    def update_entity(self, updated_entity):
        for i, client in enumerate(self.all_clients):
            if client.get("Nombre:") == updated_entity.get("Nombre:") and client.get("Número R.I.F.:") == updated_entity.get("Número R.I.F.:"):
                self.all_clients[i] = updated_entity
                break

        self.save_clients()
        self.load_clients()

    def save_clients(self):
        try:
            with open("contribuyentes.json", "w", encoding="utf-8") as file:
                json.dump(self.all_clients, file, ensure_ascii=False, indent=4)
            print("Datos guardados en contribuyentes.json.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar los datos: {e}")
            print(f"Error al guardar los datos: {e}")

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

            self.filtered_clients = clients  # Actualizar la lista de clientes filtrados con los clientes asociados a la empresa seleccionada

            self.delete_button.setText("Eliminar Cliente")
            self.delete_button.clicked.disconnect()
            self.delete_button.clicked.connect(self.delete_entity)

            self.edit_button.setText("Editar Cliente")
            self.edit_button.clicked.disconnect()
            self.edit_button.clicked.connect(self.edit_entity)

            self.view_clients_button.hide()  # Ocultar el botón "Ver Clientes"

    def closeEvent(self, event):
        if hasattr(self, 'previous_view') and self.previous_view:
            row_count, items = self.previous_view
            self.table_widget.setRowCount(row_count)
            for row, item in enumerate(items):
                item_nombre = QTableWidgetItem(item)
                item_nombre.setFont(QFont("Helvetica", 16))
                item_nombre.setFlags(item_nombre.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row, 0, item_nombre)
            self.previous_view = None
            self.selected_empresa = None
            self.filtered_clients = [client for client in self.all_clients if client.get("Tipo de Empresa:") == "Empresa"]  # Restaurar la lista de empresas
            self.update_table(self.filtered_clients)
            self.delete_button.setText("Eliminar Empresa")
            self.delete_button.clicked.disconnect()
            self.delete_button.clicked.connect(self.delete_entity)

            self.edit_button.setText("Editar Empresa")
            self.edit_button.clicked.disconnect()
            self.edit_button.clicked.connect(self.edit_entity)

            self.view_clients_button.show()  # Mostrar el botón "Ver Clientes"
            event.ignore()
        else:
            self.window_closed.emit()
            super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientListWindow()
    window.show()
    sys.exit(app.exec())
