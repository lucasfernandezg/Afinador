# -*- coding: utf-8 -*-
"""
Created on Sat May 14 16:26:28 2022

@author: Lucas

Afinador con Interfaz.
"""
import sounddevice as sd
import soundfile as sf
import numpy as np
from AfinadorGUI import Ui_MainWindow
import sys
import os.path
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QMessageBox, QFileDialog)
from PyQt5 import QtCore
import time


class Window(QMainWindow, Ui_MainWindow, QWidget):
    #rightClicked = pyqtSignal()
    def __init__(self, *args, obj=None, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Afinador")
        self.Button.clicked.connect(self.nota)



        lista = []

        for j in range(0, 72):
            lista.append(round(55*(2**(j/12)), 2))


        self.notas = {}
        self.notas["A"] = [lista[0], lista[12], lista[24], lista[36], lista[48]]
        self.notas["A#"] = [lista[1], lista[13], lista[25], lista[37], lista[49]]
        self.notas["B"] = [lista[2], lista[14], lista[26], lista[38], lista[50]]
        self.notas["C"] = [lista[3], lista[15], lista[27], lista[39], lista[51]]
        self.notas["C#"] = [lista[4], lista[16], lista[28], lista[40], lista[52]]
        self.notas["D"] = [lista[5], lista[17], lista[29], lista[41], lista[53]]
        self.notas["D#"] = [lista[6], lista[18], lista[30], lista[42], lista[54]]
        self.notas["E"] = [lista[7], lista[19], lista[31], lista[43], lista[55]]
        self.notas["F"] = [lista[8], lista[20], lista[32], lista[44], lista[56]]
        self.notas["F#"] = [lista[9], lista[21], lista[33], lista[45], lista[57]]
        self.notas["G"] = [lista[10], lista[22], lista[34], lista[46], lista[58]]
        self.notas["G#"] = [lista[11], lista[23], lista[35], lista[47], lista[59]]


    # Audio
    #Audio, fs = sf.read("piano_mf_A5.wav")
    #O
    # def clicks(self):
    #     try:
    #         while True:
    #             self.nota()
    #             time.sleep(0.5)
    #     except KeyboardInterrupt: #ctrl+C to interrupt
    #            pass





    def nota(self):
        fs = 44100  # N° de muestras
        N = 1*fs  # cantidad de muestras = 2 seg
        canales = 2
        Audio = sd.rec(N, fs, canales)  # graba por 5 seg
        sd.wait()  # Espera a que termine de grabar para seguir leyendo el codigo
        Audio = Audio[:, 0]
        #fft
        #time = np.arange(Audio.size)/fs
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

        notaslista = list(self.notas.items())


        for j in range(0, 12):
            for i in range(0, 4):
                if (notaslista[j][1][i]/1.005) < resultado < (notaslista[j][1][i]*1.005):
                    print("La nota es: ", notaslista[j][0])
                    print(resultado, "Hz")
                    self.Afinado.setStyleSheet("background:green")
                    self.Menor.setStyleSheet("background:grey")
                    self.Mayor.setStyleSheet("background:grey")
                    self.Afinado.setText(notaslista[j][0])
                    self.Menor.setText(notaslista[j][0])
                    self.Mayor.setText(notaslista[j][0])

                elif (notaslista[j][1][i]/(2**(1/24))) < resultado < (notaslista[j][1][i]):
                    print(">>> para ", notaslista[j][0])
                    self.Menor.setStyleSheet("background:red")
                    self.Afinado.setStyleSheet("background:grey")
                    self.Mayor.setStyleSheet("background:grey")
                    self.Afinado.setText(notaslista[j][0])
                    self.Menor.setText(notaslista[j][0])
                    self.Mayor.setText(notaslista[j][0])

                elif (notaslista[j][1][i]) < resultado < (notaslista[j][1][i]*(2**(1/24))):
                    print("<<< para ", notaslista[j][0])
                    self.Mayor.setStyleSheet("background:red")
                    self.Menor.setStyleSheet("background:grey")
                    self.Afinado.setStyleSheet("background:grey")
                    self.Afinado.setText(notaslista[j][0])
                    self.Menor.setText(notaslista[j][0])
                    self.Mayor.setText(notaslista[j][0])

        QtCore.QCoreApplication.processEvents()

        time.sleep(1)
        self.nota()








######

if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    #Style de la app (importada)
    #app.setStyleSheet(stylesheet1)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())
