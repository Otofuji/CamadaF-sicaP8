#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
import peakutils


class signalMeu:
    def __init__(self):
        self.init = 0

    def generateSin(self, freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = float(amplitude)*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def calcPeaks(self,y):
        indexes = peakutils.indexes(y, thres=0.2, min_dist=30)
        return indexes

    def plotFFT(self, signal,fs=44100,title = "FFT",cor='b'):
        x,y = self.calcFFT(signal,fs)
        plt.figure(title)
        plt.plot(x, y,cor)
        plt.title('Fourier')
        plt.show(block=False)
        plt.draw()
        plt.pause(0.1)
