"""Video to audio conversion logic with multi-step processing."""

import subprocess
import sys
from pathlib import Path
from typing import Tuple

from .ffmpeg_commands import (
    get_ffmpeg_path,
    build_base_conversion_command,
    build_silence_removal_command,
    build_normalization_command
)
from .file_utils import get_output_path, get_temp_path


def convert_video_to_audio(
    input_path: str,
    preferences: dict
) -> Tuple[bool, str]:
    """
    Convert video file to audio with optional processing.

    Handles multi-step processing based on user preferences:
    1. Base conversion (always)
    2. Silence removal (optional)
    3. Normalization (optional, always after silence removal)

    Args:
        input_path: Path to input video file
        preferences: Dict with keys:
            - remove_silence: bool
            - normalize_audio: bool
            - audio_track: int (1-based)

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    temp_files = []

    try:
        ffmpeg_path = get_ffmpeg_path()
        output_path = get_output_path(input_path)

        remove_silence = preferences.get('remove_silence', False)
        normalize_audio = preferences.get('normalize_audio', False)
        audio_track = preferences.get('audio_track', 1)

        # Determine processing pipeline
        if remove_silence and normalize_audio:
            # Three steps: convert -> silence -> normalize
            temp1 = get_temp_path(output_path, 1)
            temp2 = get_temp_path(output_path, 2)
            temp_files = [temp1, temp2]

            # Step 1: Base conversion
            cmd = build_base_conversion_command(
                ffmpeg_path, input_path, temp1, audio_track
            )
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Base conversion failed: {error}"

            # Step 2: Remove silence
            cmd = build_silence_removal_command(ffmpeg_path, temp1, temp2)
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Silence removal failed: {error}"

            # Step 3: Normalize
            cmd = build_normalization_command(ffmpeg_path, temp2, output_path)
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Normalization failed: {error}"

            return True, ""

        elif remove_silence:
            # Two steps: convert -> silence
            temp1 = get_temp_path(output_path, 1)
            temp_files = [temp1]

            # Step 1: Base conversion
            cmd = build_base_conversion_command(
                ffmpeg_path, input_path, temp1, audio_track
            )
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Base conversion failed: {error}"

            # Step 2: Remove silence
            cmd = build_silence_removal_command(ffmpeg_path, temp1, output_path)
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Silence removal failed: {error}"

            return True, ""

        elif normalize_audio:
            # Two steps: convert -> normalize
            temp1 = get_temp_path(output_path, 1)
            temp_files = [temp1]

            # Step 1: Base conversion
            cmd = build_base_conversion_command(
                ffmpeg_path, input_path, temp1, audio_track
            )
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Base conversion failed: {error}"

            # Step 2: Normalize
            cmd = build_normalization_command(ffmpeg_path, temp1, output_path)
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Normalization failed: {error}"

            return True, ""

        else:
            # Single step: just convert
            cmd = build_base_conversion_command(
                ffmpeg_path, input_path, output_path, audio_track
            )
            success, error = run_ffmpeg_command(cmd)
            if not success:
                return False, f"Conversion failed: {error}"

            return True, ""

    except Exception as e:
        return False, str(e)

    finally:
        # Always cleanup temporary files
        cleanup_temp_files(temp_files)


def run_ffmpeg_command(command: list) -> Tuple[bool, str]:
    """
    Execute ffmpeg command using subprocess.

    Args:
        command: Command as list of strings

    Returns:
        Tuple of (success: bool, error_message: str)
    """
    try:
        # Prepare subprocess arguments
        kwargs = {
            'capture_output': True,
            'text': True
        }

        # On Windows, hide console window for cleaner UX
        if sys.platform == 'win32':
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(command, **kwargs)

        if result.returncode == 0:
            return True, ""
        else:
            # Extract meaningful error from stderr
            error_msg = result.stderr.strip()
            # Get last few lines which usually contain the actual error
            error_lines = error_msg.split('\n')
            relevant_error = '\n'.join(error_lines[-5:]) if len(error_lines) > 5 else error_msg
            return False, relevant_error

    except FileNotFoundError:
        return False, "FFmpeg binary not found"
    except Exception as e:
        return False, str(e)


def cleanup_temp_files(file_paths: list):
    """
    Remove temporary files.

    Args:
        file_paths: List of file paths to remove
    """
    for path in file_paths:
        try:
            Path(path).unlink(missing_ok=True)
        except Exception:
            # Silently ignore cleanup errors
            pass
