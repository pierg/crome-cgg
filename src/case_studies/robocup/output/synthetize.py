import os
from pathlib import Path

from src.crome_synthesis.controller import Controller

folder_name = "ref/groce"
output_folder: Path = Path(os.path.dirname(__file__)) / folder_name

specs_path = Path = output_folder / f"spec.txt"
print(f"controller selected: {specs_path}")
controller = Controller.from_file(file_path=specs_path, name="spec")
print(controller.mealy)
print(controller.simulate(50))
controller.save(format="png", file_name="spec_", absolute_folder_path=output_folder)
