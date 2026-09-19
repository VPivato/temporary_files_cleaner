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
        non_admin = [p for p, adm in zip(paths, requires_admin) if not adm]
        admin_only = [p for p, adm in zip(paths, requires_admin) if adm]
        
        # Limpa todos diretórios não-admin antes de pedir elevação
        for path in non_admin:
            self.logger.info(f"Limpando diretório: {path}")
            try:
                self.clear_folder(path)
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao processar {path}: {e}")
        
        # Finaliza se não houver nenhum diretório admin
        if not admin_only:
            return
        
        # Limpa os diretórios admin se o processo estiver elevado
        if is_admin():
            for path in admin_only:
                self.logger.info(f"Limpando diretório: {path}")
                try:
                    self.clear_folder(path)
                except (PermissionError, OSError) as e:
                    self.logger.warning(f"Erro ao processar {path}: {e}")
            return
        
        # Faz a requisição de elevação apenas após a limpeza dos diretórios não admin, e se o processo ainda não estiver elevado.
        return request_admin_privileges(self.logger)
        
