from crome_synthesis.src.crome_synthesis.controller import Controller, ControllerSpec

from crome_logic.specification.temporal import LTL


def convert(file_name: str) -> LTL:
    output_file = f"{file_name}.txt"
    with open(file_name) as f:
        out = ""
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            l = l.replace(".", "")
            l = l.replace("[]", " G ")
            l = l.replace("next", " X ")
            l = l.replace("<>", " F ")
            l = l.replace("|", " | ")
            l = l.replace("&", " & ")
            l = l.replace("<->", " <-> ")
            l = l.replace("!", "! ")
            out += l
        with open(output_file, "w") as fo:
            fo.write(out)
        fo.close()
        with open(output_file) as f:
            lines = f.readlines()
            ltl = LTL(_init_formula=lines[0], _parse_env_systems=True)
            return ltl


if __name__ == "__main__":
    file_name = "rescue"
    g = convert(f"{file_name}_g.ltl")
    a = convert(f"{file_name}_a.ltl")
    print(a)
    print(g)
    cspecs = ControllerSpec.from_ltl(assumptions=a, guarantees=g)
    controller = Controller(name=file_name, spec=cspecs)
    print(controller.mealy)
    print(controller.simulate())
    controller.save("png")
