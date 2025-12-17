"""User interaction prompts for configuration."""


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


def prompt_remove_silence() -> bool:
    """
    Ask user if they want to remove stretches of silence.

    Returns:
        True if user wants to remove silence, False otherwise
    """
    return prompt_yes_no("Remove stretches of silence?")


def prompt_normalize_audio() -> bool:
    """
    Ask user if they want to normalize audio levels for listening.

    Returns:
        True if user wants to normalize audio, False otherwise
    """
    return prompt_yes_no("Normalize audio levels for listening?")


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

    remove_silence = prompt_remove_silence()
    normalize_audio = prompt_normalize_audio()
    audio_track = prompt_audio_track()

    print()

    return {
        'remove_silence': remove_silence,
        'normalize_audio': normalize_audio,
        'audio_track': audio_track
    }
