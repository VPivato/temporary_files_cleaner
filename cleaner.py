import shutil
from pathlib import Path 
from logging import Logger
from admin import is_admin, request_admin_privileges

class Cleaner:
    def __init__(self, logger:Logger):
        self.logger = logger
    
    def clear_folder(self, path:Path):
        if not path.exists():
            self.logger.warning(f"Diretório inexistente, ignorando: {path}")
            return
        try:
            entries = list(path.iterdir())
        except OSError as e:
            self.logger.warning(f"Não foi possível acessar {path}: {e}")
            return

        for item in entries:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao excluir {item}: {e}")
    
    def execute_cleanup(self, paths:list[Path], requires_admin:list[bool]) -> bool | None:
            if any(requires_admin) and not is_admin():
                success = request_admin_privileges(self.logger)
                if success:
                    self.logger.info("Sucesso ao elevar processo.")
                    return True
                else:
                    self.logger.warning("Falha ao elevar processo.")
                    return False
            
            for path in paths:
                self.logger.info(f"Limpando diretório: {path}")
                try:
                    self.clear_folder(path)
                except (PermissionError, OSError) as e:
                    self.logger.warning(f"Erro ao processar {path}: {e}")
            
            return
