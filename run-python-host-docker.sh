#!/bin/bash
# Main Docker launcher for Python Django SQLi Lab with Host MySQL
# This script can be called from the main sqli directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/python"
./docker-host-lab.sh "$@"
