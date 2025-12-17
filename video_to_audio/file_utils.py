"""File discovery and path handling utilities."""

import os
from pathlib import Path
from typing import List

from .config import SUPPORTED_VIDEO_EXTENSIONS, OUTPUT_EXTENSION


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
