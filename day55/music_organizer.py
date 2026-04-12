"""
Terminal-based music playlist organizer.

Features:
- Scan a music directory (recursively) and read metadata with mutagen.
- Export a CSV summary of the library.
"""

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from mutagen import File

SUPPORTED_EXTENSIONS = {".mp3", ".flac", ".m4a", ".wav", ".ogg", ".aac", ".wma"}


@dataclass
class Track:
    path: Path
    title: str
    artist: str
    album: str
    track_number: Optional[str]
    duration_seconds: Optional[int]


def scan_music(root: Path) -> List[Track]:
    tracks: List[Track] = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            ext = Path(name).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            file_path = Path(dirpath) / name
            track = read_metadata(file_path)
            tracks.append(track)
    return tracks


def read_metadata(path: Path) -> Track:
    audio = File(path)
    tags = audio.tags if audio else {}

    def first(tag_names: Iterable[str], default: str = "Unknown") -> str:
        for t in tag_names:
            if t in tags and tags[t]:
                value = tags[t]
                if isinstance(value, list):
                    if value:
                        return str(value[0])
                else:
                    return str(value)
        return default

    title = first(["TIT2", "TITLE", "\xa9nam"], path.stem)
    artist = first(["TPE1", "ARTIST", "\xa9ART"], "Unknown Artist")
    album = first(["TALB", "ALBUM", "\xa9alb"], "Unknown Album")
    track_number = first(["TRCK", "TRACKNUMBER"], "").split("/")[0] or None

    duration_seconds = int(audio.info.length) if audio and audio.info else None

    return Track(
        path=path,
        title=title.strip(),
        artist=artist.strip(),
        album=album.strip(),
        track_number=track_number.strip() if track_number else None,
        duration_seconds=duration_seconds,
    )


def export_csv(tracks: List[Track], csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "title", "artist", "album", "track_number", "duration_seconds"])
        for t in tracks:
            writer.writerow(
                [
                    str(t.path),
                    t.title,
                    t.artist,
                    t.album,
                    t.track_number or "",
                    t.duration_seconds or "",
                ]
            )
    print(f"CSV exported to {csv_path}")


def main() -> None:
    music_dir = input("Enter the music folder path: ").strip()
    source_root = Path(music_dir).expanduser().resolve()
    if not source_root.exists():
        raise SystemExit(f"Source directory not found: {source_root}")

    csv_name = input("Enter CSV file name (example: library.csv): ").strip() or "library.csv"
    if not csv_name.lower().endswith(".csv"):
        csv_name += ".csv"
    csv_path = source_root / csv_name

    print(f"\nScanning {source_root} ...")
    tracks = scan_music(source_root)
    if not tracks:
        print("No supported audio files found.")
        return
    print(f"Found {len(tracks)} tracks.")

    export_csv(tracks, csv_path)
    print(f"CSV saved at {csv_path}")


if __name__ == "__main__":
    main()
