from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
VIDEO_DIR = BASE_DIR / "Video"

FORMATS = {
    "1": {"name": "MP3", "ext": ".mp3", "codec": ["-c:a", "libmp3lame", "-b:a", "320k"]},
    "2": {"name": "WAV", "ext": ".wav", "codec": ["-c:a", "pcm_s16le"]},
    "3": {"name": "FLAC", "ext": ".flac", "codec": ["-c:a", "flac"]},
    "4": {"name": "AAC", "ext": ".aac", "codec": ["-c:a", "aac", "-b:a", "320k"]},
    "5": {"name": "M4A", "ext": ".m4a", "codec": ["-c:a", "aac", "-b:a", "320k"]},
    "6": {"name": "OGG", "ext": ".ogg", "codec": ["-c:a", "libvorbis", "-q:a", "8"]},
    "7": {"name": "OPUS", "ext": ".opus", "codec": ["-c:a", "libopus", "-b:a", "256k"]},
}

def check_tools():
    for program in ("ffmpeg", "ffprobe"):
        try:
            subprocess.run(
                [program, "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"ERROR: {program} tidak ditemukan.")
            print("Install FFmpeg dan pastikan ffmpeg/ffprobe sudah tersedia di PATH.")
            sys.exit(1)

def is_video(file_path: Path) -> bool:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=codec_type",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(file_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return "video" in result.stdout.lower()
    except Exception:
        return False

def select_format():
    print("\n" + "=" * 60)
    print("           PILIH FORMAT AUDIO OUTPUT")
    print("=" * 60)
    print("[1] MP3  - 320 kbps")
    print("[2] WAV  - PCM Lossless")
    print("[3] FLAC - Lossless")
    print("[4] AAC  - 320 kbps")
    print("[5] M4A  - AAC 320 kbps")
    print("[6] OGG  - Vorbis High Quality")
    print("[7] OPUS - 256 kbps")

    while True:
        choice = input("\nPilih format [1-7]: ").strip()
        if choice in FORMATS:
            return FORMATS[choice]
        print("Pilihan tidak valid. Masukkan angka 1 sampai 7.")

def unique_output(output_dir: Path, video_file: Path, extension: str) -> Path:
    output = output_dir / f"{video_file.stem}{extension}"
    if not output.exists():
        return output

    counter = 2
    while True:
        output = output_dir / f"{video_file.stem}_{counter}{extension}"
        if not output.exists():
            return output
        counter += 1

def convert_video(input_file: Path, output_file: Path, config):
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(input_file),
        "-map", "0:a:0?",
        "-vn",
        *config["codec"],
        str(output_file),
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0 and output_file.exists():
        return True, None

    return False, result.stderr.strip() or "Konversi gagal."

def main():
    print("=" * 60)
    print("        UNIVERSAL VIDEO TO AUDIO CONVERTER")
    print("=" * 60)

    check_tools()

    if not VIDEO_DIR.exists():
        VIDEO_DIR.mkdir(parents=True, exist_ok=True)
        print("\nFolder 'Video' dibuat.")
        print(f"Masukkan file video ke: {VIDEO_DIR}")
        return

    print("\nScanning folder Video...")

    videos = [
        file for file in sorted(VIDEO_DIR.iterdir())
        if file.is_file() and is_video(file)
    ]

    if not videos:
        print("Tidak ada file video yang terdeteksi.")
        return

    print(f"Ditemukan {len(videos)} video.")

    selected = select_format()
    output_dir = BASE_DIR / selected["name"]
    output_dir.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = 0

    print(f"\nOutput format : {selected['name']}")
    print(f"Output folder : {output_dir}\n")

    for index, video in enumerate(videos, start=1):
        output_file = unique_output(output_dir, video, selected["ext"])
        print(f"[{index}/{len(videos)}] {video.name}")

        ok, error = convert_video(video, output_file, selected)

        if ok:
            success += 1
            print(f"  BERHASIL -> {output_file.name}")
        else:
            failed += 1
            print(f"  GAGAL    -> {error}")

    print("\n" + "=" * 60)
    print("SELESAI")
    print("=" * 60)
    print(f"Total    : {len(videos)}")
    print(f"Berhasil : {success}")
    print(f"Gagal    : {failed}")
    print(f"Output   : {output_dir}")

if __name__ == "__main__":
    main()
