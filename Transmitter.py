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
# 2. Normalize esse audio.
# 3. Filtre as altas frequências desse audio.
# 4. Codifique esse audio de áudio em AM.
# 5. Construa o gráfico nos domínios do tempo da frequência para os seguintes sinais:
# 		a. audio de áudio original.
# 		b. audio de áudio normalizado.
# 		c. audio de áudio filtrado.
# 		d. audio de áudio modulado.
# 6. Execute o áudio do audio modulado

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
from scipy import signal
from signalTeste import signalMeu

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

dados, samplerate = sf.read("gravacao.wav")
audio = signalMeu()

fs= 44100
duration = 5
print(dados[:,0])

def normalizar(dados):
	abs_mod = [np.max(dados), np.abs(min(dados))]
	norm= dados/max(abs_mod)
	return norm

#Filtro construido a partir dessa fonte : https://scipy-cookbook.readthedocs.io/items/FIRFilter.html

def filtro(dados):
	nyq_rate = samplerate/2
	width = 5.0/nyq_rate
	ripple_db = 60.0 #dB
	N , beta = signal.kaiserord(ripple_db, width)
	cutoff_hz = 3000
	taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
	filterted_y = signal.lfilter(taps, 1.0, dados)
	return filterted_y

dados_normalizados= normalizar(dados[:,0])
dados_filtrados= filtro(dados_normalizados)
s, portadora = generateSin(12000,1, duration,fs)
pronta = np.multiply(portadora, dados_filtrados)

playRecording(pronta,fs)
print(pronta)
