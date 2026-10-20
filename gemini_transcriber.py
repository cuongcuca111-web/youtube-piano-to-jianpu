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

TRANSCRIPTION_PROMPT = """
You are a master concert pianist, music theorist, and professional sheet music transcriber.
Listen with extreme musical accuracy to the attached audio clip (which is a piano solo/tutorial piece) and transcribe it directly into Jianpu (Numbered Musical Notation / 简谱 / Giản Phổ).

Jianpu Musical Notation Rules:
1. Key Signature:
   - Identify the fundamental musical tonic, e.g. "1=C", "1=D", "1=G", "1=F", "1=Bb".
   - For minor keys, standard Jianpu convention uses the relative major key signature (e.g. D minor uses "1=F" with 6 (D) as tonic).
2. Time Signature & Tempo:
   - Standard time signature (usually "4/4" or "3/4" or "2/4" or "6/8").
   - Tempo in BPM (e.g. 104 BPM).
3. Measure-by-measure transcription:
   - Transcribe at least 12 to 24 consecutive measures starting from the very first sound in this clip.
   - For each measure, provide the Right Hand (Melody in treble) and Left Hand (Bass/Harmony accompaniment).
4. Scale degrees (1..7):
   - 1 = Do, 2 = Re, 3 = Mi, 4 = Fa, 5 = Sol, 6 = La, 7 = Si, 0 = Rest (Dấu nghỉ).
5. Octaves relative to the middle register:
   - 0: middle octave (e.g. 1, 2, 3)
   - 1: high octave (e.g. 1̇, 2̇, 3̇)
   - 2: very high octave (e.g. 1̈)
   - -1: low octave (e.g. 6̣, 5̣)
   - -2: very low octave (e.g. 6̤, 4̤)
6. Note durations (must add up to the total beats in the measure, e.g. 4.0 in 4/4):
   - 4.0: Whole note
   - 2.0: Half note
   - 1.5: Dotted quarter note
   - 1.0: Quarter note
   - 0.5: Eighth note
   - 0.25: Sixteenth note
7. Accurate MIDI Pitch numbers:
   - For example: C4=60, D4=62, E4=64, F4=65, G4=67, A4=69, B4=71, C5=72, D5=74, E5=76, F5=77, G5=79, A5=81.
   - Bass notes: D3=50, Bb2=46, F3=53, C3=48, A2=45.

Return strictly a valid JSON object matching this structure (no markdown fences, just pure JSON):
{
  "title": "Song Title",
  "artist": "Composer / Artist",
  "keySignature": "1=F",
  "timeSignature": "4/4",
  "tempo": 104,
  "measures": [
    {
      "measureNumber": 1,
      "rightHand": [
        {"number": "6", "octave": -1, "duration": 4.0, "display_text": "6̣", "midi": 62}
      ],
      "leftHand": [
        {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50},
        {"number": "6", "octave": -2, "duration": 2.0, "display_text": "6̤", "midi": 50}
      ]
    }
  ]
}
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

    # Slice audio to exact user selection if ffmpeg is available
    if ffmpeg_bin and os.path.exists(ffmpeg_bin) and ((start_time and start_time > 0) or (end_time is not None)):
        start_sec = max(0.0, float(start_time or 0.0))
        duration = 60.0
        if end_time is not None and float(end_time) > start_sec:
            duration = min(90.0, float(end_time) - start_sec)

        temp_dir = os.path.dirname(audio_path)
        temp_slice = os.path.join(temp_dir, f"_slice_{os.getpid()}_{int(start_sec)}_{int(duration)}.m4a")
        cmd = [
            ffmpeg_bin, "-y",
            "-ss", str(round(start_sec, 2)),
            "-i", audio_path,
            "-t", str(round(duration, 2)),
            "-c:a", "aac",
            temp_slice
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(temp_slice) and os.path.getsize(temp_slice) > 1000:
                upload_path = temp_slice
                logger.info(f"Created trimmed audio slice for Gemini: {temp_slice} ({round(duration, 1)}s)")
        except Exception as e:
            logger.warning(f"Could not slice audio for Gemini upload ({e}), using full audio.")

    audio_file = None
    try:
        logger.info(f"Uploading audio file {upload_path} to Gemini Files API...")
        audio_file = client.files.upload(file=upload_path)

        prompt = TRANSCRIPTION_PROMPT
        if song_title:
            prompt += f"\nNote: The title or topic of this piece appears to be: '{song_title}'."

        models_to_try = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
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
                        temperature=0.1
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
