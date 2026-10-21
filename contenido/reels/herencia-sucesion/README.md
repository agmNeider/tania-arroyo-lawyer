# Reel: herencia y sucesión

Reel en motion design (1080 × 1920, 30 cps, 39,5 s, con música original) a partir del guion "¿Falleció su papá o su mamá y dejó bienes?".

- `reel-herencia-sucesion.mp4`: el video listo para subir, con la música a -14 LUFS (el nivel de Instagram).
- `musica.py`: compone y sintetiza la música original, sin reclamos de derechos. Lee los tiempos de `reel.html` y pone un sonido en cada evento animado: golpe en cada número de paso, ascenso antes de cada cambio de escena, notas en cada línea de texto, señales en las casillas, campanas en los vistos, barrido en el tachón y arpegio en los dos caminos. Cada escena tiene su propio ritmo (el paso 3 va en menor y a medio tiempo). Si cambia la animación, vuelva a correr `python3 musica.py` y la música la sigue. Escribe `musica.wav` (requiere numpy y scipy).
- `reel.html`: la animación. Ábrala en el navegador para verla en bucle. Los textos se editan aquí.
- `renderizar.mjs`: lo exporta a MP4 con `node renderizar.mjs` (requiere Playwright y ffmpeg) y le agrega `musica.wav` si existe. Con `node renderizar.mjs --cuadros 5,12` saca capturas PNG de esos segundos.

Escenas: gancho "Hay una herencia en su familia y nadie sabe por dónde empezar. Son cuatro pasos." (0–5,2 s), registro civil de defunción, papeles de bienes y deudas, no repartir "de palabra", sucesión en notaría o juzgado (con la norma al pie) y cierre con el monograma, el WhatsApp y el logotipo (33,8–39,5 s). Todo el texto queda dentro de la zona segura de Reels.
