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

# 7. Demodule o sinal.
# 8. Execute o áudio do sinal demodulado.
# 9. Mostre o gráfico no domínio do tempo e frequência do sinal captado e do sinal demodulado.

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
from scipy.fftpack import fft
from scipy import signal as window
from scipy.signal import butter, lfilter
from scipy.signal import freqs

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


gravado = sd.rec(15*44100)
sd.wait()

sf.write("demodulado.wav",gravado,44100)

x, portadora = generateSin(12000,1, 15, 44100)

localValue = []
listPronta = []

for i in range(0,len(x)):
    localValue = portadora[i]*gravado.T[0][i]

    listPronta.append(localValue)



def butter_lowpass(cutOff, fs, order=5):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='low', analog = False)
    return b, a

def butter_lowpass_filter(data, cutOff, fs, order=5):
    b, a = butter_lowpass(cutOff, fs, order=order)
    y = lfilter(b, a, data)
    return y

filtro = butter_lowpass_filter(listPronta, 2000, 44100)

sd.play(filtro, 44100); sd.wait()

plt.plot(gravado.T[0]); plt.title("Original"); plt.figure(); 
plt.plot(filtro); plt.title("Demodulado"); plt.figure(); plt.show();














