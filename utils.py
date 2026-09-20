import sys, argparse
from pathlib import Path


def format_message(*dicts):
    msg = ""
    for d in dicts:
        for k, v in d.items():
            msg += f"{k}: {v} \n"
    return msg


def bytes_to_mib(*args, decimal_places=2):
    return round(sum(args) / 1024 / 1024, decimal_places)


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