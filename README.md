# Arroyo Guzmán: sistema de diseño

Identidad visual de **Arroyo Guzmán**, la imagen legal de Tania Arroyo Guzmán, abogada independiente especialista en derecho procesal civil.

Sistema de diseño publicado (vista navegable): https://claude.ai/artifact/6NcsJ5hDbYVhGsdj9qQMRf

## Contenido

- `design-system/README.md`: manual de marca (esencia, voz, color, tipografía, logo, iconografía, fotografía).
- `design-system/guias/referentes.md`: investigación de firmas que renovaron su marca (A&O Shearman, Freshfields, Clifford Chance, Mishcon de Reya, Hogan Lovells).
- `design-system/tokens.json`: paleta, tipografía, espaciado, radios y sombra. `design-system/tokens.css`: los mismos tokens compilados para web.
- `design-system/assets/Logos/`: logotipo tipográfico en SVG (una línea, con descriptor, apilado) y monograma "ag." (sin fondo, sello y avatar).
- `design-system/assets/Iconos/`: íconos de áreas de práctica.
- `design-system/fonts/`: Open Sans (licencia libre OFL), la alternativa libre más cercana a la letra de Clifford Chance.
- `design-system/components/`: plantillas en HTML para Instagram (feed e historias), tarjeta profesional, membrete, firma de correo y elementos web.
- `design-system/_herramientas/`: scripts en Python (fontTools, uharfbuzz, shapely) que generan los logos con la rr enlazada, los tokens y las plantillas.

## Sitio web (Next.js)

La app está en la raíz del repositorio: Next.js 16 (App Router) con TypeScript, sin librerías de estilos. Los colores, la tipografía, el logotipo y los íconos salen de `design-system/`.

```bash
npm install
cp .env.example .env.local   # y complete los valores
npm run dev                  # http://localhost:3000
npm run build && npm start   # producción
```

| Carpeta | Qué hay |
| --- | --- |
| `app/` | `layout.tsx` (metadatos, datos estructurados, estilos), `page.tsx`, `globals.css`, `api/citas/route.ts`, ícono, `sitemap` y `robots` |
| `components/` | Una pieza por sección: encabezado, portada, áreas, método, procesos, casos, guía, agenda, contacto y pie; `Marca.tsx` con el logotipo, el monograma, los íconos y la barra de términos |
| `lib/contenido.ts` | **Todo el texto del sitio**, los datos de contacto y los casos. Se edita aquí. |
| `lib/citas.ts` | Validación de citas (compartida por el formulario y la API), días hábiles con festivos de Colombia y el mensaje de WhatsApp |
| `lib/marca.generada.ts` | Logotipo, monograma e íconos generados desde `design-system/` por `scripts/generar-marca.mjs` (se regenera antes de `dev` y `build`) |

**Agenda de citas.** El formulario muestra los próximos 10 días hábiles (sin fines de semana ni festivos), valida los datos y los envía a `POST /api/citas`. La API los valida otra vez y los reenvía como JSON a `CITAS_WEBHOOK_URL` (por ejemplo, un webhook de Zapier, Make, n8n o Google Apps Script que los guarde en una hoja o los mande por correo). Sin esa variable, la solicitud solo queda en el log del servidor. Después, la persona puede enviar el resumen por WhatsApp.

**Variables de entorno** (ver `.env.example`): `NEXT_PUBLIC_WHATSAPP`, `CITAS_WEBHOOK_URL`, `NEXT_PUBLIC_SITIO_URL`.

**Publicar.** Vercel detecta Next.js sin configuración: importe el repositorio, agregue las variables de entorno y despliegue. También funciona en cualquier servidor con Node 20.9 o superior (`npm run build && npm start`).

**Antes de salir a producción:**

1. Datos reales en `lib/contenido.ts` (`CONTACTO`) y `datosDeEjemplo: false`.
2. Casos reales, anonimizados y autorizados por escrito en `CASOS`, y `CASOS_DE_EJEMPLO = false`.
3. `CITAS_WEBHOOK_URL` configurada, para no perder solicitudes.
4. Enlace a la política de tratamiento de datos personales (Ley 1581 de 2012) junto a la casilla de autorización.
5. Verificación de las normas citadas.

`sitio/` conserva la versión estática en un solo archivo HTML que se usó como prototipo (vista previa: https://claude.ai/artifact/Jk3s3XRUhyNANvpyRRNBiX). La versión oficial es la app de Next.js.

## Skill para Claude

`.claude/skills/arroyo-guzman-marca/SKILL.md` enseña a Claude a usar este sistema: reglas de marca, tokens, voz, cómo hacer cada pieza y cómo regenerar los archivos. Claude Code la carga sola al trabajar en este repositorio.

## Regenerar

```bash
cd design-system/_herramientas
pip install -r requirements.txt
python3 tokens.py && python3 tokens_css.py && python3 logos.py && python3 previews.py && python3 vista_previa.py
```
