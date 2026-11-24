import json
import subprocess
from pathlib import Path

import whisper


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

MODEL = None

KEYWORDS = [
    "amazing", "incredible", "crazy", "insane",
    "secret", "surprising", "shocking", "never",
    "first time", "biggest", "smallest", "million",
    "billion", "money", "future", "technology",
    "dangerous", "beautiful", "impossible",
    "why", "how", "what if", "actually",
    "wow", "look at", "the best"
]


def get_model():
    global MODEL
    if MODEL is None:
        MODEL = whisper.load_model("tiny")
    return MODEL


def run_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr[-4000:] or "FFmpeg gagal memproses video."
        )

    return result


def transcribe_video(video_path, progress=None, output_dir=None):
    output_dir = Path(output_dir or RESULTS)
    output_dir.mkdir(parents=True, exist_ok=True)

    if progress:
        progress("Membaca audio dan membuat transkrip...")

    result = get_model().transcribe(
        str(video_path),
        fp16=False,
        verbose=False
    )

    segments = result.get("segments", [])

    if not segments:
        raise RuntimeError("Transkrip tidak ditemukan.")

    with open(output_dir / "transcript.json", "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=4)

    with open(output_dir / "transcript.txt", "w", encoding="utf-8") as f:
        f.write(result.get("text", ""))

    return segments


def score_text(text):
    lower = text.lower()

    score = sum(3 for word in KEYWORDS if word in lower)
    score += text.count("!") * 2
    score += text.count("?")

    if len(text.split()) >= 45:
        score += 2

    return score


def analyze_moments(segments, clip_count, duration, output_dir=None):
    output_dir = Path(output_dir or RESULTS)
    output_dir.mkdir(parents=True, exist_ok=True)

    total_duration = max(float(s["end"]) for s in segments)
    candidates = []

    step = max(5, duration // 3)
    start = 0

    while start < total_duration:
        end = min(start + duration, total_duration)

        selected = [
            s for s in segments
            if float(s["start"]) < end
            and float(s["end"]) > start
        ]

        text = " ".join(s["text"].strip() for s in selected)

        if len(text.split()) >= 10:
            candidates.append({
                "start": start,
                "end": end,
                "score": score_text(text),
                "text": text
            })

        start += step

    candidates.sort(key=lambda x: x["score"], reverse=True)

    chosen = []

    for item in candidates:
        overlaps = any(
            item["start"] < old["end"]
            and item["end"] > old["start"]
            for old in chosen
        )

        if not overlaps:
            chosen.append(item)

        if len(chosen) >= clip_count:
            break

    if not chosen:
        raise RuntimeError("Tidak ditemukan momen yang cukup panjang.")

    chosen.sort(key=lambda x: x["start"])

    with open(output_dir / "moments.txt", "w", encoding="utf-8") as f:
        f.write("HASIL ANALISIS MOMEN VIDEO\n\n")

        for i, item in enumerate(chosen, 1):
            f.write(
                f"MOMEN {i}\n"
                f"Mulai: {item['start']:.1f}\n"
                f"Akhir: {item['end']:.1f}\n"
                f"Skor: {item['score']}\n"
                f"Transkrip: {item['text']}\n\n"
            )

    return chosen


def make_clip(video_path, item, index, duration, output_dir=None):
    output_dir = Path(output_dir or RESULTS)
    output_dir.mkdir(parents=True, exist_ok=True)

    name = f"clip_{index:02d}_auto"
    output = output_dir / f"{name}.mp4"

    actual_duration = min(
        duration,
        item["end"] - item["start"]
    )

    filter_complex = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=20:10[bg];"
        "[fg]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
    )

    run_command([
        "ffmpeg", "-y",
        "-ss", str(item["start"]),
        "-i", str(video_path),
        "-t", str(actual_duration),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output)
    ])

    return name, output, actual_duration


def make_word_srt(segments, clip_start, clip_duration, output):
    lines = []
    counter = 1

    def stamp(seconds):
        ms = round(seconds * 1000)
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)

        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    for segment in segments:
        for word in segment.get("words", []):
            start = float(word["start"]) - clip_start
            end = float(word["end"]) - clip_start

            start = max(0, start)
            end = min(clip_duration, end)

            text = word.get("word", "").strip()

            if not text or end <= start:
                continue

            lines.extend([
                str(counter),
                f"{stamp(start)} --> {stamp(end)}",
                text,
                ""
            ])

            counter += 1

    output.write_text("\n".join(lines), encoding="utf-8-sig")


def burn_subtitles(video_path, srt_path, output_path):

    def ass_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60

        return f"{h}:{m:02d}:{s:05.2f}"

    def srt_seconds(value):
        hh, mm, rest = value.split(":")
        ss, ms = rest.split(",")

        return (
            int(hh) * 3600
            + int(mm) * 60
            + int(ss)
            + int(ms) / 1000
        )

    lines = srt_path.read_text(
        encoding="utf-8-sig"
    ).strip().splitlines()

    ass_content = """[Script Info]
Title: CLIPER AI Subtitle
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,28,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,1,2,0,2,30,30,700,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    for i in range(0, len(lines), 4):
        if i + 2 >= len(lines):
            continue

        times = lines[i + 1].split(" --> ")

        start = srt_seconds(times[0])
        end = srt_seconds(times[1])

        word = lines[i + 2].replace("{", "").replace("}", "")

        ass_content += (
            f"Dialogue: 0,{ass_time(start)},"
            f"{ass_time(end)},Default,,0,0,0,,{word}\n"
        )

    ass_path = output_path.with_name(
        output_path.stem + ".ass"
    )

    ass_path.write_text(ass_content, encoding="utf-8")

    ass_filter_path = (
        ass_path.resolve()
        .as_posix()
        .replace(":", r"\:")
        .replace("'", r"\'")
        .replace(",", r"\,")
        .replace("[", r"\[")
        .replace("]", r"\]")
    )

    run_command([
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"ass=filename='{ass_filter_path}'",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-c:a", "copy",
        str(output_path)
    ])


def process_video(
    video_path,
    clip_count=5,
    duration=45,
    progress=None,
    output_dir=None
):
    video_path = Path(video_path)
    output_dir = Path(output_dir or RESULTS)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not video_path.exists():
        raise FileNotFoundError("Video sumber tidak ditemukan.")

    segments = transcribe_video(
        video_path,
        progress,
        output_dir
    )

    if progress:
        progress("Menganalisis momen terbaik berdasarkan transkrip...")

    moments = analyze_moments(
        segments,
        clip_count,
        duration,
        output_dir
    )

    results = []

    for index, item in enumerate(moments, 1):

        if progress:
            progress(f"Membuat video {index} dari {len(moments)}...")

        name, clip_path, actual_duration = make_clip(
            video_path,
            item,
            index,
            duration,
            output_dir
        )

        if progress:
            progress(f"Membuat subtitle video {index}...")

        subtitle_result = get_model().transcribe(
            str(clip_path),
            fp16=False,
            word_timestamps=True,
            verbose=False
        )

        srt_path = output_dir / f"{name}_words.srt"

        make_word_srt(
            subtitle_result.get("segments", []),
            0,
            actual_duration,
            srt_path
        )

        final_path = output_dir / f"{name}_FINAL.mp4"

        if progress:
            progress(f"Memasang subtitle video {index}...")

        burn_subtitles(
            clip_path,
            srt_path,
            final_path
        )

        results.append(final_path)

    return results
