#!/bin/sh
# Usage: ./scripts/snap.sh <armdir> <outfile>
# Snapshots current OpenCode token/cost stats for the arm directory.
set -eu
opencode stats --project "$PWD/$1" > "$2"
echo "snapshot -> $2"
