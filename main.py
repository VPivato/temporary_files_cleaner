from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton,QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Arquivos Temporários")
        self.setFixedSize(300, 380)
        
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QVBoxLayout(container)
        
        # 1 - Seção Usuário e Sistema
        main_layout.addWidget(QLabel("1 - Usuário e sistema"))
        
        cb1 = QCheckBox("temp")
        cb2 = QCheckBox("%temp%")
        cb3 = QCheckBox("SystemTemp")
        main_layout.addWidget(cb1)
        main_layout.addWidget(cb2)
        main_layout.addWidget(cb3)
        
        self.addSeparator(main_layout)
        
        
        # 2 - Seção Sistema e Windows Update
        main_layout.addWidget(QLabel("2 - Caches do sistema e Win Update"))
        
        cb4 = QCheckBox("SoftwareDistribution")
        cb5 = QCheckBox("prefetch")
        main_layout.addWidget(cb4)
        main_layout.addWidget(cb5)
        
        self.addSeparator(main_layout)
        
        
        # 3 - Seção Navegadores
        main_layout.addWidget(QLabel("3 - Caches de navegadores"))
        
        cb6 = QCheckBox("Google Chrome")
        cb7 = QCheckBox("Opera")
        main_layout.addWidget(cb6)
        main_layout.addWidget(cb7)
        
        self.addSeparator(main_layout)
        
        
        # Checkoxes ToolTips
        cb1.setToolTip("%SystemRoot%/Temp \nArquivos temporários gerados por serviços do sistema e drivers.")
        cb2.setToolTip("%USERPROFILE%/AppData/Local/Temp \nCache de aplicativos, instaladores descompactados, relatórios de travamento.")
        cb3.setToolTip("%SystemRoot%/SystemTemp \nTemporários estritos do usuário corporativo/SYSTEM.")
        
        cb4.setToolTip("%SystemRoot%/SoftwareDistribution/Download \nArquivos de instalação antigos do Windows Update após as atualizações já terem sido aplicadas.")
        cb5.setToolTip("%SystemRoot%/Prefetch \nDados de otimização de inicialização de apps. Fará com que os apps demorem um segundo a mais para abrir na primeira vez após a limpeza.")
        
        cb6.setToolTip("%USERPROFILE%/AppData/Local/Google/Chrome/User Data/Default/Cache")
        cb7.setToolTip("%USERPROFILE%/AppData/Local/Opera Software/Opera Stable/Cache")
        
        
        btn = QPushButton("Começar Limpeza")
        btn.setFixedHeight(30)
        
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

 
if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
        