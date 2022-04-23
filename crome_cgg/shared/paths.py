from __future__ import annotations

import os
from pathlib import Path

output_folder: Path = Path(os.path.join(os.path.dirname(__file__), "..", "output"))

persistence_path: Path = output_folder / "persistence"
