import logging, os
from pathlib import Path
from logging.handlers import RotatingFileHandler

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
