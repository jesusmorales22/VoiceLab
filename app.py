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

    if filtro=="Filtro 1":
        resultado=aplicar_bitcrusher(audio,sr,bits=4)

    elif filtro=="Filtro 2":
        resultado=aplicar_chopper(audio,sr,velocidad=20)

    elif filtro=="Filtro 3":
        resultado=aplicar_stutter(audio,sr)

    elif filtro=="Filtro 4":
        resultado=aplicar_robot(audio,sr)

    elif filtro=="Filtro 5":
        resultado=aplicar_downsampling(audio,sr,reduccion=15)
        
    elif filtro=="Filtro 6":
        resultado=aplicar_downsampling(audio,sr,reduccion=15)
        
    elif filtro=="Filtro 7":
        resultado=aplicar_downsampling(audio,sr,reduccion=15)    
        
    elif filtro=="Filtro 8":
        resultado=aplicar_downsampling(audio,sr,reduccion=15)

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