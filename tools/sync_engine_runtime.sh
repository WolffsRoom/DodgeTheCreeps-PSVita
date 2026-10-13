#!/usr/bin/env bash
# Explicitly refresh pinned runtime from a newly compiled engine.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="${1:-$ROOT/../GodotPSV/godot-master/bin/libgodot.so}"
export VITASDK="${VITASDK:-/usr/local/vitasdk}"
export PATH="$VITASDK/bin:$PATH"
if [[ ! -s "$SOURCE" ]]; then
  echo "Missing newly built engine runtime: $SOURCE" >&2
  exit 2
fi
TEMP="$ROOT/runtime/libgodot.so.incoming"
trap 'rm -f "$TEMP"' EXIT
cp "$SOURCE" "$TEMP"
arm-vita-eabi-strip --strip-unneeded "$TEMP"
python3 - "$TEMP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
data=p.read_bytes()
assert data[:4]==b'\x7fELF', 'Input runtime is not an ELF'
assert b'[vita-worker] caller outside pool' in data, 'Expected WorkerThreadPool fix missing'
assert b'[vita-pad] init driver=' in data, 'Expected Vita input integration missing'
print('Runtime verified: size',len(data))
PY
mv "$TEMP" "$ROOT/runtime/libgodot.so"
echo "Runtime refreshed. Rebuild VPK with tools/build.sh"
