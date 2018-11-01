#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Professor Rodrigo Carareto
# Projeto DTMF 
# Alessandra Blucher e Eric Otofuji
# Insper Instituto de Ensino e Pesquisa
# Engenharia de Computação
# São Paulo, 2018
####################################################

####################################################
# OBJETIVOS:

# 1. Faça a leitura de um arquivo de áudio previamente gravado com uma taxa de amostragem de 44100Hz.
# 2. Normalize esse sinal.
# 3. Filtre as altas frequências desse sinal.
# 4. Codifique esse sinal de áudio em AM.
# 5. Construa o gráfico nos domínios do tempo da frequência para os seguintes sinais:
# 		a. Sinal de áudio original.
# 		b. Sinal de áudio normalizado.
# 		c. Sinal de áudio filtrado.
# 		d. Sinal de áudio modulado.
# 6. Execute o áudio do sinal modulado

####################################################
# AVALIAÇÃO:



####################################################

import numpy as np
import sounddevice as sd
sd.default.samplerate = 44100
sd.default.channels = 2
import matplotlib.pyplot as plt
import soundfile as sf
import wave
import time
import peakutils
import matplotlib.pyplot as plt
from scipy.fftpack import fft, rfft, irfft, fftfreq
from scipy import signal as window


####################################################
#SignalClass
def generateSin(freq, amplitude, time, fs):
    n = time*fs
    x = np.linspace(0.0, time, n)
    s = amplitude*np.sin(freq*x*2*np.pi)
    return (x, s)



def calcFFT(signal, fs):
    N  = len(signal)
    W = window.hamming(N)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(88200), N//2)
    yf = fft(signal*W)
    return(xf, np.abs(yf[0:N//2]))



def plotFFT(signal, fs):
    x,y = calcFFT(signal, fs)
    plt.figure()
    plt.plot(x, np.abs(y))
    plt.title('Fourier')
    plt.show()



####################################################



audio, samplerate = sf.read("183_loop1_new-summits_0016.wav")
plt.plot(audio.T[0]); plt.title("Original"); plt.figure(); 
audio = audio.T[0]
audio /= np.max(np.abs(audio),axis=0)
plt.plot(audio); plt.title("Normalizado"); plt.figure(); 



from scipy.signal import butter, lfilter
from scipy.signal import freqs

def butter_lowpass(cutOff, fs, order=5):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='low', analog = False)
    return b, a

def butter_lowpass_filter(data, cutOff, fs, order=5):
    b, a = butter_lowpass(cutOff, fs, order=order)

    y = lfilter(b, a, data)
    return y

filtrado = butter_lowpass_filter(audio,4000,44100)
plt.plot(filtrado); plt.title("Filtrado"); plt.figure();
#print(filtrado)


x, portadora = generateSin(12000, 1, 0.1, 44100)
plt.plot(portadora); plt.title("Portadora"); plt.figure();
x, portadora = generateSin(12000, 1, 15, 44100)

listPronta = []
for i in range(0,len(x)):
    localValue = portadora[i]*filtrado[i]

    listPronta.append(localValue)

plt.plot(listPronta)
plt.title("Transportada Final")

plt.show()
sd.play(listPronta, 44100)
sd.wait()

































