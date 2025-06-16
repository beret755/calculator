#!/usr/bin/env python3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QHBoxLayout, QAction, QMenuBar
)
from PyQt5.QtCore import Qt
import sys
import math

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator")
        self.setGeometry(200, 200, 350, 400)
        self.mode = "simple"  

        self.init_ui()

    def init_ui(self):
        # Menu
        menubar = self.menuBar()
        mode_menu = menubar.addMenu("Tryb")
        simple_action = QAction("Prosty", self)
        advanced_action = QAction("Zaawansowany", self)
        simple_action.triggered.connect(self.set_simple_mode)
        advanced_action.triggered.connect(self.set_advanced_mode)
        mode_menu.addAction(simple_action)
        mode_menu.addAction(advanced_action)

        # Ekran kalkulatora
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(40)
        self.display.setStyleSheet("font-size: 20px;")

        # Layout główny
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.display)
        self.buttons_layout = QGridLayout()
        self.main_layout.addLayout(self.buttons_layout)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.create_simple_buttons()

    def create_simple_buttons(self):
        # Czyść stare przyciski
        for i in reversed(range(self.buttons_layout.count())):
            widget = self.buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 0, 0), 
        ]
        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(60, 40)
            btn.clicked.connect(self.on_button_clicked)
            self.buttons_layout.addWidget(btn, row, col)

    def create_advanced_buttons(self):
        # Czyść stare przyciski
        for i in reversed(range(self.buttons_layout.count())):
            widget = self.buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
            ('C', 1, 0), ('√', 1, 1), ('^', 1, 2), ('%', 1, 3),
            ('(', 0, 0), (')', 0, 1), ('1/x', 0, 2), ('±', 0, 3),
        ]
        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(60, 40)
            btn.clicked.connect(self.on_button_clicked)
            self.buttons_layout.addWidget(btn, row, col)

    def set_simple_mode(self):
        self.mode = "simple"
        self.create_simple_buttons()
        self.display.clear()

    def set_advanced_mode(self):
        self.mode = "advanced"
        self.create_advanced_buttons()
        self.display.clear()

    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()
        current = self.display.text()

        if text == 'C':
            self.display.clear()
        elif text == '=':
            try:
                expr = current.replace('^', '**')
                expr = expr.replace('√', 'math.sqrt')
                expr = expr.replace('%', '/100')
                expr = expr.replace('1/x', '1/(' + current + ')')
                expr = expr.replace('±', '-(' + current + ')')
                # Bezpieczne eval
                result = eval(expr, {"__builtins__": None, "math": math})
                self.display.setText(str(result))
            except Exception:
                self.display.setText("Błąd")
        elif text == '√':
            self.display.setText(current + '√')
        elif text == '^':
            self.display.setText(current + '^')
        elif text == '%':
            self.display.setText(current + '%')
        elif text == '1/x':
            self.display.setText('1/(' + current + ')')
        elif text == '±':
            if current.startswith('-'):
                self.display.setText(current[1:])
            else:
                self.display.setText('-' + current)
        else:
            self.display.setText(current + text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())