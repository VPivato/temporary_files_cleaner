import os
from pathlib import Path

FOLDER_OPTIONS = [
    [
        {
            "label": "temp",
            "path": Path(os.environ["SYSTEMROOT"]) / "Temp",
            "tooltip": f"{Path(os.environ["SYSTEMROOT"]) / "Temp"} \nPlacheholder text.",
            "requires_admin": True
        },
        {
            "label": "%temp%",
            "path": Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "Temp",
            "tooltip": f"{Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "Temp"} \nPlaceholder text.",
            "requires_admin": False
        },
        {
            "label": "SystemTemp",
            "path": Path(os.environ["SYSTEMROOT"]) / "SystemTemp",
            "tooltip": f"{Path(os.environ["SYSTEMROOT"]) / "SystemTemp"} \nPlaceholder text.",
            "requires_admin": True
        }
    ],
    [
        {
            "label": "SoftwareDistribution",
            "path": Path(os.environ["SYSTEMROOT"]) / "SoftwareDistribution" / "Download",
            "tooltip": f"{Path(os.environ["SYSTEMROOT"]) / "SoftwareDistribution" / "Download"} \nPlaceholder text.",
            "requires_admin": True
        },
        {
            "label": "prefetch",
            "path": Path(os.environ["SYSTEMROOT"]) / "Prefetch",
            "tooltip": f"{Path(os.environ["SYSTEMROOT"]) / "Prefetch"} \nPlaceholder text.",
            "requires_admin": True
        }
    ],
    [
        {
            "label": "Google Chrome",
            "path": Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
            "tooltip": f"{Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache"} \nPlaceholder text.",
            "requires_admin": False
        },
        {
            "label": "Opera",
            "path": Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "Opera Software" / "Opera Stable" / "Cache",
            "tooltip": f"{Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "Opera Software" / "Opera Stable" / "Cache"} \nPlaceholder text.",
            "requires_admin": False
        },
        {
            "label": "Brave",
            "path": Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "Cache",
            "tooltip": f"{Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "Cache"} \nPlaceholder text.",
            "requires_admin": False
        }
    ]
]