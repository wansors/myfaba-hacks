#!/bin/bash

set -e


log() {
    echo "[INFO] $1"
}

error() {
    echo "[ERROR] $1" >&2
}

# Prevent running with sudo
if [ "$EUID" -eq 0 ]; then
  error "This script should NOT be run as root or with sudo."
  echo "Please run it as a regular user."
  exit 1
fi

# Check if running on Linux
if [[ "$(uname)" != "Linux" ]]; then
  error "This script runs only on Linux."
  exit 1
fi

# Check if curl is available
if ! command -v curl >/dev/null 2>&1; then
  error "'curl' is required but not installed."
  echo
  echo "You can install it with:"
  echo "   sudo apt install curl"
  echo
  exit 1
fi

VENV_DIR="venv"
WX_URL_BASE="https://extras.wxpython.org/wxPython4/extras/linux/gtk3"
PYTHON_SCRIPT="redele.py"

# Determine Python command and version tag (e.g. cp312)
PYTHON_CMD=$(command -v python3 || command -v python)
if [ -z "$PYTHON_CMD" ]; then
    error "No Python interpreter found."
    exit 1
fi

# Check if 'venv' module is available
check_venv_support() {
    log "Checking if '$PYTHON_CMD -m venv' works..."
    if ! "$PYTHON_CMD" -m venv test_env 2>/dev/null; then
        error "'python -m venv' failed — required module not available."
        echo
        echo "Please install the following packages:"
        echo "   sudo apt install python3-venv python3-pip"
        echo
        exit 1
    else
        rm -rf test_env
        log "'venv' module is available."
    fi
}

check_venv_support

PY_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}{sys.version_info.minor}")')
PY_TAG="cp${PY_VERSION}"

# Detect distro and version (lowercase)
DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
RELEASE=$(lsb_release -rs)

# Compose folder URL on wxPython extras site
FOLDER="${DISTRO}-${RELEASE}"
WX_WHEEL_DIR_URL="${WX_URL_BASE}/${FOLDER}/"

create_venv() {
    log "Creating virtual environment..."
    rm -rf "$VENV_DIR"
    "$PYTHON_CMD" -m venv "$VENV_DIR" || {
        error "Failed to create virtual environment."
        exit 1
    }
    source "$VENV_DIR/bin/activate"
    log "Upgrading pip, wheel, setuptools..."
    pip install -q --upgrade pip wheel setuptools
}

install_wxpython() {
    log "Fetching available wxPython wheels for ${DISTRO}-${RELEASE}..."
    wheel_list=$(curl -s "$WX_WHEEL_DIR_URL" | grep -oP '(?i)wxpython-[^"]+\.whl')

    if [ -z "$wheel_list" ]; then
        log "No wheels found for ${DISTRO}-${RELEASE}, skipping wxPython installation."
        return
    fi

    latest_wheel=$(echo "$wheel_list" | while read -r wheel; do
        if [[ "$wheel" == *"${PY_TAG}-${PY_TAG}"* ]]; then
            ver=$(echo "$wheel" | grep -oP '4\.\d+\.\d+')
            [ -n "$ver" ] && echo -e "${ver}\t${wheel}"
        fi
    done | sort -Vr | head -n1 | cut -f2)

    if [ -n "$latest_wheel" ]; then
        log "Installing wxPython wheel: $latest_wheel"
        curl -sO "${WX_WHEEL_DIR_URL}${latest_wheel}"
        pip install "$latest_wheel"
        rm -f "$latest_wheel"
    else
        log "No compatible wxPython 4.x wheel found."
    fi
}

install_requirements() {
    if [ -f "requirements.txt" ]; then
        log "Installing requirements.txt..."
        pip install -r requirements.txt || return 1
    else
        log "No requirements.txt found."
    fi
    return 0
}

run_script() {
    "$VENV_DIR/bin/python" "$PYTHON_SCRIPT"
}

# Main execution
if [ ! -d "$VENV_DIR" ]; then
    create_venv
    install_wxpython
    install_requirements || {
        error "Initial dependency installation failed."
        exit 1
    }
else
    log "Using existing virtual environment."
    source "$VENV_DIR/bin/activate"
fi

# Try running the script, fallback if dependency issue is detected
if ! run_script; then
    error "Initial script execution failed. Recreating venv and retrying..."
    create_venv
    install_wxpython
    install_requirements || {
        error "Reinstallation of dependencies failed. Aborting."
        exit 1
    }
    run_script || {
        error "Script failed again after recreating environment."
        exit 1
    }
fi

log "Script executed successfully."
