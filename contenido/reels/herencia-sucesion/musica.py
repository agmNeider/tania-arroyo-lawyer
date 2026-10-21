"""Música original del reel, sincronizada con la animación (sin derechos de terceros).

La partitura sale de reel.html: el script lee cada escena (data-desde) y cada
elemento animado (data-fx, data-en) y le asigna un sonido. Si cambian los tiempos
de la animación, la música los sigue al volver a generarla.

- Cada escena es una sección con su propio ritmo, que arranca en el golpe del
  número del paso. Antes de cada cambio hay un ascenso y un silencio corto.
- Cada escena entra con su acorde en piano sobre el impacto. Las líneas del
  gancho suenan como notas del acorde, las casillas como un golpe de madera,
  los vistos como notas cortas de marimba, el tachón como un barrido
  descendente, las tarjetas y riesgos como golpes graves, y el trazo de los dos
  caminos como un arpegio suave. Nada en registro agudo.
- Progresión en re mayor; el paso 3 (la advertencia) va en si menor y a medio
  tiempo; el paso 4 termina en la dominante y el cierre resuelve en re.

Uso: python3 musica.py  ->  musica.wav (estéreo, 48 kHz)
Requiere numpy y scipy.
"""
import re
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
PULSO = 0.5                 # 120 ppm
GOLPE = 0.35                # el número del paso aparece 0,35 s después del inicio de la escena
rng = np.random.default_rng(11)
aqui = Path(__file__).parent


# --- Lectura de la animación -------------------------------------------------

def leer_escenas():
    html = (aqui / 'reel.html').read_text(encoding='utf-8')
    duracion = float(re.search(r'const DURACION = ([\d.]+)', html).group(1))
    escenas = []
    for m in re.finditer(r'<section([^>]*)>(.*?)</section>', html, re.S):
        attrs, cuerpo = m.groups()
        desde = float(re.search(r'data-desde="([\d.]+)"', attrs).group(1))
        hasta = float(re.search(r'data-hasta="([\d.]+)"', attrs).group(1))
        paso = re.search(r'data-paso="(\d)"', attrs)
        eventos = []
        for e in re.finditer(r'<\w+([^>]*data-fx="([\w-]+)"[^>]*)>', cuerpo):
            a, fx = e.groups()
            en = re.search(r'data-en="([\d.]+)"', a)
            if not en:
                continue
            clase = re.search(r'class="([^"]*)"', a)
            dur = re.search(r'data-dur="([\d.]+)"', a)
            eventos.append(dict(t=desde + float(en.group(1)), fx=fx, clase=clase.group(1) if clase else '',
                                dur=float(dur.group(1)) if dur else None))
        if paso:  # la casilla del paso la agrega el script de la página
            eventos.append(dict(t=desde + .25, fx='casilla-paso', clase='', dur=None))
        eventos.sort(key=lambda e: e['t'])
        escenas.append(dict(desde=desde, hasta=hasta, paso=int(paso.group(1)) if paso else None, eventos=eventos))
    return duracion, escenas


DUR, ESCENAS = leer_escenas()
N = int(SR * DUR)


# --- Utilidades ---------------------------------------------------------------

def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def filtro(x, f, tipo='low', orden=2):
    return sosfilt(butter(orden, f, tipo, fs=SR, output='sos'), x)


def tiempo(largo):
    return np.arange(int(SR * largo)) / SR


class Pista:
    def __init__(self):
        self.a = np.zeros((2, N))

    def poner(self, señal, t, g=1.0, pan=0.0):
        i = int(round(t * SR))
        if i < 0:
            señal, i = señal[-i:], 0
        if i >= N:
            return
        s = señal[: N - i] * g
        self.a[0, i:i + len(s)] += s * np.sqrt((1 - pan) / 2)
        self.a[1, i:i + len(s)] += s * np.sqrt((1 + pan) / 2)


# --- Instrumentos ------------------------------------------------------------

def piano(midi, largo=1.6, brillo=1.0):
    t = tiempo(largo)
    f = hz(midi)
    s = sum(a * np.sin(2 * np.pi * f * k * (1 + .0004 * k * k) * t) * np.exp(-t * (1.6 + 1.1 * k / brillo) * (f / 400) ** .3)
            for k, a in enumerate([1, .5, .25, .12, .06], start=1))
    s = s * np.minimum(1, t / .003) + rng.standard_normal(len(t)) * np.exp(-t * 400) * .04
    return filtro(s, 3800) * np.minimum(1, (largo - t) / .1)


def marimba(midi, largo=.9):
    """Nota corta y redonda, sin agudos: para vistos y acentos."""
    t = tiempo(largo)
    f = hz(midi)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 5) + .15 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 18)
    return filtro(s * np.minimum(1, t / .004), 2500)


def madera():
    """Golpe seco y grave para las casillas."""
    t = tiempo(.12)
    f = 420 * (1 + .2 * np.exp(-t * 80))
    return filtro(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45), 1800)


def colchon(notas, largo):
    t = tiempo(largo)
    s = np.zeros_like(t)
    for m in notas:
        for d in (-.08, 0, .07):
            s += 2 * ((hz(m) * (1 + d / 100) * t + rng.uniform()) % 1) - 1
    s = filtro(filtro(s, 1400), 1800)
    return s * np.minimum(1, t / .25) * np.minimum(1, (largo - t) / .3) / len(notas)


def bajo(midi, largo, abierto=1.0):
    t = tiempo(largo)
    f = hz(midi)
    sierra = 2 * ((f * t) % 1) - 1
    s = filtro(sierra, 260 + 600 * abierto, orden=2) * .6 + np.sin(2 * np.pi * f / 2 * t) * .8
    return s * np.minimum(1, t / .004) * np.exp(-t * 2.2) * np.minimum(1, (largo - t) / .02)


def bombo(g=1.0):
    t = tiempo(.5)
    f = 44 + 110 * np.exp(-t * 32)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) + rng.standard_normal(len(t)) * np.exp(-t * 600) * .15) * g


def palmas():
    t = tiempo(.25)
    r = rng.standard_normal(len(t))
    env = sum(np.exp(-np.maximum(0, t - d) * 40) * (t >= d) for d in (0, .011, .022))
    return filtro(r, [900, 5000], 'band') * env * .7


def hat(abierto=False):
    t = tiempo(.25 if abierto else .05)
    return filtro(rng.standard_normal(len(t)), 7500, 'high') * np.exp(-t * (14 if abierto else 80))


def impacto():
    t = tiempo(2.5)
    f = 38 + 60 * np.exp(-t * 12)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    ruido = filtro(rng.standard_normal(len(t)), 3000) * np.exp(-t * 5) * .5
    return sub + ruido + np.pad(bombo(.8), (0, len(t) - int(SR * .5)))


def ascenso(largo):
    """Ruido que se abre hacia el cambio de escena (sin tono, sin agudos)."""
    t = tiempo(largo)
    r = rng.standard_normal(len(t))
    trozos = 24
    s = np.zeros_like(t)
    for k in range(trozos):
        a, b = k * len(t) // trozos, (k + 1) * len(t) // trozos
        fc = 300 * (8 ** (k / trozos))
        s[a:b] = filtro(r, [fc * .6, fc * 1.5], 'band')[a:b]
    x = t / largo
    return s * x ** 2.2


def barrido_abajo(largo=.45):
    t = tiempo(largo)
    r = rng.standard_normal(len(t))
    s = np.zeros_like(t)
    for k in range(12):
        a, b = k * len(t) // 12, (k + 1) * len(t) // 12
        fc = 6000 * (.08 ** (k / 12))
        s[a:b] = filtro(r, [fc * .6, fc * 1.5], 'band')[a:b]
    return s * np.sin(np.pi * t / largo) ** .7


def soplo(largo=.6):
    t = tiempo(largo)
    return filtro(rng.standard_normal(len(t)), [300, 2500], 'band') * np.sin(np.pi * t / largo) ** 2


def tic():
    t = tiempo(.04)
    return filtro(rng.standard_normal(len(t)), 3000, 'high') * np.exp(-t * 150)


def golpe_grave():
    t = tiempo(.6)
    f = 70 + 80 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)


def reverb(x, segundos=2.2, mezcla=.25):
    t = tiempo(segundos)
    salida = np.zeros_like(x)
    for c in range(2):
        ir = filtro(rng.standard_normal(len(t)) * np.exp(-t * 6.9 / segundos), 7000)
        ir /= np.sqrt(np.sum(ir ** 2))
        salida[c] = fftconvolve(x[c], ir)[: x.shape[1]]
    return x * (1 - mezcla) + salida * mezcla * 1.4


# --- Armonía por escena -------------------------------------------------------

AC = {  # raíz del bajo, voces
    'D': (38, [62, 66, 69, 73]), 'A': (45, [61, 64, 69, 71]), 'Bm': (47, [59, 62, 66, 69]),
    'G': (43, [62, 66, 67, 71]), 'Em': (40, [62, 64, 67, 71]), 'F#': (42, [61, 66, 70, 73]),
    'Dfin': (38, [62, 66, 69, 73, 76]),
}
PROGRESION = [['Bm', 'G'], ['D', 'A', 'Bm', 'G'], ['D', 'A', 'Bm', 'G'], ['Bm', 'G', 'Em', 'F#'],
              ['G', 'A', 'Bm', 'A'], ['Dfin']]


def acorde_en(i, t):
    e = ESCENAS[i]
    ini = e['desde'] + (GOLPE if i else 0)
    prog = PROGRESION[i]
    if i == 0:
        return AC[prog[0] if t < e['desde'] + 2.45 else prog[1]]
    k = int(max(0, t - ini) // (PULSO * 4)) % len(prog)
    return AC[prog[k]]


musica, ritmo, sfx, graves = Pista(), Pista(), Pista(), Pista()
golpes_bombo = []

for i, e in enumerate(ESCENAS):
    ini = e['desde'] + (GOLPE if i else 0)
    fin = ESCENAS[i + 1]['desde'] + GOLPE if i + 1 < len(ESCENAS) else DUR
    corte = fin - GOLPE - .22 if i + 1 < len(ESCENAS) else DUR   # silencio corto antes del cambio

    # Colchón y bajo por acorde
    if i == 0:
        for (a, b), nombre in zip([(0, 2.45), (2.45, e['hasta'])], PROGRESION[0]):
            raiz, voces = AC[nombre]
            musica.poner(colchon(voces[:3], b - a + .3), a, .16)
            for k in range(int((b - a) / (PULSO / 2))):           # pulso de corcheas que crece
                tk = a + k * PULSO / 2
                if tk < corte:
                    graves.poner(bajo(raiz, PULSO / 2 * .9, abierto=tk / 5), tk, .1 + .15 * tk / 5)
    else:
        t = ini
        while t < min(fin, DUR):
            raiz, voces = acorde_en(i, t + .01)
            largo = min(PULSO * 4, fin - t) if i < 5 else DUR - t
            musica.poner(colchon(voces[:3], largo + .25), t, .2 if i < 5 else .28)
            if i == 3:                                            # medio tiempo: notas largas
                graves.poner(bajo(raiz, min(largo, PULSO * 2) * .95, .3), t, .3)
                if t + PULSO * 2 < corte:
                    graves.poner(bajo(raiz, PULSO * 1.8, .3), t + PULSO * 2, .24)
            elif i < 5:
                for k in range(8):
                    tk = t + k * PULSO / 2
                    if tk < corte:
                        graves.poner(bajo(raiz + (12 if i == 4 and k % 2 else 0), PULSO / 2 * .85, .5 + .1 * i), tk, .22)
            else:                                                 # cierre: un solo acorde que se deja sonar
                graves.poner(bajo(raiz, 4, .2), t, .3)
                break
            t += PULSO * 4

    # Percusión por escena
    nb = int((min(fin, DUR) - ini) / (PULSO / 2)) + 1
    for k in range(nb):
        tk = ini + k * PULSO / 2
        if tk >= corte:
            break
        beat, medio = divmod(k, 2)
        b4 = beat % 4
        if i == 0:
            if tk >= e['desde'] + 2.45 and not medio and b4 in (0, 2):
                ritmo.poner(bombo(.6), tk); golpes_bombo.append(tk)
        elif i == 1:
            if not medio and b4 in (0, 2): ritmo.poner(bombo(), tk); golpes_bombo.append(tk)
            ritmo.poner(hat(), tk, .1 if medio else .05, -.3)
        elif i == 2:
            if not medio and b4 in (0, 2): ritmo.poner(bombo(), tk); golpes_bombo.append(tk)
            if not medio and b4 in (1, 3): ritmo.poner(palmas(), tk, .5, .1)
            ritmo.poner(hat(), tk, .12 if medio else .06, -.3)
            ritmo.poner(hat(), tk + PULSO / 4, .04, .3)
        elif i == 3:
            if (not medio and b4 == 0) or (medio and b4 == 1): ritmo.poner(bombo(.9), tk); golpes_bombo.append(tk)
            if not medio and b4 == 2: ritmo.poner(palmas(), tk, .6)
            ritmo.poner(hat(), tk, .07 if medio else .03, -.3)
            ritmo.poner(hat(), tk + PULSO / 4, .025, .3)
        elif i == 4:
            if not medio: ritmo.poner(bombo(), tk); golpes_bombo.append(tk)
            if not medio and b4 in (1, 3): ritmo.poner(palmas(), tk, .55, .1)
            ritmo.poner(hat(abierto=bool(medio)), tk, .07 if medio else .05, -.3)

    # Transiciones: ascenso hacia el siguiente golpe e impacto
    if i + 1 < len(ESCENAS):
        sig = ESCENAS[i + 1]['desde'] + GOLPE
        largo = 1.6 if i + 1 < 5 else 2.2
        sfx.poner(ascenso(largo), sig - largo, .14)
        sfx.poner(impacto(), sig, .4)
        _, voces_sig = acorde_en(i + 1, sig + .01)
        for k, m in enumerate(voces_sig):
            musica.poner(piano(m, 2.4), sig + k * .02, .17, pan=-.3 + .2 * k)
        golpes_bombo.append(sig)

    # Eventos de la animación
    linea, arpegios = 0, set()
    for ev in e['eventos']:
        t, fx, clase = ev['t'], ev['fx'], ev['clase']
        raiz, voces = acorde_en(i, t)
        if fx == 'mascara' and i == 0:                        # gancho: una nota del acorde por línea
            m = voces[linea % len(voces)]
            musica.poner(piano(m, 1.6), t, .16, pan=(-1) ** linea * .25)
            linea += 1
        elif fx in ('aparece', 'casilla-paso'):               # casillas: golpe de madera, sin tono agudo
            sfx.poner(madera(), t, .22, pan=-.2)
        elif fx == 'relleno':                                 # vistos de la lista
            k = sum(1 for x in e['eventos'] if x['fx'] == 'relleno' and x['t'] < t)
            musica.poner(marimba(voces[k % len(voces)] - 12 * (k % 2)), t, .16, pan=.2)
            sfx.poner(tic(), t, .12)
        elif fx == 'traza' and (ev['dur'] or 0) >= .6:        # los dos caminos: arpegio suave que sigue el trazo
            if t in arpegios:                                 # los dos trazos arrancan juntos: un solo arpegio
                continue
            arpegios.add(t)
            for k, m in enumerate([raiz + 12, voces[0], voces[1], voces[2]]):
                musica.poner(piano(m, 1.4), t + k * ev['dur'] / 4, .13, pan=-.3 + .2 * k)
        elif fx == 'sello':
            sfx.poner(golpe_grave(), t, .45)
        elif fx == 'sube-lento':
            sfx.poner(soplo(.9), t, .15)
        elif fx == 'crece' and clase == 'tachon':
            sfx.poner(barrido_abajo(.5), t, .3)
            sfx.poner(golpe_grave(), t + .35, .5)
            musica.poner(piano(raiz - 12 + 1, 1.2), t + .35, .12)   # nota disonante, baja
            musica.poner(piano(raiz - 12, 1.2), t + .35, .12)
        elif fx == 'crece' and clase == 'barra':
            sfx.poner(tic(), t, .18, pan=.4)
        elif fx == 'sube' and clase == 'item':
            sfx.poner(tic(), t, .1)
        elif fx == 'sube' and clase == 'riesgo':
            sfx.poner(golpe_grave(), t, .45)
        elif fx == 'sube' and clase == 'tarjeta':
            sfx.poner(golpe_grave(), t, .4)
            musica.poner(marimba(voces[0] if t < e['desde'] + 2.5 else voces[2]), t, .16)
        elif fx == 'sube' and i == 5 and clase == '' and t < e['desde'] + 2:   # botón del cierre
            musica.poner(marimba(voces[2]), t, .14)

# Bombeo: el colchón y el bajo bajan con cada bombo
t = np.arange(N) / SR
bombeo = np.ones(N)
for tk in golpes_bombo:
    i0 = int(tk * SR)
    seg = t[i0:i0 + int(SR * .4)] - tk
    bombeo[i0:i0 + len(seg)] = np.minimum(bombeo[i0:i0 + len(seg)], 1 - .55 * np.exp(-seg / .09))

mezcla = reverb(musica.a * bombeo + sfx.a * .9, mezcla=.28) + graves.a * bombeo + ritmo.a * .85 + sfx.a * .25
mezcla = filtro(mezcla, 30, 'high')
mezcla *= np.minimum(1, (DUR - t) / 1.5) ** 1.5 * np.minimum(1, t / .02)
mezcla /= np.percentile(np.abs(mezcla), 99.9)
mezcla = np.tanh(mezcla * 1.2)
mezcla *= .89 / np.max(np.abs(mezcla))

destino = aqui / 'musica.wav'
with wave.open(str(destino), 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(mezcla, -1, 1).T * 32767).astype('<i2').tobytes())
print(destino, f'{DUR} s, {sum(len(e["eventos"]) for e in ESCENAS)} eventos')
