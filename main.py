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
        
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        separator1.setLineWidth(1)
        
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        separator2.setLineWidth(1)
        
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setFrameShadow(QFrame.Shadow.Sunken)
        separator3.setLineWidth(1)
        
        # 1 - Seção Usuário e Sistema
        main_layout.addWidget(QLabel("1 - Usuário e sistema"))
        
        cb1 = QCheckBox("temp")
        cb2 = QCheckBox("%temp%")
        cb3 = QCheckBox("SystemTemp")
        main_layout.addWidget(cb1)
        main_layout.addWidget(cb2)
        main_layout.addWidget(cb3)
        
        main_layout.addSpacing(5)
        main_layout.addWidget(separator1)
        main_layout.addSpacing(5)
        
        
        # 2 - Seção Sistema e Windows Update
        main_layout.addWidget(QLabel("2 - Caches do sistema e Win Update"))
        
        cb4 = QCheckBox("SoftwareDistribution")
        cb5 = QCheckBox("prefetch")
        main_layout.addWidget(cb4)
        main_layout.addWidget(cb5)
        
        main_layout.addSpacing(5)
        main_layout.addWidget(separator2)
        main_layout.addSpacing(5)
        
        
        # 3 - Seção Navegadores
        main_layout.addWidget(QLabel("3 - Caches de navegadores"))
        
        cb6 = QCheckBox("Google Chrome")
        cb7 = QCheckBox("Opera")
        main_layout.addWidget(cb6)
        main_layout.addWidget(cb7)
        
        main_layout.addSpacing(5)
        main_layout.addWidget(separator3)
        main_layout.addSpacing(5)
        
        
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

 
if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
        