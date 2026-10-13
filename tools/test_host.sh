#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GODOT_BIN="${GODOT_HOST_BIN:-$ROOT/../GodotPSV/_build/godot-host-validation/Godot_v4.8-dev7_linux.x86_64}"
if [[ ! -x "$GODOT_BIN" ]]; then
  echo "Host Godot executable missing: $GODOT_BIN" >&2
  exit 2
fi
for TEST in host_smoke host_joypad_matrix host_visual_smoke host_score10_smoke host_settings_smoke; do
  echo "Running $TEST..."
  "$GODOT_BIN" --headless --path "$ROOT/game" --script "$ROOT/tests/$TEST.gd"
done
echo "All host gameplay and controller checks passed."
