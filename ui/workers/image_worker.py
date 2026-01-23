import urllib.request

from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QPixmap, QImage


class ImageWorker(QThread):
    loaded = Signal(QPixmap)
    _active_workers = set()

    def __init__(self, url, size=None):
        super().__init__()
        self.url = url
        self.size = size
        self.finished.connect(self._cleanup)

    def start(self):
        ImageWorker._active_workers.add(self)
        super().start()

    def _cleanup(self):
        if self in ImageWorker._active_workers:
            ImageWorker._active_workers.remove(self)
        self.deleteLater()

    def run(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=10).read()
            image = QImage()
            image.loadFromData(data)
            pixmap = QPixmap(image)
            if self.size:
                pixmap = pixmap.scaled(self.size[0], self.size[1], Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.loaded.emit(pixmap)
        except Exception:
            pass
