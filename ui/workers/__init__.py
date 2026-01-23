import os
import zipfile

from PySide6.QtCore import QThread, Signal


class SearchWorker(QThread):
    finished = Signal(list, int)
    error = Signal(str)

    def __init__(self, client, query, category="mods", sort_field=2, sort_order="desc", index=0):
        super().__init__()
        self.client = client
        self.query = query
        self.category = category
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.index = index

    def run(self):
        try:
            print(self.category)
            mods, total = self.client.search(
                self.query,
                self.category,
                self.sort_field,
                self.sort_order,
                self.index
            )
            self.finished.emit(mods, total)
        except Exception as e:
            self.error.emit(str(e))


class DownloadWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, client, mod_id, target_dir, is_zip=False):
        super().__init__()
        self.client = client
        self.mod_id = mod_id
        self.target_dir = target_dir
        self.is_world = is_zip

    def run(self):
        try:
            file_data = self.client.get_download_url(self.mod_id)
            if not file_data['url']:
                raise Exception("No download URL found")

            zip_path = os.path.join(self.target_dir, file_data['name'])

            self.client.download_file(file_data['url'], zip_path)

            if self.is_world and zip_path.endswith('.zip'):
                extract_path = os.path.join(self.target_dir, file_data['name'].replace('.zip', ''))

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                os.remove(zip_path)
                self.finished.emit(f"Extracted to {os.path.basename(extract_path)}")
            else:
                self.finished.emit(file_data['name'])

        except Exception as e:
            self.error.emit(str(e))


class InitWorker(QThread):
    finished = Signal(str)

    def __init__(self, client): super().__init__(); self.client = client

    def run(self): self.finished.emit(self.client.init_connection())
