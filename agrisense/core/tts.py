"""
AgriSense - Multilingual Voice Advisory (Text-to-Speech)
Powered by gTTS (Google Text-to-Speech) supporting both English ('en') and Marathi ('mr').
"""

from functools import lru_cache
from io import BytesIO
from typing import Optional
from gtts import gTTS


@lru_cache(maxsize=64)
def synthesize_advisory_speech(text: str, language: str = "en") -> Optional[bytes]:
    """
    Converts agricultural advisory text into an MP3 audio byte stream.
    
    Args:
        text: Plaintext advisory to read aloud
        language: 'en' for English, 'mr' for Marathi
        
    Returns:
        bytes of MP3 audio or None if offline/error
    """
    if not text or not text.strip():
        return None

    # Truncate to reasonable length for quick spoken summary
    clean_text = text[:450].replace("*", "").replace("#", "").strip()
    if language == "mr":
        lang_code = "mr"
    elif language == "hi":
        lang_code = "hi"
    else:
        lang_code = "en"

    try:
        fp = BytesIO()
        tts = gTTS(text=clean_text, lang=lang_code, slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.getvalue()
    except Exception as e:
        print(f"[AgriSense TTS] Speech generation error: {e}")
        return None
