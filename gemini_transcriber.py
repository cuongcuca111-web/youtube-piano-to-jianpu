"""
Gemini Multimodal Audio Transcription module for Piano to Jianpu.
Uses Google Gemini API to analyze audio and transcribe notes directly into Jianpu notation.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

TRANSCRIPTION_PROMPT = """
You are an elite concert pianist, music theorist, and professional sheet music transcriber.
Analyze the attached piano audio track with extreme musical precision and transcribe it into Jianpu (Numbered Musical Notation / 简谱 / Giản Phổ: Đô=1, Rê=2, Mi=3, Pha=4, Sol=5, La=6, Si=7, Dấu nghỉ=0).

Rules for Jianpu Notation:
1. Identify the fundamental musical Key Signature (e.g. "1=C", "1=D", "1=G", "1=F", "1=Bb").
2. Identify Time Signature ("4/4", "3/4", "2/4", "6/8") and Tempo (BPM).
3. Transcribe measure-by-measure for at least 8 to 16 full measures of the main theme/intro/chorus.
4. Scale degrees:
   - 1 = Do, 2 = Re, 3 = Mi, 4 = Fa, 5 = Sol, 6 = La, 7 = Si, 0 = Rest.
5. Octaves relative to the middle register (middle C / tonic C4):
   - 0: middle octave (no dot)
   - 1: high octave (one dot above, e.g. 1̇, 2̇, 3̇)
   - 2: very high octave (two dots above, e.g. 1̈)
   - -1: low octave (one dot below, e.g. 1̣, 5̣)
   - -2: very low octave (two dots below, e.g. 1̤, 5̤)
6. Rhythm durations:
   - 4.0 = Whole note (nốt tròn, 4 beats)
   - 2.0 = Half note (nốt trắng, 2 beats)
   - 1.5 = Dotted quarter note (1.5 beats)
   - 1.0 = Quarter note (nốt đen, 1 beat)
   - 0.5 = Eighth note (móc đơn, 0.5 beat)
   - 0.25 = Sixteenth note (móc kép, 0.25 beat)
7. Separate Right Hand (Melody) and Left Hand (Chords/Bass accompaniment).
8. Ensure each note includes its corresponding approximate MIDI pitch number (e.g. Middle C = 60).

Return ONLY a valid JSON object strictly matching this format (no markdown code blocks, just raw json):
{
  "title": "Song Title",
  "artist": "Composer or Performer",
  "keySignature": "1=C",
  "timeSignature": "4/4",
  "tempo": 76,
  "measures": [
    {
      "measureNumber": 1,
      "rightHand": [
        {
          "number": "1",
          "octave": 0,
          "accidental": "",
          "duration": 1.0,
          "display_text": "1",
          "midi": 60
        }
      ],
      "leftHand": [
        {
          "number": "1",
          "octave": -1,
          "accidental": "",
          "duration": 4.0,
          "display_text": "1̣",
          "midi": 48
        }
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
    end_time: Optional[float] = None
) -> Dict[str, Any]:
    """Transcribes an audio file into Jianpu notation using Gemini API"""
    if not api_key:
        raise ValueError("Chưa cung cấp Gemini API Key.")

    client = genai.Client(api_key=api_key)

    logger.info(f"Uploading audio file {audio_path} to Gemini...")
    audio_file = client.files.upload(file=audio_path)

    prompt = TRANSCRIPTION_PROMPT
    if song_title:
        prompt += f"\nNote: The title or topic of this piece appears to be: '{song_title}'."

    if (start_time and start_time > 0) or (end_time is not None):
        start_min = int(start_time // 60)
        start_sec = int(start_time % 60)
        start_str = f"{start_min}:{start_sec:02d}"
        if end_time is not None:
            end_min = int(end_time // 60)
            end_sec = int(end_time % 60)
            end_str = f"{end_min}:{end_sec:02d}"
        else:
            end_str = "the end"

        prompt += (
            f"\n\nCRITICAL TIMING INSTRUCTION: The user has selected a specific trimmed segment of this audio.\n"
            f"You MUST transcribe ONLY the piano music played between timestamp {start_str} ({start_time} seconds) "
            f"and timestamp {end_str} ({end_time} seconds). Ignore any notes or speech outside this segment."
        )

    logger.info("Calling Gemini 2.5 Flash for audio transcription...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
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
    # Remove markdown code fences if model enclosed in ```json
    if text_resp.startswith("```"):
        first_line_end = text_resp.find("\n")
        text_resp = text_resp[first_line_end+1:]
        if text_resp.endswith("```"):
            text_resp = text_resp[:-3].strip()

    data = json.loads(text_resp)
    return data
