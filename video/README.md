# Product and onboarding explainer

The current film is an eight-scene character story using the exact website bot artwork: `testo.avif`, `fronto.avif` and `producto.avif`. The original transparent images are mapped onto deformable GPU meshes inside a 3D office, preserving their faces, costumes, curls and ears. This is a 2.5D character treatment with walking, arm movement, breathing and floating role icons; the human teammate and environment are 3D geometry. Moving cameras, beveled props, four-sample antialiasing and directional lighting render in a headless OpenGL context. Testo receives a role and boundaries, arrives as separate employee instances, passes verification and encounters policy gates.

Narration uses the Windows Microsoft Zira Desktop voice. The quiet original synthesized score is mixed and ducked beneath speech. The film is an illustrated product story, not a recording of private workspaces or live execution.

The 5–10 minute figure is the requested **guided onboarding target**, for a configured organization and active employee accounts. It is not a measured benchmark or a claim that external systems are integrated in that time. The QA batch assignment and verification flow follows `docs/admin-agent-assignments.md` in the product repository. Broader templates and connected execution remain labeled as future work.

## Edit and render

1. Edit `storyboard.json`, including the narration and captions.
2. On Windows, run `powershell -NoProfile -File video/narrate.ps1` to synthesize local narration files. Change `voice` to another installed English voice if desired.
3. Install the video-only dependencies from `requirements.txt`; they are separate from the website's Node build. A working OpenGL 3.3 graphics driver is required.
4. Run `python video/movie.py --preview-only` to review scene composition, then `python video/movie.py` to render. Set `FFMPEG_BINARY` to an official FFmpeg executable, or use `imageio-ffmpeg==0.6.0` to locate one.
5. To update caption layout without re-rendering the scenes, run `python video/captions.py`; it reads the existing v3 film and render metadata. The full renderer performs this packaging automatically.
6. Review the scene preview JPEGs and render metadata in ignored `video/generated/` before publishing.

The export is 1920×1080, 30 fps, H.264/AAC, with fast-start playback. Versioned `agents-foundry-movie-v4` files in `public/assets/` include MP4, English WebVTT/SRT captions and a plain-text transcript, plus `onboarding-movie-v4-poster.jpg`. Captions use short phrases centered in a dedicated dark strip at the top of the film. The scene artwork is scaled and inset without cropping; a lower strip gives the native controls clearance. Website cue styling uses a responsive font and no text highlighting. Native captions also retain this safe position in fullscreen. Generated WAVs and previews stay out of Git. The website embeds the film with native controls, captions and an expandable transcript, without autoplay.

`render.py` and the earlier `agents-foundry-explainer` assets are retained as the previous graphic-based edition. The website uses the new character film.
