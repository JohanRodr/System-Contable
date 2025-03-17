from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QApplication, QLabel, QPushButton, QAbstractItemView, QScrollArea, QAbstractScrollArea, QHBoxLayout, QLineEdit, QDateEdit, QMessageBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog
from PySide6.QtGui import QFont, QDoubleValidator
from PySide6.QtCore import Qt, QDate, Signal
import json
import sys
from datetime import datetime
import os
import shutil

class FacturaWindow(QWidget):
    window_closed = Signal()  # Señal personalizada para indicar que la ventana se ha cerrado

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

    def closeEvent(self, event):
        self.window_closed.emit()  # Emitir la señal personalizada cuando la ventana se cierra
        event.accept()

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
                    file_path = factura.get("Archivo", "")
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
    def open_file(self, file_path):
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, "Error", f"No se encontró el archivo: {file_path}")

    def attach_file(self, row):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Seleccionar archivo", "", "Images (*.png *.xpm *.jpg *.jpeg);;PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.empresa_facturas[row]["Archivo"] = file_path
            self.update_factura_table(self.empresa_facturas)

    def search_facturas(self):
        search_text = self.search_input.text().strip().lower()
        filtered_facturas = [factura for factura in self.empresa_facturas if search_text in factura.get("Nombre del Cliente", "").lower()]
        self.update_factura_table(filtered_facturas)

    def filter_by_date(self):
        day = self.day_filter.currentText()
        month = self.month_filter.currentText()
        year = self.year_filter.currentText()

        filtered_facturas = self.empresa_facturas
        if day != "Todos":
            filtered_facturas = [factura for factura in filtered_facturas if factura.get("Fecha", "").split("-")[2] == day]
        if month != "Todos":
            filtered_facturas = [factura for factura in filtered_facturas if factura.get("Fecha", "").split("-")[1] == month]
        if year != "Todos":
            filtered_facturas = [factura for factura in filtered_facturas if factura.get("Fecha", "").split("-")[0] == year]

        self.update_factura_table(filtered_facturas)

    def toggle_transaction_type(self):
        if self.transaction_type == "Compras":
            self.transaction_type = "Ventas"
            self.toggle_button.setText("Compras")
        else:
            self.transaction_type = "Compras"
            self.toggle_button.setText("Ventas")
        self.load_facturas()

    def edit_factura(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            factura = self.empresa_facturas[selected_row]
            self.edit_window = EditFacturaWindow(factura)
            self.edit_window.factura_updated.connect(self.load_facturas)
            self.edit_window.show()

    def delete_factura(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            factura = self.empresa_facturas[selected_row]
            reply = QMessageBox.question(self, 'Eliminar Factura', f'¿Estás seguro de que deseas eliminar la factura de {factura["Nombre del Cliente"]}?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Eliminar el archivo adjunto si existe
                file_path = factura.get("Archivo", "")
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)

                self.empresa_facturas.pop(selected_row)
                self.update_factura_table(self.empresa_facturas)
                self.save_facturas()

    def save_facturas(self):
        try:
            with open("datos_guardados.json", "w", encoding="utf-8") as file:
                json.dump(self.empresa_facturas, file, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron guardar las facturas: {e}")

    def export_to_excel(self):
        # Implementar la lógica para exportar a Excel
        pass

class EditFacturaWindow(QWidget):
    factura_updated = Signal()

    def __init__(self, factura):
        super().__init__()
        self.factura = factura
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Editar Factura")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        self.entry_nombre_cliente = QLineEdit(self.factura.get("Nombre del Cliente", ""))
        self.entry_nombre_cliente.setFont(QFont("Helvetica", 12))
        layout.addWidget(QLabel("Nombre del Cliente:"))
        layout.addWidget(self.entry_nombre_cliente)

        self.entry_rif = QLineEdit(self.factura.get("RIF", ""))
        self.entry_rif.setFont(QFont("Helvetica", 12))
        layout.addWidget(QLabel("RIF:"))
        layout.addWidget(self.entry_rif)

        self.entry_numero_control = QLineEdit(self.factura.get("Número de Control", ""))
        self.entry_numero_control.setFont(QFont("Helvetica", 12))
        layout.addWidget(QLabel("Número de Control:"))
        layout.addWidget(self.entry_numero_control)

        self.entry_numero_documento = QLineEdit(self.factura.get("Número de Documento", ""))
        self.entry_numero_documento.setFont(QFont("Helvetica", 12))
        layout.addWidget(QLabel("Número de Documento:"))
        layout.addWidget(self.entry_numero_documento)

        self.entry_base_16 = QLineEdit(self.factura.get("Base imponible 16%", ""))
        self.entry_base_16.setFont(QFont("Helvetica", 12))
        self.entry_base_16.setValidator(QDoubleValidator(0, 1000000, 2))
        layout.addWidget(QLabel("Base imponible 16%:"))
        layout.addWidget(self.entry_base_16)

        self.entry_iva_16 = QLineEdit(self.factura.get("IVA 16%", ""))
        self.entry_iva_16.setFont(QFont("Helvetica", 12))
        self.entry_iva_16.setReadOnly(True)
        layout.addWidget(QLabel("IVA 16%:"))
        layout.addWidget(self.entry_iva_16)

        self.entry_base_8 = QLineEdit(self.factura.get("Base imponible 8%", ""))
        self.entry_base_8.setFont(QFont("Helvetica", 12))
        self.entry_base_8.setValidator(QDoubleValidator(0, 1000000, 2))
        layout.addWidget(QLabel("Base imponible 8%:"))
        layout.addWidget(self.entry_base_8)

        self.entry_iva_8 = QLineEdit(self.factura.get("IVA 8%", ""))


        self.entry_iva_8.setFont(QFont("Helvetica", 12))
        self.entry_iva_8.setReadOnly(True)
        layout.addWidget(QLabel("IVA 8%:"))
        layout.addWidget(self.entry_iva_8)

        self.entry_total = QLineEdit(self.factura.get("Total", ""))
        self.entry_total.setFont(QFont("Helvetica", 12))
        self.entry_total.setReadOnly(True)
        layout.addWidget(QLabel("Total:"))
        layout.addWidget(self.entry_total)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_changes)
        button_box.rejected.connect(self.close)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def save_changes(self):
        self.factura["Nombre del Cliente"] = self.entry_nombre_cliente.text()
        self.factura["RIF"] = self.entry_rif.text()
        self.factura["Número de Control"] = self.entry_numero_control.text()
        self.factura["Número de Documento"] = self.entry_numero_documento.text()
        self.factura["Base imponible 16%"] = self.entry_base_16.text()
        self.factura["IVA 16%"] = self.entry_iva_16.text()
        self.factura["Base imponible 8%"] = self.entry_base_8.text()
        self.factura["IVA 8%"] = self.entry_iva_8.text()
        self.factura["Total"] = self.entry_total.text()

        self.factura_updated.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FacturaWindow()
    window.show()
    sys.exit(app.exec())
