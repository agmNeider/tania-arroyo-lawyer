---
name: arroyo-guzman-marca
description: Sistema de diseño de Arroyo Guzmán, la imagen legal de la abogada Tania Arroyo Guzmán (procesalista civil). Úsala siempre que vayas a crear o revisar cualquier pieza de la marca: publicaciones e historias de Instagram, carruseles, tarjeta profesional, membrete, memoriales, firma de correo, sitio web, presentaciones, avatares o cualquier diseño, texto o código que deba verse o sonar como Arroyo Guzmán. También para cambiar el logo, la paleta, la tipografía o las plantillas, y para regenerar los archivos del sistema.
---

# Arroyo Guzmán: sistema de diseño

Todo el sistema está en `design-system/` en la raíz de este repositorio. Esta skill dice qué usar y cómo usarlo. Si hay dudas de detalle, la fuente de verdad es:

| Qué | Dónde |
| --- | --- |
| Manual de marca (voz, color, tipografía, logo, fotografía) | `design-system/README.md` |
| Tokens (fuente única) | `design-system/tokens.json` |
| Tokens listos para CSS | `design-system/tokens.css` (se genera, no se edita a mano) |
| Logos SVG | `design-system/assets/Logos/` (léase su `README.md`) |
| Íconos de áreas | `design-system/assets/Iconos/` |
| Fuente Open Sans (OFL) | `design-system/fonts/` |
| Plantillas HTML de cada pieza | `design-system/components/<Pieza>/preview.html` + `README.md` |
| Referentes investigados | `design-system/guias/referentes.md` |
| Scripts que generan todo | `design-system/_herramientas/` |

Versión navegable publicada: https://claude.ai/artifact/6NcsJ5hDbYVhGsdj9qQMRf

## La marca en una línea

Abogada joven e independiente, especialista en derecho procesal civil, que atiende casos civiles, laborales, de familia, sucesiones y contratos. Idea central: **"Cada término, cumplido."** Debe verse joven por el color y responsable por la precisión. Nada de balanzas doradas, columnas, martillos ni togas.

## Reglas que no se rompen

1. **Nombre:** la marca es "Arroyo Guzmán". La persona es "Tania Arroyo Guzmán, Abogada · Procesalista civil". Nunca "& Asociados" ni siglas.
2. **Logotipo:** usa siempre los SVG de `assets/Logos/`. Nunca reescribas "Arroyo Guzmán" con la fuente: el logotipo tiene la **rr enlazada** dibujada a mano (el brazo de la primera r corre hasta la segunda) y el teclado no la produce.
3. **Monograma "ag.":** las iniciales en minúsculas y un punto cuadrado. El punto es la última casilla de la barra de términos (término cumplido). Sobre verde: letras `marca-papel` y punto `marca-lila`. Sobre lila: letras `marca-tinta` y punto `marca-pino`. Sobre papel: todo `marca-pino`. Nunca en mayúsculas, nunca con el punto redondo.
4. **Una sola tipografía:** Open Sans (400, 500, 600, 700, itálica 400). Los titulares siempre llevan espaciado negativo (-0,015 a -0,03 em).
5. **Piezas fijas vs. interfaz:** Instagram, impresos, tarjeta, membrete, sello y avatar usan **solo tokens `marca-*`**, que no cambian con el modo oscuro. La web y las apps usan los tokens con tema (`pino`, `papel`, `tinta`…).
6. **Contraste:** el texto cumple 4,5:1 en ambos temas. El `lila` nunca va como texto sobre `papel`.
7. **Datos reales:** teléfono y WhatsApp **+57 313 699 4178**, correo **arroyo752tania@gmail.com** Instagram **@taniaarroyo_abogada** y ciudad **Chinú, Córdoba** (sin dirección de calle). Aún no hay número de T.P.: no inventes uno ni dejes ceros de relleno; pídelo si una pieza lo exige. No dejes textos de relleno ni avisos de "ejemplo" en piezas publicadas.

## Color

| Token | Claro | Oscuro | Uso |
| --- | --- | --- | --- |
| `pino` | #17433D | #7CC2B1 | Marca, botón primario. Texto encima: `on-pino` |
| `lila` | #B9A6F2 | #C4B4F6 | Acento joven, solo relleno. Texto encima: `on-lila` |
| `lila-suave` | #ECE6FC | #2A2442 | Fondo de relieve, texto `tinta` |
| `menta` | #DCEBE5 | #1B332E | Fondo secundario, texto `tinta` |
| `papel` | #F4F5F2 | #0D1917 | Fondo de página |
| `superficie` | #FFFFFF | #142421 | Tarjetas y campos |
| `linea` | #D3DAD6 | #2A3D39 | Filetes de 1 px |
| `tinta` / `tinta-suave` | #0E211F / #4F5E5A | #ECF1EE / #A3B3AE | Texto principal / secundario |
| `plazo` / `cumplido` | #A94F17 / #1F5E4D | #F0A06B / #8FD3BE | Estados, siempre con palabra |
| `foco` | #5B3FC4 | #C4B4F6 | Anillo de foco de 2 px |

Fijos (`marca-*`, iguales en ambos temas): `marca-pino` #17433D, `marca-bosque` #0F2E2A, `marca-lila` #B9A6F2, `marca-lila-suave` #ECE6FC, `marca-menta` #DCEBE5, `marca-papel` #F4F5F2, `marca-tinta` #0E211F, `marca-gris` #4F5E5A.

Proporción en una vista: 60 % papel, 25 % pino o bosque, 10 % menta o lila suave, 5 % lila.

## Tipografía (clases en `tokens.css`)

| Estilo | Tamaño / interlínea | Peso | Espaciado |
| --- | --- | --- | --- |
| `display` | 60 / 64 | 500 | -0,03 em |
| `titulo-1` | 38 / 44 | 500 | -0,025 em |
| `titulo-2` | 27 / 34 | 600 | -0,015 em |
| `titulo-3` | 20 / 28 | 600 | -0,01 em |
| `cuerpo` | 16 / 26 | 400 | máx. 65 caracteres por línea |
| `cuerpo-sm` | 14 / 21 | 400 | |
| `cita` | 21 / 32 | 400 itálica | |
| `etiqueta` | 11 / 16 | 600 | +0,16 em, MAYÚSCULAS |
| `norma` | 13 / 18 | 400 | citas normativas y radicados |
| `ig-titular` | 80 / 88 (lienzo 1080) | 600 | -0,03 em, máx. 12 palabras |
| `ig-cuerpo` | 32 / 46 | 400 | máx. 30 palabras por lámina |
| `ig-etiqueta` | 22 / 28 | 600 | +0,14 em, MAYÚSCULAS |

Espaciado en grilla de 4 px (`space-1`=4 … `space-18`=72). Radios: `radius-sm` 4 px (etiquetas, casillas), `radius-md` 10 px (botones, tarjetas), `radius-lg` 22 % (ícono de app), `radius-pill` solo para estados. Una sola sombra (`sombra-tarjeta`); la jerarquía se hace con filetes, no con sombras.

## Voz

- Trata al cliente de **usted**. Tania habla en primera persona del singular ("reviso", "le explico"), nunca "nosotros".
- Frases cortas y en voz activa. Primero la palabra común y después el término técnico: "el plazo para contestar (traslado de la demanda)".
- Cuando des un dato, cita la norma: "Código General del Proceso, art. 369". Verifica la norma antes de publicarla.
- No prometas resultados ("ganamos su caso"). Promete proceso, plazos y claridad.
- Sin emojis en las piezas. En el *caption* se permite como máximo uno, al final.
- Títulos en tipo oración. Mayúsculas solo en las etiquetas.

## Recurso gráfico: barra de términos

Casillas, una por día hábil de un término procesal: las transcurridas llenas en `pino`, la de hoy en `lila`, las que faltan solo con borde. Filas de 10, casillas `space-6`, separación `space-2`, radio `radius-sm`. Úsala cuando la pieza hable de un plazo real y cita la norma debajo. Plantilla: `components/BarraTerminos/preview.html`.

## Cómo hacer cada pieza

Parte siempre de la plantilla de la pieza en `components/` y lee su `README.md`: tiene las medidas, las reglas y los "no".

- **Publicación de Instagram (1080 × 1350):** `components/PostIG/`. Hay cuatro fondos según el propósito: dato útil (`marca-lila-suave`), frase (`marca-pino`), portada de carrusel (`marca-papel`) y área de práctica (`marca-bosque`). Margen de 72 px, logotipo arriba a la izquierda (300 px), etiqueta del área con su ícono arriba a la derecha y el usuario o la norma en el pie. En cada fila del feed, al menos una pieza oscura.
- **Historia (1080 × 1920) y destacados:** `components/StoryIG/`. Deja libres 220 px arriba y 260 px abajo.
- **Tarjeta profesional (85 × 55 mm):** `components/TarjetaProfesional/`. Frente en `marca-pino` con el logotipo apilado. Dorso en `marca-papel` con el nombre, el T.P., los contactos y el monograma "ag.". 3 mm de sangrado.
- **Membrete, memoriales y firma de correo:** `components/Membrete/`. Carta, márgenes de 25 mm y asunto con el radicado completo de 23 dígitos. Existe versión sin color para despachos que la exijan.
- **Web:** el sitio oficial es la app de Next.js en la raíz del repositorio. El texto, el contacto y los casos se editan en `lib/contenido.ts`; los estilos, en `app/globals.css`; las secciones, en `components/`. Para el logotipo, el monograma y los íconos usa `components/Marca.tsx`, que lee `lib/marca.generada.ts` (se genera desde `design-system/` con `npm run marca`). Valida con `npm run typecheck` y `npm run build`. `sitio/` es solo el prototipo estático. Procesal civil es la única área destacada en `marca-pino`. Los casos resueltos son de ejemplo (`CASOS_DE_EJEMPLO`) hasta que haya casos reales autorizados. La agenda usa Cal.com (`TIPOS_CITA` en `lib/contenido.ts`, usuario `arroyotania`): duración, horario y correos se configuran en Cal.com.
- **Avatar, favicon e ícono de app:** `assets/Logos/ag-avatar-circulo.svg`, `ag-sello-pino.svg` y `ag-sello-lila.svg`.

Íconos: usa solo los del grupo `Iconos` (trazo de 1,75 px en grilla de 24, esquinas rectas). Si falta uno, dibújalo con las mismas reglas y guárdalo ahí.

## Cambiar el sistema

Todo sale de los scripts de `design-system/_herramientas/`. No edites a mano los SVG ni las vistas previas: edita el script y regenera.

```bash
cd design-system/_herramientas
pip install -r requirements.txt   # fonttools, uharfbuzz, shapely
python3 tokens.py        # escribe tokens.json (edita aquí colores, estilos, espaciado)
python3 tokens_css.py    # compila tokens.css
python3 logos.py         # logotipo con rr enlazada, apilado, monograma "ag.", sellos y avatar -> assets/Logos + marks.json
python3 previews.py      # plantillas HTML de components/ (usa marks.json e íconos)
python3 vista_previa.py  # arma _vista/<Pieza>-light|dark.html con tokens.css para revisarlas
```

Revisa `_vista/` con capturas en claro y en oscuro antes de dar algo por terminado (Chromium está en `/opt/pw-browsers/chromium`). `_vista/` está en `.gitignore`.

`wm2.py` dibuja el logotipo con la rr enlazada. `lowdet.py` dibuja el monograma "ag." y depende de `mini.py`, `fuse.py` y `lower.py`, que también contienen las exploraciones descartadas (plumilla, AG fusionada, minúsculas con viga). Las imágenes `exploracion-*.png` muestran esas opciones: no las vuelvas a proponer sin que te lo pidan.

Después de un cambio:

1. Actualiza el `README.md` afectado (el del sistema, el de la pieza o el de `assets/Logos/`).
2. Si cambia algo visible, republica el sistema navegable (el artefacto de arriba) con los archivos de `design-system/` bajo `project/`.
3. Haz commit en este repositorio.

## Lista de revisión antes de entregar

- [ ] Logotipo y monograma salen de `assets/Logos/`, no escritos con la fuente.
- [ ] Solo Open Sans, con espaciado negativo en los titulares.
- [ ] Las piezas fijas usan solo tokens `marca-*`.
- [ ] El texto tiene 4,5:1 de contraste; no hay lila como texto sobre papel.
- [ ] Hay una idea por pieza, el titular tiene como máximo 12 palabras y cada dato cita su norma.
- [ ] Trato de usted, primera persona y sin promesas de resultado.
- [ ] Los datos de contacto son los reales y no queda ningún texto de relleno ni aviso de "ejemplo".
