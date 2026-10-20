#!/bin/sh
# Build a fresh, bounded offline analysis from the preserved 1061 containers.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_root"
project_name=${1:-refined-1061-reproduction}
case "$project_name" in
    ''|*[!a-zA-Z0-9_-]*)
        echo 'Use letters, digits, underscores or hyphens for the project name.' >&2
        exit 1
        ;;
esac
ghidra="$project_root/analysis/tools/ghidra_12.1.4_PUBLIC/support/analyzeHeadless"
if [ ! -x "$ghidra" ]; then
    echo 'Project Ghidra installation is missing.' >&2
    exit 1
fi
if [ -e "analysis/1061/ghidra/$project_name.gpr" ]; then
    echo 'Choose a fresh project name to preserve the existing database.' >&2
    exit 1
fi
python3 scripts/inspect_1061_odx.py
python3 scripts/verify_1061_frf.py
python3 scripts/build_1061_map.py
mkdir -p analysis/1061/ghidra
"$ghidra" analysis/1061/ghidra "$project_name" \
    -import analysis/1061/mapped-update.bin \
    -loader BinaryLoader -loader-baseAddr 0x2000 \
    -processor V850:LE:32:default -scriptPath scripts/ghidra \
    -preScript RefineMapped1061.java \
    -postScript ReportMapped1061.java "$project_root/analysis/1061/$project_name-report.txt" \
    -analysisTimeoutPerFile 120
"$ghidra" analysis/1061/ghidra "$project_name" \
    -process mapped-update.bin -noanalysis -scriptPath scripts/ghidra \
    -postScript AnnotateDiagnostics1061.java "$project_root/analysis/1061/$project_name-annotations.txt"
"$ghidra" analysis/1061/ghidra "$project_name" \
    -process mapped-update.bin -noanalysis -scriptPath scripts/ghidra \
    -postScript ExportFunctions1061.java "$project_root/analysis/1061/$project_name-diagnostics.txt" 2fd96,30006,2fd2a
