from pathlib import Path
from logging import Logger
import sys, ctypes, subprocess, argparse

def get_pythonw():
    """pythonw.exe para não exibir um terminal ao relançar o processo com privilégios de administrador"""
    
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    
    if pythonw.exists():
        return str(pythonw)
    
    return sys.executable

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--elevated",
        action="store_true"
    )
    
    parser.add_argument(
        "--cleaned_count",
        type=str
    )
    
    parser.add_argument(
        "--freed_bytes",
        type=str
    )
    
    parser.add_argument(
        "--failed_count",
        type=str
    )
    
    parser.add_argument(
        "--failed_reason",
        type=str
    )
    
    parser.add_argument(
        "--cleanup",
        nargs="+",
        type=str
    )
    
    return parser.parse_args()

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