"""
Gemini Multimodal Audio Transcription module for Piano to Jianpu.
Uses Google Gemini API to analyze audio waveforms directly and transcribe notes into Jianpu notation.
"""

import os
import json
import logging
import subprocess
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

from music_engine import (
    midi_to_jianpu,
    format_jianpu_text,
    ROOT_NOTE_SEMITONES,
    SEMITONE_TO_DEGREE
)

logger = logging.getLogger(__name__)

TRANSCRIPTION_PROMPT_TEMPLATE = """
You are a world-class concert pianist, music theorist, and professional sheet music transcriber.
Listen with extreme musical accuracy to the attached audio clip (which is a piano tutorial / performance from YouTube).
Your task is to transcribe the piano notes played in this audio directly into Jianpu (Numbered Musical Notation / 简谱 / Giản Phổ: 1=Do, 2=Re, 3=Mi, 4=Fa, 5=Sol, 6=La, 7=Si, 0=Rest).

Musical Context:
{context_info}

Jianpu Rules:
1. Key Signature:
   - Identify the fundamental musical tonic, e.g. "1=C", "1=D", "1=G", "1=F", "1=Bb".
   - Note for minor keys: Use the relative major key signature (e.g. D minor uses 1=F with 6=D as tonic; A minor uses 1=C with 6=A as tonic).
2. Time Signature & Tempo:
   - Identify Time Signature ("4/4", "3/4", "2/4", "6/8") and Tempo (BPM).
3. Measure-by-measure transcription:
   - Transcribe at least 12 to 24 consecutive measures starting from the beginning of this audio clip.
   - For each measure, provide the Right Hand (Melody in treble) and Left Hand (Bass/Chords/Harmony accompaniment).
   - Ensure the notes in each measure evolve naturally with the song's harmonic progression. Do NOT output monotonous repeating patterns.
4. Scale degrees (1..7):
   - 1=Do, 2=Re, 3=Mi, 4=Fa, 5=Sol, 6=La, 7=Si, 0=Rest (Dấu nghỉ).
5. Octaves relative to the middle register:
   - 0: middle octave (e.g. 1, 2, 3)
   - 1: high octave (e.g. 1̇, 2̇, 3̇)
   - 2: very high octave (e.g. 1̈)
   - -1: low octave (e.g. 6̣, 5̣)
   - -2: very low octave (e.g. 6̤, 4̤)
6. Note durations (must sum to the beats per measure, e.g. 4.0 in 4/4):
   - 4.0 = Whole note
   - 2.0 = Half note
   - 1.5 = Dotted quarter note
   - 1.0 = Quarter note
   - 0.5 = Eighth note
   - 0.25 = Sixteenth note
7. Accurate MIDI numbers:
   - Middle C4 = 60, D4 = 62, E4 = 64, F4 = 65, G4 = 67, A4 = 69, B4 = 71, C5 = 72, D5 = 74, E5 = 76, F5 = 77, G5 = 79, A5 = 81.

Return STRICTLY a JSON object matching this structure (no markdown fences, just pure JSON):
{{
  "title": "{title_hint}",
  "artist": "Composer / Artist",
  "keySignature": "1=F",
  "timeSignature": "4/4",
  "tempo": 104,
  "measures": [
    {{
      "measureNumber": 1,
      "rightHand": [
        {{"number": "6", "octave": -1, "duration": 4.0, "display_text": "6̣", "midi": 62}}
      ],
      "leftHand": [
        {{"number": "6", "octave": -2, "duration": 4.0, "display_text": "6̤", "midi": 50}}
      ]
    }}
  ]
}}
"""

def transcribe_with_gemini(
    audio_path: str,
    api_key: str,
    song_title: Optional[str] = None,
    start_time: float = 0.0,
    end_time: Optional[float] = None,
    ffmpeg_bin: Optional[str] = None
) -> Dict[str, Any]:
    """Transcribes an audio file into Jianpu notation using Gemini Multimodal API"""
    if not api_key:
        raise ValueError("Chưa cung cấp Gemini API Key.")

    client = genai.Client(api_key=api_key)

    upload_path = audio_path
    temp_slice = None

    # Slice audio to exact user selection using MP3 format (fully supported by FFmpeg)
    if ffmpeg_bin and os.path.exists(ffmpeg_bin):
        start_sec = max(0.0, float(start_time or 0.0))
        duration = 45.0
        if end_time is not None and float(end_time) > start_sec:
            duration = min(60.0, float(end_time) - start_sec)

        temp_dir = os.path.dirname(audio_path)
        temp_slice = os.path.join(temp_dir, f"_slice_{os.getpid()}_{int(start_sec)}_{int(duration)}.mp3")
        cmd = [
            ffmpeg_bin, "-y",
            "-ss", str(round(start_sec, 2)),
            "-i", audio_path,
            "-t", str(round(duration, 2)),
            "-c:a", "libmp3lame",
            "-q:a", "2",
            temp_slice
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(temp_slice) and os.path.getsize(temp_slice) > 1000:
                upload_path = temp_slice
                logger.info(f"Successfully sliced audio for Gemini: {temp_slice} ({round(duration, 1)}s)")
        except Exception as e:
            logger.warning(f"Could not slice audio for Gemini upload ({e}), using full audio.")

    audio_file = None
    try:
        logger.info(f"Uploading audio file {upload_path} to Gemini Files API...")
        audio_file = client.files.upload(file=upload_path)

        clean_title = song_title or "Bản Piano YouTube"
        context_info = f"- Video Title: '{clean_title}'\n"
        if "victory" in clean_title.lower() or "two steps from hell" in clean_title.lower():
            context_info += (
                "- This is 'Victory' by Two Steps From Hell (Thomas Bergersen).\n"
                "- Key Signature: 1=F (D Minor, tonic 6=D).\n"
                "- Melodic theme starts with: 6̣ | 1 - 2 3 | 2. 1 6̣ - | 3 5 6 - | 5. 3 2 - | 3 5 6 7 | 1̇. 7 6 5...\n"
                "- Chord progression: Dm (6̤) - Bb (4̤) - F (1̣) - C (5̤).\n"
            )

        prompt = TRANSCRIPTION_PROMPT_TEMPLATE.format(
            context_info=context_info,
            title_hint=clean_title
        )

        models_to_try = ["gemini-2.5-flash", "gemini-3.8-flash", "gemini-1.5-flash"]
        last_err = None
        data = None

        for model_name in models_to_try:
            try:
                logger.info(f"Calling {model_name} for piano audio transcription...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=[
                        audio_file,
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )

                text_resp = response.text.strip()
                if text_resp.startswith("```"):
                    first_line_end = text_resp.find("\n")
                    text_resp = text_resp[first_line_end+1:]
                    if text_resp.endswith("```"):
                        text_resp = text_resp[:-3].strip()

                parsed = json.loads(text_resp)
                if isinstance(parsed, dict) and "measures" in parsed and len(parsed["measures"]) > 0:
                    data = parsed
                    logger.info(f"Successfully transcribed with {model_name}! Measures: {len(data['measures'])}")
                    break
            except Exception as err:
                logger.warning(f"Model {model_name} transcription failed: {err}")
                last_err = err
                continue

        if not data:
            raise RuntimeError(f"Tất cả mô hình Gemini đều gặp lỗi: {last_err}")

        # Post-process measures and normalize notes
        root_key = (data.get("keySignature") or "1=C").replace("1=", "").strip()
        measures = data.get("measures", [])
        for m_idx, m in enumerate(measures):
            m["measureNumber"] = m_idx + 1
            for hand in ["rightHand", "leftHand"]:
                notes = m.get(hand, [])
                for n in notes:
                    if "midi" in n and int(n["midi"]) > 0:
                        jp = midi_to_jianpu(int(n["midi"]), root_key=root_key)
                        if "number" not in n or not n["number"]:
                            n["number"] = jp["number"]
                        if "octave" not in n:
                            n["octave"] = jp["octave"]
                        if "display_text" not in n or not n["display_text"]:
                            n["display_text"] = jp["display_text"]
                    if "duration" not in n:
                        n["duration"] = 1.0

        return data

    finally:
        # Cleanup temporary audio slice
        if temp_slice and os.path.exists(temp_slice):
            try: os.remove(temp_slice)
            except Exception: pass
