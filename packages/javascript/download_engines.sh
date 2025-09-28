#!/bin/bash

# TavoAI JavaScript SDK Engine Downloader
# Downloads and bundles OpenGrep and OPA binaries for the JS SDK

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINES_DIR="$SCRIPT_DIR/engines"
CACHE_DIR="$HOME/.tavoai/engines"

# Create directories
mkdir -p "$ENGINES_DIR"
mkdir -p "$CACHE_DIR"

# Detect platform
detect_platform() {
    case "$(uname -s)" in
        Linux*)     PLATFORM="linux" ;;
        Darwin*)    PLATFORM="darwin" ;;
        CYGWIN*|MINGW*|MSYS*) PLATFORM="windows" ;;
        *)          PLATFORM="unknown" ;;
    esac

    case "$(uname -m)" in
        x86_64)     ARCH="x86_64" ;;
        aarch64|arm64) ARCH="aarch64" ;;
        *)          ARCH="unknown" ;;
    esac
}

download_opengrep() {
    echo "Downloading OpenGrep..."
    local version="1.10.0"
    local base_url="https://github.com/opengrep/opengrep/releases/download/v${version}"

    case "$PLATFORM-$ARCH" in
        "linux-x86_64")   asset="opengrep-core_linux_x86.tar.gz" ;;
        "linux-aarch64")  asset="opengrep-core_linux_aarch64.tar.gz" ;;
        "darwin-x86_64")  asset="opengrep-core_osx_x86.tar.gz" ;;
        "darwin-aarch64") asset="opengrep-core_osx_aarch64.tar.gz" ;;
        "windows-x86_64") asset="opengrep-core_windows_x86.zip" ;;
        *) echo "Unsupported platform: $PLATFORM-$ARCH"; return 1 ;;
    esac

    local url="$base_url/$asset"
    local dest="$CACHE_DIR/$asset"

    if [ ! -f "$dest" ]; then
        curl -L -o "$dest" "$url"
    fi

    # Extract
    cd "$ENGINES_DIR"
    if [[ $asset == *.tar.gz ]]; then
        tar -xzf "$CACHE_DIR/$asset"
    elif [[ $asset == *.zip ]]; then
        unzip -o "$CACHE_DIR/$asset"
    fi
}

download_opa() {
    echo "Downloading OPA..."
    local base_url="https://github.com/open-policy-agent/opa/releases/latest/download"

    case "$PLATFORM-$ARCH" in
        "linux-x86_64")   asset="opa_linux_amd64_static" ;;
        "linux-aarch64")  asset="opa_linux_arm64_static" ;;
        "darwin-x86_64")  asset="opa_darwin_amd64" ;;
        "darwin-aarch64") asset="opa_darwin_arm64_static" ;;
        "windows-x86_64") asset="opa_windows_amd64.exe" ;;
        *) echo "Unsupported platform: $PLATFORM-$ARCH"; return 1 ;;
    esac

    local url="$base_url/$asset"
    local dest="$ENGINES_DIR/opa"

    if [[ $PLATFORM == "windows" ]]; then
        dest="$ENGINES_DIR/opa.exe"
    fi

    if [ ! -f "$dest" ]; then
        curl -L -o "$dest" "$url"
        chmod +x "$dest"
    fi
}

main() {
    detect_platform
    echo "Detected platform: $PLATFORM-$ARCH"

    download_opengrep
    download_opa

    echo "Engines downloaded to: $ENGINES_DIR"
    ls -la "$ENGINES_DIR"
}

main "$@"