// Exporta reel.html a MP4 (1080 × 1920, 30 cps, H.264).
// Uso: node renderizar.mjs [salida.mp4]            -> video completo
//      node renderizar.mjs --cuadros 1.5,6,12      -> solo capturas PNG de esos segundos
// Requiere Playwright (Chromium) y ffmpeg. Genere antes la música con python3 musica.py.
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import { existsSync } from 'node:fs';

const require = createRequire(import.meta.url);
let playwright;
try { playwright = require('playwright'); } catch { playwright = require('/opt/node22/lib/node_modules/playwright'); }

const aqui = path.dirname(fileURLToPath(import.meta.url));
const FPS = 30;
const args = process.argv.slice(2);
const iCuadros = args.indexOf('--cuadros');

const navegador = await playwright.chromium.launch();
const pagina = await navegador.newPage({ viewport: { width: 1080, height: 1920 } });
await pagina.goto(pathToFileURL(path.join(aqui, 'reel.html')).href + '?render');
await pagina.evaluate(() => document.fonts.ready);
const lienzo = await pagina.$('#lienzo');

if (iCuadros >= 0) {
  for (const s of args[iCuadros + 1].split(',').map(Number)) {
    await pagina.evaluate(t => window.render(t), s);
    await lienzo.screenshot({ path: path.join(aqui, `cuadro-${s}.png`) });
    console.log(`cuadro-${s}.png`);
  }
} else {
  const salida = path.resolve(args[0] || path.join(aqui, 'reel-herencia-sucesion.mp4'));
  const duracion = await pagina.evaluate(() => window.DURACION);
  const total = Math.round(duracion * FPS);
  // Si existe musica.wav (python3 musica.py), se agrega normalizada a -14 LUFS
  const musica = path.join(aqui, 'musica.wav');
  const audio = existsSync(musica)
    ? ['-i', musica, '-map', '0:v', '-map', '1:a', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest']
    : [];
  const ffmpeg = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...audio,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', salida],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < total; f++) {
    await pagina.evaluate(t => window.render(t), f / FPS);
    const png = await lienzo.screenshot({ type: 'png' });
    if (!ffmpeg.stdin.write(png)) await new Promise(r => ffmpeg.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`${f}/${total}`);
  }
  ffmpeg.stdin.end();
  await new Promise(r => ffmpeg.on('close', r));
  console.log(salida);
}
await navegador.close();
