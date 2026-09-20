import json
import logging, os, sys
from pathlib import Path
from cleaner import Cleaner
from folder_options import FOLDER_OPTIONS
from logging.handlers import RotatingFileHandler
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton,QVBoxLayout, QWidget, QFrame, QMessageBox
from admin import parse_args

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
        
        btn.clicked.connect(self.clean)
        
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
    
    def get_checked(self):
        checked = [(path, req_adm) for cb, (path, req_adm) in self.checkboxpaths.items() if cb.isChecked()]
        return checked
    
    def clean(self):
        result = cleaner.execute_cleanup(self.get_checked())
        if result.elevation_requested and result.elevation_granted:
            QApplication.quit()
            sys.exit()
        
        logger.info(f"Sucesso ao limpar: {result.cleaned_count} Falha: {result.failed_count}")
        msg = QMessageBox(self)
        msg.setText(f"Sucesso ao limpar: {result.cleaned_count} \nFalha: {result.failed_count} \n{bytes_to_mib(result.freed_bytes)} Mib limpos.")
        msg.setDetailedText(format_message(result.failed_reason))
        msg.exec()

def format_message(*dicts):
    msg = ""
    for d in dicts:
        for k, v in d.items():
            msg += f"{k}: {v} \n"
    return msg

def bytes_to_mib(*args, decimal_places=2):
    return round(sum(args) / 1024 / 1024, decimal_places)
 
if __name__ == "__main__":
    app = QApplication()
    args = parse_args()
    
    if not args.elevated:
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
    else:
        data = [(Path(p), True) for p in args.cleanup]
        result = cleaner.execute_cleanup(data)
        msg = QMessageBox()
        msg.setText(f"Sucesso ao limpar: {result.cleaned_count + int(args.cleaned_count)}\nFalha: {result.failed_count + int(args.failed_count)} \n{bytes_to_mib(result.freed_bytes, int(args.freed_bytes))} Mib limpos.")
        failed_reason = json.loads(args.failed_reason)
        msg.setDetailedText(format_message(failed_reason, result.failed_reason))
        msg.exec()
        sys.exit(0)
        