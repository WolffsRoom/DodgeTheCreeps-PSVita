# Godot 4 Vita audio testing

The game uses 48-kHz stereo PCM assets and a native Godot4Vita AudioServer
runtime, not OpenAL. The new runtime adapts DeltaruneVita's SCE BGM output
port usage, configured with 72% hardware gain and automatic leveling off.
The original DeltaruneVita project was inspected read-only.

## Physical Vita checklist

- Compare music on speakers and headphones for static/crackle.
- Confirm 50%, 75%, 100% volume in Settings; watch for music clipping
  when a death effect or other sound plays simultaneously.
- Confirm music loops without click or a silent dropout.
- Inspect ux0:data/godot_loader.log for [vita-audio] route= and
  output_failed, if present.
- Report whether the audio stays clean for several minutes.

Builds and host checks are not confirmation of clean real-device audio.
See engine documentation at
https://github.com/WolffsRoom/godot4-vita/blob/main/platform/vita/AUDIO_BACKEND.md
