#!/usr/bin/env python3
"""Validate a Dodge Vita VPK against files owned by this workspace."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LIVEAREA = ROOT / "assets" / "LiveArea"
EXPECTED_SIZES = {
    "bg0.png": (840, 500),
    "icon0.png": (128, 128),
    "pic0.png": (960, 544),
    "startup.png": (280, 158),
}
VPK_ASSETS = {
    "bg0.png": "sce_sys/livearea/contents/bg0.png",
    "icon0.png": "sce_sys/icon0.png",
    "pic0.png": "sce_sys/pic0.png",
    "startup.png": "sce_sys/livearea/contents/startup.png",
    "template.xml": "sce_sys/livearea/contents/template.xml",
}
def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def png_size(data: bytes) -> tuple[int, int]:
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "Invalid PNG header"
    assert data[12:16] == b"IHDR", "Invalid PNG IHDR"
    return struct.unpack(">II", data[16:24])

def check(vpk: Path, output: Path, build_id: str) -> None:
    assets_hash = {}
    for name, expected in EXPECTED_SIZES.items():
        data = (LIVEAREA / name).read_bytes()
        assert png_size(data) == expected, (name, png_size(data), expected)
        assets_hash[name] = sha(data)
    xml_data = (LIVEAREA / "template.xml").read_bytes()
    tree = ET.fromstring(xml_data)
    assert tree.attrib.get("style") == "a5"
    assert int(tree.attrib.get("content-rev", "0")) >= 2
    assert tree.findtext(".//livearea-background/image") == "bg0.png"
    assert tree.findtext(".//gate/startup-image") == "startup.png"
    assets_hash["template.xml"] = sha(xml_data)

    with zipfile.ZipFile(vpk) as z:
        assert z.testzip() is None, "CRC verification failed"
        names = set(z.namelist())
        for name, path in VPK_ASSETS.items():
            assert path in names, f"Missing LiveArea package asset: {path}"
            assert z.read(path) == (LIVEAREA / name).read_bytes(), f"Wrong asset: {name}"
        assert b"GDDC40001" in z.read("sce_sys/param.sfo")
        assert z.read("gxm2d.cfg") == b"native-canvas-v2\n"
        boot_file = ROOT / "assets/boot_animation/boot_anim.dat"
        boot_data = boot_file.read_bytes()
        assert z.read("boot_anim.dat") == boot_data, "Wrong bundled native boot animation"
        assert boot_data[:4] == b"DVAN"
        assert struct.unpack("<5I", boot_data[4:24]) == (1, 960, 544, 30, 180)
        offset = 24
        source_frames = ROOT / "assets/boot_animation/frames"
        for index in range(180):
            assert offset + 4 <= len(boot_data)
            (size,) = struct.unpack_from("<I", boot_data, offset)
            offset += 4
            assert size > 0 and offset + size <= len(boot_data)
            assert boot_data[offset:offset+size] == (source_frames / f"{index:04d}.png").read_bytes()
            offset += size
        assert offset == len(boot_data)
        runtime = (ROOT / "runtime/libgodot.so").read_bytes()
        assert z.read("libgodot.so") == runtime, "Packaged runtime differs from pinned runtime"
        game=root_game=ROOT / "game"
        count=0
        for item in game.rglob("*"):
            if not item.is_file():
                continue
            rel = item.relative_to(game)
            if rel.parts[0] == ".godot" and (len(rel.parts)<2 or rel.parts[1] not in ["imported", "uid_cache.bin"]):
                continue
            if item.name in [".gitignore", ".gdignore"]:
                continue
            inner = "game_data/" + rel.as_posix()
            assert inner in names, f"Missing game asset: {inner}"
            assert z.read(inner) == item.read_bytes(), f"Stale game asset: {inner}"
            count += 1
        imported = len([name for name in names if name.startswith("game_data/.godot/imported/")])
        assert imported > 0, "No imported assets - Godot Vita cannot import sources on device"
        assert b"[vita-worker] caller outside pool" in runtime, "Runtime stability fix missing"
        assert b"boot_splash/show_image=false" in z.read("game_data/project.godot")
        assert b"VITA_TRAIL_LIFETIME" in z.read("game_data/player.gd")
        assert b"StartBackdrop" not in z.read("game_data/hud.tscn")
        report = {
          "build_id": build_id,
          "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "status": "built",
          "hardware_result": "not_run",
          "project": "Dodge the Creeps Vita",
          "godot_version": "4.8.dev7",
          "backend": "native-gxm2d",
          "title_id": "GDDC40001",
          "runtime_sha256": sha(runtime),
          "vitagl_sha256": sha((ROOT/"deps/VitaGL/libvitaGL.a").read_bytes()),
          "vpk_sha256": sha(vpk.read_bytes()),
          "vpk_bytes": vpk.stat().st_size,
          "vpk_files": len(names),
          "game_files": count,
          "imported_files": imported,
          "livearea_sha256": assets_hash,
          "livearea_style": "a5",
          "boot_animation": {
             "format": "DVAN1",
             "sha256": sha(boot_data),
             "frames": 180,
             "fps": 30,
             "duration_seconds": 6.0,
             "dimensions": [960, 544],
             "loader_source_sha256": sha((ROOT/"loader/boot_splash.c").read_bytes())
          },
          "vpk_name": vpk.name,
          "test_result": "package verified; hardware not yet tested",
        }
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("VERIFICATION PASS")
    print("Title ID:", report["title_id"])
    print("Game files:", report["game_files"], "Imported:", report["imported_files"])
    print("LiveArea: a5, 5 files confirmed, exact byte match")
    print("Boot animation: 180 exact original frames, 960x544 30 FPS, 6 seconds")
    print("SHA-256:", report["vpk_sha256"])
    print("Manifest:", output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vpk", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--build-id", required=True)
    args = parser.parse_args()
    check(args.vpk, args.output, args.build_id)
