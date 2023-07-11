
main_window = """QMainWindow{
    background-color: #24272C;
    font-family: 'Courier New'; 
    font-size: 14px; 
    color: white;
}"""

keyboard_widget = """QWidget{
    background-color: #24272C;
    text-align: center;
}"""

lampboard_widget = """QWidget{
    background-color: #24272C;
}"""

plugboard_widget = """QWidget{
    background-color: #24272C;
}"""

keyboard_button = """QPushButton{
    background-image: url(asset/key.png);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    border-radius: 20px;
    font-size: 14px;
    font-family: "Courier New";
}
QPushButton:hover{
    background-image: url(asset/key_pressed.png);
}"""

keyboard_button_pressed = """QPushButton{
    background-image: url(asset/key_pressed.png);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    border-radius: 20px;
    font-size: 14px;
    font-family: "Courier New";
}"""

lampboard_button = """QPushButton{
    background-image: url(asset/key.png);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    border-radius: 20px;
    font-size: 14px;
    font-family: "Courier New";
    color: #FFFFFF;
}"""

lampboard_on = """QPushButton{
    background-image: url(asset/key_light_up.png);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    border-radius: 20px;
    font-size: 14px;
    font-family: "Courier New";
    color: #D69458;
}"""

plugboard_button = """QPushButton{
    background-image: url(asset/key_plug.png);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    border-radius: 20px;
    font-size: 14px;
    font-family: "Courier New";
}
QPushButton:hover{
    background-image: url(asset/plug_hover.png);
}"""

label = """QLabel{
    font-size: 14px;
    font-family: "Courier New";
}"""

textfield = """QTextEdit{
    background-image: url(asset/textfield_container.png);
    border-radius: 8px;
    padding: 5px;
    font-family: "Courier New";
}"""

button = """QPushButton{
    background-color: #1E2023;
    border-radius: 8px;
    font-family: "Courier New";
}
QPushButton:hover{
    background-color: #393A44;
}"""

step_by_step_widget = """QWidget{
    background-color: #1E2023;
}"""

settings_widget = """QWidget{
    background-image: url(asset/settings_container.png);
    border-radius: 8px;
    padding: 5px;
}
"""

combobox = """QComboBox{
    background-color: #1E2023;
    font-family: "Courier New";
    font-size: 14px;
}"""

step_button = """QPushbutton{
    background-color: #24272C;
    font-family: "Courier New";
    font-size: 14px;
    border: none;
}
QPushButton:pressed{
    color: #7B7A7A;
}
QPushButton:hover{
    color: #7B7A7A;
}
"""

step_widget = """QWidget{
    padding: 0px;
    background-color: #24272C;
    font-family: "Courier New";
}"""

line = """QLabel{
    background-image: url(asset/line.png);
}
"""

plug_color = ["plug1", "plug2", "plug3", "plug4", "plug5",
              "plug6", "plug7", "plug8", "plug9", "plug10",
              "plug11", "plug12", "plug13"]