# crome-cgg

Contract-Based Goal Graph package.


## Installation

We use
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to
manage the environment and dependencies.

We use [poetry](https://github.com/python-poetry/poetry) to manage 'development'
dependencies (e.g. linting, type checking).

Create the environment using conda:

```bash
conda env create -f environment.yml
```

Activate the conda environment

```bash
conda activate crome-logic
```

Install the other dependencies with poetry (optional):

```bash
poetry install
```

### System Requirements

[Strix](https://strix.model.in.tum.de) must be installed on the system. Alternatively, a
[docker](https://www.docker.com) must be installed and running.



### Other Dependencies

Clone crome-logic, crome-contracts, and crome-synthesis from git
in the same folder where crome-web is located

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
export PYTHONPATH=$PYTHONPATH:../crome-logic/:../crome-contracts/:../crome-synthesis/
```



## Docker

You can directly run the project by running the docker image on any platform

`docker run -it --platform linux/x86_64 pmallozzi/crome-synthesis:latest`

### Building the image

To build the image you can run the following command

`docker buildx build --platform linux/x86_64 -t [DOCKERUSERNAME]/[PROJECT]:[TAG] --push .`

## Usage

Check the `examples` folder


## One magic command

Run `make lint` to run all the typing, linting and formatting tools

Run `make pre-commit` to run all the pre-commit tools

Check all the available commands in `Makefile`

## License

[MIT](https://github.com/piergiuseppe/crome-synthesis/blob/master/LICENSE)

## Features and Credits

- Fully typed with annotations and checked with mypy,
  [PEP561 compatible](https://www.python.org/dev/peps/pep-0o561/)

- This project has been initially generated with
  [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package).
