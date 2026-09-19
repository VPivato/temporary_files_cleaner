import logging, os, sys
from pathlib import Path
from cleaner import Cleaner
from folder_options import FOLDER_OPTIONS
from logging.handlers import RotatingFileHandler
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton,QVBoxLayout, QWidget, QFrame

log_dir = Path(os.environ["LOCALAPPDATA"]) / "TemporaryFilesCleaner"
log_dir.mkdir(parents=True, exist_ok=True)

handler = RotatingFileHandler(
    filename=log_dir / "cleanup.log",
    maxBytes=1024 * 1024, # 1 MiB
    backupCount=2
)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
handler.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

cleaner = Cleaner(logger)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Arquivos Temporários")
        self.setFixedSize(300, 410)
        
        self.checkboxpaths = {}
        
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QVBoxLayout(container)
        
        # 1 - Seção Usuário e Sistema
        main_layout.addWidget(QLabel("1 - Usuário e sistema"))
        
        for opt in FOLDER_OPTIONS[0]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = [opt["path"], opt["requires_admin"]]
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        # 2 - Seção Sistema e Windows Update
        main_layout.addWidget(QLabel("2 - Caches do sistema e Win Update"))
        
        for opt in FOLDER_OPTIONS[1]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = [opt["path"], opt["requires_admin"]]
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        # 3 - Seção Navegadores
        main_layout.addWidget(QLabel("3 - Caches de navegadores"))
        
        for opt in FOLDER_OPTIONS[2]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = [opt["path"], opt["requires_admin"]]
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        btn = QPushButton("Começar Limpeza")
        btn.setFixedHeight(30)
        
        btn.clicked.connect(lambda: self.clean(
            paths=[path for cb, (path, _) in self.checkboxpaths.items() if cb.isChecked()],
            requires_admin=[requires_admin for cb, (_, requires_admin) in self.checkboxpaths.items() if cb.isChecked()]
        ))
        
        main_layout.addWidget(btn)
    
    
    def addSeparator(self, parent, line_size=1, spacing_top=5, spacing_bottom=5):
        sep = QFrame(
            frameShape=QFrame.Shape.HLine,
            frameShadow=QFrame.Shadow.Sunken,
            lineWidth=line_size
        )
        
        parent.addSpacing(spacing_top)
        parent.addWidget(sep)
        parent.addSpacing(spacing_bottom)
    
    def clean(self, paths, requires_admin):
        reopened_with_admin = cleaner.execute_cleanup(paths, requires_admin)
        if reopened_with_admin:
            QApplication.quit()
            sys.exit()

 
if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
        