#!/usr/bin/env python3
"""Build byte-exact native Vita loading frame package from the supplied 180 PNGs.

Format is little-endian DVAN + u32 version/width/height/fps/frame_count
+ repeated {u32 PNG size, PNG bytes} with no alignment. Single texture reused.
"""
from pathlib import Path
import hashlib
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/boot_animation/frames"
OUTPUT = ROOT / "assets/boot_animation/boot_anim.dat"
MANIFEST = ROOT / "assets/boot_animation/frame_manifest.json"
FRAMES = 180
W, H, FPS = 960, 544, 30


def build() -> None:
    frames = sorted(SOURCE.glob("*.png"))
    assert len(frames) == FRAMES, ("Incorrect frame count", len(frames))
    manifest = {
        "origin": "GodotPSV/Load/animation/alternativa_mastigando/frames",
        "frame_count": FRAMES,
        "width": W,
        "height": H,
        "fps": FPS,
        "duration_s": FRAMES / FPS,
        "frames": [],
    }
    with OUTPUT.open("wb") as output:
        output.write(b"DVAN" + struct.pack("<5I", 1, W, H, FPS, FRAMES))
        for i, frame in enumerate(frames):
            assert frame.name == f"{i:04d}.png", frame.name
            data = frame.read_bytes()
            assert data[:8] == b"\x89PNG\r\n\x1a\n"
            assert data[12:16] == b"IHDR"
            assert struct.unpack(">II", data[16:24]) == (W, H)
            assert data[24:26] == bytes((8, 2)), (frame, data[24:26])
            output.write(struct.pack("<I", len(data)))
            output.write(data)
            manifest["frames"].append({
                "name": frame.name,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            })
    manifest["data_sha256"] = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    manifest["size_bytes"] = OUTPUT.stat().st_size
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Boot animation: {FRAMES} frames, {W}x{H}, {FPS} fps, {FRAMES / FPS:.1f}s, {OUTPUT.stat().st_size} bytes")
    print("SHA-256:", manifest["data_sha256"])


if __name__ == "__main__":
    build()
