import sounddevice as sd
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt

# PROYECTO DE AFINADOR

# Lee un audio, lo descompone por fft, se fija cual es la frecuencia de mayor amplitud y la muestra.
# ¿Como hacer para indicarle que esta un poquito pasado de x nota?
# Armamos Intervalos: Falta/la nota/Pasado (tension)

# Diccionario: partiendo de A=440 Entonces A=55. Diccionarios
#
#lista = []
#for i in range (1,5):
#    for j in range (0,12):
#        lista.append(round(i*55*(2**(j/12)),2))


lista = []

for j in range(0, 72):
    lista.append(round(55*(2**(j/12)), 2))


notas = {}
notas["A"] = [lista[0], lista[12], lista[24], lista[36], lista[48]]
notas["A#"] = [lista[1], lista[13], lista[25], lista[37], lista[49]]
notas["B"] = [lista[2], lista[14], lista[26], lista[38], lista[50]]
notas["C"] = [lista[3], lista[15], lista[27], lista[39], lista[51]]
notas["C#"] = [lista[4], lista[16], lista[28], lista[40], lista[52]]
notas["D"] = [lista[5], lista[17], lista[29], lista[41], lista[53]]
notas["D#"] = [lista[6], lista[18], lista[30], lista[42], lista[54]]
notas["E"] = [lista[7], lista[19], lista[31], lista[43], lista[55]]
notas["F"] = [lista[8], lista[20], lista[32], lista[44], lista[56]]
notas["F#"] = [lista[9], lista[21], lista[33], lista[45], lista[57]]
notas["G"] = [lista[10], lista[22], lista[34], lista[46], lista[58]]
notas["G#"] = [lista[11], lista[23], lista[35], lista[47], lista[59]]


# Audio
#Audio, fs = sf.read("piano_mf_A5.wav")
#O


def nota():
    fs = 44100  # N° de muestras
    N = 2*fs  # cantidad de muestras = 2 seg
    canales = 2
    Audio = sd.rec(N, fs, canales)  # graba por 5 seg
    sd.wait()  # Espera a que termine de grabar para seguir leyendo el codigo
    Audio = Audio[:, 0]
    #fft
    time = np.arange(Audio.size)/fs
    spectrum = np.abs(np.fft.rfft(Audio))
    # =spectrum = Sprectrum/np.max(spectrum)
    spectrum = spectrum/np.max(spectrum)
    # plt.figure()
    # plt.plot(spectrum)
    #spectrum[0]= 0
    Freq = np.fft.rfftfreq(len(Audio), 1/fs)

    Freqlist = Freq.tolist()
    speclist = spectrum.tolist()
    M = speclist.index(1.0)
    resultado = round(Freqlist[M], 2)

    notaslista = list(notas.items())

    for j in range(0, 12):
        for i in range(0, 4):
            if (notaslista[j][1][i]/1.01) < resultado < (notaslista[j][1][i]*1.01):
                print("La nota es: ", notaslista[j][0])
                print(resultado, "Hz")
            elif (notaslista[j][1][i]/(2**(1/24))) < resultado < (notaslista[j][1][i]):
                print(">>> para ", notaslista[j][0])
            elif (notaslista[j][1][i]) < resultado < (notaslista[j][1][i]*(2**(1/24))):
                print("<<< para ", notaslista[j][0])
            
#Loop eterno de esuchas de 2 segundos, hasta que no se interrumpa sigue.

# nota()
try:
    while True:
        nota()
except KeyboardInterrupt: #ctrl+C to interrupt
    pass


#for j in ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]:
#    for i in notas[j]:
#        if (i/1.01)<resultado<(i*1.01):
#            print(i)

#plt.figure(1)
#plt.plot(Freq,spectrum)
#plt.xlim([lista[0],lista[-1]])
#plt.xticks(lista,listastr)
#plt.grid()
#listastr = []
#for i in range(0,len(lista)):
#    listastr.append(str(lista[i]))
