"""
Music Engine for Jianpu (Numbered Musical Notation)
Converts MIDI, frequencies, and note data into standard Jianpu notation
and handles key transpositions, rhythm quantizations, and MIDI export.
"""

from typing import List, Dict, Any, Optional, Tuple
import math

# Chromatic scale definitions
SEMITONE_TO_DEGREE = {
    0: ("1", ""),
    1: ("1", "#"),
    2: ("2", ""),
    3: ("2", "#"),  # or b3
    4: ("3", ""),
    5: ("4", ""),
    6: ("4", "#"),  # or b5
    7: ("5", ""),
    8: ("5", "#"),  # or b6
    9: ("6", ""),
    10: ("6", "#"), # or b7
    11: ("7", "")
}

ROOT_NOTE_SEMITONES = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4,
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11
}

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def midi_to_note_name(midi_number: int) -> str:
    """Returns note name with octave, e.g. 60 -> C4"""
    octave = (midi_number // 12) - 1
    note = NOTE_NAMES[midi_number % 12]
    return f"{note}{octave}"

def note_name_to_midi(note_name: str) -> int:
    """Converts e.g. C4 -> 60, F#4 -> 66, Bb3 -> 58"""
    note = note_name[:-1]
    octave = int(note_name[-1])
    semitone = ROOT_NOTE_SEMITONES.get(note, 0)
    return (octave + 1) * 12 + semitone

def midi_to_freq(midi_number: int) -> float:
    """Converts MIDI note to frequency in Hz (A4 = 440 Hz = MIDI 69)"""
    return 440.0 * (2.0 ** ((midi_number - 69) / 12.0))

def midi_to_jianpu(midi_number: int, root_key: str = "C") -> Dict[str, Any]:
    """
    Converts a MIDI note number (e.g. 60 = C4) to Jianpu representation
    based on the key signature (default 1=C).
    Returns dict:
      number: '1'..'7'
      accidental: '#' or 'b' or ''
      octave_dot: 0 (middle), 1 (high), 2 (very high), -1 (low), -2 (very low)
      display_html: formatted text with dots above/below
    """
    if midi_number <= 0:
        return {
            "number": "0",
            "accidental": "",
            "octave": 0,
            "display_text": "0",
            "name": "Rest"
        }

    root_semi = ROOT_NOTE_SEMITONES.get(root_key, 0)
    # Pitch class relative to root
    pitch_class = (midi_number - root_semi) % 12
    degree_info = SEMITONE_TO_DEGREE.get(pitch_class, ("1", ""))
    num, acc = degree_info

    # Determine octave relative to root in octave 4
    # Middle C (60) in 1=C is degree 1, octave 0
    ref_root_midi = 60 + root_semi
    octave_offset = (midi_number - ref_root_midi) // 12

    # Formatting display with unicode combining dots
    # \u0307 is combining dot above, \u0323 is combining dot below
    display_str = acc + num
    if octave_offset == 1:
        display_str = acc + num + "\u0307"
    elif octave_offset == 2:
        display_str = acc + num + "\u0308"
    elif octave_offset == -1:
        display_str = acc + num + "\u0323"
    elif octave_offset <= -2:
        display_str = acc + num + "\u0324"

    return {
        "number": num,
        "accidental": acc,
        "octave": octave_offset,
        "display_text": display_str,
        "midi": midi_number,
        "note_name": midi_to_note_name(midi_number),
        "freq": round(midi_to_freq(midi_number), 2)
    }

def format_jianpu_text(song_data: Dict[str, Any]) -> str:
    """Formats full song into a clean, copyable Jianpu text document"""
    title = song_data.get("title", "Bản nhạc Piano")
    key = song_data.get("keySignature", "1=C")
    time_sig = song_data.get("timeSignature", "4/4")
    tempo = song_data.get("tempo", 80)
    measures = song_data.get("measures", [])

    lines = []
    lines.append(f"==================================================")
    lines.append(f" SHEET NHẠC GIẢN PHỔ (JIANPU / ĐÔ=1, RÊ=2, MI=3)")
    lines.append(f" Bài hát: {title}")
    lines.append(f" Giọng: {key}   |   Nhịp: {time_sig}   |   Tốc độ: {tempo} BPM")
    lines.append(f"==================================================\n")

    current_line = "| "
    measures_per_line = 4

    for idx, m in enumerate(measures):
        rh_notes = m.get("rightHand", [])
        m_notes_str = []
        for n in rh_notes:
            txt = n.get("display_text") or n.get("textNotation") or str(n.get("number", "0"))
            dur = float(n.get("duration", 1.0))
            if dur >= 4.0:
                txt += " - - -"
            elif dur >= 3.0:
                txt += " - -"
            elif dur >= 2.0:
                txt += " -"
            elif dur == 1.5:
                txt += "."
            elif dur <= 0.25:
                txt += "‗"
            elif dur <= 0.5:
                txt += "_"
            m_notes_str.append(txt)

        measure_str = " ".join(m_notes_str) + " | "
        current_line += measure_str

        if (idx + 1) % measures_per_line == 0:
            lines.append(current_line)
            current_line = "| "

    if current_line.strip() != "|":
        lines.append(current_line)

    lines.append("\nChú thích:")
    lines.append("- Dấu chấm trên đầu (1̇, 2̇...): Quãng tám cao (+1 Octave)")
    lines.append("- Dấu chấm dưới chân (1̣, 2̣...): Quãng tám trầm (-1 Octave)")
    lines.append("- Gạch nối ngang (-): Ngân dài thêm 1 phách (ví dụ: 1 - là nốt trắng)")
    lines.append("- Gạch dưới (_): Móc đơn (1/2 phách), (‗): Móc kép (1/4 phách)")
    lines.append("- Số 0: Dấu lặng (Nghỉ)")

    return "\n".join(lines)
