import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np

audio, fm = sf.read("./rl002_30ms.wav")
 
t = (np.linspace(0, len(audio)-1, len(audio)))/fm 
                                                 
#Calculem autocorrelació i axis
r = np.correlate(audio, audio, "same")
r = r / r[int(len(r)/2)] 
raxis = np.arange(len(r))

#Plots
plt.subplot(2,1,1)
plt.plot(t, audio)
plt.grid(True)
plt.xlabel("Temps(s)")
plt.ylabel("Amplitud")

plt.subplot(2,1,2)
plt.plot(raxis, r)
plt.grid(True)
plt.xlabel("Mostres")
plt.ylabel("Autocorrelacio")

plt.show()  