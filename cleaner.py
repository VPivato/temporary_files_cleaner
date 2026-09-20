import json
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
    freed_bytes: int


class Cleaner:
    def __init__(self, logger:Logger):
        self.logger = logger
    
    def clear_folder(self, path:Path) -> tuple[bool, int]:
        """Limpa o diretório designado arquivo por arquivo usando a função recursiva _remove_tree().
        
        Args:
            path: Objeto pathlib.Path representando o diretório a ser esvaziado.
        
        Returns:
            (bool, freed_bytes): Booleano representando se a operação foi bem sucedida, número inteiro expressando quantos bytes foram excluidos.
        """
        
        if not path.exists():
            self.logger.warning(f"Diretório inexistente, ignorando: {path}")
            return False, 0
        
        try:
            entries = list(path.iterdir())
        except OSError as e:
            self.logger.warning(f"Não foi possível acessar {path}: {e}")
            return False, 0
        
        freed_bytes = 0

        for item in entries:
            try:
                if item.is_symlink(): # Proteção contra links simólicos, evita limpar pastas que apontem para outro lugar.
                    item.unlink
                if item.is_dir():
                    freed_bytes += self._remove_tree(item)
                    item.rmdir()
                else:
                    size = item.stat().st_size
                    item.unlink()
                    freed_bytes += size
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao excluir {item}: {e}")
        
        return True, freed_bytes
    
    
    def _clear_batch(self, paths:list[Path], result:CleanupResult) -> None:
        """Chama a função clear_folder para uma lista de pathlib.Path e atualiza as variáveis do CleanupResult especificado.
        
        Args:
            paths: Lista de objetos pathlib.Path. São os diretórios a serem limpos.
            result: Objeto CleanupResult. Variáveis como cleaned_count e failed_count são incrementadas durante a limpeza.
        """
        
        for path in paths:
            self.logger.info(f"Limpando diretório: {path}")
            try:
                success, freed_bytes = self.clear_folder(path)
                result.freed_bytes += freed_bytes
                if success:
                    result.cleaned_count += 1
                else:
                    result.failed_count += 1
                    result.failed_reason[path] = "Diretório inexistente ou não foi possível acessar."
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao processar {path}: {e}")
    
    
    def _remove_tree(self, path:Path) -> int:
        """Função recursiva que remove (unlink) arquivo por arquivo até esvaziar o diretório especificado.
        
        Args:
            path: Objeto pathlib.Path, o diretório a ser limpo.
        
        Returns:
            freed_bytes: valor inteiro representado quantos bytes foram excluidos.        
        """
        
        freed_bytes = 0
        
        for item in path.iterdir():
            try:
                if item.is_dir():
                    freed_bytes += self._remove_tree(item)
                    item.rmdir()
                else:
                    size = item.stat().st_size
                    item.unlink()
                    freed_bytes += size
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao excluir {item}: {e}")
        
        return freed_bytes
    
    
    def execute_cleanup(self, data:list[tuple[Path, bool]]) -> CleanupResult:
        """Com base na lista de diretórios e booleanos fornecida, chama _clear_batch após separar os caminhos entre admin e não-admin.
        Caso haja a necessidade de privilégios de administrador e o processo não estiver elevado, envia uma requisição ao usuário
        via 'ctypes.windll.shell32.ShellExecuteW'.
        
        Args:
            data: Lista de tuplas (path, requires_admin), o valor booleano é usado para separar entre pastas admin e não-admin.
        
        Returns:
            Objeto CleanupResult contendo variáveis como cleaned_count, failed_count, freed_bytes...
        """
        
        non_admin = [p for p, adm in data if not adm]
        admin_only = [p for p, adm in data if adm]
        
        result = CleanupResult(
            cleaned_count = 0,
            failed_count = 0,
            elevation_requested=False,
            elevation_granted=None,
            failed_reason={},
            freed_bytes=0
        )
        
        # Limpa todos diretórios não-admin antes de pedir elevação
        self._clear_batch(non_admin, result)
        
        # Finaliza se não houver nenhum diretório admin
        if not admin_only:
            return result
        
        # Limpa os diretórios admin se o processo estiver elevado
        if is_admin():
            self._clear_batch(admin_only, result)
            return result
        
        # Faz a requisição de elevação apenas após a limpeza dos diretórios não admin, e se o processo ainda não estiver elevado.
        extra_args = [
            "--elevated",
            "--cleaned_count",
            str(result.cleaned_count),
            "--freed_bytes",
            str(result.freed_bytes),
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
        
