from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton,QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PySide6.QtCore import Qt
from pathlib import Path
import shutil
from folder_options import FOLDER_OPTIONS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Arquivos Temporários")
        self.setFixedSize(300, 410)
        
        self.checkboxpaths = {}
        self.selected = []
        
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QVBoxLayout(container)
        
        # 1 - Seção Usuário e Sistema
        main_layout.addWidget(QLabel("1 - Usuário e sistema"))
        
        for opt in FOLDER_OPTIONS[0]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = opt["path"]
            cb.toggled.connect(lambda _, cb=cb: self.add_if_checked(cb))
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        # 2 - Seção Sistema e Windows Update
        main_layout.addWidget(QLabel("2 - Caches do sistema e Win Update"))
        
        for opt in FOLDER_OPTIONS[1]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = opt["path"]
            cb.toggled.connect(lambda _, cb=cb: self.add_if_checked(cb))
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        # 3 - Seção Navegadores
        main_layout.addWidget(QLabel("3 - Caches de navegadores"))
        
        for opt in FOLDER_OPTIONS[2]:
            cb = QCheckBox(opt["label"])
            cb.setToolTip(opt["tooltip"])
            self.checkboxpaths[cb] = opt["path"]
            cb.toggled.connect(lambda _, cb=cb: self.add_if_checked(cb))
            main_layout.addWidget(cb)
        
        self.addSeparator(main_layout)
        
        
        btn = QPushButton("Começar Limpeza")
        btn.setFixedHeight(30)
        btn.clicked.connect(lambda: print(self.selected))
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
    
    
    def add_if_checked(self, checkbox):
        if checkbox.isChecked():
            self.selected.append(checkbox)
        else:
            try:
                self.selected.remove(checkbox)
            except ValueError:
                pass

 
if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
        