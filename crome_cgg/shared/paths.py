from __future__ import annotations

import os
from pathlib import Path

output_folder_cgg: Path = (
    Path(os.path.join(os.path.dirname(__file__))).parent / "output"
)

persistence_path: Path = output_folder_cgg / "persistence"
