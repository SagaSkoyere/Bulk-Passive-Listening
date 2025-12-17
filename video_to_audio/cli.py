"""Command-line interface for video-to-audio converter."""

import sys
from pathlib import Path
from typing import List, Tuple

from .prompts import get_user_preferences
from .file_utils import find_video_files, validate_directory
from .converter import convert_video_to_audio


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
                print(f"      Status: \u2713 Completed")
            else:
                print(f"      Status: \u2717 FAILED")
                errors.append((video_file.name, error_msg))

        except Exception as e:
            print(f"      Status: \u2717 FAILED")
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


if __name__ == '__main__':
    main()
