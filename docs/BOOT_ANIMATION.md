# Boot animation - Godot Vita / Dodge the Creeps

## Player sequence

1. The PS Vita displays sce_sys/pic0.png (owned by the shell).
2. The eboot launcher starts its dedicated boot_splash thread.
3. The thread opens app0:boot_anim.dat (the exact 180 original PNG frames
   from GodotPSV/Load/animation/alternativa_mastigando), initializes
   Vita2D and renders the full-screen sequence.
4. Meanwhile, the main thread loads, relocates and resolves libgodot.so.
5. The splash thread completes at least one 6-second cycle. If engine
   loading takes longer, the sequence loops seamlessly.
6. The splash thread releases its reusable GPU texture, CPU buffer, PNG
   package, and Vita2D context. Only then Godot initializes native GXM.
7. The game scene opens without Godot's default static boot logo.

This is a real pre-engine loading animation, not a timer inside the game.

## Frame assets

- Native source: assets/boot_animation/frames/0000.png through 0179.png
- 960x544 RGB8 images, 30 FPS, 6 seconds.
- User's reference MP4, GIF, and logo are retained alongside the frames.
- tools/pack_boot_animation.py creates boot_anim.dat and frame_manifest.json.
- Frames are stored as compressed original PNG bytes (DVAN v1 container).
- The loader decodes one frame into a single persistent 960x544 Vita2D
  texture, never uploading 180 textures simultaneously.
- Frame pacing derives from sceKernelGetProcessTimeWide; late frames can be
  skipped to maintain the intended animation duration.

## Logs

The Vita loader writes its status to ux0:data/godot_loader.log:

    [boot-anim] loader animation thread=1
    [boot-anim] begin 960x544 180 frames 30fps (during runtime loading)
    [boot-anim] finished frames_displayed=...; releasing GPU before Godot
    [boot-anim] handoff to Godot engine

Failure paths log the missing asset, unsupported texture, or PNG decode
problem and continue launch where possible.

## LiveArea

The template is style a5, revision 2. The original icon0, bg0, pic0 and
startup PNG assets are unchanged. The native animation only starts once
the eboot runs; LiveArea itself remains static.

## Validation

- 180 bundled PNGs confirmed byte-identical to their source files.
- All 180 decoded using libpng's simplified RGBA API on the Linux host.
- Native boot_splash.c compiled and linked into the Vita eboot.
- VPK contains boot_anim.dat, a5 template, correct Title ID, and exact assets.
- Hardware video output, frame rate, and GPU handoff: not yet tested on Vita.

If a reinstalled app displays the old LiveArea layout, close its LiveArea
and refresh/restart the Vita shell because the shell can cache LiveArea
content for an installed title.
