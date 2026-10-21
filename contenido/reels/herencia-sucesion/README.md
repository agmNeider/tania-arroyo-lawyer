# Reel: herencia y sucesión

Reel en motion design (1080 × 1920, 30 cps, 38,5 s, con música original) a partir del guion "¿Falleció su papá o su mamá y dejó bienes?".

- `reel-herencia-sucesion.mp4`: el video listo para subir, con la música a -14 LUFS (el nivel de Instagram).
- `musica.py`: compone y sintetiza la música (piano, colchón, bajo y percusión suave a 95 ppm, con barridos y marcas sincronizados con la animación). Es original, así que no tiene reclamos de derechos. `python3 musica.py` escribe `musica.wav` (requiere numpy y scipy).
- `reel.html`: la animación. Ábrala en el navegador para verla en bucle. Los textos se editan aquí.
- `renderizar.mjs`: lo exporta a MP4 con `node renderizar.mjs` (requiere Playwright y ffmpeg) y le agrega `musica.wav` si existe. Con `node renderizar.mjs --cuadros 5,12` saca capturas PNG de esos segundos.

Escenas: gancho (0–4 s), registro civil de defunción, papeles de bienes y deudas, no repartir "de palabra", sucesión en notaría o juzgado (con la norma al pie) y cierre con el monograma, el WhatsApp y el logotipo (32,8–38,5 s). Todo el texto queda dentro de la zona segura de Reels.
