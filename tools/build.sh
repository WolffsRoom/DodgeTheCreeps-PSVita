#!/usr/bin/env bash
# Reproducible standalone Dodge the Creeps Vita package from this workspace.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export VITASDK="${VITASDK:-/usr/local/vitasdk}"
export PATH="$VITASDK/bin:$PATH"
if [[ ! -f "$VITASDK/share/vita.cmake" ]]; then
  echo "VitaSDK not found: $VITASDK" >&2
  exit 2
fi
IMPORTED_COUNT=$(find "$ROOT/game/.godot/imported" -maxdepth 1 -type f 2>/dev/null | wc -l || true)
if [[ "$IMPORTED_COUNT" -lt 10 ]]; then
  HOST_GODOT="${GODOT_HOST_BIN:-$ROOT/../GodotPSV/_build/godot-host-validation/Godot_v4.8-dev7_linux.x86_64}"
  if [[ ! -x "$HOST_GODOT" ]]; then HOST_GODOT="$(command -v godot || true)"; fi
  if [[ -z "$HOST_GODOT" || ! -x "$HOST_GODOT" ]]; then
    echo "Run a Godot 4.8 host import (set GODOT_HOST_BIN) before packaging." >&2
    exit 2
  fi
  "$HOST_GODOT" --headless --editor --import --path "$ROOT/game"
fi
if [[ ! -s "$ROOT/deps/VitaGL/libvitaGL.a" ]]; then
  echo "VitaGL archive missing. Run tools/setup_engine.sh with godot4-vita sources." >&2
  exit 2
fi
if [[ ! -s "$ROOT/runtime/libgodot.so" ]]; then
  echo "Pinned runtime missing: $ROOT/runtime/libgodot.so" >&2
  exit 2
fi
VERSION="dodge-gxm2d-$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$ROOT/releases/$VERSION"
BUILD="$ROOT/build/$VERSION"
mkdir -p "$OUT" "$BUILD"
echo "Project: $ROOT"
echo "Build ID: $VERSION"
echo "Game: $ROOT/game"
echo "Native GXM runtime: $ROOT/runtime/libgodot.so"
python3 "$ROOT/tools/pack_boot_animation.py"
cmake -S "$ROOT/loader" -B "$BUILD"   -DVITA_RUNTIME="$ROOT/runtime/libgodot.so"   -DVITA_GL_ROOT="$ROOT/deps/VitaGL"   -DVITA_GAME_DATA="$ROOT/game"   -DVITA_LIVEAREA_DIR="$ROOT/assets/LiveArea"   -DVITA_TITLEID="GDDC40001"   -DVITA_APP_NAME="Dodge the Creeps Vita"   -DVITA_VERSION="01.00"   -DVITA_GXM2D=ON   -DVITA_FULL_GAME_DATA=ON   -DVITA_RUNTIME_BUILD_ID="$VERSION"   > "$OUT/build.log" 2>&1 || { tail -60 "$OUT/build.log"; exit 1; }
cmake --build "$BUILD" --parallel 4 >> "$OUT/build.log" 2>&1 || { tail -60 "$OUT/build.log"; exit 1; }
VPK="$OUT/dodge_the_creeps_vita.vpk"
cp "$BUILD/godot_loader.vpk" "$VPK"
python3 "$ROOT/tools/verify_package.py" "$VPK"   --output "$OUT/manifest.json"   --build-id "$VERSION"
LATEST="$ROOT/releases/latest"
mkdir -p "$LATEST"
cp "$VPK" "$LATEST/dodge_the_creeps_vita.vpk"
cp "$OUT/manifest.json" "$LATEST/manifest.json"
echo "PASS: $VPK"
echo "Latest: $LATEST/dodge_the_creeps_vita.vpk"
