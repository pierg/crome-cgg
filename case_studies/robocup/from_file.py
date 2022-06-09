import os
from pathlib import Path

from crome_synthesis.controller import Controller

specs_path = Path = Path(os.path.dirname(__file__)) / "output" / "spec.txt"
print(f"controller selected: {specs_path}")

controller = Controller.from_file(file_path=specs_path, name="spec")
print(controller.mealy)
print(controller.mealy.simulate(50))
