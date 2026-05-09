import numpy as np

# Esta función tiene el objetivo de que el audio no sature.
# Busca el valor más alto del audio y si se pasa de volumen, lo divide
#    para que se quede en un rango seguro.
def normalizar(audio):

    maximo = np.max(np.abs(audio))

    if maximo > 1:
        audio = audio / maximo

    return audio


# Esta función es muy simple, simplemente recibe el audio y lo devuelve
#   pero invertido en el tiempo de fin a inicio. 
def aplicar_reverse(audio, sr):

    return audio[::-1]


# El objetivo de esta función es cambiar la velocidad del audio.
# El parámetro rate indica cuanto de acelera o relentiza el audio.
# Creo los indices dejando separación entre ellos de rate.
# Luego aseguro que no estos indices estén dentro del tamaño del audio
#   y los convierto a enteros.
def aplicar_playback_rate(audio, sr, rate=1.0):

    if rate <= 0:
        raise ValueError("El parámetro 'rate' debe ser mayor que 0.")
    
    indices = np.arange(0, len(audio), rate)
    indices = indices[indices < len(audio)].astype(int)

    return audio[indices]


# El objetivo de esta función es mover el audio hacia la izquierda o derecha.
# El parámetro 'pan' indica cuanto se mueve el audio.
# Primero limito el valor de la variable 'pan' entre -1.0 y 1.0.
# Luego comprueba si el audio es mono, para crear dos canales en ese caso.
# Reparto entre ambos canales dependiendo del valor de 'pan'.
def aplicar_panning(audio, sr, pan=0.0):

    pan = np.clip(pan, -1.0, 1.0)

    if audio.ndim == 1:
        audio = np.column_stack((audio, audio))

    ganancia_izquierda = (1 - pan) / 2
    ganancia_derecha = (1 + pan) / 2

    audio_procesado = np.zeros_like(audio)
    audio_procesado[:, 0] = audio[:, 0] * ganancia_izquierda
    audio_procesado[:, 1] = audio[:, 1] * ganancia_derecha

    return normalizar(audio_procesado)


# El objetivo de esta función es subir y bajar el volumen de forma periódica.
# El parámetro 'frecuencia' indica cuantas veces por segundo cambia el volumen.
# El parámetro 'profundidad' indica cuanto cambia el volumen, entre 0.0 y 1.0.
# Primero limite profundidad y creo el eje de tiempo (muestras por segundo).
# Creo la onda senoidal y modulo cómo sube y baja. Adapto el audio si es estéreo. 
def aplicar_tremolo(audio, sr, frecuencia=5.0, profundidad=0.5):
    profundidad = np.clip(profundidad, 0.0, 1.0)

    tiempo = np.arange(len(audio)) / sr
    modulador = 1 - profundidad * (0.5 * (1 + np.sin(2 * np.pi * frecuencia * tiempo)))

    if audio.ndim == 2:
        modulador = modulador[:, np.newaxis]

    audio_procesado = audio * modulador

    return normalizar(audio_procesado)


# El objetivo de esta función es añadir un eco al audio.
# El parámetro 'delay_ms' indica el tiempo de retardo en milisegundos.
# El parámetro 'gain' indica cuanto se atenúa el eco, entre 0.0 y 1.0.
# Primer convertimos ms a muestras, copiamos el audio origual y añadimos
#   la señal retardada. Si el audio es estereo, lo hacemos para ambos canales.
def aplicar_delay(audio, sr, delay_ms=300, gain=0.4):
    delay_muestras = int(sr * delay_ms / 1000)

    if delay_muestras <= 0:
        return audio

    audio_procesado = np.copy(audio)

    if audio.ndim == 1:
        audio_procesado[delay_muestras:] += gain * audio[:-delay_muestras]
    else:
        audio_procesado[delay_muestras:, :] += gain * audio[:-delay_muestras, :]

    return normalizar(audio_procesado)
