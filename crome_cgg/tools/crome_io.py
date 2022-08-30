# type: ignore
import os
from pathlib import Path

from src.crome_cgg.shared.paths import output_folder_cgg


def save_to_file(
    file_content: str,
    file_name: str,
    folder_name: str | None = None,
    absolute_folder_path: Path | None = None,
) -> Path:
    if Path(file_name).suffix == "":
        file_name = f"{Path(file_name)}.txt"

    if folder_name is not None and absolute_folder_path is not None:
        raise AttributeError

    if folder_name is not None:
        file_folder = output_folder_cgg / folder_name

    elif absolute_folder_path is not None:
        file_folder = absolute_folder_path

    else:
        file_folder = output_folder_cgg

    if not file_folder.exists():
        os.makedirs(file_folder)

    file_path: Path = file_folder / file_name

    with open(file_path, "w") as f:  # mypy crashes on this line, i don't know why
        f.write(file_content)

    f.close()

    return file_path
