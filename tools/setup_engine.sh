#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINE="${1:-$ROOT/../GodotPSV}"
LIB="$ENGINE/_build/ubo-20261010-02/vitagl"
RUNTIME="$ENGINE/godot-master/bin/libgodot.so"
if [[ ! -s "$LIB/libvitaGL.a" || ! -s "$LIB/source/vitaGL.h" ]]; then
  echo "Missing validated VitaGL. Build godot4-vita as instructed in BUILDING.md" >&2
  exit 2
fi
if [[ ! -s "$RUNTIME" ]]; then echo "Missing engine libgodot.so: $RUNTIME" >&2; exit 2; fi
mkdir -p "$ROOT/deps/VitaGL/source"
cp "$LIB/libvitaGL.a" "$ROOT/deps/VitaGL/libvitaGL.a"
cp "$LIB/source/vitaGL.h" "$ROOT/deps/VitaGL/source/vitaGL.h"
bash "$ROOT/tools/sync_engine_runtime.sh" "$RUNTIME"
echo "Engine runtime and matching VitaGL dependencies available."
