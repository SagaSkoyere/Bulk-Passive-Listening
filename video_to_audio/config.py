"""Configuration constants for the video-to-audio converter."""

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

# Temporary file suffixes
TEMP_SUFFIX_1 = '.temp1.m4a'
TEMP_SUFFIX_2 = '.temp2.m4a'
