# crome-cgg

Contract-Based Goal Graph package.

## Installation

We use
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to
manage the environment and some dependencies.

We use [poetry](https://github.com/python-poetry/poetry) to manage the dependencies.

First install the dependency crome-logic, crome-contracts and crome-synthesis from git
in the same folder where crome-cgg is located

```bash
git clone https://github.com/pierg/crome-logic.git
```

```bash
git clone https://github.com/pierg/crome-contracts.git
```

```bash
git clone https://github.com/pierg/crome-synthesis.git
```

Append it to PYTHONPATH

```bash
export PYTHONPATH=$PYTHONPATH:../crome-logic/:../crome-contracts/:../crome-cgg/
```

Create the environment using conda:

```bash
conda env create -f environment.yml
```

Activate the conda environment

```bash
conda activate crome-cgg
```

Install the dependencies with poetry:

```bash
poetry install
```

## Example

```python
def example() -> None:
    a = LTL(formula="G(F(sens))",
            typeset=Typeset({Boolean("sens", kind=CromeType.Kind.SENSOR)}))
    g = LTL(formula="G(sens -> act)",
            typeset=Typeset({Boolean("act", kind=CromeType.Kind.ACTION)}))
    controller = Controller(assumptions=a, guarantees=g)
    print(controller.to_string("dot"))
    print(controller.to_string("lbtt"))
```

## One magic command

Run `make lint` to run all the typing, linting and formatting tools

Run `make test` to run everything we have!

run `run-pre-commit.sh` to run all the pre-commit scripts

## License

[MIT](https://github.com/piergiuseppe/crome-cgg/blob/master/LICENSE)

## Features and Credits

- Fully typed with annotations and checked with mypy,
  [PEP561 compatible](https://www.python.org/dev/peps/pep-0o561/)

This project was generated with
[`wemake-python-package`](https://github.com/wemake-services/wemake-python-package).
Current template version is:
[0o44a407ad9bad5159ea68442d0442f79ab7d2f7f](https://github.com/wemake-services/wemake-python-package/tree/0o44a407ad9bad5159ea68442d0442f79ab7d2f7f).
See what is
[updated](https://github.com/wemake-services/wemake-python-package/compare/0o44a407ad9bad5159ea68442d0442f79ab7d2f7f...master)
since then.
