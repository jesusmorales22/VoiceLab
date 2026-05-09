import numpy as np


def aplicar_reverse(audio, sr):
    # Invierte la señal en el tiempo
    return np.flip(audio, axis=0)


def aplicar_playback_rate(audio, sr, rate=1.0):
    # Cambia la velocidad de reproducción
    if rate <= 0:
        raise ValueError("El parámetro rate debe ser mayor que 0")

    indices = np.arange(0, len(audio), rate)
    indices = indices[indices < len(audio)].astype(int)

    return audio[indices]


def aplicar_panning(audio, sr, pan=0.0):
    # Mueve el audio entre el canal izquierdo y derecho
    pan = np.clip(pan, -1.0, 1.0)

    if audio.ndim == 1:
        audio = np.column_stack((audio, audio))

    left_gain = (1 - pan) / 2
    right_gain = (1 + pan) / 2

    audio_procesado = np.zeros_like(audio)
    audio_procesado[:, 0] = audio[:, 0] * left_gain
    audio_procesado[:, 1] = audio[:, 1] * right_gain

    return audio_procesado


def aplicar_tremolo(audio, sr, frecuencia=5.0, profundidad=0.5):
    # Modula periódicamente la amplitud de la señal
    profundidad = np.clip(profundidad, 0.0, 1.0)

    t = np.arange(len(audio)) / sr
    modulador = 1 - profundidad * (0.5 * (1 + np.sin(2 * np.pi * frecuencia * t)))

    if audio.ndim == 2:
        modulador = modulador[:, np.newaxis]

    return audio * modulador


def aplicar_delay(audio, sr, delay_ms=300, gain=0.4):
    # Añade una copia retardada y atenuada de la señal
    delay_samples = int(sr * delay_ms / 1000)

    if delay_samples <= 0:
        return audio

    audio_procesado = np.copy(audio)

    if audio.ndim == 1:
        audio_procesado[delay_samples:] += gain * audio[:-delay_samples]
    else:
        audio_procesado[delay_samples:, :] += gain * audio[:-delay_samples, :]

    max_val = np.max(np.abs(audio_procesado))
    if max_val > 1:
        audio_procesado = audio_procesado / max_val

    return audio_procesado