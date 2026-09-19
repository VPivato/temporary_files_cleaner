from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QCheckBox, QPushButton,QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PySide6.QtCore import Qt
from pathlib import Path
import shutil, logging, os, ctypes, sys, subprocess
from logging.handlers import RotatingFileHandler
from folder_options import FOLDER_OPTIONS

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

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_pythonw():
    """pythonw.exe para não exibir um terminal ao relançar o processo com privilégios de administrador"""
    
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    
    if pythonw.exists():
        return str(pythonw)
    
    return sys.executable


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
        if not path.exists():
            logger.warning(f"Diretório inexistente, ignorando: {path}")
            return
        try:
            entries = list(path.iterdir())
        except OSError as e:
            logger.warning(f"Não foi possível acessar {path}: {e}")
            return
        
        for item in entries:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            except (PermissionError, OSError) as e:
                logger.warning(f"Erro ao excluir {item}: {e}")
    
    def execute_cleanup(self):
        adm_count = 0
        for checkbox, (_, requires_admin) in self.checkboxpaths.items():
            if checkbox.isChecked() and requires_admin:
                adm_count += 1
        
        if adm_count > 0 and not is_admin():
            try:
                success = self.request_admin_privileges()
                if success:
                    logger.info("Sucesso ao elevar processo.")
                    QApplication.quit()
                    sys.exit()
                else:
                    logger.warning("Falha ao elevar processo.")
                    return
            except Exception as e:
                logger.error(f"Erro no processo de elevação: {e}")
        
        try:
            for checkbox, (path, requires_admin) in self.checkboxpaths.items():
                if checkbox.isChecked():
                    logger.info(f"Limpando diretório: {path}")
                    self.clear_folder(path)
        except (PermissionError, OSError) as e:
            logger.warning(f"Erro: {e}")
    
    def request_admin_privileges(self):
        if is_admin():
            return
        else:
            try:
                result = ctypes.windll.shell32.ShellExecuteW(None, "runas", get_pythonw(), subprocess.list2cmdline(sys.argv), None, 1)
                if result > 32:
                    logger.info("Iniciado: processo com privilegios de administrador")
                    return True
                else:
                    logger.warning("Não iniciado: processo com privilegios de administrador")
                    return False
            except Exception as e:
                logger.error(f"Erro ao soliticar elevação - {e}")

 
if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
        