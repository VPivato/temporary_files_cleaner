from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton,QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PySide6.QtCore import Qt
from pathlib import Path
import shutil
from folder_options import FOLDER_OPTIONS
import logging

logging.basicConfig(
    filename="cleanup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
            self.checkboxpaths[cb] = opt["path"]
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        # 2 - Seção Sistema e Windows Update
        main_layout.addWidget(QLabel("2 - Caches do sistema e Win Update"))
        
        for opt in FOLDER_OPTIONS[1]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = opt["path"]
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        # 3 - Seção Navegadores
        main_layout.addWidget(QLabel("3 - Caches de navegadores"))
        
        for opt in FOLDER_OPTIONS[2]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = opt["path"]
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        btn = QPushButton("Começar Limpeza")
        btn.setFixedHeight(30)
        btn.clicked.connect(self.execute_cleanup)
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
    
    def clear_folder(self, path:Path):
        for item in path.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            except (PermissionError, OSError) as e:
                logging.info(f"Falha ao excluir {item}: {e}")
    
    def execute_cleanup(self):
        for checkbox, path in self.checkboxpaths.items():
            if checkbox.isChecked():
                self.clear_folder(path)

 
if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
        