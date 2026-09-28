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

## Sitio web

`sitio/`: página única con áreas, procesos típicos, casos, guía de plazos, agenda de citas y contacto. Vista previa: https://claude.ai/artifact/Jk3s3XRUhyNANvpyRRNBiX. Instrucciones en `sitio/README.md`.

## Skill para Claude

`.claude/skills/arroyo-guzman-marca/SKILL.md` enseña a Claude a usar este sistema: reglas de marca, tokens, voz, cómo hacer cada pieza y cómo regenerar los archivos. Claude Code la carga sola al trabajar en este repositorio.

## Regenerar

```bash
cd design-system/_herramientas
pip install -r requirements.txt
python3 tokens.py && python3 tokens_css.py && python3 logos.py && python3 previews.py && python3 vista_previa.py
```
