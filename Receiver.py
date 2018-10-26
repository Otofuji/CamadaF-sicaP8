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

# 7. Demodule o audio.
# 8. Execute o áudio do audio demodulado.
# 9. Mostre o gráfico no domínio do tempo e frequência do audio captado e do audio demodulado.

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

fs= 44100
duration = 10
freq = 12000
audio = signalMeu()

def grava (duration, fs):
	print("Gravando. . . ")
	myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
	sd.wait()

	print(len(myrecording))
	print(myrecording)
	return myrecording[:,0]


def demodula (dados, freq, fs, duration):
	s, portadora = generateSin(freq,1, duration,fs)
	demodulate = np.multiply(portadora,data)
	return demodulate

def filtro(dados,samplerate,cutoff_hz = 2000.0):
	nyq_rate = samplerate/2
	width = 5.0/nyq_rate
	ripple_db = 60.0 #dB
	N , beta = signal.kaiserord(ripple_db, width)
	taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
	filterted_y = signal.lfilter(taps, 1.0, dados)
	return filterted_y


gravado = grava(duration,fs)
demodulada = demodula(gravado,freq,fs,duration)
pronta = filtro(demodulada,fs,4000)
