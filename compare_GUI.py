import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QLabel,QHeaderView


class PriceComparisonGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Price Comparison")

        # Calculate the desired position and size of the window
        screen = QDesktopWidget().screenGeometry()
        self.width = int(screen.width() * 0.75)
        self.height = int(screen.height() * 0.75)
        self.left = int((screen.width() - self.width) / 2)
        self.top = int((screen.height() - self.height) / 2)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        self.text_box = QLineEdit()
        layout.addWidget(self.text_box)

        button_layout = QHBoxLayout()

        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer_left)

        compare_button = QPushButton( "Compare Prices")
        compare_button.clicked.connect(self.compare_prices)
        button_layout.addWidget(compare_button)

        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer_right)

        layout.addLayout(button_layout)

        tables_layout = QHBoxLayout()

        self.jumia_label = QLabel("Jumia")
        tables_layout.addWidget(self.jumia_label)

        self.jumia_table = QTableWidget()
        self.jumia_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        tables_layout.addWidget(self.jumia_table)

        self.konga_label = QLabel("Konga")
        tables_layout.addWidget(self.konga_label)

        self.konga_table = QTableWidget()
        self.konga_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        tables_layout.addWidget(self.konga_table)

        layout.addLayout(tables_layout)

        self.setLayout(layout)

    def compare_prices(self):
        product = self.text_box.text().strip()

        if not product:
            QMessageBox.warning(self, "Warning", "Please enter a product in the text box.")
        else:
            # Run the first script and pass the input
            script1_process = subprocess.Popen(["python", "main_jumia.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            script1_output, script1_error = script1_process.communicate(input=product)
            
            # Run the second script and pass the input
            script2_process = subprocess.Popen(["python", "main_konga.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            script2_output, script2_error = script2_process.communicate(input=product)

            # Load data from the updated text files (Jumia and Konga)
            jumia_data = self.load_data_from_file("jumia.txt")
            konga_data = self.load_data_from_file("konga.txt")

            # Clear the tables before populating them with new data
            self.jumia_table.clear()
            self.konga_table.clear()

            # Set the number of rows and columns in the tables
            num_rows = max(len(jumia_data), len(konga_data))
            self.jumia_table.setRowCount(num_rows)
            self.jumia_table.setColumnCount(1)
            self.konga_table.setRowCount(num_rows)
            self.konga_table.setColumnCount(1)

            # Populate the tables with data from the files
            for row in range(num_rows):
                if row < len(jumia_data):
                    item1 = QTableWidgetItem(jumia_data[row])
                    self.jumia_table.setItem(row, 0, item1)

                if row < len(konga_data):
                    item2 = QTableWidgetItem(konga_data[row])
                    self.konga_table.setItem(row, 0, item2)

    def load_data_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf8") as file:
                data = file.readlines()
                data = [line.strip() for line in data]
                return data
        except FileNotFoundError:
            return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PriceComparisonGUI()
    gui.show()
    sys.exit(app.exec_())
