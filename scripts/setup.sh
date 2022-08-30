#!/usr/bin/env bash
set -e


PYTHON_VERSIONS="${PYTHON_VERSIONS-3.10 3.11}"

install_with_pipx() {
    if ! command -v "$1" &>/dev/null; then
        if ! command -v pipx &>/dev/null; then
            python3 -m pip install --user pipx
        fi
        pipx install "$1"
    fi
}


setup() {
    echo "pulling the submodules"
    git submodule init 
    git submodule update --remote --merge
    pdm install
    echo "pdm dependecies installed"
    echo "creating conda environment..."
    pdm venv create --with conda
    echo "activating conda environment..."
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate ./.venv
    echo "installing conda dependencies..."
    conda env update --file conda-dependencies.yml --prune
}

install_with_pipx pdm

restore_previous_python_version() {
    if pdm use -f "$1" &>/dev/null; then
        echo "> Restored previous Python version: ${1##*/}"
    fi
}

if [ -n "${PYTHON_VERSIONS}" ]; then
    if old_python_version="$(pdm config python.path 2>/dev/null)"; then
        echo "> Currently selected Python version: ${old_python_version##*/}"
        trap "restore_previous_python_version ${old_python_version}" EXIT
    fi
    for python_version in ${PYTHON_VERSIONS}; do
        if pdm use -f "python${python_version}" &>/dev/null; then
            echo "> Using Python ${python_version} interpreter"
            setup
        else
            echo "> pdm use -f python${python_version}: Python interpreter not available?" >&2
        fi
    done
else
    setup
fi
