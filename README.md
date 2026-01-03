# Bulk Audio Converter

_Batch-convert a folder of video (or audio files) to .m4a audio format for passive listening. Useful for extracting audio from lectures, tutorials, and other educational content. Optionally normalize audio or trim non-spoken portions._

## Quick Start
Download the exe from the [url](https://github.com/SagaSkoyere/Bulk-Passive-Listening/releases), and simply run! You'll be prompted for the directory of your video files, asked whether you want to normalize audio (make loud parts quieter/soft parts louder), and whether you want to remove non-spoken portions from the video*.

*In my testing, "compressing" the audio from a show or anime episode typically removes somewhere from 15-35% of the clip's runtime.

## Features

- **Batch Processing**: Convert all videos in a directory at once
- **Format Support**: .mp4, .mov, .avi, .mkv, .webm, and 15+ other formats
- **Audio Processing**:
  - Silence removal using FFmpeg or ML-based speech detection (TEN VAD)
  - Audio normalization to -16 LUFS for consistent volume
  - Multi-track audio selection
- **Standalone**: Pre-bundled executable with all dependencies (no installation required)

## Processing Options

### Silence Removal

Removes quiet sections (below -55dB for >1.2 seconds):
- **FFmpeg method**: Fast, reliable, threshold-based
- **TEN VAD ML method**: More accurate speech detection with 1-second buffer

### Audio Normalization

Adjusts loudness to -16 LUFS for consistent volume across files. Applied after silence removal.

### Audio Track Selection

Choose which audio track to extract (useful for multi-language videos or commentary tracks).

## System Requirements

- Windows 10+ (64-bit), macOS 10.13+, or Linux
- Disk space: ~150-600MB for executable (depending on ML support) + output files
- All dependencies bundled in executable

## Supported Formats

.mp4, .mov, .avi, .mkv, .webm, .flv, .wmv, .m4v, .mpg, .mpeg, .3gp, .ogv, .ts, .mts, .m2ts, .vob, .divx, .f4v

## For Developers

### Run from Source

```bash
python video_to_audio_converter.py
```

Requires Python 3.8+ and FFmpeg.

### Build Executable

```bash
pip install pyinstaller
pyinstaller video_to_audio.spec
```

See BUILD_INSTRUCTIONS.md for details.

## Troubleshooting

- **No video files found**: Check directory path and supported formats
- **Directory not accessible**: Verify path and permissions; use quotes for paths with spaces
- **Conversion fails**: File may be corrupted or lack audio track; try different track number

## Limitations

- Only processes files in specified directory (not subdirectories)
- Overwrites existing .m4a files
- Silence removal may cut intentionally quiet audio
