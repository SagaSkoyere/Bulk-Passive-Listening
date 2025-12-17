#!/usr/bin/env python3
"""
Video to Audio Converter - Single File Version

A command-line tool that batch-converts video files to audio format (.m4a)
with optional silence removal and normalization.

Usage:
    python video_to_audio_converter.py [directory_path]

For building standalone executable:
    pyinstaller --onefile --name video-to-audio video_to_audio_converter.py --add-data "ffmpeg/windows/ffmpeg.exe;ffmpeg/windows"
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Tuple


# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

# Supported video file extensions
SUPPORTED_VIDEO_EXTENSIONS = {
    '.mp4', '.mov', '.avi', '.mkv', '.webm',
    '.flv', '.wmv', '.m4v', '.mpg', '.mpeg',
    '.3gp', '.ogv', '.ts', '.mts', '.m2ts',
    '.vob', '.divx', '.f4v'
}

# Audio conversion settings
AUDIO_CODEC = 'aac'
AUDIO_BITRATE = '160k'
OUTPUT_EXTENSION = '.m4a'

# Silence removal settings (hardcoded as per requirements)
SILENCE_THRESHOLD = '-55dB'
SILENCE_DURATION = '1.2'

# Normalization settings (hardcoded as per requirements)
TARGET_LUFS = '-16'
LOUDNESS_RANGE = '11'
TRUE_PEAK = '-1.5'


# ============================================================================
# FILE UTILITIES
# ============================================================================

def validate_directory(path: str) -> bool:
    """
    Check if directory exists and is accessible.

    Args:
        path: Directory path to validate

    Returns:
        True if directory exists and is accessible, False otherwise
    """
    path_obj = Path(path)
    return path_obj.exists() and path_obj.is_dir()


def find_video_files(directory_path: str) -> List[Path]:
    """
    Find all video files in the specified directory (non-recursive).

    Args:
        directory_path: Path to directory to search

    Returns:
        List of Path objects for all video files found
    """
    directory = Path(directory_path)
    video_files = []

    if not directory.exists() or not directory.is_dir():
        return video_files

    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS:
            video_files.append(item)

    # Sort by name for consistent processing order
    video_files.sort(key=lambda p: p.name.lower())

    return video_files


def get_output_path(input_path: str) -> str:
    """
    Generate output audio file path from input video path.

    Output file will be in the same directory with the same name
    but with .m4a extension.

    Args:
        input_path: Path to input video file

    Returns:
        Path to output audio file
    """
    input_file = Path(input_path)
    output_file = input_file.with_suffix(OUTPUT_EXTENSION)
    return str(output_file)


def get_temp_path(base_path: str, temp_number: int) -> str:
    """
    Generate temporary file path for intermediate processing.

    Args:
        base_path: Base output path
        temp_number: Temporary file number (1 or 2)

    Returns:
        Path to temporary file
    """
    base = Path(base_path)
    if temp_number == 1:
        return str(base.parent / f"{base.stem}.temp1.m4a")
    elif temp_number == 2:
        return str(base.parent / f"{base.stem}.temp2.m4a")
    else:
        raise ValueError(f"Invalid temp_number: {temp_number}. Must be 1 or 2.")


# ============================================================================
# FFMPEG COMMAND CONSTRUCTION
# ============================================================================

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
        # Running as script - same directory as this script
        base_path = Path(__file__).parent

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


# ============================================================================
# CONVERSION LOGIC
# ============================================================================

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


# ============================================================================
# USER INTERACTION
# ============================================================================

def prompt_yes_no(question: str) -> bool:
    """
    Prompt user for yes/no answer.

    Args:
        question: Question to ask the user

    Returns:
        True if user answers yes, False otherwise
    """
    while True:
        response = input(f"{question} (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'")


def prompt_audio_track() -> int:
    """
    Ask user which audio track to use.

    Returns:
        Audio track number (1-based)
    """
    while True:
        try:
            response = input("Audio track to use (1/2/3): ").strip()
            track = int(response)
            if track >= 1:
                return track
            else:
                print("Please enter a positive number (1, 2, 3, etc.)")
        except ValueError:
            print("Please enter a valid number (1, 2, 3, etc.)")


def get_user_preferences() -> dict:
    """
    Get all user preferences through interactive prompts.

    Returns:
        Dictionary with keys:
            - remove_silence: bool
            - normalize_audio: bool
            - audio_track: int
    """
    print()
    print("Configuration Options:")
    print("-" * 50)

    remove_silence = prompt_yes_no("Remove stretches of silence?")
    normalize_audio = prompt_yes_no("Normalize audio levels for listening?")
    audio_track = prompt_audio_track()

    print()

    return {
        'remove_silence': remove_silence,
        'normalize_audio': normalize_audio,
        'audio_track': audio_track
    }


# ============================================================================
# COMMAND-LINE INTERFACE
# ============================================================================

def get_directory_path() -> str:
    """
    Get and validate directory path from user.

    Accepts path from command-line argument or prompts user interactively.

    Returns:
        Validated directory path

    Exits:
        If directory is invalid or not found
    """
    if len(sys.argv) > 1:
        # Use command-line argument
        directory = sys.argv[1]
    else:
        # Prompt user for input
        directory = input("Enter directory path: ").strip()

        # Remove quotes if user wrapped path in quotes
        if directory.startswith('"') and directory.endswith('"'):
            directory = directory[1:-1]
        elif directory.startswith("'") and directory.endswith("'"):
            directory = directory[1:-1]

    # Validate directory
    if not validate_directory(directory):
        print(f"\nError: Directory not found or not accessible: {directory}")
        sys.exit(1)

    print(f"Directory: {directory}")

    return directory


def process_files(
    video_files: List[Path],
    preferences: dict
) -> List[Tuple[str, str]]:
    """
    Process all video files and collect errors.

    Continues processing even if individual files fail.

    Args:
        video_files: List of Path objects for video files
        preferences: User preferences dictionary

    Returns:
        List of tuples (filename, error_message) for failed conversions
    """
    errors = []
    total = len(video_files)

    for i, video_file in enumerate(video_files, 1):
        # Display progress
        print(f"\n[{i}/{total}] Converting: {video_file.name}")
        output_name = video_file.stem + ".m4a"
        print(f"      Output: {output_name}")

        try:
            success, error_msg = convert_video_to_audio(
                str(video_file),
                preferences
            )

            if success:
                print(f"      Status: ✓ Completed")
            else:
                print(f"      Status: ✗ FAILED")
                errors.append((video_file.name, error_msg))

        except Exception as e:
            print(f"      Status: ✗ FAILED")
            errors.append((video_file.name, str(e)))

    return errors


def display_summary(video_files: List[Path], errors: List[Tuple[str, str]]):
    """
    Display processing summary with success/failure counts and error details.

    Args:
        video_files: List of all video files processed
        errors: List of tuples (filename, error_message) for failures
    """
    print()
    print("=" * 60)
    print(" " * 20 + "SUMMARY")
    print("=" * 60)

    successful = len(video_files) - len(errors)
    failed = len(errors)

    print(f"Total files:  {len(video_files)}")
    print(f"Successful:   {successful}")
    print(f"Failed:       {failed}")

    if errors:
        print()
        print("=" * 60)
        print("ERRORS")
        print("=" * 60)

        for filename, error_msg in errors:
            print()
            print(f"File: {filename}")
            print(f"Error:")
            # Indent error message for readability
            for line in error_msg.split('\n'):
                print(f"  {line}")

        print()
        print("=" * 60)

    print()

    if failed == 0:
        print("All files converted successfully!")
    else:
        print(f"Conversion completed with {failed} error(s).")


def main():
    """Main entry point for the CLI application."""
    print("=" * 60)
    print(" " * 15 + "Video to Audio Converter")
    print("=" * 60)
    print()

    # Get directory path
    directory = get_directory_path()

    # Get user preferences
    preferences = get_user_preferences()

    # Find video files
    print("Searching for video files...")
    video_files = find_video_files(directory)

    if not video_files:
        print("\nNo video files found in directory.")
        print("Supported formats: .mp4, .mov, .avi, .mkv, .webm, and more")
        sys.exit(0)

    print(f"\nFound {len(video_files)} video file(s)")
    print()

    # Display processing header
    print("=" * 60)
    print("Processing Files")
    print("=" * 60)

    # Process all files
    errors = process_files(video_files, preferences)

    # Display summary
    display_summary(video_files, errors)


if __name__ == '__main__':
    main()
