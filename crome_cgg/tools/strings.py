def tab(stringable_object, how_many=1, init_character: str = "") -> str:
    t: str = ""
    t += init_character
    t += "\t" * how_many
    if stringable_object == "":
        return t
    return "\n".join(
        list(map(lambda x: f"{t}{x}", str(stringable_object).splitlines()))
    )


def tabar(stringable_object, how_many=1) -> str:
    t: str = ""
    t += "|\t" * how_many
    if stringable_object == "":
        return t
    return "\n".join(
        list(map(lambda x: f"{t}{x}", str(stringable_object).splitlines()))
    )


def repr_dictionary(dictionary: dict) -> str:
    ret = ""
    for key, value in dictionary.items():
        if isinstance(value, list):
            val = "\t".join([str(v) for v in value])
            ret += f"{key}: \t {val}\n"
        else:
            ret += f"{key}: \t{value}\n"
    return ret
