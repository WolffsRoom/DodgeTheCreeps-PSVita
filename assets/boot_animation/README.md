# Godot 4 Vita - alternative chewing loading

Built using the original ../../Godot-4-Vita.svg and its PNG references.
Does not overwrite the first loading animation.

6 seconds / 30fps / seamless loop / 960x544.
00-0.55: face; 0.55-2.0: chewing; 2.0-3.1: mouth opens and logo emerges;
3.1-4.05: full GODOT / VITA logo; 4.05-5.15: text shrinks and jaw closes;
5.15-6.00: closed face.

Exports: loading_mastigando.mp4, loading_mastigando.gif, frames/ (180 PNGs),
frames_mastigando_960x544.zip, preview_etapas.png and individual stage previews.
To regenerate: python render_alt_chew.py from the animation folder.
On PS Vita, stream frames rather than preloading all 960x544 PNGs into RAM.
