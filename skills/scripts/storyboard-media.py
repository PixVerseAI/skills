#!/usr/bin/env python3
"""Local storyboard splitting and clip composition; no network or generation."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def tool(name):
    path = shutil.which(name)
    if not path:
        raise ValueError(f"Required tool not found: {name}")
    return path


def run(args):
    return subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE).stdout


def source(path):
    path = Path(path).resolve()
    if not path.is_file():
        raise ValueError(f"Input file not found: {path}")
    return path


def split(image, directory):
    image = source(image)
    magick = shutil.which("magick")
    convert = [magick] if magick else [tool("convert")]
    identify = [magick, "identify"] if magick else [tool("identify")]
    dimensions = run(identify + ["-format", "%w %h", str(image)]).split()
    if len(dimensions) != 2:
        raise ValueError("Expected one storyboard image, not multiple frames")
    width, height = map(int, dimensions)
    if width < 2 or height < 2:
        raise ValueError("Storyboard must be at least 2 by 2 pixels")
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    x, y = width // 2, height // 2
    rectangles = [(x, y, 0, 0), (width-x, y, x, 0),
                  (x, height-y, 0, y), (width-x, height-y, x, y)]
    outputs = []
    try:
        for i, (w, h, left, top) in enumerate(rectangles, 1):
            output = directory / f"shot{i}.png"
            run(convert + [str(image), "-crop", f"{w}x{h}+{left}+{top}",
                           "+repage", str(output)])
            if not output.is_file():
                raise ValueError(f"Image tool did not create {output}")
            outputs.append(str(output))
    except BaseException:
        # mkdir above succeeded exclusively: never clean an existing caller directory.
        shutil.rmtree(directory)
        raise
    return {"frames": outputs}


def probe(path, ffprobe):
    result = json.loads(run([ffprobe, "-v", "error", "-show_streams",
                             "-show_format", "-of", "json", str(path)]))
    videos = [s for s in result.get("streams", []) if s.get("codec_type") == "video"]
    if not videos:
        raise ValueError(f"No video stream: {path}")
    duration = videos[0].get("duration")
    if duration in (None, "N/A"):
        duration = result.get("format", {}).get("duration")
    try:
        duration = float(duration)
    except (TypeError, ValueError):
        raise ValueError(f"Cannot determine video duration: {path}") from None
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"Invalid video duration: {path}")
    audio = any(s.get("codec_type") == "audio" for s in result.get("streams", []))
    return duration, audio


def concat(output, clips, width, height, fps):
    if width <= 0 or height <= 0 or width % 2 or height % 2 or fps <= 0:
        raise ValueError("Width/height must be positive even integers; fps must be positive")
    if not clips:
        raise ValueError("At least one clip is required")
    output = Path(output).resolve()
    if output.exists():
        raise ValueError(f"Output already exists: {output}")
    if output.suffix.lower() != ".mp4":
        raise ValueError("Output must have an .mp4 suffix")
    clips = [source(p) for p in clips]
    ffmpeg, ffprobe = tool("ffmpeg"), tool("ffprobe")
    metadata = [probe(p, ffprobe) for p in clips]
    has_audio = any(audio for _, audio in metadata)
    args = [ffmpeg, "-nostdin", "-v", "error", "-y"]
    for clip in clips:
        args.extend(["-i", str(clip)])
    filters, streams = [], []
    for i, (duration, audio) in enumerate(metadata):
        filters.append(f"[{i}:v:0]setpts=PTS-STARTPTS,"
                       f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                       f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
                       f"setsar=1,fps={fps},format=yuv420p[v{i}]")
        streams.append(f"[v{i}]")
        if has_audio:
            if audio:
                filters.append(f"[{i}:a:0]asetpts=PTS-STARTPTS,aresample=48000,"
                               f"aformat=channel_layouts=stereo,apad,"
                               f"atrim=duration={duration}[a{i}]")
            else:
                filters.append(f"anullsrc=r=48000:cl=stereo,"
                               f"atrim=duration={duration},asetpts=PTS-STARTPTS[a{i}]")
            streams.append(f"[a{i}]")
    filters.append("".join(streams) + f"concat=n={len(clips)}:v=1:a={int(has_audio)}"
                   + "[outv]" + ("[outa]" if has_audio else ""))
    args.extend(["-filter_complex", ";".join(filters), "-map", "[outv]"])
    if has_audio:
        args.extend(["-map", "[outa]", "-c:a", "aac", "-b:a", "192k"])
    args.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "18"])
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".storyboard-", suffix=".mp4", dir=output.parent)
    os.close(fd)
    try:
        run(args + [temporary])
        if Path(temporary).stat().st_size == 0:
            raise ValueError("ffmpeg produced an empty output")
        # Publish without overwriting even if another process created the destination.
        os.link(temporary, output)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return {"file": str(output), "clips": len(clips), "audio": has_audio}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    crop = commands.add_parser("split", help="Split a 2x2 grid using ImageMagick 6 or 7")
    crop.add_argument("image")
    crop.add_argument("directory", help="New directory for shot1.png through shot4.png")
    join = commands.add_parser("concat", help="Join clips, preserving available audio")
    join.add_argument("output")
    join.add_argument("clips", nargs="+")
    join.add_argument("--width", type=int, default=1280)
    join.add_argument("--height", type=int, default=720)
    join.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()
    try:
        if args.command == "split":
            result = split(args.image, args.directory)
        else:
            result = concat(args.output, args.clips, args.width, args.height, args.fps)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"storyboard-media: {error}\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
