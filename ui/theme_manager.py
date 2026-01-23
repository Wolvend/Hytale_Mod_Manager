from PySide6.QtWidgets import QApplication

SHARED_CSS = """
QComboBox { border-radius: 6px; padding: 5px 12px; min-width: 6em; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    border: 1px solid #323238;
    selection-background-color: #323238;
    outline: none;
}

QScrollArea { background-color: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }

QScrollBar:vertical { border: none; width: 8px; margin: 0px; }
QScrollBar::handle:vertical { border-radius: 4px; min-height: 20px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }

QPushButton { border-radius: 6px; padding: 8px 16px; font-weight: 600; }
QLineEdit, QSpinBox { border-radius: 6px; padding: 8px; }


"""

DARK_STYLESHEET = SHARED_CSS + """
QMainWindow, QDialog, QWidget#CentralWidget, QWidget#ScrollContent {
    background-color: #121214;
    color: #E1E1E6;
}

QFrame#Sidebar { background-color: #1a1a1e; border-right: 1px solid #29292e; }
QFrame#Sidebar QLabel { color: #E1E1E6; }
QFrame#Sidebar QLabel[header="true"] { color: #7C7C8A; font-size: 11px; text-transform: uppercase; }
QFrame#Sidebar QPushButton#FolderBtn {
    background-color: #00875F;
    color: #FFFFFF;
    border: 1px solid #00B37E;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
    text-align: center;
}

QFrame#Sidebar QPushButton#FolderBtn:hover {
    background-color: #00B37E;
}

QFrame#Sidebar QPushButton#FolderBtn:pressed {
    background-color: #005F43;
}

QFrame#Sidebar QPushButton#ApiKeyBtn {
    background-color: #29292E;
    color: #E1E1E6;
    border: 1px solid #323238;
    border-radius: 8px;
    margin-top: 5px;
    padding: 10px;
    text-align: center;
}

QFrame#Sidebar QPushButton#ApiKeyBtn:hover {
    background-color: #323238;
}

QFrame#Sidebar QPushButton#ApiKeyBtn:pressed {
    background-color: #202024;
}

QWidget#UniversalCardSurface {
    background-color: #1a1a1e;
    border: 1px solid #29292e;
    border-radius: 10px;
}
QWidget#UniversalCardSurface:hover { border-color: #00875F; background-color: #202024; }

QLabel#Title { font-size: 26px; font-weight: 800; color: #FFFFFF; }
QLabel#CardTitle { font-size: 15px; font-weight: 600; color: #E1E1E6; }
QLabel#CardSubtitle, QLabel#DimLabel { color: #8D8D99; font-size: 13px; }

QPushButton { background-color: #29292E; color: #E1E1E6; border: 1px solid #323238; }
QPushButton#ActionBtn { background-color: #00875F; color: white; border: none; }
QPushButton#ActionBtn:hover { background-color: #00B37E; }

QComboBox, QLineEdit, QSpinBox { background-color: #121214; border: 1px solid #323238; color: #E1E1E6; }
QScrollBar:vertical { background: #121214; }
QScrollBar::handle:vertical { background: #323238; }

QComboBox QAbstractItemView {
    background-color: #1a1a1e;
    color: #E1E1E6;
    border: 1px solid #323238;
    selection-background-color: #29292E;
    selection-color: #00B37E; 
    outline: none;
}

QComboBox QAbstractItemView QScrollBar:vertical {
    background-color: #121214;
    width: 6px;
}

QComboBox QAbstractItemView QScrollBar::handle:vertical {
    background-color: #323238;
    border-radius: 3px;
}

QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
    background-color: #4D4D57;
}

QComboBox {
    combobox-popup: 0; 
}

QPushButton#DeleteBtn {
    background-color: transparent;
    color: #FF6B6B;
    border: 1px solid #FF6B6B;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton#DeleteBtn:hover {
    background-color: rgba(255, 107, 107, 0.1);
    border-color: #FF8E8E;
}

QPushButton#DeleteBtn:pressed {
    background-color: rgba(255, 107, 107, 0.2);
}


QInputDialog, QDialog {
    background-color: #1a1a1e;
    color: #E1E1E6;
}

QInputDialog QLabel {
    color: #E1E1E6;
    font-size: 14px;
}

QInputDialog QLineEdit {
    background-color: #121214;
    color: #FFFFFF;
    border: 1px solid #323238;
    border-radius: 6px;
    padding: 8px;
}

QInputDialog QLineEdit:focus {
    border: 1px solid #00875F; 
}

QInputDialog QPushButton {
    background-color: #29292E;
    color: #E1E1E6;
    border: 1px solid #323238;
    padding: 8px 16px;
    border-radius: 6px;
}

QInputDialog QPushButton:hover {
    background-color: #323238;
}

QInputDialog QPushButton[text="OK"], QInputDialog QPushButton[text="&OK"] {
    background-color: #00875F;
    color: white;
    border: none;
}

"""

LIGHT_STYLESHEET = SHARED_CSS + """
QMainWindow, QDialog, QWidget#CentralWidget, QWidget#ScrollContent {
    background-color: #F0F2F5;
    color: #1C1E21;
}

QFrame#Sidebar { background-color: #FFFFFF; border-right: 1px solid #CCD0D5; }
QFrame#Sidebar QLabel { color: #1C1E21; }
QFrame#Sidebar QLabel[header="true"] { color: #65676B; font-size: 11px; text-transform: uppercase; }

QFrame#Sidebar QPushButton#FolderBtn {
    background-color: #1877F2;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
    text-align: center;
}

QFrame#Sidebar QPushButton#FolderBtn:hover {
    background-color: #166FE5;
}

QFrame#Sidebar QPushButton#FolderBtn:pressed {
    background-color: #145DBF;
}

QFrame#Sidebar QPushButton#ApiKeyBtn {
    background-color: #E4E6EB;
    color: #050505;
    border: none;
    border-radius: 8px;
    margin-top: 5px;
    padding: 10px;
    text-align: center;
}

QFrame#Sidebar QPushButton#ApiKeyBtn:hover {
    background-color: #D8DADE;
}

QFrame#Sidebar QPushButton#ApiKeyBtn:pressed {
    background-color: #BEC3C9;
}

QWidget#UniversalCardSurface {
    background-color: #FFFFFF;
    border: 1px solid #DCDFE4;
    border-radius: 10px;
}
QWidget#UniversalCardSurface:hover { border-color: #1877F2; background-color: #F9FAFB; }

QLabel#Title { font-size: 26px; font-weight: 800; color: #1C1E21; }
QLabel#CardTitle { font-size: 15px; font-weight: 600; color: #1C1E21; }
QLabel#CardSubtitle, QLabel#DimLabel { color: #606770; font-size: 13px; }

QPushButton { background-color: #E4E6EB; color: #050505; border: none; }
QPushButton#ActionBtn { background-color: #1877F2; color: white; }
QPushButton#ActionBtn:hover { background-color: #166FE5; }

QComboBox, QLineEdit, QSpinBox { background-color: #FFFFFF; border: 1px solid #CCD0D5; color: #1C1E21; }
QScrollBar:vertical { background: #F0F2F5; }
QScrollBar::handle:vertical { background: #CCD0D5; }

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #1C1E21;
    border: 1px solid #CCD0D5;
    selection-background-color: #E7F3FF;
    selection-color: #1877F2;
    outline: none;
}

QComboBox QAbstractItemView QScrollBar:vertical {
    background-color: #F0F2F5;
    width: 6px;
}

QComboBox QAbstractItemView QScrollBar::handle:vertical {
    background-color: #CCD0D5;
    border-radius: 3px;
}

QComboBox {
    combobox-popup: 0; 
}

QPushButton#DeleteBtn {
    background-color: #FFFFFF;
    color: #D93025;
    border: 1px solid #D93025;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton#DeleteBtn:hover {
    background-color: #FEEBE9;
    border-color: #B21F16;
}

QPushButton#DeleteBtn:pressed {
    background-color: #FAD2CF;
}

QLabel#SuccessLabel {
    color: #1A7F37;
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 0.5px;
}

QPushButton#FolderBtn {
    background-color: #1877F2 !important; 
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
}

QPushButton#FolderBtn:hover {
    background-color: #166FE5 !important;
}

QPushButton#FolderBtn:pressed {
    background-color: #145DBF;
}

QInputDialog, QDialog {
    background-color: #FFFFFF;
    color: #1C1E21;
}

QInputDialog QLabel {
    color: #1C1E21;
}

QInputDialog QLineEdit {
    background-color: #F0F2F5;
    color: #1C1E21;
    border: 1px solid #CCD0D5;
    border-radius: 6px;
    padding: 8px;
}

QInputDialog QLineEdit:focus {
    border: 1px solid #1877F2;
}

QInputDialog QPushButton {
    background-color: #E4E6EB;
    color: #050505;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
}

QInputDialog QPushButton:hover {
    background-color: #D8DADF;
}

QInputDialog QPushButton[text="OK"], QInputDialog QPushButton[text="&OK"] {
    background-color: #1877F2;
    color: white;
}
"""

class ThemeManager:
    @staticmethod
    def apply_theme(theme_name):
        app = QApplication.instance()
        if not app: return

        if theme_name == "Dark":
            app.setStyleSheet(DARK_STYLESHEET)
        else:
            app.setStyleSheet(LIGHT_STYLESHEET)