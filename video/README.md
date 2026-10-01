# Product and onboarding explainer

Original eight-scene animation, narrated with the Windows Microsoft Zira Desktop voice. The render uses the existing bot illustrations, animated organization diagrams and assignment/policy cards. It does not record private workspaces or simulate live agent execution.

The 5–10 minute figure is the requested **guided onboarding target**, for a configured organization and active employee accounts. It is not a measured benchmark or a claim that external systems are integrated in that time. The QA batch assignment and verification flow follows `docs/admin-agent-assignments.md` in the product repository. Broader templates and connected execution remain labeled as future work.

## Edit and render

1. Edit `storyboard.json`, including the narration and captions.
2. On Windows, run `powershell -NoProfile -File video/narrate.ps1` to synthesize local narration files. Change `voice` to another installed English voice if desired.
3. Run `python video/render.py` with Pillow, numpy and FFmpeg available. Set `FFMPEG_BINARY` to an official FFmpeg executable, or install `imageio-ffmpeg==0.6.0` to locate one.
4. Review the scene preview JPEGs and render metadata in ignored `video/generated/` before publishing.

The export is 1920×1080, 24 fps, H.264/AAC, with fast-start playback. Output files in `public/assets/`: MP4, poster JPEG, English WebVTT/SRT captions and plain-text transcript. Generated WAVs and render previews stay out of Git. The website embeds the film with native controls, captions and an expandable transcript, without autoplay.
