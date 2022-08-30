# crome-cgg

**Contract-Based Goal Graph**

The tool helps the designer model and deploy robotic missions using contracts. The designer can model the environment, and the goals that the robot must achieve using LTL or Specification Patterns. The tool analyze the goals, build the CGG (a graph of contracts) and realize the controllers via reactive synthesis and simulate the robotic mission.


[Contract for System Design](https://hal.inria.fr/hal-0o0757488/file/RR-8147.pdf)

Documentation available [here](https://pierg.github.io/crome-cgg).

## Installation

We use [pdm](https://github.com/pdm-project/pdm) to most of the dependencies, and
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). Make sure they are installed on your system.

To setup the environment, simply run:

```bash
make setup
```

The setup script will:
* Pull all the submodule dependencies
* Install all the dependecies via pdm
* Create a new conda environment and isntall the conda dependencies


> NOTE:
> If it fails for some reason,
> you'll need to install
> [PDM](https://github.com/pdm-project/pdm)
> manually.
>
> You can install it with:
>
> ```bash
> python3 -m pip install --user pipx
> pipx install pdm
> ```
>
> Now you can try running `make setup` again,
> or simply `pdm install`.

> NOTE: Conda for Mac with Apple Silicon
>
> Some of the packages in conda do not support arm64 architecture. To install all the dependencies correctly on a Mac with Apple Silicon, make sure that you are running conda for x86_64 architecture.
>
> You can install miniconda for MacOSX x86_64 by running the following commands
>
> ```bash
> curl -L https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh > Miniconda3-latest-MacOSX-x86_64.sh
> ```
>
> ```bash
> sh Miniforge3-MacOSX-arm64.sh
> ```


### Activate conda enviornmnet

```bash
conda activate ./.venv
```


> NOTE: Working with PEP 582
> With PEP 582, dependencies will be installed into __pypackages__ directory under the project root. With PEP 582 enabled globally, you can also use the project interpreter to run scripts directly.
> Check [pdm documentation](https://pdm.fming.dev/latest/usage/pep582/) on PEP 582.
> To configure VSCode to support PEP 582, open `.vscode/settings.json` (create one if it does not exist) and add the following entries:
> ```json
> {
>   "python.autoComplete.extraPaths": ["__pypackages__/3.10/lib"],
>   "python.analysis.extraPaths": ["__pypackages__/3.10/lib"]
> }
> ```

## Usage

Check the `examples` folder

Run `make help` to see all the available commands

## Docker

You can directly run the project by running the docker image on any platform

```bash
docker run -it --platform linux/x86_64 pmallozzi/crome-cgg:latest
```

### Building the image

To build the image you can run the following command

```bash
docker buildx build --platform linux/x86_64 -t [DOCKERUSERNAME]/[PROJECT]:[TAG] --push .
```

## License

[MIT](https://github.com/piergiuseppe/crome-cgg/blob/master/LICENSE)

## Features and Credits

- Fully typed with annotations and checked with mypy,
  [PEP561 compatible](https://www.python.org/dev/peps/pep-0o561/)