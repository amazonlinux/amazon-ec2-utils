#!/usr/bin/bash
# Capture ec2-metadata output for each subcommand into a directory.
# Usage: ./capture-output.sh [output-dir]
#   default output-dir: output

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EC2_METADATA="${SCRIPT_DIR}/../ec2-metadata"
OUTDIR="${1:-output}"

[[ -x "$EC2_METADATA" ]] || { echo "ERROR: ec2-metadata not found at $EC2_METADATA" >&2; exit 1; }

mapfile -t cmds < <("$EC2_METADATA" --help | grep -oP '(?<=/--)[a-z][-a-z0-9]+' | grep -v 'help\|quiet\|all\|path')
if [[ ${#cmds[@]} -eq 0 ]]; then
	echo "ERROR: No subcommands found in --help output" >&2
	exit 1
fi

mkdir -p "$OUTDIR"

for cmd in "${cmds[@]}"; do
	"$EC2_METADATA" --"$cmd" > "$OUTDIR/$cmd.txt" 2>&1 || echo "WARN: --$cmd failed" >&2
done

"$EC2_METADATA" > "$OUTDIR/default.txt" 2>&1 || echo "WARN: default (no args) failed" >&2

files=("$OUTDIR"/*.txt)
echo "Captured ${#files[@]} files in $OUTDIR/"
