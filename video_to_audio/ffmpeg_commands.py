"""FFmpeg command construction and binary path detection."""

import sys
import os
from pathlib import Path
from typing import List

from .config import (
    AUDIO_CODEC,
    AUDIO_BITRATE,
    SILENCE_THRESHOLD,
    SILENCE_DURATION,
    TARGET_LUFS,
    LOUDNESS_RANGE,
    TRUE_PEAK
)


def get_ffmpeg_path() -> str:
    """
    Get path to ffmpeg binary (bundled or local).

    When running as PyInstaller executable, uses sys._MEIPASS.
    When running as script, uses relative path to ffmpeg directory.

    Returns:
        Path to ffmpeg executable

    Raises:
        FileNotFoundError: If ffmpeg binary not found
        OSError: If running on unsupported platform
    """
    # Determine base path
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        base_path = Path(sys._MEIPASS)
    else:
        # Running as script - go up from this file to repo root
        base_path = Path(__file__).parent.parent

    # Determine platform-specific path
    if sys.platform == 'win32':
        ffmpeg = base_path / 'ffmpeg' / 'windows' / 'ffmpeg.exe'
    elif sys.platform == 'darwin':
        ffmpeg = base_path / 'ffmpeg' / 'macos' / 'ffmpeg'
    elif sys.platform == 'linux':
        # For Linux, try to use system ffmpeg
        ffmpeg = Path('ffmpeg')
        if not os.path.exists('/usr/bin/ffmpeg') and not os.path.exists('/usr/local/bin/ffmpeg'):
            # If system ffmpeg not found, try bundled version
            ffmpeg = base_path / 'ffmpeg' / 'linux' / 'ffmpeg'
    else:
        raise OSError(f'Unsupported platform: {sys.platform}')

    # For system ffmpeg on Linux, just return the command name
    if sys.platform == 'linux' and str(ffmpeg) == 'ffmpeg':
        return 'ffmpeg'

    # Check if bundled binary exists
    if not ffmpeg.exists():
        raise FileNotFoundError(
            f'FFmpeg binary not found at {ffmpeg}. '
            f'Please ensure ffmpeg is bundled correctly.'
        )

    return str(ffmpeg)


def build_base_conversion_command(
    ffmpeg_path: str,
    input_file: str,
    output_file: str,
    audio_track: int
) -> List[str]:
    """
    Build basic video-to-audio conversion command.

    Args:
        ffmpeg_path: Path to ffmpeg executable
        input_file: Input video file path
        output_file: Output audio file path
        audio_track: Audio track number (1-based, e.g., 1, 2, 3)

    Returns:
        Command as list of strings for subprocess
    """
    # Convert 1-based track number to 0-based index for ffmpeg
    track_index = audio_track - 1

    command = [
        ffmpeg_path,
        '-i', input_file,
        '-vn',  # No video
        '-c:a', AUDIO_CODEC,  # Audio codec
        '-b:a', AUDIO_BITRATE,  # Audio bitrate
        '-map', f'0:a:{track_index}',  # Select audio track
        '-y',  # Overwrite without asking
        output_file
    ]

    return command


def build_silence_removal_command(
    ffmpeg_path: str,
    input_file: str,
    output_file: str
) -> List[str]:
    """
    Build command to remove silence from audio.

    Removes audio below threshold that lasts more than specified duration.

    Args:
        ffmpeg_path: Path to ffmpeg executable
        input_file: Input audio file path
        output_file: Output audio file path

    Returns:
        Command as list of strings for subprocess
    """
    # Build silence removal filter
    silence_filter = (
        f'silenceremove='
        f'stop_periods=-1:'  # Remove all silence periods
        f'stop_duration={SILENCE_DURATION}:'  # Minimum silence duration
        f'stop_threshold={SILENCE_THRESHOLD}'  # Threshold for silence
    )

    command = [
        ffmpeg_path,
        '-i', input_file,
        '-af', silence_filter,  # Audio filter
        '-c:a', AUDIO_CODEC,
        '-b:a', AUDIO_BITRATE,
        '-y',
        output_file
    ]

    return command


def build_normalization_command(
    ffmpeg_path: str,
    input_file: str,
    output_file: str
) -> List[str]:
    """
    Build command to normalize audio to target LUFS.

    Uses single-pass loudnorm filter for simplicity.

    Args:
        ffmpeg_path: Path to ffmpeg executable
        input_file: Input audio file path
        output_file: Output audio file path

    Returns:
        Command as list of strings for subprocess
    """
    # Build loudnorm filter (single-pass)
    loudnorm_filter = (
        f'loudnorm='
        f'I={TARGET_LUFS}:'  # Target integrated loudness
        f'LRA={LOUDNESS_RANGE}:'  # Loudness range
        f'TP={TRUE_PEAK}'  # True peak
    )

    command = [
        ffmpeg_path,
        '-i', input_file,
        '-af', loudnorm_filter,  # Audio filter
        '-c:a', AUDIO_CODEC,
        '-b:a', AUDIO_BITRATE,
        '-y',
        output_file
    ]

    return command
