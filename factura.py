from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QApplication, QLabel, QPushButton, QAbstractItemView, QScrollArea, QAbstractScrollArea, QHBoxLayout, QLineEdit, QDateEdit, QMessageBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QDate
import json
import sys
from datetime import datetime
import os
import shutil

class FacturaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_empresas()

    def init_ui(self):
        self.setWindowTitle("Lista de Empresas")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        # Crear y colocar el campo de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre de empresa...")
        self.search_input.setFont(QFont("Helvetica", 12))
        self.search_input.textChanged.connect(self.search_empresas)  # Conectar la señal textChanged
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        # Crear y colocar los botones
        button_layout = QHBoxLayout()

        view_button = QPushButton("Ver Facturas")
        view_button.setFont(QFont("Helvetica", 14))
        view_button.clicked.connect(self.view_factura)
        button_layout.addWidget(view_button)

        view_books_button = QPushButton("Ver Libros")
        view_books_button.setFont(QFont("Helvetica", 14))
        view_books_button.clicked.connect(self.view_books)
        button_layout.addWidget(view_books_button)

        delete_company_button = QPushButton("Eliminar Empresa")
        delete_company_button.setFont(QFont("Helvetica", 14))
        delete_company_button.clicked.connect(self.delete_empresa)
        button_layout.addWidget(delete_company_button)

        exit_button = QPushButton("Salir")
        exit_button.setFont(QFont("Helvetica", 14))
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        # Crear y configurar la tabla con barra de desplazamiento
        self.table_widget = QTableWidget()
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def load_empresas(self):
        try:
            with open("contribuyentes.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                empresas = [client for client in data if client.get("Tipo de Empresa:") == "Empresa"]

                # Configurar la tabla
                headers = ["Nombre de la Empresa"]
                self.table_widget.setColumnCount(len(headers))
                self.table_widget.setHorizontalHeaderLabels(headers)
                self.table_widget.setRowCount(len(empresas))

                header_font = QFont("Helvetica", 16)
                self.table_widget.horizontalHeader().setFont(header_font)
                self.table_widget.horizontalHeader().setStretchLastSection(True)
                self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                cell_font = QFont("Helvetica", 16)
                for row, empresa in enumerate(empresas):
                    self.add_table_item(row, 0, empresa.get("Nombre:", "").upper(), cell_font)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar los datos: {e}")
            self.table_widget.setRowCount(1)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No se encontraron datos de empresas."))

    def add_table_item(self, row, column, text, font):
        item = QTableWidgetItem(text)
        item.setFont(font)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table_widget.setItem(row, column, item)

    def view_factura(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            nombre_empresa = self.table_widget.item(selected_row, 0).text()
            self.view_window = ViewFacturaWindow(nombre_empresa)
            self.view_window.show()

    def search_empresas(self):
        search_text = self.search_input.text().strip().lower()
        if search_text:
            try:
                with open("contribuyentes.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    filtered_empresas = [empresa for empresa in data if empresa.get("Tipo de Empresa:") == "Empresa" and search_text in empresa.get("Nombre:", "").lower()]

                    self.update_empresa_table(filtered_empresas)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error al cargar las empresas: {e}")
                self.table_widget.setRowCount(1)
                self.table_widget.setItem(0, 0, QTableWidgetItem("No se encontraron datos de empresas."))
        else:
            self.load_empresas()  # Cargar todas las empresas si no hay texto de búsqueda

    def update_empresa_table(self, empresas):
        headers = ["Nombre de la Empresa"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setRowCount(len(empresas))

        header_font = QFont("Helvetica", 16)
        self.table_widget.horizontalHeader().setFont(header_font)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        cell_font = QFont("Helvetica", 16)
        for row, empresa in enumerate(empresas):
            self.add_table_item(row, 0, empresa.get("Nombre:", "").upper(), cell_font)

    def view_books(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            nombre_empresa = self.table_widget.item(selected_row, 0).text()
            self.view_books_dialog = ViewBooksDialog(nombre_empresa)
            self.view_books_dialog.exec()

    def delete_empresa(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            nombre_empresa = self.table_widget.item(selected_row, 0).text()
            reply = QMessageBox.question(self, 'Eliminar Empresa', f'¿Estás seguro de que deseas eliminar la empresa {nombre_empresa}?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Eliminar la carpeta de la empresa
                empresa_dir = f'C:/Users/Dell/Desktop/System Contable/INFORMES CONTADORES/EMPRESAS/{nombre_empresa}'
                if os.path.exists(empresa_dir):
                    shutil.rmtree(empresa_dir)

                # Eliminar la empresa del archivo JSON
                try:
                    with open("contribuyentes.json", "r", encoding="utf-8") as file:
                        data = json.load(file)
                    data = [empresa for empresa in data if empresa.get("Nombre:", "").upper() != nombre_empresa.upper()]
                    with open("contribuyentes.json", "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error al eliminar la empresa: {e}")

                self.load_empresas()  # Recargar la lista de empresas

class ViewBooksDialog(QDialog):
    def __init__(self, nombre_empresa):
        super().__init__()
        self.nombre_empresa = nombre_empresa
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Seleccione el mes y el año")
        self.setFixedSize(400, 200)  # Ajustar el tamaño del cuadro de diálogo

        layout = QVBoxLayout(self)

        self.month_edit = QComboBox()
        self.month_edit.setFont(QFont("Helvetica", 12))
        self.month_edit.addItems([f"{month:02d}" for month in range(1, 13)])
        self.month_edit.setCurrentText(f"{QDate.currentDate().month():02d}")
        layout.addWidget(QLabel("Mes:"))
        layout.addWidget(self.month_edit)

        self.year_edit = QComboBox()
        self.year_edit.setFont(QFont("Helvetica", 12))
        self.year_edit.addItems([str(year) for year in range(2000, QDate.currentDate().year() + 1)])
        self.year_edit.setCurrentText(str(QDate.currentDate().year()))
        layout.addWidget(QLabel("Año:"))
        layout.addWidget(self.year_edit)

        self.tipo_libro_edit = QComboBox()
        self.tipo_libro_edit.setFont(QFont("Helvetica", 12))
        self.tipo_libro_edit.addItems(["LIBRO DE VENTAS", "LIBRO DE COMPRAS", "AMBOS"])
        layout.addWidget(QLabel("Tipo de Libro:"))
        layout.addWidget(self.tipo_libro_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.open_books)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def open_books(self):
        month = int(self.month_edit.currentText())
        year = int(self.year_edit.currentText())
        tipo_libro = self.tipo_libro_edit.currentText()

        base_path = f'INFORMES CONTADORES/EMPRESAS/{self.nombre_empresa.upper()}/LIBROS DE COMPRAS Y VENTAS/{year}/{month:02d}'
        month_name = datetime(year, month, 1).strftime('%B').upper()

        if tipo_libro in ["LIBRO DE COMPRAS", "AMBOS"]:
            compras_path = os.path.join(base_path, f'LIBRO DE COMPRAS {month_name} {year} - {self.nombre_empresa.upper()}.xlsx')
            if os.path.exists(compras_path):
                os.startfile(compras_path)
            else:
                QMessageBox.warning(self, "Error", f"No se encontró el archivo: {compras_path}")

        if tipo_libro in ["LIBRO DE VENTAS", "AMBOS"]:
            ventas_path = os.path.join(base_path, f'LIBRO DE VENTAS {month_name} {year} - {self.nombre_empresa.upper()}.xlsx')
            if os.path.exists(ventas_path):
                os.startfile(ventas_path)
            else:
                QMessageBox.warning(self, "Error", f"No se encontró el archivo: {ventas_path}")

        self.accept()

class ViewFacturaWindow(QWidget):
    def __init__(self, nombre_empresa):
        super().__init__()
        self.nombre_empresa = nombre_empresa
        self.transaction_type = "Compras"  # Default transaction type to Compras
        
        # Definir las rutas de las plantillas como atributos de la clase
        self.template_path_compras = 'C:/Users/Dell/Desktop/SC/LIBRO DE COMPRAS ENERO 2025 - INVERSIONES JEPA ELECTRIC, C.A.xlsx'
        self.template_path_ventas = 'C:/Users/Dell/Desktop/SC/LIBRO DE VENTAS FEBRERO 2025 - INVERSIONES JEPA ELECTRIC, C.A.xlsx'
        
        self.init_ui()
        self.load_facturas()

    def init_ui(self):
        self.setWindowTitle(f"Facturas de {self.nombre_empresa}")
        self.setFixedSize(1500, 600)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        # Crear y colocar la barra de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre del cliente...")
        self.search_input.setFont(QFont("Helvetica", 12))
        self.search_input.textChanged.connect(self.search_facturas)  # Conectar la señal textChanged
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        # Crear y colocar los botones
        button_layout = QHBoxLayout()

        edit_button = QPushButton("Editar")
        edit_button.setFont(QFont("Helvetica", 14))
        edit_button.clicked.connect(self.edit_factura)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Eliminar")
        delete_button.setFont(QFont("Helvetica", 14))
        delete_button.clicked.connect(self.delete_factura)
        button_layout.addWidget(delete_button)

        # Crear y colocar el botón toggle "Ventas/Compras"
        self.toggle_button = QPushButton("Ventas")
        self.toggle_button.setFont(QFont("Helvetica", 14))
        self.toggle_button.clicked.connect(self.toggle_transaction_type)
        button_layout.addWidget(self.toggle_button)

        export_button = QPushButton("Exportar a Excel")
        export_button.setFont(QFont("Helvetica", 14))
        export_button.clicked.connect(self.export_to_excel)
        button_layout.addWidget(export_button)

        exit_button = QPushButton("Cerrar")
        exit_button.setFont(QFont("Helvetica", 14))
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        # Crear y colocar el filtro de fecha
        date_filter_layout = QHBoxLayout()

        self.day_filter = QComboBox()
        self.day_filter.setFont(QFont("Helvetica", 12))
        self.day_filter.addItem("Todos")
        self.day_filter.addItems([f"{day:02d}" for day in range(1, 32)])
        self.day_filter.setCurrentText("Todos")
        self.day_filter.currentIndexChanged.connect(self.filter_by_date)

        self.month_filter = QComboBox()
        self.month_filter.setFont(QFont("Helvetica", 12))
        self.month_filter.addItem("Todos")
        self.month_filter.addItems([f"{month:02d}" for month in range(1, 13)])
        self.month_filter.setCurrentText(f"{QDate.currentDate().month():02d}")
        self.month_filter.currentIndexChanged.connect(self.filter_by_date)

        self.year_filter = QComboBox()
        self.year_filter.setFont(QFont("Helvetica", 12))
        self.year_filter.addItem("Todos")
        self.year_filter.addItems([str(year) for year in range(2000, QDate.currentDate().year() + 1)])
        self.year_filter.setCurrentText(str(QDate.currentDate().year()))
        self.year_filter.currentIndexChanged.connect(self.filter_by_date)

        date_filter_layout.addWidget(QLabel("Filtrar por Día:"))
        date_filter_layout.addWidget(self.day_filter)
        date_filter_layout.addWidget(QLabel("Filtrar por Mes:"))
        date_filter_layout.addWidget(self.month_filter)
        date_filter_layout.addWidget(QLabel("Filtrar por Año:"))
        date_filter_layout.addWidget(self.year_filter)

        layout.addLayout(date_filter_layout)

        # Crear y configurar la tabla con barra de desplazamiento
        self.table_widget = QTableWidget()
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def load_facturas(self):
        try:
            with open("datos_guardados.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = [data]

                # Filtrar las facturas de la empresa seleccionada
                self.empresa_facturas = [factura for factura in data if factura.get("Empresa", "").upper() == self.nombre_empresa.upper()]

                # Filtrar por tipo de transacción
                self.empresa_facturas = [factura for factura in self.empresa_facturas if factura.get("Tipo de Transacción", "Compras") == self.transaction_type]

                # Ordenar las facturas por fecha
                self.empresa_facturas.sort(key=lambda x: datetime.strptime(x['Fecha'], '%Y-%m-%d'))

                self.update_factura_table(self.empresa_facturas)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar las facturas: {e}")
            self.table_widget.setRowCount(1)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No se encontraron datos de facturas."))

    def update_factura_table(self, facturas):
        headers = ["Anexar Adj", "Fecha", "Nombre del Cliente", "RIF", "Número de Control", "Número de Documento", "Base imponible 16%", "IVA 16%", "Base imponible 8%", "IVA 8%", "Total"]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setRowCount(len(facturas))

        header_font = QFont("Helvetica", 16)
        self.table_widget.horizontalHeader().setFont(header_font)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        cell_font = QFont("Helvetica", 16)
        for row, factura in enumerate(facturas):
            for col, key in enumerate(headers):
                if key == "Anexar Adj":
                    file_path = factura.get("Anexar Adj", "")
                    if file_path:
                        button = QPushButton("Ver")
                        button.clicked.connect(lambda _, p=file_path: self.open_file(p))
                    else:
                        button = QPushButton("Anexar Adj")
                        button.clicked.connect(lambda _, r=row: self.attach_file(r))
                    button.setFont(QFont("Helvetica", 12))
                    self.table_widget.setCellWidget(row, col, button)
                else:
                    value = factura.get(key, "")
                    if key in ["Base imponible 16%", "IVA 16%", "Base imponible 8%", "IVA 8%", "Total"]:
                        value = float(value) if value else 0.0
                    if key == "Nombre del Cliente":
                        value = value.upper()
                    self.add_table_item(row, col, str(value), cell_font)

    def add_table_item(self, row, column, text, font):
        item = QTableWidgetItem(text)
        item.setFont(font)
        if "IVA" in self.table_widget.horizontalHeaderItem(column).text() or "Total" in self.table_widget.horizontalHeaderItem(column).text():
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table_widget.setItem(row, column, item)

    def attach_file(self, row):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Seleccionar archivo", "", "Images (*.png *.xpm *.jpg *.jpeg);;PDF Files (*.pdf);;All Files (*)")
        if file_path:
            # Obtener la fecha de la factura
            fecha_item = self.table_widget.item(row, 1)
            if fecha_item:
                fecha = fecha_item.text()
                year, month, _ = fecha.split('-')

                # Determinar el tipo de transacción
                tipo_transaccion = "Compras" if self.transaction_type == "Compras" else "Ventas"

                # Crear la ruta de destino
                dest_dir = f'C:/Users/Dell/Desktop/System Contable/INFORMES CONTADORES/EMPRESAS/{self.nombre_empresa}/FACTURAS/{tipo_transaccion}/{year}/{month}'
                os.makedirs(dest_dir, exist_ok=True)

                # Mover el archivo
                dest_path = os.path.join(dest_dir, os.path.basename(file_path))

                # Eliminar el archivo anterior si existe
                old_file_path_item = self.table_widget.item(row, 0)
                if old_file_path_item:
                    old_file_path = old_file_path_item.text()
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                shutil.copy(file_path, dest_path)

                # Actualizar la tabla y guardar la ruta del archivo
                self.table_widget.setItem(row, 0, QTableWidgetItem(dest_path))
                self.save_facturas()

                # Cambiar el texto del botón a "Ver"
                button = self.table_widget.cellWidget(row, 0)
                button.setText("Ver")
                button.clicked.disconnect()
                button.clicked.connect(lambda _, p=dest_path: self.open_file(p))

    def open_file(self, file_path):
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, "Error", f"No se encontró el archivo: {file_path}")

    def filter_by_date(self):
        selected_day = self.day_filter.currentText()
        selected_month = self.month_filter.currentText()
        selected_year = self.year_filter.currentText()

        filtered_facturas = self.empresa_facturas

        if selected_year != "Todos":
            filtered_facturas = [factura for factura in filtered_facturas if datetime.strptime(factura.get("Fecha", ""), '%Y-%m-%d').year == int(selected_year)]
        if selected_month != "Todos":
            filtered_facturas = [factura for factura in filtered_facturas if datetime.strptime(factura.get("Fecha", ""), '%Y-%m-%d').month == int(selected_month)]
        if selected_day != "Todos":
            filtered_facturas = [factura for factura in filtered_facturas if datetime.strptime(factura.get("Fecha", ""), '%Y-%m-%d').day == int(selected_day)]

        self.update_factura_table(filtered_facturas)

    def search_facturas(self):
        search_text = self.search_input.text().strip().lower()
        if search_text:
            filtered_facturas = [factura for factura in self.empresa_facturas if search_text in factura.get("Nombre del Cliente", "").lower()]
            self.update_factura_table(filtered_facturas)
        else:
            self.update_factura_table(self.empresa_facturas)

    def edit_factura(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            factura_data = {}
            for col in range(self.table_widget.columnCount()):
                key = self.table_widget.horizontalHeaderItem(col).text()
                item = self.table_widget.item(selected_row, col)
                value = item.text() if item else ""
                factura_data[key] = value
            factura_data["Empresa"] = self.nombre_empresa  # Asegurarse de que el campo "Empresa" esté presente
            self.edit_window = EditFacturaWindow(factura_data, self.save_edited_factura, selected_row)
            self.edit_window.show()

    def delete_factura(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            reply = QMessageBox.question(self, 'Eliminar Factura', '¿Estás seguro de que deseas eliminar esta factura?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Obtener la ruta del archivo adjunto
                file_path_item = self.table_widget.item(selected_row, 0)
                if file_path_item:
                    file_path = file_path_item.text()
                    if os.path.exists(file_path):
                        os.remove(file_path)  # Eliminar el archivo adjunto

                self.table_widget.removeRow(selected_row)
                self.save_facturas()

    def save_edited_factura(self, factura_data, row):
        for col, key in enumerate(factura_data.keys()):
            item = self.table_widget.item(row, col)
            if item:
                item.setText(factura_data[key])
            else:
                self.table_widget.setItem(row, col, QTableWidgetItem(factura_data[key]))
        self.save_facturas()
        self.load_facturas()  # Recargar las facturas después de guardar

    def save_facturas(self):
        try:
            with open("datos_guardados.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Actualizar las facturas de la empresa actual
        updated_data = []
        for row in range(self.table_widget.rowCount()):
            factura = {}
            for col in range(self.table_widget.columnCount()):
                key = self.table_widget.horizontalHeaderItem(col).text()
                item = self.table_widget.item(row, col)
                value = item.text() if item else ""
                factura[key] = value
            factura["Empresa"] = self.nombre_empresa  # Asegurarse de que el campo "Empresa" esté presente
            factura["Tipo de Transacción"] = self.transaction_type  # Asegurarse de que el campo "Tipo de Transacción" esté presente
            updated_data.append(factura)

        # Reemplazar las facturas de la empresa actual en el archivo
        data = [factura for factura in data if factura.get("Empresa", "").upper() != self.nombre_empresa.upper()]
        data.extend(updated_data)

        try:
            with open("datos_guardados.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error al guardar los datos: {e}")

    def export_to_excel(self):
        from export_excel import export_to_excel

        # Crear un cuadro de diálogo personalizado para seleccionar el mes y el año
        dialog = QDialog(self)
        dialog.setWindowTitle("Seleccione el mes y el año")
        dialog.setFixedSize(400, 200)  # Ajustar el tamaño del cuadro de diálogo

        layout = QVBoxLayout(dialog)

        month_edit = QComboBox()
        month_edit.setFont(QFont("Helvetica", 12))
        month_edit.addItems([f"{month:02d}" for month in range(1, 13)])
        month_edit.setCurrentText(f"{QDate.currentDate().month():02d}")
        layout.addWidget(QLabel("Mes:"))
        layout.addWidget(month_edit)

        year_edit = QComboBox()
        year_edit.setFont(QFont("Helvetica", 12))
        year_edit.addItems([str(year) for year in range(2000, QDate.currentDate().year() + 1)])
        year_edit.setCurrentText(str(QDate.currentDate().year()))
        layout.addWidget(QLabel("Año:"))
        layout.addWidget(year_edit)

        tipo_libro_edit = QComboBox()
        tipo_libro_edit.setFont(QFont("Helvetica", 12))
        tipo_libro_edit.addItems(["LIBRO DE VENTAS", "LIBRO DE COMPRAS", "AMBOS"])
        layout.addWidget(QLabel("Tipo de Libro:"))
        layout.addWidget(tipo_libro_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.Accepted:
            month = int(month_edit.currentText())
            year = int(year_edit.currentText())
            tipo_libro = tipo_libro_edit.currentText()

            # Llamar a export_to_excel con todos los argumentos requeridos
            if export_to_excel(
                self.template_path_compras,
                self.template_path_ventas,
                usuario=self.nombre_empresa,
                year=year,
                month=month,
                tipo_libro=tipo_libro
            ):
                QMessageBox.information(self, "Éxito", "Datos exportados correctamente")
            else:
                QMessageBox.warning(self, "Error", "Error al exportar los datos")

    def toggle_transaction_type(self):
        if self.transaction_type == "Compras":
            self.transaction_type = "Ventas"
            self.toggle_button.setText("Compras")
        else:
            self.transaction_type = "Compras"
            self.toggle_button.setText("Ventas")
        self.load_facturas()  # Recargar las facturas según el tipo de transacción seleccionado

class EditFacturaWindow(QWidget):
    def __init__(self, factura_data, save_callback, row):
        super().__init__()
        self.factura_data = factura_data
        self.save_callback = save_callback
        self.row = row
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Editar Factura")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        self.inputs = {}
        for key, value in self.factura_data.items():
            h_layout = QHBoxLayout()
            label = QLabel(key)
            label.setFont(QFont("Helvetica", 12))
            h_layout.addWidget(label)
            if key == "Fecha":
                input_field = QDateEdit()
                input_field.setDate(QDate.fromString(value, "yyyy-MM-dd"))
            elif "IVA" in key or "Total" in key:
                input_field = QLineEdit(value)
                input_field.setReadOnly(True)
            elif key == "Anexar Adj":
                input_field = QPushButton("Cambiar Archivo")
                input_field.clicked.connect(self.change_file)
                self.file_path_label = QLabel(value)
                h_layout.addWidget(self.file_path_label)
            else:
                input_field = QLineEdit(value)
                if "Base imponible" in key:
                    input_field.textChanged.connect(self.update_totals)
            input_field.setFont(QFont("Helvetica", 12))
            h_layout.addWidget(input_field)
            layout.addLayout(h_layout)
            self.inputs[key] = input_field

        save_button = QPushButton("Guardar")
        save_button.setFont(QFont("Helvetica", 14))
        save_button.clicked.connect(self.save_factura)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def update_totals(self):
        try:
            base_16_value = float(self.inputs["Base imponible 16%"].text()) if self.inputs["Base imponible 16%"].text() else 0.0
            iva_16_value = base_16_value * 0.16
            self.inputs["IVA 16%"].setText(f"{iva_16_value:.2f}")
            base_8_value = float(self.inputs["Base imponible 8%"].text()) if self.inputs["Base imponible 8%"].text() else 0.0
            iva_8_value = base_8_value * 0.08
            self.inputs["IVA 8%"].setText(f"{iva_8_value:.2f}")

            total_value = base_16_value + iva_16_value + base_8_value + iva_8_value
            self.inputs["Total"].setText(f"{total_value:.2f}")
        except ValueError:
            self.inputs["IVA 16%"].setText("")
            self.inputs["IVA 8%"].setText("")
            self.inputs["Total"].setText("")

    def change_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Seleccionar archivo", "", "Images (*.png *.xpm *.jpg *.jpeg);;PDF Files (*.pdf);;All Files (*)")
        if file_path:
            # Obtener la fecha de la factura
            fecha = self.inputs["Fecha"].date().toString("yyyy-MM-dd")
            year, month, _ = fecha.split('-')

            # Determinar el tipo de transacción
            tipo_transaccion = "Compras" if self.factura_data.get("Tipo de Transacción", "Compras") == "Compras" else "Ventas"

            # Crear la ruta de destino
            dest_dir = f'C:/Users/Dell/Desktop/System Contable/INFORMES CONTADORES/EMPRESAS/{self.factura_data["Empresa"]}/FACTURAS/{tipo_transaccion}/{year}/{month}'
            os.makedirs(dest_dir, exist_ok=True)

            # Mover el archivo
            dest_path = os.path.join(dest_dir, os.path.basename(file_path))

            # Eliminar el archivo anterior si existe
            old_file_path = self.file_path_label.text()
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

            shutil.copy(file_path, dest_path)

            # Actualizar la etiqueta de la ruta del archivo
            self.file_path_label.setText(dest_path)

    def save_factura(self):
        for key, input_field in self.inputs.items():
            if key == "Fecha":
                self.factura_data[key] = input_field.date().toString("yyyy-MM-dd")
            elif key == "Anexar Adj":
                self.factura_data[key] = self.file_path_label.text()
            else:
                self.factura_data[key] = input_field.text()
        self.save_callback(self.factura_data, self.row)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FacturaWindow()
    window.show()
    sys.exit(app.exec())
