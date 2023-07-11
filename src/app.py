import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
from enigma_machine import Enigma
import reflector as rf
import rotor as rt
import style as s

class MainWindow(QMainWindow):
    '''main application window'''
    def __init__(self):
        '''initialize main window'''
        super().__init__()
        self.setStyleSheet(s.main_window)
        self.wdw = None
        self.setWindowTitle('Enigma M3')
        self.setContentsMargins(5, 5, 5, 5)
        content_widget = QWidget()
        main_layout = QGridLayout(content_widget)
        main_layout.setSpacing(3)
        main_layout.setColumnStretch(0, 2)
        main_layout.setColumnStretch(1, 1)
        main_layout.setColumnStretch(2, 1)
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 2)
        main_layout.setRowStretch(2, 2)
        self.setCentralWidget(content_widget)

        # initialize enigma machine
        self.rotor_wiring = [rt.ROTOR_I_WIRING, rt.ROTOR_II_WIRING, rt.ROTOR_III_WIRING]
        self.rotor_notch = [rt.ROTOR_I_NOTCH, rt.ROTOR_II_NOTCH, rt.ROTOR_III_NOTCH]
        self.reflector = rf.Reflector()
        self.rotors = [rt.Rotor(self.rotor_wiring[0], self.rotor_notch[0]), 
                       rt.Rotor(self.rotor_wiring[0], self.rotor_notch[0]),
                       rt.Rotor(self.rotor_wiring[0], self.rotor_notch[0])]
        self.rotor_state = ["A", "A", "A"]
        self.rotor_ring = ["A", "A", "A"]
        self.plugs = ""
        plugboard_settings = [(elem[0], elem[1]) for elem in self.plugs.split()]
        self.enigma = Enigma(self.reflector, self.rotors[0], self.rotors[1], self.rotors[2], 
                             self.rotor_state, self.rotor_ring, plugboard_settings)

        # create keyboard, lampboard and plugboard
        self.keyboard_widget = QWidget()
        self.keyboard_widget.setStyleSheet(s.keyboard_widget)
        self.keyboard_widget.setFixedSize(650, 220)
        keyboard_layout = QVBoxLayout()
        self.keyboard_buttons = []
        self.create_board_buttons(keyboard_layout, self.handle_keyboard_click, self.keyboard_buttons, s.keyboard_button)
        self.keyboard_widget.setLayout(keyboard_layout)

        lampboard_widget = QWidget()
        lampboard_widget.setFixedSize(650, 230)
        lampboard_widget.setStyleSheet(s.lampboard_widget)
        lampboard_layout = QVBoxLayout(lampboard_widget)
        lampboard_widget.setEnabled(False)
        self.lampboard_buttons = []
        self.create_board_buttons(lampboard_layout, None, self.lampboard_buttons, s.lampboard_button, True)
        line_board1 = QLabel()
        line_board1.setStyleSheet(s.line)
        line_board1.setFixedSize(570, 11)
        lampboard_layout.addWidget(line_board1)
        lampboard_widget.setLayout(lampboard_layout)
        lampboard_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        plugboard_widget = QWidget()
        plugboard_widget.setFixedSize(650, 250)
        plugboard_widget.setStyleSheet(s.plugboard_widget)
        line_board2 = QLabel()
        line_board2.setStyleSheet(s.line)
        line_board2.setFixedSize(570, 11)
        plugboard_layout = QVBoxLayout(plugboard_widget)
        plugboard_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        plugboard_layout.addWidget(line_board2)
        self.plugboard_buttons = []
        self.create_board_buttons(plugboard_layout, self.handle_plugboard_click, self.plugboard_buttons, s.plugboard_button)
        self.plug_keys = {}
        for button in self.plugboard_buttons:
            self.plug_keys[button] = {"is_active": False, "color": None}
        plugboard_widget.setLayout(plugboard_layout)
        self.selected_plug_color = []

        # create settings widget
        settings_widget = QWidget()
        settings_widget.setFixedSize(280, 230)
        settings_widget.setContentsMargins(5, 5, 5, 5)
        settings_widget.setStyleSheet(s.settings_widget)
        settings_layout = QGridLayout(settings_widget)

        # create labels
        rotor1_label = QLabel("Rotor 1")
        rotor2_label = QLabel("Rotor 2")
        rotor3_label = QLabel("Rotor 3")
        position_label = QLabel("Position")
        ring_label = QLabel("Ring")
        rotor1_label.setStyleSheet(s.label)
        rotor2_label.setStyleSheet(s.label)
        rotor3_label.setStyleSheet(s.label)
        position_label.setStyleSheet(s.label)
        ring_label.setStyleSheet(s.label)

        # create rotor comboboxes
        rotor1_combobox = QComboBox()
        rotor2_combobox = QComboBox()
        rotor3_combobox = QComboBox()
        rotor1_combobox.addItems(["I", "II", "III"])
        rotor2_combobox.addItems(["I", "II", "III"])
        rotor3_combobox.addItems(["I", "II", "III"])
        rotor1_combobox.currentIndexChanged.connect(lambda index: self.handle_rotor_change(index, 0))
        rotor2_combobox.currentIndexChanged.connect(lambda index: self.handle_rotor_change(index, 1))
        rotor3_combobox.currentIndexChanged.connect(lambda index: self.handle_rotor_change(index, 2))
        rotor1_combobox.setFixedSize(80, 35)
        rotor2_combobox.setFixedSize(80, 35)
        rotor3_combobox.setFixedSize(80, 35)
        rotor1_combobox.setStyleSheet(s.combobox)
        rotor2_combobox.setStyleSheet(s.combobox)
        rotor3_combobox.setStyleSheet(s.combobox)

        # create rotor position settings
        self.position_rotor1 = QLabel(self.rotor_state[0])
        stepup_position_rotor1 = QPushButton("+")
        stepdown_position_rotor1 = QPushButton("-")
        pos_rotor1_widget = QWidget()
        pos_rotor1_widget.setFixedSize(80, 35)
        pos_rotor1_layout = QHBoxLayout(pos_rotor1_widget)
        pos_rotor1_layout.addWidget(stepup_position_rotor1)
        pos_rotor1_layout.addWidget(self.position_rotor1)
        pos_rotor1_layout.addWidget(stepdown_position_rotor1)
        self.position_rotor2 = QLabel(self.rotor_state[1])
        stepup_position_rotor2 = QPushButton("+")
        stepdown_position_rotor2 = QPushButton("-")
        pos_rotor2_widget = QWidget()
        pos_rotor2_widget.setFixedSize(80, 35)
        pos_rotor2_layout = QHBoxLayout(pos_rotor2_widget)
        pos_rotor2_layout.addWidget(stepup_position_rotor2)
        pos_rotor2_layout.addWidget(self.position_rotor2)
        pos_rotor2_layout.addWidget(stepdown_position_rotor2)
        self.position_rotor3 = QLabel(self.rotor_state[2])
        stepup_position_rotor3 = QPushButton("+")
        stepdown_position_rotor3 = QPushButton("-")
        pos_rotor3_widget = QWidget()
        pos_rotor3_widget.setFixedSize(80, 35)
        pos_rotor3_layout = QHBoxLayout(pos_rotor3_widget)
        pos_rotor3_layout.addWidget(stepup_position_rotor3)
        pos_rotor3_layout.addWidget(self.position_rotor3)
        pos_rotor3_layout.addWidget(stepdown_position_rotor3)
        stepup_position_rotor1.clicked.connect(lambda: self.handle_stepup_pos_click(0))
        stepdown_position_rotor1.clicked.connect(lambda: self.handle_stepdown_pos_click(0))
        stepup_position_rotor2.clicked.connect(lambda: self.handle_stepup_pos_click(1))
        stepdown_position_rotor2.clicked.connect(lambda: self.handle_stepdown_pos_click(1))
        stepup_position_rotor3.clicked.connect(lambda: self.handle_stepup_pos_click(2))
        stepdown_position_rotor3.clicked.connect(lambda: self.handle_stepdown_pos_click(2))
        self.position_rotor1.setStyleSheet(s.label)
        self.position_rotor2.setStyleSheet(s.label)
        self.position_rotor3.setStyleSheet(s.label)
        pos_rotor1_widget.setStyleSheet(s.step_widget)
        pos_rotor2_widget.setStyleSheet(s.step_widget)
        pos_rotor3_widget.setStyleSheet(s.step_widget)
        stepup_position_rotor1.setStyleSheet(s.step_button)
        stepup_position_rotor1.setFixedSize(10, 20)
        stepdown_position_rotor1.setStyleSheet(s.step_button)
        stepdown_position_rotor1.setFixedSize(10, 20)
        stepup_position_rotor2.setStyleSheet(s.step_button)
        stepup_position_rotor2.setFixedSize(10, 20)
        stepdown_position_rotor2.setStyleSheet(s.step_button)
        stepdown_position_rotor2.setFixedSize(10, 20)
        stepup_position_rotor3.setStyleSheet(s.step_button)
        stepup_position_rotor3.setFixedSize(10, 20)
        stepdown_position_rotor3.setStyleSheet(s.step_button)
        stepdown_position_rotor3.setFixedSize(10, 20)

        # create rotor ring settings
        self.ring_rotor1 = QLabel(self.rotor_ring[0])
        stepup_ring_rotor1 = QPushButton("+")
        stepdown_ring_rotor1 = QPushButton("-")
        ring_rotor1_widget = QWidget()
        ring_rotor1_widget.setFixedSize(80, 35)
        ring_rotor1_layout = QHBoxLayout(ring_rotor1_widget)
        ring_rotor1_layout.addWidget(stepup_ring_rotor1)
        ring_rotor1_layout.addWidget(self.ring_rotor1)
        ring_rotor1_layout.addWidget(stepdown_ring_rotor1)
        self.ring_rotor2 = QLabel(self.rotor_ring[1])
        stepup_ring_rotor2 = QPushButton("+")
        stepdown_ring_rotor2 = QPushButton("-")
        ring_rotor2_widget = QWidget()
        ring_rotor2_widget.setFixedSize(80, 35)
        ring_rotor2_layout = QHBoxLayout(ring_rotor2_widget)
        ring_rotor2_layout.addWidget(stepup_ring_rotor2)
        ring_rotor2_layout.addWidget(self.ring_rotor2)
        ring_rotor2_layout.addWidget(stepdown_ring_rotor2)
        self.ring_rotor3 = QLabel(self.rotor_ring[2])
        stepup_ring_rotor3 = QPushButton("+")
        stepdown_ring_rotor3 = QPushButton("-")
        ring_rotor3_widget = QWidget()
        ring_rotor3_widget.setFixedSize(80, 35)
        ring_rotor3_layout = QHBoxLayout(ring_rotor3_widget)
        ring_rotor3_layout.addWidget(stepup_ring_rotor3)
        ring_rotor3_layout.addWidget(self.ring_rotor3)
        ring_rotor3_layout.addWidget(stepdown_ring_rotor3)
        stepup_ring_rotor1.clicked.connect(lambda: self.handle_stepup_ring_click(0))
        stepdown_ring_rotor1.clicked.connect(lambda: self.handle_stepdown_ring_click(0))
        stepup_ring_rotor2.clicked.connect(lambda: self.handle_stepup_ring_click(1))
        stepdown_ring_rotor2.clicked.connect(lambda: self.handle_stepdown_ring_click(1))
        stepup_ring_rotor3.clicked.connect(lambda: self.handle_stepup_ring_click(2))
        stepdown_ring_rotor3.clicked.connect(lambda: self.handle_stepdown_ring_click(2))
        ring_rotor1_widget.setStyleSheet(s.step_widget)
        ring_rotor2_widget.setStyleSheet(s.step_widget)
        ring_rotor3_widget.setStyleSheet(s.step_widget)
        self.ring_rotor1.setStyleSheet(s.label)
        self.ring_rotor2.setStyleSheet(s.label)
        self.ring_rotor3.setStyleSheet(s.label)
        ring_rotor1_widget.setStyleSheet(s.step_widget)
        ring_rotor2_widget.setStyleSheet(s.step_widget)
        ring_rotor3_widget.setStyleSheet(s.step_widget)
        stepup_ring_rotor1.setStyleSheet(s.step_button)
        stepup_ring_rotor1.setFixedSize(10, 20)
        stepdown_ring_rotor1.setStyleSheet(s.step_button)
        stepdown_ring_rotor1.setFixedSize(10, 20)
        stepup_ring_rotor2.setStyleSheet(s.step_button)
        stepup_ring_rotor2.setFixedSize(10, 20)
        stepdown_ring_rotor2.setStyleSheet(s.step_button)
        stepdown_ring_rotor2.setFixedSize(10, 20)
        stepup_ring_rotor3.setStyleSheet(s.step_button)
        stepup_ring_rotor3.setFixedSize(10, 20)
        stepdown_ring_rotor3.setStyleSheet(s.step_button)
        stepdown_ring_rotor3.setFixedSize(10, 20)

        # create rotor settings layout
        settings_layout.setVerticalSpacing(5)
        settings_layout.setHorizontalSpacing(5)
        settings_layout.addWidget(rotor1_label, 0, 0)
        settings_layout.addWidget(position_label, 0, 1)
        settings_layout.addWidget(ring_label, 0, 2)
        settings_layout.addWidget(rotor1_combobox, 1, 0)
        settings_layout.addWidget(pos_rotor1_widget, 1, 1)
        settings_layout.addWidget(ring_rotor1_widget, 1, 2)
        settings_layout.addWidget(rotor2_label, 2, 0)
        settings_layout.addWidget(rotor2_combobox, 3, 0)
        settings_layout.addWidget(pos_rotor2_widget, 3, 1)
        settings_layout.addWidget(ring_rotor2_widget, 3, 2)
        settings_layout.addWidget(rotor3_label, 4, 0)
        settings_layout.addWidget(rotor3_combobox, 5, 0)
        settings_layout.addWidget(pos_rotor3_widget, 5, 1)
        settings_layout.addWidget(ring_rotor3_widget, 5, 2)

        # create text fields
        textfields_widget = QWidget()
        textfields_widget.setFixedSize(300, 470)
        textfields_layout = QVBoxLayout(textfields_widget)
        plain_text_label = QLabel("Plain Text")
        plain_text_label.setStyleSheet(s.label)
        self.plain_textfield = QTextEdit()
        self.plain_textfield.setStyleSheet(s.textfield)
        self.plain_textfield.setFixedSize(250, 150)
        self.plain_textfield.setReadOnly(True)

        self.edit_textfield1 = QPushButton("Edit")
        self.edit_textfield1.setFixedSize(75, 25)
        self.edit_textfield1.setStyleSheet(s.button)
        self.edit_textfield1.clicked.connect(self.toggle_button_text1)

        self.clear_textfield1 = QPushButton("Clear")
        self.clear_textfield1.setFixedSize(75, 25)
        self.clear_textfield1.setStyleSheet(s.button)
        self.clear_textfield1.clicked.connect(self.handle_clear_textfield)
        
        edit_clear_layout1 = QHBoxLayout()
        edit_clear_layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        edit_clear_layout1.addWidget(self.edit_textfield1)
        edit_clear_layout1.addWidget(self.clear_textfield1)

        cipher_text_label = QLabel("Cipher Text")
        cipher_text_label.setStyleSheet(s.label)
        self.cipher_textfield = QTextEdit()
        self.cipher_textfield.setStyleSheet(s.textfield)
        self.cipher_textfield.setFixedSize(250, 150)
        self.cipher_textfield.setReadOnly(True)

        self.edit_textfield2 = QPushButton("Edit")
        self.edit_textfield2.setFixedSize(75, 25)
        self.edit_textfield2.setStyleSheet(s.button)
        self.edit_textfield2.clicked.connect(self.toggle_button_text2)

        self.clear_textfield2 = QPushButton("Clear")
        self.clear_textfield2.setFixedSize(75, 25)
        self.clear_textfield2.setStyleSheet(s.button)
        self.clear_textfield2.clicked.connect(self.handle_clear_textfield)
        
        edit_clear_layout2 = QHBoxLayout()
        edit_clear_layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        edit_clear_layout2.addWidget(self.edit_textfield2)
        edit_clear_layout2.addWidget(self.clear_textfield2)

        textfields_layout.addWidget(plain_text_label)
        textfields_layout.addWidget(self.plain_textfield)
        textfields_layout.addLayout(edit_clear_layout1)
        textfields_layout.addWidget(cipher_text_label)
        textfields_layout.addWidget(self.cipher_textfield)
        textfields_layout.addLayout(edit_clear_layout2)

        # Create step by step widget
        step_scroll_area = QScrollArea()
        step_by_step_widget = QWidget()
        step_by_step_widget.setStyleSheet(s.step_by_step_widget)
        self.step_text = QLabel()
        self.step_text.setStyleSheet(s.label)
        self.step_text.setWordWrap(True)

        # Create layout for step_by_step_widget
        step_layout = QVBoxLayout(step_by_step_widget)
        step_layout.addWidget(self.step_text)
        step_layout.addStretch(1)

        step_scroll_area.setWidgetResizable(True)
        step_scroll_area.setWidget(step_by_step_widget)
        scroll_bar = step_scroll_area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))

        # Add widgets to main layout
        main_layout.addWidget(lampboard_widget, 0, 0)
        main_layout.addWidget(settings_widget, 0, 1)
        main_layout.addWidget(self.keyboard_widget, 1, 0)
        main_layout.addWidget(plugboard_widget, 2, 0)
        main_layout.addWidget(step_scroll_area, 0, 2, 3, 1)
        main_layout.addWidget(textfields_widget, 1, 1, 2, 1)

    
    def keyPressEvent(self, event):
        '''handle key press event'''
        key = event.key()
        key_map = {
            Qt.Key_A: 'A', Qt.Key_B: 'B', Qt.Key_C: 'C', Qt.Key_D: 'D',
            Qt.Key_E: 'E', Qt.Key_F: 'F', Qt.Key_G: 'G', Qt.Key_H: 'H',
            Qt.Key_I: 'I', Qt.Key_J: 'J', Qt.Key_K: 'K', Qt.Key_L: 'L',
            Qt.Key_M: 'M', Qt.Key_N: 'N', Qt.Key_O: 'O', Qt.Key_P: 'P',
            Qt.Key_Q: 'Q', Qt.Key_R: 'R', Qt.Key_S: 'S', Qt.Key_T: 'T',
            Qt.Key_U: 'U', Qt.Key_V: 'V', Qt.Key_W: 'W', Qt.Key_X: 'X',
            Qt.Key_Y: 'Y', Qt.Key_Z: 'Z'
        }
        if key in key_map:
            character = key_map[key]
            for button in self.keyboard_buttons:
                if button.text() == character:
                    button.setStyleSheet(s.keyboard_button_pressed)
                    reset_style = partial(self.reset_button_style, button, s.keyboard_button)
                    QTimer.singleShot(500, reset_style)
                    break
            self.handle_keyboard_click(character)
        
        elif (key == Qt.Key_Backspace or key == Qt.Key_Delete):
            if len(self.plain_textfield.toPlainText()) > 0 and len(self.cipher_textfield.toPlainText()) > 0:
                deleted_text_plain = self.plain_textfield.toPlainText()[:-1]
                deleted_text_cipher = self.cipher_textfield.toPlainText()[:-1]
                self.plain_textfield.setText(deleted_text_plain)
                self.cipher_textfield.setText(deleted_text_cipher)
                self.step_text.setText(self.step_text.text()[:-133])
                self.handle_stepdown_pos_click(0)

    def create_board_buttons(self, layout, click_handler, button_list, style, islampboard=False):
        '''create buttons for board'''
        keys = "QWERTZUIOASDFGHJKPYXCVBNML"
        row = 0
        col = 0
        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for key in keys:
            button = QPushButton(key)
            button.setStyleSheet(style)
            button.setFixedSize(50, 50)
            hlayout.addWidget(button)
            if not islampboard: button.clicked.connect(lambda checked, key=key: click_handler(key))
            button_list.append(button)
            col += 1
            if col > 7 and row == 1:
                layout.addLayout(hlayout)
                hlayout = QHBoxLayout()
                hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                col = 0
                row += 1
            elif col > 8:
                layout.addLayout(hlayout)
                hlayout = QHBoxLayout()
                hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                col = 0
                row += 1
    
    def handle_keyboard_click(self, key):
        '''handle keyboard click'''
        self.plain_textfield.setText(self.plain_textfield.toPlainText() + key)
        cipher_key = self.enigma.enchiper(key)
        self.cipher_textfield.setText(self.cipher_textfield.toPlainText() + cipher_key)
        
        for button in self.lampboard_buttons:
            if button.text() == cipher_key:
                button.setStyleSheet(s.lampboard_on)
                button.setFixedSize(50, 50)
                reset_style = partial(self.reset_button_style, button, s.lampboard_button)
                QTimer.singleShot(500, reset_style)
        
        self.rotor_state[0], self.rotor_state[1], self.rotor_state[2] = self.enigma.get_state()
        self.position_rotor1.setText(self.rotor_state[0])
        self.position_rotor2.setText(self.rotor_state[1])
        self.position_rotor3.setText(self.rotor_state[2])

        prev_text = self.step_text.text()
        self.step_text.setText(prev_text + self.enigma.step_by_step)

    def reset_button_style(self, button, style):
        '''reset button style'''
        button.setStyleSheet(style)

    def handle_plugboard_click(self, key):
        '''handle plugboard button click'''
        this_key_deleted = False
        if self.delete_plug(key):
            idx = self.plugs.find(key)
            if idx + 1 < len(self.plugs) and self.plugs[idx + 1] != " ":
                tmp_plugs = self.plugs.replace(self.plugs[idx + 1], "")
                self.delete_plug(self.plugs[idx + 1])
                self.plugs = tmp_plugs.replace(key, "")
                this_key_deleted = True
            if idx - 1 >= 0 and self.plugs[idx - 1] != " ":
                tmp_plugs = self.plugs.replace(self.plugs[idx - 1], "")
                self.delete_plug(self.plugs[idx - 1])
                self.plugs = tmp_plugs.replace(key, "")
                this_key_deleted = True
            if(not this_key_deleted): self.plugs = self.plugs.replace(key, "")
        else:
            self.add_plug(key)
        if len(self.plugs) > 0 and self.plugs[0] == " ":
            self.plugs = self.plugs[1:]
        self.plugs = self.plugs.replace("  ", " ")
        plugs_string = self.plugs.replace(" ", "")
        if len(plugs_string) % 2 == 0:
            plugboard_settings = [(elem[0], elem[1]) for elem in self.plugs.split()]
            self.enigma.plugboard_settings = plugboard_settings

    def delete_plug(self, key):
        for plugkey in self.plugboard_buttons:
            if(plugkey.text() == key):
                if(self.plug_keys[plugkey]["is_active"]):
                    self.plug_keys[plugkey]["is_active"] = False
                    plugkey.setStyleSheet(s.plugboard_button)
                    self.selected_plug_color.remove(self.plug_keys[plugkey]["color"])
                    return True
        return False
    
    def add_plug(self, key):
        for plugkey in self.plugboard_buttons:
            if(plugkey.text() == key):
                if(not self.plug_keys[plugkey]["is_active"]):
                    self.plug_keys[plugkey]["is_active"] = True
                    if(len(self.plugs) == 0):
                        self.plugs += key
                    elif(self.plugs[len(self.plugs) - 1] != " "):
                        self.plugs += key + " "
                    else:
                        self.plugs += key
                    available_plug_color = [x for x in s.plug_color if self.selected_plug_color.count(x) < 2]
                    available_plug_color.sort(key=lambda x: self.selected_plug_color.count(x), reverse=True)
                    self.selected_plug_color.append(available_plug_color[0])
                    self.plug_keys[plugkey]["color"] = available_plug_color[0]
                    selected_plug_image = "asset/{}.png".format(available_plug_color[0])
                    plugkey.setStyleSheet("QPushButton {background-image: url(" + selected_plug_image + ");"
                                          + "border-radius: 20px; background-position: center;"
                                          + "background-origin: content; font-family: 'Courier New';" 
                                          + "font-size: 14px; color: white;}")
   
    def toggle_button_text1(self):
        '''toggle button edit plain text'''
        current_text = self.edit_textfield1.text()
        if current_text == "Edit":
            self.edit_textfield1.setText("Encrypt")
            self.plain_textfield.setReadOnly(False)
            self.cipher_textfield.setReadOnly(True)
            self.edit_textfield2.setEnabled(False)
            self.keyboard_widget.setEnabled(False)
        else:
            self.edit_textfield1.setText("Edit")
            self.plain_textfield.setReadOnly(True)
            self.edit_textfield2.setEnabled(True)
            self.keyboard_widget.setEnabled(True)
            input = self.plain_textfield.toPlainText()
            output = ""
            self.step_text.clear()
            for char in input:
                output += self.enigma.enchiper(char)
                self.cipher_textfield.setText(output)
                prev_text = self.step_text.text()
                self.step_text.setText(prev_text + self.enigma.step_by_step)
                self.rotor_state[0], self.rotor_state[1], self.rotor_state[2] = self.enigma.get_state()
                self.position_rotor1.setText(self.rotor_state[0])
                self.position_rotor2.setText(self.rotor_state[1])
                self.position_rotor3.setText(self.rotor_state[2])

    def toggle_button_text2(self):
        '''toggle button edit cipher text'''
        current_text = self.edit_textfield2.text()
        if current_text == "Edit":
            self.edit_textfield2.setText("Decrypt")
            self.cipher_textfield.setReadOnly(False)
            self.plain_textfield.setReadOnly(True)
            self.edit_textfield1.setEnabled(False)
            self.keyboard_widget.setEnabled(False)
        else:
            self.edit_textfield2.setText("Edit")
            self.cipher_textfield.setReadOnly(True)
            self.edit_textfield1.setEnabled(True)
            self.keyboard_widget.setEnabled(True)
            input = self.cipher_textfield.toPlainText()
            output = ""
            self.step_text.clear()
            for char in input:
                output += self.enigma.enchiper(char)
                self.plain_textfield.setText(output)
                prev_text = self.step_text.text()
                self.step_text.setText(prev_text + self.enigma.step_by_step)
                self.rotor_state[0], self.rotor_state[1], self.rotor_state[2] = self.enigma.get_state()
                self.position_rotor1.setText(self.rotor_state[0])
                self.position_rotor2.setText(self.rotor_state[1])
                self.position_rotor3.setText(self.rotor_state[2])
    
    def handle_rotor_change(self, index, rotor_index):
        '''handle rotor change'''
        self.rotors[rotor_index].wiring = self.rotor_wiring[index]
        self.rotors[rotor_index].notch = self.rotor_notch[index]

    def handle_stepup_pos_click(self, rotor_index):
        '''handle stepup position click'''
        self.rotor_state[rotor_index] = chr((ord(self.rotor_state[rotor_index]) + 1 - ord('A')) % 26 + ord('A'))
        if rotor_index == 0:
            self.position_rotor1.setText(self.rotor_state[0])
            self.enigma.rotor1.state = self.rotor_state[0]
        elif rotor_index == 1:
            self.position_rotor2.setText(self.rotor_state[1])
            self.enigma.rotor2.state = self.rotor_state[1]
        elif rotor_index == 2:
            self.position_rotor3.setText(self.rotor_state[2])
            self.enigma.rotor3.state = self.rotor_state[2]

    def handle_stepdown_pos_click(self, rotor_index):
        '''handle stepdown position click'''
        self.rotor_state[rotor_index] = chr((ord(self.rotor_state[rotor_index]) - 1 - ord('A')) % 26 + ord('A'))
        if rotor_index == 0:
            self.position_rotor1.setText(self.rotor_state[0])
            self.enigma.rotor1.state = self.rotor_state[0]
        elif rotor_index == 1:
            self.position_rotor2.setText(self.rotor_state[1])
            self.enigma.rotor2.state = self.rotor_state[1]
        elif rotor_index == 2:
            self.position_rotor3.setText(self.rotor_state[2])
            self.enigma.rotor3.state = self.rotor_state[2]

    def handle_stepup_ring_click(self, rotor_index):
        '''handle stepup ring click'''
        self.rotor_ring[rotor_index] = chr((ord(self.rotor_ring[rotor_index]) + 1 - ord('A')) % 26 + ord('A'))
        if rotor_index == 0:
            self.ring_rotor1.setText(self.rotor_ring[0])
            self.enigma.rotor1.ring = self.rotor_ring[0]
        elif rotor_index == 1:
            self.ring_rotor2.setText(self.rotor_ring[1])
            self.enigma.rotor2.ring = self.rotor_ring[1]
        elif rotor_index == 2:
            self.ring_rotor3.setText(self.rotor_ring[2])
            self.enigma.rotor3.ring = self.rotor_ring[2]

    def handle_stepdown_ring_click(self, rotor_index):
        '''handle stepdown ring click'''
        self.rotor_ring[rotor_index] = chr((ord(self.rotor_ring[rotor_index]) - 1 - ord('A')) % 26 + ord('A'))
        if rotor_index == 0:
            self.ring_rotor1.setText(self.rotor_ring[0])
            self.enigma.rotor1.ring = self.rotor_ring[0]
        elif rotor_index == 1:
            self.ring_rotor2.setText(self.rotor_ring[1])
            self.enigma.rotor2.ring = self.rotor_ring[1]
        elif rotor_index == 2:
            self.ring_rotor3.setText(self.rotor_ring[2])
            self.enigma.rotor3.ring = self.rotor_ring[2]
    
    def handle_clear_textfield(self):
        '''handle clear textfield1'''
        self.plain_textfield.clear()
        self.step_text.clear()
        self.cipher_textfield.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("asset/icon.png"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())