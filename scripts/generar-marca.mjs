// Genera lib/marca.generada.ts desde el sistema de diseño (design-system/):
// logotipo con la rr enlazada, monograma "ag." e íconos oficiales.
// Se ejecuta solo antes de `dev` y `build`. No edite el archivo generado.
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = join(dirname(fileURLToPath(import.meta.url)), '..');
const ds = join(raiz, 'design-system');
const marcas = JSON.parse(readFileSync(join(ds, '_herramientas', 'marks.json'), 'utf8'));

const iconos = {};
for (const f of readdirSync(join(ds, 'assets', 'Iconos')).filter((f) => f.endsWith('.svg')).sort()) {
  const svg = readFileSync(join(ds, 'assets', 'Iconos', f), 'utf8');
  iconos[f.replace('.svg', '')] = svg.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '').trim();
}

const salida = `// Archivo generado por scripts/generar-marca.mjs desde design-system/. No editar a mano.
export const LOGOTIPO = ${JSON.stringify(marcas.wordmark)} as const;
export const APILADO = ${JSON.stringify(marcas.stacked)} as const;
export const MONOGRAMA = ${JSON.stringify(marcas.ag)} as const;
export const ICONOS = ${JSON.stringify(iconos, null, 2)} as const;
export type NombreIcono = keyof typeof ICONOS;
`;
writeFileSync(join(raiz, 'lib', 'marca.generada.ts'), salida);
console.log('marca: logotipo, monograma y', Object.keys(iconos).length, 'íconos');
