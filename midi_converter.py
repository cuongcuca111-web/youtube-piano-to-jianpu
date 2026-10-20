"""
MIDI Parser and Generator for Jianpu.
Converts standard MIDI files to Jianpu notation and exports Jianpu back to MIDI.
"""

from typing import Dict, Any, List
import mido
from mido import MidiFile, MidiTrack, Message
from music_engine import midi_to_jianpu, ROOT_NOTE_SEMITONES

def parse_midi_to_jianpu(midi_path: str, root_key: str = "C", time_sig: str = "4/4") -> Dict[str, Any]:
    """Parses a MIDI file and converts note events into Jianpu measures"""
    mid = MidiFile(midi_path)
    ticks_per_beat = mid.ticks_per_beat or 480

    # Extract all note events with absolute ticks
    all_notes = []
    current_tempo = 500000 # default 120 bpm

    for i, track in enumerate(mid.tracks):
        abs_tick = 0
        active_notes = {}
        for msg in track:
            abs_tick += msg.time
            if msg.type == 'set_tempo':
                current_tempo = msg.tempo
            elif msg.type == 'note_on' and msg.velocity > 0:
                active_notes[msg.note] = (abs_tick, msg.velocity)
            elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active_notes:
                    start_tick, vel = active_notes.pop(msg.note)
                    duration_ticks = abs_tick - start_tick
                    duration_beats = duration_ticks / ticks_per_beat
                    all_notes.append({
                        "midi": msg.note,
                        "start_tick": start_tick,
                        "duration_beats": max(0.25, round(duration_beats * 4) / 4),
                        "track": i,
                        "velocity": vel
                    })

    # Sort notes chronologically
    all_notes.sort(key=lambda x: x["start_tick"])
    bpm = round(mido.tempo2bpm(current_tempo))

    # Beats per measure
    num_beats = int(time_sig.split("/")[0]) if "/" in time_sig else 4
    ticks_per_measure = num_beats * ticks_per_beat

    # Group notes into measures
    measures_map = {}
    for n in all_notes:
        m_idx = int(n["start_tick"] // ticks_per_measure)
        if m_idx not in measures_map:
            measures_map[m_idx] = []
        measures_map[m_idx].append(n)

    measures = []
    max_measures = min(32, max(measures_map.keys()) + 1 if measures_map else 8)

    for m_num in range(max_measures):
        m_notes = measures_map.get(m_num, [])
        rh_notes = []
        lh_notes = []

        # Separate into right hand (treble > 60) and left hand (bass <= 60)
        for n in m_notes:
            j_note = midi_to_jianpu(n["midi"], root_key=root_key)
            j_note["duration"] = n["duration_beats"]
            if n["midi"] >= 60:
                rh_notes.append(j_note)
            else:
                lh_notes.append(j_note)

        # Fallback if no notes in measure
        if not rh_notes:
            rh_notes.append({
                "number": "0", "octave": 0, "accidental": "",
                "duration": float(num_beats), "display_text": "0", "midi": 0
            })

        measures.append({
            "measureNumber": m_num + 1,
            "rightHand": rh_notes,
            "leftHand": lh_notes
        })

    return {
        "title": "Bản nhạc từ MIDI",
        "keySignature": f"1={root_key}",
        "timeSignature": time_sig,
        "tempo": bpm or 80,
        "measures": measures
    }

def export_jianpu_to_midi(song_data: Dict[str, Any], output_path: str):
    """Exports a Jianpu song data structure to a playable standard MIDI file"""
    mid = MidiFile()
    track_rh = MidiTrack()
    track_lh = MidiTrack()
    mid.tracks.append(track_rh)
    mid.tracks.append(track_lh)

    tempo = int(song_data.get("tempo", 80))
    time_sig = song_data.get("timeSignature", "4/4")
    num_beats = int(time_sig.split("/")[0]) if "/" in time_sig else 4

    ticks_per_beat = 480
    mid.ticks_per_beat = ticks_per_beat
    tempo_us = mido.bpm2tempo(tempo)

    track_rh.append(mido.MetaMessage('set_tempo', tempo=tempo_us, time=0))
    track_rh.append(mido.MetaMessage('track_name', name='Piano Right Hand', time=0))
    track_lh.append(mido.MetaMessage('track_name', name='Piano Left Hand', time=0))

    measures = song_data.get("measures", [])

    # Process right hand
    for m in measures:
        for n in m.get("rightHand", []):
            midi_pitch = int(n.get("midi", 0))
            dur_beats = float(n.get("duration", 1.0))
            dur_ticks = int(dur_beats * ticks_per_beat)

            if midi_pitch > 0:
                track_rh.append(Message('note_on', note=midi_pitch, velocity=85, time=0))
                track_rh.append(Message('note_off', note=midi_pitch, velocity=0, time=dur_ticks))
            else:
                # Rest: add time with dummy note or silence (accumulate delta time)
                track_rh.append(Message('note_on', note=60, velocity=0, time=dur_ticks))

    # Process left hand
    for m in measures:
        for n in m.get("leftHand", []):
            midi_pitch = int(n.get("midi", 0))
            dur_beats = float(n.get("duration", 1.0))
            dur_ticks = int(dur_beats * ticks_per_beat)

            if midi_pitch > 0:
                track_lh.append(Message('note_on', note=midi_pitch, velocity=75, time=0))
                track_lh.append(Message('note_off', note=midi_pitch, velocity=0, time=dur_ticks))
            else:
                track_lh.append(Message('note_on', note=48, velocity=0, time=dur_ticks))

    mid.save(output_path)
    return output_path
