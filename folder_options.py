import os
from pathlib import Path

SYSTEMROOT = os.environ["SYSTEMROOT"]
USERPROFILE = os.environ["USERPROFILE"]

def item(label:str, path:Path, tooltip:str, requires_admin:bool) -> dict:
    return {
        "label": label,
        "path": path,
        "tooltip": f"{path} \n{tooltip}",
        "requires_admin": requires_admin
    }

FOLDER_OPTIONS = [
    [
        item(
            label="temp",
            path=Path(SYSTEMROOT) / "Temp",
            tooltip="Arquivos temporários usados por programas e pelo Windows.",
            requires_admin=True
        ),
        item(
            label="%temp%",
            path=Path(USERPROFILE) / "AppData" / "Local" / "Temp",
            tooltip="Arquivos temporários do usuário atual.",
            requires_admin=False
        ),
        item(
            label="SystemTemp",
            path=Path(SYSTEMROOT) / "SystemTemp",
            tooltip="Arquivos temporários usados por componentes e serviços do sistema.",
            requires_admin=True
        )
    ],
    [
        item(
            label="SoftwareDistribution",
            path=Path(SYSTEMROOT) / "SoftwareDistribution" / "Download",
            tooltip="Arquivos temporários e caches do Windows Update.",
            requires_admin=True
        ),
        item(
            label="prefetch",
            path=Path(SYSTEMROOT) / "Prefetch",
            tooltip="Arquivos de inicialização de aplicativos.",
            requires_admin=True
        )
    ],
    [
        item(
            label="Google Chrome",
            path=Path(USERPROFILE) / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
            tooltip="Cache do Google Chrome.",
            requires_admin=False
        ),
        item(
            label="Opera",
            path=Path(USERPROFILE) / "AppData" / "Local" / "Opera Software" / "Opera Stable" / "Cache",
            tooltip="Cache do Opera Browser.",
            requires_admin=False
        ),
        item(
            label="Brave",
            path=Path(USERPROFILE) / "AppData" / "Local" / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "Cache",
            tooltip="Cache do Brave Browser.",
            requires_admin=False
        )
    ]
]