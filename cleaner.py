import json
import shutil
from pathlib import Path 
from logging import Logger
from dataclasses import dataclass
from admin import is_admin, request_admin_privileges

@dataclass
class CleanupResult:
    cleaned_count: int
    failed_count: int
    elevation_requested: bool
    elevation_granted: bool | None
    failed_reason: dict[Path, str]


class Cleaner:
    def __init__(self, logger:Logger):
        self.logger = logger
    
    def clear_folder(self, path:Path):
        if not path.exists():
            self.logger.warning(f"Diretório inexistente, ignorando: {path}")
            return False
        
        try:
            entries = list(path.iterdir())
        except OSError as e:
            self.logger.warning(f"Não foi possível acessar {path}: {e}")
            return False

        for item in entries:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao excluir {item}: {e}")
        
        return True
    
    def _clear_batch(self, paths:list[Path], result:CleanupResult):
        for path in paths:
            self.logger.info(f"Limpando diretório: {path}")
            try:
                success = self.clear_folder(path)
                if success:
                    result.cleaned_count += 1
                else:
                    result.failed_count += 1
                    result.failed_reason[path] = "Diretório inexistente ou não foi possível acessar."
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao processar {path}: {e}")
    
    def execute_cleanup(self, data:list[tuple[Path, bool]]) -> CleanupResult:
        non_admin = [p for p, adm in data if not adm]
        admin_only = [p for p, adm in data if adm]
        
        result = CleanupResult(
            cleaned_count = 0,
            failed_count = 0,
            elevation_requested=False,
            elevation_granted=None,
            failed_reason={}
        )
        
        # Limpa todos diretórios não-admin antes de pedir elevação
        self._clear_batch(non_admin, result)
        
        # Finaliza se não houver nenhum diretório admin
        if not admin_only:
            return result
        
        # Limpa os diretórios admin se o processo estiver elevado
        if is_admin():
            self._clear_batch(admin_only, result)
        
        # Faz a requisição de elevação apenas após a limpeza dos diretórios não admin, e se o processo ainda não estiver elevado.
        extra_args = [
            "--elevated",
            "--cleaned_count",
            str(result.cleaned_count),
            "--failed_count",
            str(result.failed_count),
            "--failed_reason",
            json.dumps({str(k): v for k, v in result.failed_reason.items()}),
            "--cleanup",
            *[str(path) for path in admin_only]
        ]
        admin_request = request_admin_privileges(self.logger, extra_args)
        
        result.elevation_requested = True
        result.elevation_granted = admin_request
        if not result.elevation_granted:
            result.failed_count += len(admin_only)
            for path in admin_only:
                result.failed_reason[path] = "Privilégios de administrador negados."
        return result
        
