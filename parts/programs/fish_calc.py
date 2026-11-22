import sys
import os

from decimal import Decimal, InvalidOperation
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.local_data = (os.path.join(os.getenv('LOCALAPPDATA'), 'FishOS') if 'win' in sys.platform else
                           os.path.join(os.path.expanduser('~'), '.local/share/FishOS') if 'linux' in sys.platform else '')

        self.setWindowTitle("FishCalc")
        self.setWindowIcon(QIcon(os.path.join(self.local_data, 'calc.png')))
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout(self)
        self.buttons_layout = QGridLayout()

        self.resize(280, 420)

        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = False
        self.error_state = False

        main_layout = QVBoxLayout(self)

        self.secondary_label = QLabel("")
        self.secondary_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        sec_font = self.secondary_label.font()
        sec_font.setPointSize(11)
        self.secondary_label.setFont(sec_font)

        self.main_label = QLabel("0")
        self.main_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        main_font = self.main_label.font()
        main_font.setPointSize(26)
        self.main_label.setFont(main_font)

        main_layout.addWidget(self.secondary_label)
        main_layout.addWidget(self.main_label)

        grid = QGridLayout()
        main_layout.addLayout(grid)

        self.number_buttons = []
        for i in range(10):
            btn = QPushButton(str(i))
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            btn_font = btn.font()
            btn_font.setPointSize(14)
            btn.setFont(btn_font)
            btn.clicked.connect(lambda checked, d=str(i): self.on_digit(d))
            self.number_buttons.append(btn)

        self.clear_button = self._create_button("C", self.on_clear)
        self.clear_entry_button = self._create_button("CE", self.on_clear_entry)
        self.divide_button = self._create_button("/", lambda: self.on_operator("/"))
        self.multiply_button = self._create_button("*", lambda: self.on_operator("*"))
        self.substract_button = self._create_button("-", lambda: self.on_operator("-"))
        self.add_button = self._create_button("+", lambda: self.on_operator("+"))
        self.float_point_button = self._create_button(".", self.on_point)
        self.plus_minus_button = self._create_button("±", self.on_plus_minus)
        self.equals_button = self._create_button("=", self.on_equals)

        grid.addWidget(self.number_buttons[7], 0, 0)
        grid.addWidget(self.number_buttons[8], 0, 1)
        grid.addWidget(self.number_buttons[9], 0, 2)
        grid.addWidget(self.divide_button, 0, 3)

        grid.addWidget(self.number_buttons[4], 1, 0)
        grid.addWidget(self.number_buttons[5], 1, 1)
        grid.addWidget(self.number_buttons[6], 1, 2)
        grid.addWidget(self.multiply_button, 1, 3)

        grid.addWidget(self.number_buttons[1], 2, 0)
        grid.addWidget(self.number_buttons[2], 2, 1)
        grid.addWidget(self.number_buttons[3], 2, 2)
        grid.addWidget(self.substract_button, 2, 3)

        grid.addWidget(self.clear_button, 3, 0)
        grid.addWidget(self.number_buttons[0], 3, 1)
        grid.addWidget(self.clear_entry_button, 3, 2)
        grid.addWidget(self.add_button, 3, 3)

        grid.addWidget(self.float_point_button, 4, 0)
        grid.addWidget(self.plus_minus_button, 4, 1)
        grid.addWidget(self.equals_button, 4, 2, 1, 2)

    def _create_button(self, text, handler):
        btn = QPushButton(text)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_font = btn.font()
        btn_font.setPointSize(14)
        btn.setFont(btn_font)
        btn.clicked.connect(handler)
        return btn

    def _clean_decimal(self, value):
        if value == 0:
            return Decimal(0)
        if value == value.to_integral_value():
            return Decimal(int(value))
        text = format(value, "f").rstrip("0").rstrip(".")
        return Decimal(text)

    def _decimal_to_raw_str(self, value):
        cleaned = self._clean_decimal(value)
        return format(cleaned, "f")

    def _to_sci_str(self, value):
        formatted = f"{value:.2e}"
        mantissa, exp = formatted.split("e")
        return f"{mantissa}e{int(exp)}"

    def _format_main(self, raw_str):
        if len(raw_str) <= 11:
            return raw_str
        try:
            value = Decimal(raw_str)
        except InvalidOperation:
            return raw_str[:11]
        return self._to_sci_str(value)

    def _format_secondary(self, value):
        cleaned = self._clean_decimal(value)
        plain = format(cleaned, "f")
        digits_without_sign = plain.lstrip("-")
        if len(digits_without_sign) <= 30:
            return plain
        return self._to_sci_str(cleaned)

    def _update_main_label(self):
        self.main_label.setText(self._format_main(self.current_input))

    def _reset_from_error(self):
        self.error_state = False
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = False
        self.current_input = "0"
        self.secondary_label.setText("")
        self.main_label.setText("0")

    def _set_error(self):
        self.error_state = True
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = False
        self.current_input = "0"
        self.secondary_label.setText("")
        self.main_label.setText("ОШИБКА")

    def _calculate(self, left, right, op):
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            if right == 0:
                return None
            return left / right
        return right

    def on_digit(self, digit):
        if self.error_state:
            self._reset_from_error()
            self.current_input = digit
            self._update_main_label()
            return

        if self.waiting_for_operand:
            self.current_input = digit
            self.waiting_for_operand = False
        elif self.current_input == "0":
            self.current_input = digit
        elif self.current_input == "-0":
            self.current_input = "-" + digit
        else:
            self.current_input += digit

        self._update_main_label()

    def on_point(self):
        if self.error_state:
            self._reset_from_error()
            return

        if self.waiting_for_operand:
            self.current_input = "0."
            self.waiting_for_operand = False
            self._update_main_label()
            return

        if "." not in self.current_input:
            self.current_input += "."
            self._update_main_label()

    def on_plus_minus(self):
        if self.error_state:
            self._reset_from_error()
            return

        try:
            value = Decimal(self.current_input)
        except InvalidOperation:
            return

        if value == 0:
            return

        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input

        self._update_main_label()

    def on_clear(self):
        self._reset_from_error()

    def on_clear_entry(self):
        if self.error_state:
            self._reset_from_error()
            return

        self.current_input = "0"
        self.waiting_for_operand = False
        self.main_label.setText("0")

    def on_operator(self, op):
        if self.error_state:
            self._reset_from_error()
            return

        current_val = Decimal(self.current_input)

        if self.operator is not None and not self.waiting_for_operand:
            result = self._calculate(self.first_operand, current_val, self.operator)
            if result is None:
                self._set_error()
                return
            self.first_operand = self._clean_decimal(result)
            self.current_input = self._decimal_to_raw_str(self.first_operand)
            self._update_main_label()
        else:
            self.first_operand = self._clean_decimal(current_val)

        self.operator = op
        self.secondary_label.setText(f"{self._format_secondary(self.first_operand)} {op}")
        self.waiting_for_operand = True

    def on_equals(self):
        if self.error_state:
            self._reset_from_error()
            return

        if self.operator is None or self.first_operand is None:
            return

        current_val = Decimal(self.current_input)
        result = self._calculate(self.first_operand, current_val, self.operator)
        if result is None:
            self._set_error()
            return

        cleaned = self._clean_decimal(result)
        self.current_input = self._decimal_to_raw_str(cleaned)
        self._update_main_label()
        self.secondary_label.setText("")
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = True

    def toggle(self):
        if not self.isHidden():
            self.hide()
        else:
            self.show()
            self.raise_()