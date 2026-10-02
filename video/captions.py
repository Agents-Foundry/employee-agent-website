"""Package the film with a reserved caption strip and concise native captions."""
import json, os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'public/assets'
STEM = 'agents-foundry-movie-v4'
# Keep all scene artwork visible, with 96px for captions and 48px for controls.
LAYOUT = 'scale=1664:936:flags=lanczos,pad=1920:1080:128:96:color=0x18142d,setsar=1'
CUE_SETTINGS = 'line:1.5%,center position:50%,center size:88% align:center'

def stamp(seconds, separator='.'):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{separator}{ms%1000:03}'

def caption_cues(scenes):
    cues = []
    for scene in scenes:
        words = scene['narration'].split()
        groups, group = [], []
        for word in words:
            if group and (len(group) == 5 or len(' '.join(group + [word])) > 32):
                groups.append(group); group = []
            group.append(word)
            if len(group) >= 3 and word.endswith(('.', ',', '?', '!')):
                groups.append(group); group = []
        if group: groups.append(group)
        spoken_duration = scene['duration'] - 1.2
        start = scene['start'] + .45
        for group in groups:
            end = start + spoken_duration * len(group) / len(words)
            cues.append((start, end, ' '.join(group)))
            start = end
    return cues

def export_captions(scenes):
    cues = caption_cues(scenes)
    (ASSETS / (STEM + '.vtt')).write_text('WEBVTT\n\n' + '\n\n'.join(
        f'{stamp(a)} --> {stamp(b)} {CUE_SETTINGS}\n{text}' for a, b, text in cues) + '\n', encoding='utf8')
    (ASSETS / (STEM + '.srt')).write_text('\n\n'.join(
        f'{i+1}\n{stamp(a, ",")} --> {stamp(b, ",")}\n{text}' for i, (a, b, text) in enumerate(cues)) + '\n', encoding='utf8')
    spec = json.loads((ROOT / 'video/storyboard.json').read_text(encoding='utf8'))
    (ASSETS / (STEM + '-transcript.txt')).write_text(spec['title'] + '\n\n' + spec['targetContext'] + '\n\n' +
        '\n\n'.join(s['eyebrow'] + '\n' + s['narration'] for s in scenes), encoding='utf8')

def package_caption_film(source, scenes):
    import imageio_ffmpeg
    ffmpeg = os.environ.get('FFMPEG_BINARY') or imageio_ffmpeg.get_ffmpeg_exe()
    target = ASSETS / (STEM + '.mp4')
    export_captions(scenes)
    subprocess.run([ffmpeg, '-y', '-v', 'error', '-i', str(source), '-vf', LAYOUT,
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p',
        '-c:a', 'copy', '-movflags', '+faststart', str(target)], check=True)
    subprocess.run([ffmpeg, '-y', '-v', 'error', '-ss', '5', '-i', str(target),
        '-frames:v', '1', '-q:v', '2', str(ASSETS / 'onboarding-movie-v4-poster.jpg')], check=True)
    print(f'Packaged caption-safe film: {target.stat().st_size/1048576:.1f} MB', flush=True)
    return target

if __name__ == '__main__':
    info = json.loads((ROOT / 'video/generated/movie-info.json').read_text(encoding='utf8'))
    package_caption_film(ASSETS / 'agents-foundry-movie-v3.mp4', info['scenes'])
