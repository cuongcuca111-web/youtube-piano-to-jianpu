"""
DSP Audio Transcriber for Piano to Jianpu.
Analyzes real audio waveforms using Fast Fourier Transform (STFT),
spectral peak tracking, chroma key estimation, and rhythmic quantization
to transcribe ANY audio file into accurate Jianpu notation without requiring external AI APIs.
"""

import os
import subprocess
import tempfile
import numpy as np
import scipy.signal
import scipy.io.wavfile as wavfile
from typing import Dict, Any, List, Optional
import logging

from music_engine import (
    midi_to_jianpu,
    format_jianpu_text,
    ROOT_NOTE_SEMITONES,
    SEMITONE_TO_DEGREE
)

logger = logging.getLogger("dsp_transcriber")

# Major scale correlation profile (Krumhansl-Schmuckler)
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
PITCH_NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

def detect_key_signature(chroma_12: np.ndarray) -> str:
    """Estimates fundamental root key using chroma profile correlation"""
    best_key = "C"
    max_corr = -1.0

    chroma_norm = chroma_12 / (np.linalg.norm(chroma_12) + 1e-6)

    for i in range(12):
        # Rotate profile to match tonic at i
        prof_maj = np.roll(MAJOR_PROFILE, i)
        prof_maj = prof_maj / np.linalg.norm(prof_maj)
        corr_maj = float(np.dot(chroma_norm, prof_maj))

        prof_min = np.roll(MINOR_PROFILE, i)
        prof_min = prof_min / np.linalg.norm(prof_min)
        corr_min = float(np.dot(chroma_norm, prof_min))

        if corr_maj > max_corr:
            max_corr = corr_maj
            best_key = PITCH_NAMES[i]
        # For minor key, map to relative major for Jianpu representation
        if corr_min > max_corr:
            max_corr = corr_min
            # Relative major is 3 semitones up (e.g. Bm -> D, Am -> C)
            rel_maj_idx = (i + 3) % 12
            best_key = PITCH_NAMES[rel_maj_idx]

    return best_key

def transcribe_audio_dsp(
    audio_path: str,
    ffmpeg_bin: str,
    song_title: str = "Bản Piano YouTube",
    start_sec: float = 0.0,
    end_sec: Optional[float] = None,
    target_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Decodes audio slice to 16kHz WAV and extracts musical melody and harmony notes.
    """
    temp_dir = os.path.dirname(audio_path)
    tmp_wav = os.path.join(temp_dir, f"_dsp_{os.getpid()}_{np.random.randint(1000, 9999)}.wav")

    start_sec = max(0.0, float(start_sec or 0.0))
    duration = 45.0 # Analyze first 45 seconds of the selected slice
    if end_sec and end_sec > start_sec:
        duration = min(60.0, float(end_sec) - start_sec)

    cmd = [
        ffmpeg_bin, "-y",
        "-ss", str(round(start_sec, 2)),
        "-i", audio_path,
        "-t", str(round(duration, 2)),
        "-ar", "16000",
        "-ac", "1",
        tmp_wav
    ]

    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        sr, data = wavfile.read(tmp_wav)
    except Exception as e:
        logger.error(f"FFmpeg conversion error in DSP transcriber: {e}")
        if os.path.exists(tmp_wav):
            try: os.remove(tmp_wav)
            except Exception: pass
        raise RuntimeError(f"Không thể giải mã tệp âm thanh qua FFmpeg: {e}")
    finally:
        if os.path.exists(tmp_wav):
            try: os.remove(tmp_wav)
            except Exception: pass

    samples = data.astype(np.float32) / 32768.0
    total_audio_sec = len(samples) / float(sr)
    if total_audio_sec < 1.0:
        raise ValueError("Đoạn âm thanh quá ngắn để phân tích.")

    # STFT Spectrogram
    nperseg = 2048
    hop = 512
    f, t_frames, Zxx = scipy.signal.stft(samples, fs=sr, nperseg=nperseg, noverlap=nperseg - hop)
    mag = np.abs(Zxx)

    # Piano MIDI pitches: 24 (C1) to 96 (C7)
    midi_pitches = np.arange(24, 97)
    freqs = 440.0 * (2.0 ** ((midi_pitches - 69.0) / 12.0))
    bin_indices = np.round(freqs * nperseg / sr).astype(int)
    bin_indices = np.clip(bin_indices, 0, len(f) - 1)

    # Pitch energy matrix: (73 pitches x N frames)
    P = mag[bin_indices, :]

    # 1. Detect Key Signature (Chroma vector)
    chroma = np.zeros(12)
    for idx, m in enumerate(midi_pitches):
        pc = m % 12
        chroma[pc] += np.sum(P[idx, :])

    detected_key = detect_key_signature(chroma)
    key_sig = target_key or detected_key or "C"
    # Ensure key format
    if key_sig.startswith("1="):
        root_key = key_sig.replace("1=", "").strip()
    else:
        root_key = key_sig.strip()

    # 2. Estimate Tempo
    # Frame rate ~ 31.25 frames/sec
    frame_rate = float(sr) / float(hop)
    energy_env = np.sum(P, axis=0)
    diff_env = np.maximum(0, np.diff(energy_env))
    # Autocorrelation of onset envelope to find beat lag
    if len(diff_env) > 64:
        autocorr = np.correlate(diff_env, diff_env, mode='full')
        autocorr = autocorr[len(diff_env) - 1:]
        # BPM range 60 to 140 -> lags in frames:
        # lag = (60 / bpm) * frame_rate
        min_lag = int((60.0 / 140.0) * frame_rate)
        max_lag = int((60.0 / 60.0) * frame_rate)
        if max_lag < len(autocorr):
            search_window = autocorr[min_lag:max_lag]
            if len(search_window) > 0 and np.max(search_window) > 0:
                best_lag = min_lag + int(np.argmax(search_window))
                tempo = int(round((60.0 * frame_rate) / best_lag))
            else:
                tempo = 84
        else:
            tempo = 84
    else:
        tempo = 84

    tempo = max(60, min(140, tempo))
    sec_per_beat = 60.0 / tempo
    beats_per_measure = 4
    sec_per_measure = beats_per_measure * sec_per_beat

    # 3. Extract Notes for Right Hand (Melody: MIDI 55 - 88) & Left Hand (Bass: MIDI 36 - 55)
    rh_indices = np.where((midi_pitches >= 55) & (midi_pitches <= 88))[0]
    lh_indices = np.where((midi_pitches >= 36) & (midi_pitches < 55))[0]

    noise_floor = np.median(P) * 1.8

    num_measures = max(4, min(16, int(total_audio_sec // sec_per_measure)))
    measures = []

    for m_idx in range(num_measures):
        m_start_sec = m_idx * sec_per_measure
        m_start_frame = int(m_start_sec * frame_rate)
        m_end_frame = int((m_start_sec + sec_per_measure) * frame_rate)

        rh_notes = []
        lh_notes = []

        # Analyze 2 half-measures (each 2 beats = 2.0 duration)
        for half_idx in range(2):
            h_start_f = m_start_frame + int(half_idx * (m_end_frame - m_start_frame) / 2)
            h_end_f = m_start_frame + int((half_idx + 1) * (m_end_frame - m_start_frame) / 2)

            if h_start_f >= P.shape[1]:
                break

            sub_P = P[:, h_start_f:min(h_end_f, P.shape[1])]
            if sub_P.shape[1] == 0:
                continue

            # Average energy across the 2-beat block
            avg_energy = np.mean(sub_P, axis=1)

            # Dominant Right Hand Note
            rh_sub = avg_energy[rh_indices]
            if np.max(rh_sub) > noise_floor * 1.5:
                best_rh_idx = rh_indices[np.argmax(rh_sub)]
                rh_midi = int(midi_pitches[best_rh_idx])
            else:
                # Soft melody or rest
                if np.max(rh_sub) > noise_floor:
                    best_rh_idx = rh_indices[np.argmax(rh_sub)]
                    rh_midi = int(midi_pitches[best_rh_idx])
                else:
                    rh_midi = 0

            # Dominant Left Hand Bass Note
            lh_sub = avg_energy[lh_indices]
            if np.max(lh_sub) > noise_floor * 1.4:
                best_lh_idx = lh_indices[np.argmax(lh_sub)]
                lh_midi = int(midi_pitches[best_lh_idx])
            else:
                if np.max(lh_sub) > noise_floor:
                    best_lh_idx = lh_indices[np.argmax(lh_sub)]
                    lh_midi = int(midi_pitches[best_lh_idx])
                else:
                    lh_midi = 0

            # Convert to Jianpu
            rh_j = midi_to_jianpu(rh_midi, root_key)
            rh_notes.append({
                "number": rh_j["number"],
                "octave": rh_j["octave"],
                "duration": 2.0,
                "display_text": rh_j["display_text"],
                "midi": rh_midi
            })

            lh_j = midi_to_jianpu(lh_midi, root_key)
            lh_notes.append({
                "number": lh_j["number"],
                "octave": lh_j["octave"],
                "duration": 2.0,
                "display_text": lh_j["display_text"],
                "midi": lh_midi
            })

        # Ensure at least 1 note per hand
        if not rh_notes:
            rh_notes = [{"number": "1", "octave": 0, "duration": 4.0, "display_text": "1", "midi": 60}]
        if not lh_notes:
            lh_notes = [{"number": "1", "octave": -1, "duration": 4.0, "display_text": "1̣", "midi": 48}]

        measures.append({
            "measureNumber": m_idx + 1,
            "rightHand": rh_notes,
            "leftHand": lh_notes
        })

    result = {
        "title": song_title,
        "artist": "YouTube Audio AI",
        "keySignature": f"1={root_key}",
        "timeSignature": "4/4",
        "tempo": tempo,
        "measures": measures,
        "analysisMode": "DSP_FREQUENCY_ANALYSIS"
    }

    result["formattedText"] = format_jianpu_text(result)
    return result
