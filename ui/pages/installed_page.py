import os
import shutil
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QMessageBox, QFrame
)
from PySide6.QtCore import Qt

from ui.common.maps import PATH_MAP
from ui.components.universal_card import UniversalCard
from ui.layouts.mod_dialog import ModDetailsDialog

class InstalledPage(QWidget):
    def __init__(self):
        super().__init__()
        self.game_path = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Installed Files")
        title.setObjectName("Title")
        layout.addWidget(title)

        refresh_btn = QPushButton("Refresh List")
        refresh_btn.setFixedWidth(120)
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.viewport().setAutoFillBackground(False)

        self.content = QWidget()
        self.content.setObjectName("ScrollContent")
        self.content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.layout_content = QVBoxLayout(self.content)
        self.layout_content.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_content.setSpacing(12)

        scroll.setWidget(self.content)
        layout.addWidget(scroll)

    def set_game_path(self, path):
        self.game_path = os.path.normpath(path) if path else ""
        self.refresh()

    def refresh(self):
        self.clear_list()
        if not self.game_path or not os.path.exists(self.game_path):
            self.layout_content.addWidget(QLabel("Please set game folder."))
            return

        found_any = False

        for class_id, subfolder in PATH_MAP.items():
            folder_path = os.path.normpath(os.path.join(self.game_path, subfolder))
            if not os.path.exists(folder_path):
                continue

            try:
                items = os.listdir(folder_path)
                if not items:
                    continue

                found_any = True
                cat_label = QLabel(subfolder.upper())
                cat_label.setProperty("header", "true")
                self.layout_content.addWidget(cat_label)

                for name in items:
                    full_path = os.path.join(folder_path, name)
                    rel_path = os.path.join(subfolder, name)

                    is_dir = os.path.isdir(full_path)
                    is_file = name.endswith(('.jar', '.zip'))

                    if not (is_dir or is_file):
                        continue

                    created = datetime.fromtimestamp(os.path.getctime(full_path)).strftime('%Y-%m-%d')

                    if is_dir:
                        size_mb = self.get_dir_size(full_path)
                        icon = "🌍" if "Saves" in subfolder else "📂"
                    else:
                        size_mb = os.path.getsize(full_path) / (1024 * 1024)
                        icon = "📦"

                    fake_data = {
                        'name': name,
                        'authors': [{'name': 'Local File'}],
                        'summary': f"Location: {rel_path}",
                        'classId': class_id
                    }

                    card = UniversalCard(
                        title=name,
                        subtitle=f"{size_mb:.2f} MB  •  {created}",
                        is_installed=True,
                        delete_callback=lambda p=rel_path: self.delete_file(p),
                        click_callback=lambda d=fake_data, p=rel_path: ModDetailsDialog(
                            d, is_installed=True, remove_callback=lambda: self.delete_file(p), parent=self
                        ).exec(),
                        icon_char=icon
                    )
                    self.layout_content.addWidget(card)
            except Exception as e:
                print(f"Error scanning {subfolder}: {e}")

        if not found_any:
            self.layout_content.addWidget(QLabel("No installed content found."))

    def get_dir_size(self, path):
        """Calculates total MB of a folder by summing its files."""
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total += os.path.getsize(fp)
        except:
            return 0
        return total / (1024 * 1024)

    def delete_file(self, relative_path):
        full_path = os.path.normpath(os.path.join(self.game_path, relative_path))
        filename = os.path.basename(relative_path)

        if QMessageBox.question(None, "Uninstall", f"Permanently delete {filename}?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            try:
                if os.path.exists(full_path):
                    if os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                    else:
                        os.remove(full_path)
                self.refresh()
                return True
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to delete: {str(e)}")
                return False
        return False

    def clear_list(self):
        while self.layout_content.count():
            child = self.layout_content.takeAt(0)
            if child.widget(): child.widget().deleteLater()