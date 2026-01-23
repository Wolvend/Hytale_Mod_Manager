from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QComboBox
from PySide6.QtCore import Qt


class Sidebar(QFrame):
    def __init__(self, parent=None, on_navigate=None, on_set_folder=None, on_theme_change=None, on_set_api_key=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.on_navigate = on_navigate

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 30, 10, 20)
        layout.setSpacing(10)

        title = QLabel("HYTALE MOD MANAGER")
        f = title.font()
        f.setBold(True)
        f.setPointSize(10)
        title.setFont(f)
        layout.addWidget(title)

        attribution = QLabel("Client for CurseForge API")
        attribution.setEnabled(False)
        layout.addWidget(attribution)

        layout.addSpacing(10)

        lbl_browse = QLabel("BROWSE")
        lbl_browse.setProperty("header", "true")
        layout.addWidget(lbl_browse)

        self.nav_btns = []
        self.nav_btns.append(self.create_btn("Search Mods", "📦", 0, "mods"))
        self.nav_btns.append(self.create_btn("Search Worlds", "🌍", 0, "worlds"))
        self.nav_btns.append(self.create_btn("Search Prefabs", "🏗️", 0, "prefabs"))
        self.nav_btns.append(self.create_btn("Search Bootstrap", "⚡", 0, "bootstrap"))
        self.nav_btns.append(self.create_btn("Search Translations", "🌐", 0, "translations"))

        layout.addSpacing(20)

        lbl_lib = QLabel("LIBRARY")
        lbl_lib.setProperty("header", "true")
        layout.addWidget(lbl_lib)

        self.btn_installed = self.create_btn("Installed", "📂", 1, None)

        if self.nav_btns:
            self.nav_btns[0].setChecked(True)

        layout.addStretch()

        layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        from PySide6.QtWidgets import QStyledItemDelegate
        self.theme_combo.setItemDelegate(QStyledItemDelegate())

        if on_theme_change:
            self.theme_combo.currentTextChanged.connect(on_theme_change)
        layout.addWidget(self.theme_combo)
        layout.addSpacing(15)

        self.folder_btn = QPushButton("⚙ Game Folder")
        self.folder_btn.setObjectName("FolderBtn")
        self.folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if on_set_folder:
            self.folder_btn.clicked.connect(on_set_folder)
        layout.addWidget(self.folder_btn)

        self.api_key_btn = QPushButton("🔑 Set API Key")
        self.api_key_btn.setObjectName("ApiKeyBtn")
        self.api_key_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if on_set_api_key:
            self.api_key_btn.clicked.connect(on_set_api_key)
        layout.addWidget(self.api_key_btn)

        self.folder_status = QLabel("Path: Not Set")
        self.folder_status.setEnabled(False)
        self.folder_status.setWordWrap(True)
        layout.addWidget(self.folder_status)

    def create_btn(self, text, icon, index, category):
        btn = QPushButton(f"{icon}  {text}")
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        btn.clicked.connect(lambda _: self.handle_click(index, category, btn))

        self.layout().addWidget(btn)
        return btn

    def handle_click(self, index, category, btn):
        for b in self.findChildren(QPushButton):
            if b.objectName() != "FolderBtn":
                b.setChecked(False)

        btn.setChecked(True)

        if self.on_navigate:
            self.on_navigate(index, category)

    def set_path_status(self, path):
        if not path:
            self.folder_status.setText("Path: Not Set")
            return
        display = path if len(path) < 30 else "..." + path[-25:]
        self.folder_status.setText(f"{display}")