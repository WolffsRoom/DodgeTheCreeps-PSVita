<p align="center">
  <img src="https://github.com/user-attachments/assets/3c75bfe2-4e3b-49a8-a242-21ca991c89f1" alt="Dodge the Creeps on PS Vita" width="900">
</p>

<p align="center">
  Port of <strong>Dodge the Creeps</strong> for the PlayStation Vita.
</p>

A native PlayStation Vita port of Godot's **Dodge the Creeps** demo, using [Godot 4 Vita](https://github.com/WolffsRoom/godot4-vita) (4.8-dev7, native GXM 2D). 

Original gameplay, audio and controller support were confirmed functional on real hardware. The latest settings menu and animated loading screen have passed build/host tests but still need a new physical-Vita check.

## Features

- D-pad/analog movement: **X or START** to begin and **Triangle** to open settings.
- Speed (250/400/550 px/s), master volume (0–100%) and FPS cap (30/45/60); preferences persist. **Circle** closes the menu.
- Background colors change progressively with score.

## Screenshots

<p align="center">
  <a href="assets/prints/2026-10-13-030730-125858.png"><img src="assets/prints/2026-10-13-030730-125858.png" alt="Dodge the Creeps Vita screenshot 1" width="48%"></a>
  <a href="assets/prints/2026-10-13-030732-845114.png"><img src="assets/prints/2026-10-13-030732-845114.png" alt="Dodge the Creeps Vita screenshot 2" width="48%"></a>
</p>
<p align="center">
  <a href="assets/prints/2026-10-13-030736-649110.png"><img src="assets/prints/2026-10-13-030736-649110.png" alt="Dodge the Creeps Vita screenshot 3" width="48%"></a>
  <a href="assets/prints/2026-10-13-030748-394306.png"><img src="assets/prints/2026-10-13-030748-394306.png" alt="Dodge the Creeps Vita screenshot 4" width="48%"></a>
</p>

## Build

Requires [VitaSDK](https://vitasdk.org), CMake, Python 3, a Godot 4.8 host executable to import assets, and a matching engine/VitaGL build from [godot4-vita](https://github.com/WolffsRoom/godot4-vita). Follow the [engine build guide](https://github.com/WolffsRoom/godot4-vita/blob/main/platform/vita/BUILDING.md) first.

Place `GodotPSV/` and `DodgeCreepsVita/` as sibling folders. From WSL Ubuntu:

```bash
bash tools/setup_engine.sh
bash tools/test_host.sh
bash tools/build.sh
```

Or run `./build.ps1` in PowerShell. The VPK is generated under `releases/latest/dodge_the_creeps_vita.vpk`. Engine binaries, VitaGL libraries, asset-import caches and compiled VPKs are not committed; the build recreates them locally.

## Source layout

| Path | Purpose |
|---|---|
| `game/` | Godot scenes, scripts, original audio/art and imports |
| `loader/` | Vita native executable and loading animation |
| `assets/LiveArea/` | Icon, backgrounds and a5 layout |
| `assets/boot_animation/frames/` | 180 original 960×544 PNG frames |
| `tools/`, `tests/` | Build/setup/verification and host regressions |

## Credits

- [Godot Engine](https://godotengine.org) and [Dodge the Creeps](https://github.com/godotengine/godot-demo-projects/tree/master/2d/dodge_the_creeps).
- [WolffsRoom/godot4-vita](https://github.com/WolffsRoom/godot4-vita) for the Vita engine/backend, based on [VitaSDK](https://vitasdk.org), [VitaGL](https://github.com/Rinnegatamante/vitagl) and [kuBridge](https://github.com/TheOfficialFloW/kuBridge).
- Original game, fonts and library licenses are retained in their respective folders.
