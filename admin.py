from pathlib import Path
from logging import Logger
import sys, ctypes, subprocess

def get_pythonw():
    """pythonw.exe para não exibir um terminal ao relançar o processo com privilégios de administrador"""
    
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    
    if pythonw.exists():
        return str(pythonw)
    
    return sys.executable

def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:
        return False

def request_admin_privileges(logger:Logger):
        if is_admin():
            return
        else:
            try:
                result = ctypes.windll.shell32.ShellExecuteW(None, "runas", get_pythonw(), subprocess.list2cmdline(sys.argv), str(Path(__file__).resolve().parent), 1)
                if result > 32:
                    logger.info("Iniciado: processo com privilegios de administrador")
                    return True
                else:
                    logger.warning("Não iniciado: processo com privilegios de administrador")
                    return False
            except Exception as e:
                logger.error(f"Erro ao soliticar elevação - {e}")