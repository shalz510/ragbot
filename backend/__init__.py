"""
Backend module for RAG Learning Assistant
"""

# Make TTS functions easily importable
try:
    from .tts import (
        text_to_speech,
        text_to_speech_cached,
        text_to_speech_gtts,
        text_to_speech_pyttsx3,
        text_to_speech_edge,
        get_available_voices_pyttsx3,
        get_available_voices_edge
    )
except ImportError:
    # TTS dependencies not installed yet
    pass

__all__ = [
    'text_to_speech',
    'text_to_speech_cached',
    'text_to_speech_gtts',
    'text_to_speech_pyttsx3',
    'text_to_speech_edge',
    'get_available_voices_pyttsx3',
    'get_available_voices_edge'
]