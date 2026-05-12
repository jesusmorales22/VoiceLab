from flask import Flask,request,send_file,render_template
import io
import numpy as np
import scipy.io.wavfile as wav
from diseño_Audios import *

app=Flask(__name__)

def procesar_audio_en_memoria(file,filtro):
    sr,audio=wav.read(file)

    audio=audio.astype(np.float32)/32768.0

    if len(audio.shape)>1:
        audio=audio[:,0]

    if filtro=="bitcrusher":
        resultado=aplicar_bitcrusher(audio,sr,bits=4)

    elif filtro=="chopper":
        resultado=aplicar_chopper(audio,sr,velocidad=20)

    elif filtro=="stutter":
        resultado=aplicar_stutter(audio,sr)

    elif filtro=="robot":
        resultado=aplicar_robot(audio,sr)

    elif filtro=="downsampling":
        resultado=aplicar_downsampling(audio,sr,reduccion=15)
        
    elif filtro=="reverse":
        resultado=aplicar_reverse(audio,sr)
        
    elif filtro=="playback_rate":
        resultado=aplicar_playback_rate(audio,sr,rate=1.0)    
        
    elif filtro=="panning":
        resultado=aplicar_panning(audio, sr, pan=0.0)
        
    elif filtro=="tremolo":
        resultado=aplicar_tremolo(audio, sr, frecuencia=5.0, profundidad=0.5) 
        
    elif filtro=="delay":
        resultado=aplicar_delay(audio, sr, delay_ms=300, gain=0.4)

    else:
        resultado=audio

    resultado_final=(resultado*32767).astype(np.int16)

    byte_io=io.BytesIO()
    wav.write(byte_io,sr,resultado_final)
    byte_io.seek(0)

    return byte_io

@app.route('/')
def index():
    return render_template('diseño_visual.html')

@app.route('/procesar',methods=['POST'])
def procesar():
    if 'audio' not in request.files:
        return "No hay archivo",400

    archivo=request.files['audio']
    filtro=request.form.get('filtro')

    audio_procesado=procesar_audio_en_memoria(archivo,filtro)

    return send_file(
        audio_procesado,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="audio_modificado.wav"
    )

if __name__=='__main__':
    app.run(debug=True)