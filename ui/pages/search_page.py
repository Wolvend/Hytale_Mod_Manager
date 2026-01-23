import os
import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QMessageBox, QComboBox, QFrame, QSpinBox
)
from PySide6.QtCore import Qt
from ui.workers import SearchWorker, DownloadWorker
from ui.common.maps import PATH_MAP
from ui.components.universal_card import UniversalCard
from ui.layouts.mod_dialog import ModDetailsDialog


class SearchPage(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.game_path = ""
        self.category = "mods"

        self.current_index = 0
        self.page_size = 20
        self.total_results = 0
        self.is_loading = False

        self.setup_ui()

    def update_client(self, client):
        self.client = client
        if self.input.text():
            self.reset_and_search()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title_box = QVBoxLayout()

        self.lbl_title = QLabel("Search Mods")
        self.lbl_title.setObjectName("Title")

        lbl_sub = QLabel("Discover new content for Hytale")
        lbl_sub.setObjectName("DimLabel")

        title_box.addWidget(self.lbl_title)
        title_box.addWidget(lbl_sub)
        header.addLayout(title_box)
        header.addStretch()
        layout.addLayout(header)

        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Search by name...")
        self.input.setMinimumWidth(300)
        self.input.setFixedHeight(40)
        self.input.returnPressed.connect(self.reset_and_search)

        self.sort_combo = QComboBox()
        self.sort_combo.setFixedHeight(40)
        self.sort_combo.setFixedWidth(150)
        self.sort_combo.addItems([
            "🔥 Popularity", "📅 Last Updated",
            "✨ Featured", "⬇ Downloads", "🔤 Name"
        ])
        self.sort_map = {0: 2, 1: 3, 2: 1, 3: 6, 4: 4}

        btn = QPushButton("Search")
        btn.setFixedSize(100, 40)
        btn.setObjectName("ActionBtn")
        btn.clicked.connect(self.reset_and_search)

        search_row.addWidget(self.input)
        search_row.addWidget(self.sort_combo)
        search_row.addWidget(btn)
        layout.addLayout(search_row)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll.viewport().setAutoFillBackground(False)

        self.content = QWidget()
        self.content.setObjectName("ScrollContent")

        self.content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.layout_content = QVBoxLayout(self.content)
        self.scroll.setWidget(self.content)

        layout.addWidget(self.scroll)

        self.setup_pagination(layout)

    def set_category(self, category):
        self.category = category

        display_name = category.capitalize()
        self.lbl_title.setText(f"Search {display_name}")
        self.input.setPlaceholderText(f"Search {category} by name...")

        self.reset_and_search()

    def setup_pagination(self, parent_layout):
        pag_frame = QFrame()
        pag_frame.setObjectName("PaginationFrame")

        pag_layout = QHBoxLayout(pag_frame)
        pag_layout.setContentsMargins(10, 5, 10, 5)

        self.btn_prev = QPushButton("◀")
        self.btn_prev.setFixedSize(40, 30)
        self.btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_prev.clicked.connect(self.prev_page)

        self.page_input = QSpinBox()
        self.page_input.setFixedSize(70, 30)
        self.page_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_input.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.page_input.setRange(1, 1)
        self.page_input.editingFinished.connect(self.jump_to_page)

        self.lbl_total = QLabel("of 1")
        self.lbl_total.setStyleSheet("font-weight: bold; margin-left: 5px;")

        self.btn_next = QPushButton("▶")
        self.btn_next.setFixedSize(40, 30)
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_next.clicked.connect(self.next_page)

        pag_layout.addStretch()
        pag_layout.addWidget(self.btn_prev)
        pag_layout.addWidget(QLabel("Page"))
        pag_layout.addWidget(self.page_input)
        pag_layout.addWidget(self.lbl_total)
        pag_layout.addWidget(self.btn_next)
        pag_layout.addStretch()

        parent_layout.addWidget(pag_frame)

    def reset_and_search(self):
        self.current_index = 0
        self.execute_search()

    def next_page(self):
        if self.current_index + self.page_size < self.total_results:
            self.current_index += self.page_size
            self.execute_search()

    def prev_page(self):
        if self.current_index >= self.page_size:
            self.current_index -= self.page_size
            self.execute_search()

    def jump_to_page(self):
        if self.is_loading: return

        target_page = self.page_input.value()
        new_index = (target_page - 1) * self.page_size

        if new_index != self.current_index:
            self.current_index = new_index
            self.execute_search()

    def execute_search(self):
        self.is_loading = True
        self.clear_list()
        self.layout_content.addWidget(QLabel("Loading..."))

        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(False)
        self.page_input.setEnabled(False)

        current_page = (self.current_index // self.page_size) + 1
        self.page_input.blockSignals(True)
        self.page_input.setValue(current_page)
        self.page_input.blockSignals(False)

        sort_id = self.sort_map.get(self.sort_combo.currentIndex(), 2)

        self.worker = SearchWorker(
            self.client,
            self.input.text(),
            category=self.category,
            sort_field=sort_id,
            index=self.current_index
        )
        self.worker.finished.connect(self.display_results)
        self.worker.start()

    def display_results(self, mods, total_count):
        self.clear_list()
        self.is_loading = False
        self.page_input.setEnabled(True)

        self.total_results = total_count
        total_pages = math.ceil(total_count / self.page_size)
        if total_pages < 1: total_pages = 1

        self.lbl_total.setText(f"of {total_pages}")
        self.page_input.setRange(1, total_pages)

        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled((self.current_index + self.page_size) < total_count)

        if not mods:
            self.layout_content.addWidget(QLabel("No results found."))
            return

        self.scroll.verticalScrollBar().setValue(0)

        for mod in mods:
            relative_path = self.find_local_file(mod['name'], mod.get('classId'))
            is_inst = relative_path is not None

            card = UniversalCard(
                title=mod['name'],
                subtitle=f"by {mod.get('authors', [{'name': 'Unknown'}])[0]['name']}",
                icon_url=mod.get('logo', {}).get('thumbnailUrl'),
                is_installed=is_inst,
                install_callback=lambda btn, m=mod: self.install(m, btn),
                delete_callback=lambda p=relative_path: self.delete(p),
                click_callback=lambda m=mod: self.show_mod_details(m)
            )
            self.layout_content.addWidget(card)

    def show_mod_details(self, mod_data):
        local_filename = self.find_local_file(mod_data['name'])
        is_installed = local_filename is not None

        def remove_handler():
            current_file = self.find_local_file(mod_data['name'])
            if current_file: return self.delete(current_file, confirm=True)
            return False

        def install_handler(btn, on_finish):
            self.install(mod_data, btn, on_finish)

        dialog = ModDetailsDialog(
            mod_data, is_installed=is_installed,
            install_callback=install_handler, remove_callback=remove_handler, parent=self
        )
        dialog.exec()
        self.execute_search()

    def find_local_file(self, mod_name, class_id=None):
        if not self.game_path or not os.path.exists(self.game_path):
            return None

        subfolder = PATH_MAP.get(class_id, "UserData/Mods")
        search_path = os.path.normpath(os.path.join(self.game_path, subfolder))

        if not os.path.exists(search_path):
            return None

        clean_name = mod_name.lower().replace(" ", "")

        try:
            for item in os.listdir(search_path):
                full_item_path = os.path.join(search_path, item)
                item_lower = item.lower().replace(" ", "")

                if clean_name in item_lower:
                    is_valid_file = item.endswith(('.jar', '.zip')) and os.path.isfile(full_item_path)
                    is_valid_folder = os.path.isdir(full_item_path)

                    if is_valid_file or is_valid_folder:
                        return os.path.join(subfolder, item)

        except Exception as e:
            print(f"Error scanning {search_path}: {e}")

        return None

    def delete(self, relative_path, confirm=True):
        if not self.game_path or not relative_path: return False

        full_path = os.path.normpath(os.path.join(self.game_path, relative_path))

        if confirm:
            filename = os.path.basename(relative_path)
            reply = QMessageBox.question(
                None, "Uninstall", f"Are you sure you want to delete '{filename}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes: return False

        try:
            if os.path.exists(full_path):
                os.remove(full_path)
            self.execute_search()
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Delete failed: {e}")
            return False

    def install(self, mod, btn, on_finish_ui=None):
        if not self.game_path:
            return QMessageBox.warning(self, "Error", "Set folder first!")

        class_id = mod.get('classId')
        subfolder = PATH_MAP.get(class_id, "UserData/Mods")
        target_dir = os.path.normpath(os.path.join(self.game_path, subfolder))

        is_zip = (class_id == 9184)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        if hasattr(btn, "setText"):
            btn.setText("Downloading..." if not is_zip else "Installing...")
            btn.setEnabled(False)

        self.dl_worker = DownloadWorker(self.client, mod['id'], target_dir, is_zip)

        def on_done(filename):
            if on_finish_ui:
                on_finish_ui(True)
            else:
                self.execute_search()

        self.dl_worker.finished.connect(on_done)
        self.dl_worker.start()

        return None

    def clear_list(self):
        while self.layout_content.count():
            child = self.layout_content.takeAt(0)
            if child.widget(): child.widget().deleteLater()

    def set_game_path(self, path):
        self.game_path = path
