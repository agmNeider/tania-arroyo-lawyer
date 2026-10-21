# Reel: herencia y sucesión

Reel en motion design (1080 × 1920, 30 cps, 38 s, con música original) a partir del guion "¿Falleció su papá o su mamá y dejó bienes?".

- `reel-herencia-sucesion.mp4`: el video listo para subir, con la música a -14 LUFS (el nivel de Instagram).
- `musica.py`: compone y sintetiza la música original, sin reclamos de derechos. Lee los tiempos de `reel.html` y pone un sonido en cada evento animado: un ascenso suave e impacto con el acorde de la escena nueva en cada cambio, notas del acorde en las líneas del gancho, golpe de madera en las casillas, marimba en los vistos, barrido en el tachón y arpegio en los dos caminos, todo en registro medio y grave. Cada escena tiene su propio ritmo (el paso 3 va en menor y a medio tiempo). Si cambia la animación, vuelva a correr `python3 musica.py` y la música la sigue. Escribe `musica.wav` (requiere numpy y scipy).
- `reel.html`: la animación. Ábrala en el navegador para verla en bucle. Los textos se editan aquí.
- `renderizar.mjs`: lo exporta a MP4 con `node renderizar.mjs` (requiere Playwright y ffmpeg) y le agrega `musica.wav` si existe. Con `node renderizar.mjs --cuadros 5,12` saca capturas PNG de esos segundos.

Escenas: gancho "Hay una herencia en su familia y nadie sabe por dónde empezar. Son cuatro pasos." (0–6 s), registro civil de defunción, papeles de bienes y deudas, no repartir "de palabra", sucesión en notaría o juzgado (con la norma al pie) y cierre con el monograma, el WhatsApp y el logotipo (32–38 s). Todo el texto queda dentro de la zona segura de Reels.

Video y música van sobre la misma rejilla: 120 ppm, pulso de 0,5 s y compás de 2 s. Cada escena entra en el primer tiempo de un compás (`data-golpe`: 0, 6, 12, 18, 24 y 32 s) y la cortina pasa durante el pulso anterior, mientras la percusión calla. Todos los `data-en` son múltiplos de 0,25 s contados desde ese golpe. Si cambia un tiempo, manténgalo en la rejilla y vuelva a generar la música.
