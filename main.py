import json, sys
from pathlib import Path
from logger import logger
from cleaner import Cleaner
from admin import parse_args
from PySide6.QtGui import QIcon
from folder_options import FOLDER_OPTIONS
from utils import format_message, bytes_to_mib
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton,QVBoxLayout, QWidget, QFrame, QMessageBox

def resource_path(relative_path:str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent / relative_path

ICON_PATH =  resource_path("assets/icon.ico")

cleaner = Cleaner(logger)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Arquivos Temporários")
        self.setWindowIcon(QIcon(str(ICON_PATH)))
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
        msg.setWindowTitle("Arquivos Temporários")
        msg.setText(f"Sucesso ao limpar: {result.cleaned_count} \nFalha: {result.failed_count} \n{bytes_to_mib(result.freed_bytes)} MiB limpos.")
        msg.setDetailedText(format_message(result.failed_reason))
        msg.exec()
        sys.exit(0)

 
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
        msg.setWindowTitle("Arquivos Temporários")
        msg.setText(f"Sucesso ao limpar: {result.cleaned_count + int(args.cleaned_count)}\nFalha: {result.failed_count + int(args.failed_count)} \n{bytes_to_mib(result.freed_bytes, int(args.freed_bytes))} MiB limpos.")
        failed_reason = json.loads(args.failed_reason)
        msg.setDetailedText(format_message(failed_reason, result.failed_reason))
        msg.exec()
        sys.exit(0)
