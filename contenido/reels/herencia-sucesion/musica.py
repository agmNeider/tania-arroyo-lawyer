"""Música original del reel (sintetizada aquí, sin derechos de terceros).

Piano, colchón armónico, bajo y percusión suave a 95 ppm, con la progresión
A sus4 · D maj9 · Bm7 · G maj7. El compás 13 cae justo en el cierre (33,8 s) y
resuelve en D. Los efectos (barridos, marcas y sellos) van sincronizados con
las animaciones de reel.html.

Uso: python3 musica.py  ->  musica.wav (estéreo, 48 kHz, 39,5 s)
Requiere numpy y scipy.
"""
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
DUR = 39.5
COMPAS = 33.8 / 13          # el compás 13 empieza con la escena de cierre
PULSO = COMPAS / 4
N = int(SR * DUR)
rng = np.random.default_rng(7)

# Cambios de escena y momentos de la animación (segundos), tomados de reel.html
ESCENAS = [5.2, 11.2, 18.4, 25.8, 33.8]
MARCAS = [11.2 + 2.4, 11.2 + 3.1, 11.2 + 3.8, 11.2 + 4.5]   # vistos de la lista del paso 2
SELLOS = [5.2 + 2.9, 33.8 + 0.3]                            # sello del documento y monograma
CASILLAS = [e + .25 for e in ESCENAS[:4]]                    # casilla del paso que se llena


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def lp(x, f, orden=2):
    return sosfilt(butter(orden, f, 'low', fs=SR, output='sos'), x)


def hp(x, f, orden=2):
    return sosfilt(butter(orden, f, 'high', fs=SR, output='sos'), x)


def bp(x, f1, f2):
    return sosfilt(butter(2, [f1, f2], 'band', fs=SR, output='sos'), x)


def poner(pista, señal, t, ganancia=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    if i < 0:
        señal, i = señal[-i:], 0
    s = señal[: N - i] * ganancia
    pista[0, i:i + len(s)] += s * np.sqrt((1 - pan) / 2)
    pista[1, i:i + len(s)] += s * np.sqrt((1 + pan) / 2)


def piano(midi, largo=2.5, vel=1.0):
    t = np.arange(int(SR * largo)) / SR
    f = hz(midi)
    s = np.zeros_like(t)
    for k, a in enumerate([1, .45, .22, .12, .06, .03], start=1):
        fk = f * k * (1 + .0004 * k * k)
        s += a * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.4 + .9 * k) * (f / 400) ** .3)
    ataque = np.minimum(1, t / .004)
    martillo = rng.standard_normal(len(t)) * np.exp(-t * 300) * .05
    s = (s * ataque + martillo) * vel
    cola = np.minimum(1, (largo - t) / .15)
    return lp(s, 5200) * cola


def colchon(notas, largo):
    t = np.arange(int(SR * largo)) / SR
    s = np.zeros_like(t)
    for m in notas:
        for d in (-.07, 0, .06):
            fase = rng.uniform(0, 1)
            s += 2 * ((hz(m) * (1 + d / 100) * t + fase) % 1) - 1
    s = lp(lp(s, 1100), 1500)
    env = np.minimum(1, t / .9) * np.minimum(1, (largo - t) / .9)
    return s * env / len(notas) * (1 + .08 * np.sin(2 * np.pi * .25 * t))


def bajo(midi, largo):
    t = np.arange(int(SR * largo)) / SR
    f = hz(midi)
    s = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)
    return lp(s * np.minimum(1, t / .01) * np.exp(-t * 1.3) * np.minimum(1, (largo - t) / .05), 900)


def bombo():
    t = np.arange(int(SR * .45)) / SR
    f = 46 + 70 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def platillo(largo=.06):
    t = np.arange(int(SR * largo)) / SR
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 70)


def chasquido():
    t = np.arange(int(SR * .18)) / SR
    return bp(rng.standard_normal(len(t)), 1200, 4500) * np.exp(-t * 32)


def barrido(largo=1.1, pico=.75):
    """Ruido que sube hacia el cambio de escena."""
    t = np.arange(int(SR * largo)) / SR
    r = rng.standard_normal(len(t))
    bajo_, alto = lp(r, 900), bp(r, 1500, 7000)
    x = t / largo
    env = np.where(x < pico, (x / pico) ** 2.5, np.exp(-(x - pico) * 14))
    return (bajo_ * (1 - x) + alto * x * .6) * env


def marca():
    t = np.arange(int(SR * .25)) / SR
    return (np.sin(2 * np.pi * 1760 * t) * .6 + np.sin(2 * np.pi * 2637 * t) * .3) * np.exp(-t * 22)


def sello():
    t = np.arange(int(SR * .6)) / SR
    f = 220 + 300 * np.exp(-t * 30)
    golpe = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12)
    brillo = sum(np.sin(2 * np.pi * hz(m) * t) * np.exp(-t * 4) for m in (86, 90, 93)) * .12
    return golpe * .7 + brillo


def reverb(x, segundos=2.6, mezcla=.28):
    t = np.arange(int(SR * segundos)) / SR
    salida = np.zeros_like(x)
    for c in range(2):
        ir = rng.standard_normal(len(t)) * np.exp(-t * 6.9 / segundos)
        ir = lp(ir, 6000)
        ir /= np.sqrt(np.sum(ir ** 2))
        salida[c] = fftconvolve(x[c], ir)[: x.shape[1]]
    return x * (1 - mezcla) + salida * mezcla * 1.4


# Acordes: (bajo, voces)
ACORDES = [
    (45, [64, 69, 74, 76]),   # A sus4
    (50, [66, 69, 73, 76]),   # D maj9
    (47, [66, 69, 71, 74]),   # Bm7
    (43, [66, 71, 74, 78]),   # G maj7
]
FINAL = (50, [62, 66, 69, 74, 76])

pianos = np.zeros((2, N))
pads = np.zeros((2, N))
graves = np.zeros((2, N))
ritmo = np.zeros((2, N))
efectos = np.zeros((2, N))

for c in range(13):
    t0 = c * COMPAS
    raiz, voces = ACORDES[c % 4]
    if c % 4 == 0 and c > 0:
        voces = [64, 69, 73, 76]                 # A sus4 se abre a A en la segunda vuelta
    poner(pads, colchon(voces[:3], COMPAS + .9), t0 - .2, .22)
    # Piano: acorde en el tiempo 1 y arpegio en corcheas
    for k, m in enumerate(voces):
        poner(pianos, piano(m, 3.0, .32), t0 + k * .012, pan=-.3 + .2 * k)
    densidad = 4 if c < 2 else 8
    orden = voces + voces[::-1][1:3] + [voces[0] + 12]
    for k in range(densidad):
        tk = t0 + (k + 1) * COMPAS / (densidad + 1) if c < 2 else t0 + k * PULSO / 2
        if c >= 2 and k == 0:
            continue
        m = orden[k % len(orden)] + (12 if c >= 6 and k % 4 == 3 else 0)
        poner(pianos, piano(m, 1.8, .18 + .05 * (k % 2 == 0)), tk, pan=(-1) ** k * .35)
    if c >= 2:
        poner(graves, bajo(raiz, PULSO * 2), t0, .3)
        poner(graves, bajo(raiz, PULSO * 1.5), t0 + PULSO * 2.5, .2)
        for b in range(4):
            if b in (0, 2):
                poner(ritmo, bombo(), t0 + b * PULSO, .35)
            if c >= 6 and b in (1, 3):
                poner(ritmo, chasquido(), t0 + b * PULSO, .16, pan=.15)
            for o in (0, .5):
                poner(ritmo, platillo(), t0 + (b + o) * PULSO, .05 if o else .025, pan=-.4)

# Cierre: resuelve en D y se deja sonar
t0 = 13 * COMPAS
largo_final = DUR - t0
poner(pads, colchon(FINAL[1][1:4], largo_final + .5), t0 - .1, .26)
poner(graves, bajo(FINAL[0], 3.5), t0, .3)
for k, m in enumerate(FINAL[1]):
    poner(pianos, piano(m, largo_final, .34), t0 + k * .03, pan=-.3 + .15 * k)
for k, m in enumerate([81, 78, 74, 76]):
    poner(pianos, piano(m, 3.0, .14), t0 + 1.3 + k * PULSO, pan=.3)

# Efectos sincronizados con la animación
for e in ESCENAS:
    poner(efectos, barrido(), e - .8, .12, pan=0)
for t in MARCAS:
    poner(efectos, marca(), t + .05, .07, pan=.2)
for t in SELLOS:
    poner(efectos, sello(), t + .05, .2)
for t in CASILLAS:
    poner(efectos, marca(), t, .045, pan=-.2)

mezcla = reverb(pianos * 1.0 + pads * .8 + efectos * .6, mezcla=.3) + graves + ritmo * .9 + efectos * .4
# Entrada sin clic y salida en desvanecido
t = np.arange(N) / SR
mezcla *= np.minimum(1, (DUR - t) / 2.2) ** 1.5 * np.minimum(1, t / .05)
mezcla = hp(mezcla, 35)
mezcla = np.tanh(mezcla * 1.6) / 1.6
mezcla *= .89 / np.max(np.abs(mezcla))

datos = (mezcla.T * 32767).astype('<i2')
destino = Path(__file__).with_name('musica.wav')
with wave.open(str(destino), 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(datos.tobytes())
print(destino)
