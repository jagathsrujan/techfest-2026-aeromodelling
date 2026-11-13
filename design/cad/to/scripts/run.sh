#!/bin/zsh
# usage: run.sh script.py [args]  -> runs in FreeCAD's bundled python (headless, separate process)
B=/Applications/FreeCAD.app/Contents/Resources
cd "$(dirname "$0")"
PYTHONPATH="$B/lib:$(pwd)" exec $B/bin/python "$@"
