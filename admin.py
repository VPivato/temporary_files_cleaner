from pathlib import Path
from logging import Logger
from utils import get_pythonw
import sys, ctypes, subprocess

def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:
        return False

def request_admin_privileges(logger:Logger, extra_args:list[str]):
        if is_admin():
            return True
        
        try:
            params = subprocess.list2cmdline(sys.argv + extra_args)
            result = ctypes.windll.shell32.ShellExecuteW(None, "runas", get_pythonw(), params, str(Path(__file__).resolve().parent), 1)
            if result > 32:
                logger.info("Iniciado: processo com privilegios de administrador")
                return True
            else:
                logger.warning("Não iniciado: processo com privilegios de administrador")
                return False
        except Exception as e:
            logger.error(f"Erro ao soliticar elevação - {e}")