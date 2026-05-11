import numpy as np
from scipy.signal import butter, lfilter
import scipy.io.wavfile as wav



#Compresor: Controlar los picos de volumen (usando DynamicsCompressorNode). #Esta función tiene el objetivo de que el audio no sature.
# Busca el valor más alto del audio y si se pasa de volumen, lo divide
# para que se quede en un rango seguro.

def normalizar(audio):

    maximo = np.max(np.abs(audio))
    if maximo > 1:

        audio = audio / maximo
    
    return audio 

def aplicar_bitcrusher(audio, sr, bits=4):
    # Reducimos los niveles de volumen a solo 16 pasos (2^4)
    niveles = 2**bits
    audio_8bit = np.round(audio * niveles) / niveles
    return normalizar(audio_8bit)


def aplicar_downsampling(audio, sr, reduccion=10):
    # 'reduccion' indica cada cuántas muestras cogemos una.
    # Si es 10, el audio tendrá 10 veces menos detalle.
    audio_nuevo = np.copy(audio)
    for i in range(0, len(audio), reduccion):
        # Cogemos un valor y lo repetimos durante el bloque
        audio_nuevo[i : i + reduccion] = audio[i]
    return normalizar(audio_nuevo)


def aplicar_chopper(audio, sr, velocidad=10):
    # Creamos una onda cuadrada (0 y 1) para mutear el audio a trozos
    t = np.arange(len(audio)) / sr
    mudo = (np.sin(2 * np.pi * velocidad * t) > 0).astype(float)
    return audio * mudo

def aplicar_robot(audio, sr, f=400):
    # Multiplicamos el audio por una frecuencia pura de 400Hz
    t = np.arange(len(audio)) / sr
    modulador = np.sin(2 * np.pi * f * t)
    return normalizar(audio * modulador)

def aplicar_stutter(audio, sr, segundos_trozo=0.1):
    # Calculamos cuántos puntos de audio son 0.1 segundos
    muestras = int(segundos_trozo * sr)
    nuevo = np.copy(audio)
    
    # Vamos saltando por el audio de 4 en 4 trozos
    for i in range(0, len(audio) - muestras * 4, muestras * 4):
        # Guardamos el trocito actual
        trozo = audio[i : i + muestras]
        # Lo pegamos en las siguientes posiciones para que "tartamudee"
        nuevo[i + muestras : i + muestras * 2] = trozo
        nuevo[i + muestras * 2 : i + muestras * 3] = trozo
        nuevo[i + muestras * 3 : i + muestras * 4] = trozo
        
    return nuevo


# Pruebas
# archivo_entrada = "singing.wav" 


#     # 1. Leer el audio
# sr, audio = wav.read(archivo_entrada)

#     # Convertir a float y asegurar que sea MONO (un solo canal)
# audio = audio.astype(np.float32) / 32768.0
# if len(audio.shape) > 1:
#         audio = audio[:, 0]

    
    
  
# v_bit = aplicar_bitcrusher(audio, sr, bits=2) 
# wav.write("1_audio_bitcrusher.wav", sr, v_bit)

   
# v_chop = aplicar_chopper(audio, sr, velocidad=20)
# wav.write("2_audio_chopper.wav", sr, v_chop)


# v_rect = aplicar_stutter(audio, sr)
# wav.write("3_audio_stutter.wav", sr, v_rect)

# v_rob = aplicar_robot(audio, sr, f=600)
# wav.write("4_audio_robot.wav", sr, v_rob)

# v_ruido = aplicar_downsampling(audio, sr, reduccion=20)
# wav.write("5_audio_downsimpling.wav", sr, v_ruido)