import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = HERE + '/..'
IC = P + '/assets/Iconos/'

import json
MARKS = json.load(open(HERE + '/marks.json'))
MARK_D = MARKS['ag']['d']

def _svg(key, cls, label):
    m = MARKS[key]
    return '<svg class="%s" viewBox="0 0 %s %s" role="img" aria-label="%s"><path d="%s"/></svg>' % (cls, m['w'], m['h'], label, m['d'])

def mark(cls='mk'):
    """AG short mark: the A drawn as a fountain-pen nib (slit + breather hole)."""
    return _svg('ag', cls, 'AG')

def seal(cls='mk'):
    """Notarial seal: legend ring + nib monogram."""
    return _svg('sello', cls, 'Sello Arroyo Guzmán, abogada')

def wordmark(cls='wm'):
    """One-line logotype Arroyo Guzmán with the joined rr."""
    return _svg('wordmark', cls, 'Arroyo Guzmán')

def stacked(cls='wm'):
    return _svg('stacked', cls, 'Arroyo Guzmán')

def icon(name, cls='ic'):
    s = open(IC + name + '.svg').read().strip()
    s = s.replace('stroke="#17433D"', 'stroke="currentColor"')
    s = s.replace('<svg ', '<svg class="%s" aria-hidden="true" ' % cls, 1)
    return re.sub(r' width="24" height="24"', '', s)

BASE = """
  html,body{margin:0}
  body{background:var(--papel);color:var(--tinta);font-family:var(--font-sans);-webkit-font-smoothing:antialiased;padding:20px}
  *{box-sizing:border-box}
  .mk path,.wm path{fill:currentColor}
  .wm{display:block;height:auto}
  .ic{width:20px;height:20px;flex:none}
  .lbl{font-size:11px;line-height:14px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--tinta-suave);margin:0 0 8px}
  .row{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}
  .ab{position:relative;overflow:hidden;flex:none}
  .ab>.in{position:absolute;top:0;left:0;transform-origin:0 0}
"""

def doc(marker, title, css, body):
    return ('%s\n<!doctype html>\n<html lang="es">\n<head><meta charset="utf-8"><title>%s</title>\n'
            '<style>%s%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n') % (marker, title, BASE, css, body)

def write(comp, html, readme=None):
    d = P + '/components/' + comp
    os.makedirs(d, exist_ok=True)
    open(d + '/preview.html', 'w').write(html)
    if readme:
        open(d + '/README.md', 'w').write(readme.strip() + '\n')

def ab(w, h, scale, inner, extra=''):
    return ('<div class="ab" style="width:%gpx;height:%gpx%s"><div class="in" style="width:%dpx;height:%dpx;transform:scale(%g)">%s</div></div>'
            % (w * scale, h * scale, extra, w, h, scale, inner))

def terminos(n, done, today=True, cls='tb'):
    cells = []
    for i in range(1, n + 1):
        k = 'hecho' if i <= done else ('hoy' if (today and i == done + 1) else 'libre')
        cells.append('<i class="%s"></i>' % k)
    return '<div class="%s">%s</div>' % (cls, ''.join(cells))

# ---------------------------------------------------------------- Logo
logo_css = """
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
  .tile{border:1px solid var(--linea);border-radius:var(--radius-md);padding:28px 28px 44px;min-height:170px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;position:relative}
  .tile .lbl{position:absolute;left:12px;bottom:4px}
  .t-papel{background:var(--marca-papel);color:var(--marca-tinta)}
  .t-pino{background:var(--marca-pino);color:var(--marca-papel);border-color:var(--marca-pino)}
  .t-lila{background:var(--marca-lila);color:var(--marca-tinta);border-color:var(--marca-lila)}
  .t-pino .lbl{color:var(--marca-papel)} .t-lila .lbl,.t-papel .lbl{color:var(--marca-gris)}
  .sub{font-size:9px;line-height:12px;font-weight:600;letter-spacing:.16em;margin:10px 0 0 2px;text-transform:uppercase;white-space:nowrap}
  .t-papel .sub{color:var(--marca-pino)} .t-pino .sub{color:var(--marca-lila)}
  .zoom{display:flex;align-items:center;justify-content:center;width:100%}
  .zoom svg{width:100%}
  .ag{display:flex;gap:14px;align-items:center}
  .seal{width:72px;height:72px;border-radius:22%;display:flex;align-items:center;justify-content:center}
  .seal .mk{width:62%}
  .seal.p{background:var(--marca-pino);color:var(--marca-lila)} .seal.l{background:var(--marca-lila);color:var(--marca-tinta)}
  .seal.pl{background:var(--marca-papel);color:var(--marca-pino);box-shadow:inset 0 0 0 1px var(--linea)}
  .nibz{display:flex;align-items:center;gap:20px;color:var(--marca-lila)}
  .nibz .mk{width:110px;flex:none}
  .notes{margin:0;padding:0;list-style:none;font-size:12px;line-height:18px;color:var(--marca-papel)}
  .notar{width:150px;height:150px;border-radius:50%;color:var(--marca-pino);display:flex}
  .notar.p{background:var(--marca-pino);color:var(--marca-lila)}
  .notar .mk{width:100%;height:100%}
  .clear{outline:1px dashed var(--marca-lila);padding:14px}
"""
logo_body = """
<div class="grid">
  <div class="tile t-papel">%(w1)s<p class="sub">Abogada · Procesalista civil</p><p class="lbl">Logotipo · principal</p></div>
  <div class="tile t-pino">%(w2)s<p class="sub">Abogada · Procesalista civil</p><p class="lbl">Sobre pino</p></div>
  <div class="tile t-papel">%(st)s<p class="lbl">Apilado</p></div>
  <div class="tile t-papel"><div class="zoom">%(zoom)s</div><p class="lbl">Detalle: la rr enlazada</p></div>
  <div class="tile t-papel"><div class="ag"><div class="seal p">%(m)s</div><div class="seal l">%(m)s</div><div class="seal pl">%(m)s</div></div><p class="lbl">Monograma AG · la A es una plumilla</p></div>
  <div class="tile t-pino"><div class="nibz">%(mz)s<ul class="notes"><li>Punta = la firma</li><li>Ranura = el trazo</li><li>Orificio = el respiradero de la pluma</li></ul></div><p class="lbl">Detalle del monograma</p></div>
  <div class="tile t-papel" style="grid-column:span 2"><div class="ag" style="gap:24px"><div class="notar p">%(sl)s</div><div class="notar">%(sl2)s</div></div><p class="lbl">Sello notarial · avatar y documentos</p></div>
  <div class="tile t-papel"><div class="clear">%(w3)s</div><p class="lbl">Área de respeto = alto de la o</p></div>
</div>
""" % {'w1': wordmark('wm').replace('class="wm"', 'class="wm" style="width:210px"'),
       'w2': wordmark('wm').replace('class="wm"', 'class="wm" style="width:210px"'),
       'st': stacked('wm').replace('class="wm"', 'class="wm" style="width:150px;color:var(--marca-pino)"'),
       'zoom': '<svg class="wm" viewBox="0 0 %s %s" style="width:220px;color:var(--marca-tinta)" aria-hidden="true"><path d="%s"/></svg>' % (MARKS['wordmark']['w'] * 0.335, MARKS['wordmark']['h'], MARKS['wordmark']['d']),
       'm': mark(),
       'mz': mark(),
       'sl': seal(), 'sl2': seal(),
       'w3': wordmark('wm').replace('class="wm"', 'class="wm" style="width:170px;color:var(--marca-pino)"')}
write('Logo', doc('<!-- @dsCard group="Marca" height=640 subtitle="Logotipo con rr enlazada, monograma plumilla y sello notarial" -->', 'Logo', logo_css, logo_body), """
# Logo

Logotipo tipográfico "Arroyo Guzmán" en Open Sans 500 con espaciado de -0,03 em. Su rasgo propio es la **rr enlazada**: el brazo de la primera r corre recto hasta el asta de la segunda, igual que la ff compartida del logotipo de Clifford Chance.

**Qué entrega el consumidor:** nada; use los archivos del grupo de assets `Logos` (SVG con el texto en curvas y la ligadura ya dibujada). No lo reescriba con la fuente: la ligadura no existe en el teclado.

## Versiones

- **Logotipo** (`ag-logotipo-pino.svg`, `-tinta`, `-papel`): la principal, en una línea. Sitio web, membrete, portadas y esquina de las publicaciones.
- **Con descriptor** (`ag-firma-pino.svg`, `ag-firma-papel.svg`): con "Abogada · Procesalista civil" debajo en 600 y mayúsculas espaciadas. Tarjeta, membrete y firma de correo.
- **Apilado** (`ag-apilado-pino.svg`, `ag-apilado-papel.svg`): "Arroyo" sobre "Guzmán", alineado a la izquierda. Frente de la tarjeta, historias, formatos cuadrados.
- **Monograma AG plumilla** (`ag-monograma-pino.svg`, `ag-monograma-papel.svg`, `ag-sello-pino.svg`, `ag-sello-lila.svg`): la A está dibujada como la punta de una pluma estilográfica, con la ranura que baja desde la punta y el orificio respiradero. Es el guiño al derecho: la firma del memorial, del contrato, del poder. Úselo donde el logotipo no cabe: favicon, ícono de app, esquinas, firma de correo.
- **Sello notarial** (`ag-avatar-circulo.svg`, `ag-sello-notarial-pino.svg`): el monograma dentro de un doble anillo con la leyenda "ARROYO GUZMÁN · ABOGADA", como un sello seco. Foto de perfil de Instagram y WhatsApp, dorso de la tarjeta, sello de agua en documentos, sticker para sobres y carpetas. Mínimo 48 px o 18 mm (por debajo de eso la leyenda no se lee: use el monograma).

## Reglas

- Área de respeto: el alto de la "o" por los cuatro lados.
- Tamaño mínimo del logotipo: 110 px o 30 mm de ancho. Por debajo de eso, use el monograma AG (mínimo 16 px).
- Combinaciones: `marca-tinta` o `marca-pino` sobre `marca-papel`; `marca-papel` sobre `marca-pino` o `marca-bosque`; `marca-tinta` sobre `marca-lila`. El descriptor puede ir en `marca-lila` sobre verde.
- No: separar la rr, cerrar la ranura de la plumilla, cambiar la fuente, poner el nombre en mayúsculas, en negrita o en itálica, estirarlo ni añadir sombras.
""")

# ---------------------------------------------------------------- Boton
btn_css = """
  .b{font:500 15px/20px var(--font-sans);padding:12px 20px;border-radius:var(--radius-md);border:1px solid transparent;cursor:pointer;display:inline-flex;align-items:center;gap:8px}
  .b:focus-visible{outline:2px solid var(--foco);outline-offset:2px}
  .p{background:var(--pino);color:var(--on-pino)}
  .p:hover{filter:brightness(1.12)}
  .s{background:transparent;color:var(--tinta);border-color:var(--tinta)}
  .s:hover{background:var(--menta)}
  .l{background:transparent;color:var(--pino);padding-inline:4px;text-decoration:underline;text-decoration-color:var(--lila);text-decoration-thickness:2px;text-underline-offset:5px}
  .dis{opacity:.45;cursor:not-allowed}
  .ring{outline:2px solid var(--foco);outline-offset:2px}
  .row{align-items:center;gap:16px}
"""
btn_body = """
<div class="row">
  <button class="b p" type="button">Agendar consulta</button>
  <button class="b p ring" type="button">Con foco</button>
  <button class="b s" type="button">Ver áreas de práctica</button>
  <button class="b l" type="button">Leer el artículo →</button>
  <button class="b p dis" type="button" disabled>Enviando…</button>
</div>
"""
write('Boton', doc('<!-- @dsCard group="Web" height=90 -->', 'Botón', btn_css, btn_body), """
# Boton

Botón de acción para el sitio web y formularios: primario en `pino`, secundario con borde `tinta`, enlace subrayado en `lila`.

**Qué entrega el consumidor:** el texto del botón (verbo + objeto: "Agendar consulta", "Enviar documentos") y el manejador.

- Un solo botón primario por vista.
- Relleno `space-3` × 20 px, radio `radius-md`, texto `cuerpo-sm` a 500.
- Foco: anillo sólido de 2 px en `foco` con 2 px de separación. Sobre fondos `pino`, el anillo va en `on-pino`.
- Deshabilitado: 45 % de opacidad y un texto que diga qué pasa ("Enviando…").
""")

# ---------------------------------------------------------------- EtiquetaArea
areas = [('procesal', 'Procesal civil'), ('civil', 'Civil'), ('laboral', 'Laboral'), ('familia', 'Familia'),
         ('sucesiones', 'Sucesiones'), ('contratos', 'Contratos'), ('terminos', 'Términos'), ('consulta', 'Consulta')]
ea_css = """
  .chip{display:inline-flex;align-items:center;gap:var(--space-2);padding:6px 12px 6px 8px;border-radius:var(--radius-sm);background:var(--menta);color:var(--tinta);font-size:12px;line-height:16px;font-weight:500;letter-spacing:.12em;text-transform:uppercase}
  .chip .ic{width:18px;height:18px;color:var(--pino)}
  .chip.main{background:var(--pino);color:var(--on-pino)} .chip.main .ic{color:var(--on-pino)}
  .row{gap:10px}
  .icons{display:flex;flex-wrap:wrap;gap:20px;margin-top:20px;color:var(--pino)}
  .icons .ic{width:32px;height:32px}
  .state{display:inline-flex;align-items:center;gap:6px;font-size:13px;line-height:18px;font-weight:500;padding:3px 10px;border-radius:var(--radius-pill);border:1px solid currentColor}
  .ok{color:var(--cumplido)} .warn{color:var(--plazo)}
"""
ea_body = ('<div class="row">' + '<span class="chip main">%s%s</span>' % (icon('procesal'), 'Procesal civil') +
           ''.join('<span class="chip">%s%s</span>' % (icon(k), n) for k, n in areas[1:6]) + '</div>'
           '<div class="icons">' + ''.join(icon(k) for k, _ in areas) + '</div>'
           '<div class="row" style="margin-top:20px"><span class="state ok">● Término cumplido</span><span class="state warn">● Vence en 3 días hábiles</span></div>')
write('EtiquetaArea', doc('<!-- @dsCard group="Web" height=190 -->', 'Etiqueta de área', ea_css, ea_body), """
# EtiquetaArea

Etiqueta de área de práctica con ícono, más los indicadores de estado de un término.

**Qué entrega el consumidor:** el área (una de: Procesal civil, Civil, Laboral, Familia, Sucesiones, Contratos) y su ícono del grupo `Iconos`.

- Procesal civil es la especialidad: es la única etiqueta en `pino` con texto `on-pino`; las demás van en `menta` con texto `tinta`.
- Texto en mayúsculas con el estilo `etiqueta`; radio `radius-sm`.
- Estados: `cumplido` y `plazo`, en píldora `radius-pill`, siempre con palabra. Nunca solo el color.
- Íconos: trazo de 1,75 px en una grilla de 24, esquinas en ángulo recto; el color lo pone el contenedor.
""")

# ---------------------------------------------------------------- BarraTerminos
bt_css = """
  .tb{display:grid;grid-template-columns:repeat(10,var(--space-6));gap:var(--space-2)}
  .tb i{display:block;height:var(--space-6);border-radius:var(--radius-sm);border:1.5px solid var(--pino)}
  .tb i.hecho{background:var(--pino)}
  .tb i.hoy{background:var(--lila);border-color:var(--lila)}
  .cap{display:flex;justify-content:space-between;max-width:312px;font-size:13px;line-height:18px;color:var(--tinta-suave);margin-top:10px}
  .fig{font-variant-numeric:tabular-nums;font-size:40px;line-height:44px;font-weight:600;letter-spacing:-.02em;margin:0 0 4px}
  .wrap{display:flex;flex-wrap:wrap;gap:40px;align-items:flex-end}
"""
bt_body = """
<div class="wrap">
  <div><p class="lbl">Contestación de demanda · proceso verbal</p><p class="fig">Día 14 de 20</p>%s<div class="cap"><span>Notificación</span><span>Vence el término</span></div></div>
  <div><p class="lbl">Recurso de apelación · auto</p><p class="fig">Día 2 de 3</p>%s</div>
</div>
""" % (terminos(20, 13), terminos(3, 1).replace('class="tb"', 'class="tb" style="grid-template-columns:repeat(3,var(--space-6))"'))
write('BarraTerminos', doc('<!-- @dsCard group="Marca" height=170 subtitle="El recurso gráfico propio: los días hábiles de un término" -->', 'Barra de términos', bt_css, bt_body), """
# BarraTerminos

Recurso gráfico propio de la marca: una fila de casillas, una por día hábil de un término procesal; las transcurridas van llenas en `pino` y la de hoy en `lila`.

**Qué entrega el consumidor:** el total de días hábiles del término, los días transcurridos y el nombre de la actuación.

- Úsela para explicar plazos reales (traslado de la demanda, recursos, ejecutoria). Cada casilla es un día hábil: no cuente fines de semana ni festivos.
- Casillas de `space-6` con separación `space-2`, radio `radius-sm`, filas de 10.
- En IG la barra puede ser el único gráfico de la pieza; en web acompaña el seguimiento de un caso.
- Cite la norma debajo con el estilo `norma` (por ejemplo "CGP, art. 369").
""")

# ---------------------------------------------------------------- PostIG (feed 1080x1350)
ig_css = """
  .post{width:1080px;height:1350px;padding:var(--space-18);display:flex;flex-direction:column;font-family:var(--font-sans);position:relative}
  .post .mk{width:72px;height:72px}
  .post .wm{width:300px}
  .eye{font-size:22px;line-height:28px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin:0;display:flex;align-items:center;gap:14px}
  .eye .ic{width:36px;height:36px}
  .h{font-size:80px;line-height:88px;font-weight:600;letter-spacing:-.03em;margin:0;text-wrap:balance}
  .b{font-size:34px;line-height:46px;margin:0}
  .foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:24px;line-height:30px}
  .hand{font-weight:500}
  .tbig{display:grid;grid-template-columns:repeat(10,64px);gap:16px;margin:56px 0 24px}
  .tbig i{display:block;height:64px;border-radius:8px;border:3px solid var(--marca-pino)}
  .tbig i.hecho{background:var(--marca-pino)} .tbig i.hoy{background:var(--marca-lila);border-color:var(--marca-lila)}
  .v-tip{background:var(--marca-lila-suave);color:var(--marca-tinta)} .v-tip .wm,.v-tip .eye{color:var(--marca-pino)}
  .v-cita{background:var(--marca-pino);color:var(--marca-papel)} .v-cita .wm{color:var(--marca-papel)}
  .v-cita .q{font-size:76px;line-height:92px;font-style:italic;font-weight:400;letter-spacing:-.01em;margin:auto 0 0;text-wrap:balance}
  .v-cita .q em{font-style:italic;background:linear-gradient(transparent 62%,rgba(185,166,242,.55) 62%)}
  .v-car{background:var(--marca-papel);color:var(--marca-tinta)} .v-car .wm{color:var(--marca-pino)}
  .v-car .num{font-size:420px;line-height:340px;font-weight:600;letter-spacing:-.05em;color:var(--marca-pino);margin:auto 0 24px}
  .v-car .pg{font-variant-numeric:tabular-nums}
  .v-area{background:var(--marca-bosque);color:var(--marca-papel)} .v-area .wm{color:var(--marca-papel)}
  .v-area .eye{color:var(--marca-lila)}
  .v-area .list{margin:48px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:0}
  .v-area .list li{font-size:34px;line-height:46px;padding:22px 0;border-top:2px solid rgba(244,245,242,.22)}
  .top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:auto}
  .src{font-size:22px;line-height:28px;color:var(--marca-gris)}
  .v-car .rule{height:4px;width:160px;background:var(--marca-lila);margin:0 0 40px}
"""
S = 0.25
tip = """<div class="post v-tip"><div class="top">%s<p class="eye">%sProcesal civil · Dato útil</p></div>
<p class="h">¿Le notificaron una demanda? Tiene 20 días hábiles para contestarla.</p>%s
<p class="b">Cuente desde el día siguiente a la notificación. Sin contestación, el juez puede tener por ciertos los hechos.</p>
<div class="foot"><span class="src">Código General del Proceso, arts. 97 y 369</span><span class="hand">@arroyoguzman.abogada</span></div></div>""" % (wordmark(), icon('terminos'), terminos(20, 13, cls='tbig'))
cita = """<div class="post v-cita"><div class="top">%s<p class="eye" style="color:var(--marca-lila)">Cómo trabajo</p></div>
<p class="q">“Un proceso bien llevado empieza por un <em>plazo bien contado.</em>”</p>
<div class="foot" style="margin-top:72px"><span class="hand">Tania Arroyo Guzmán · Abogada</span><span>Procesalista civil</span></div></div>""" % wordmark()
car = """<div class="post v-car"><div class="top">%s<p class="eye" style="color:var(--marca-pino)">Contratos · Arrendamiento</p></div>
<p class="num">5</p><div class="rule"></div>
<p class="h" style="font-size:68px;line-height:76px">cosas que debe revisar antes de firmar un contrato de arriendo</p>
<div class="foot"><span class="hand">@arroyoguzman.abogada</span><span class="pg">1/6 · Deslice →</span></div></div>""" % wordmark()
area = """<div class="post v-area"><div class="top">%s<p class="eye">%sLaboral</p></div>
<p class="h" style="margin-top:0">¿Terminaron su contrato sin justa causa?</p>
<ul class="list"><li>Revisamos su liquidación y la indemnización.</li><li>Calculamos lo que le deben, con soporte.</li><li>Negociamos o demandamos, según su caso.</li></ul>
<div class="foot"><span class="hand">Agende su consulta · link en la biografía</span></div></div>""" % (wordmark(), icon('laboral'))
ig_body = '<div class="row">' + ''.join(
    '<div><p class="lbl">%s</p>%s</div>' % (lab, ab(1080, 1350, S, x)) for lab, x in
    [('Dato útil · lila suave', tip), ('Frase · pino', cita), ('Portada de carrusel · papel', car), ('Área de práctica · bosque', area)]) + '</div>'
write('PostIG', doc('<!-- @dsCard group="Instagram" height=400 subtitle="Feed 1080 × 1350 (4:5), mostrado al 25 %" -->', 'Publicaciones IG', ig_css, ig_body), """
# PostIG

Cuatro plantillas de publicación para el feed de Instagram a 1080 × 1350 px (4:5): dato útil, frase, portada de carrusel y área de práctica.

**Qué entrega el consumidor:** antetítulo (área), un titular de máximo 12 palabras, un texto de apoyo de máximo 30 palabras y, si aplica, la norma citada.

## Estructura fija

- Margen de seguridad `space-18` (72 px) en los cuatro lados.
- Arriba a la izquierda el logotipo de 300 px de ancho; arriba a la derecha el antetítulo en `ig-etiqueta` con el ícono del área.
- Titular en `ig-titular`, texto en `ig-cuerpo`, pie con el usuario `@arroyoguzman.abogada` o la norma en `norma` ampliado.
- Solo tokens `marca-*`: las piezas no cambian con el tema del teléfono.

## Cuándo usar cada fondo

| Plantilla | Fondo | Para |
| --- | --- | --- |
| Dato útil | `marca-lila-suave` | Plazos, requisitos, preguntas frecuentes. Lleva la barra de términos cuando hay un plazo. |
| Frase | `marca-pino` | Forma de trabajo, valores, testimonios (con permiso escrito del cliente). |
| Portada de carrusel | `marca-papel` | Guías de 5 a 8 láminas; el número grande dice cuántos puntos hay. |
| Área de práctica | `marca-bosque` | Presentar un servicio: laboral, familia, sucesiones, contratos, civil. |

## Ritmo del feed

Alterne claro y oscuro: en cada fila de tres publicaciones debe haber al menos una en `marca-pino` o `marca-bosque`. Máximo una frase por semana; el resto, contenido útil.

## No

- Martillos de juez, balanzas doradas, columnas griegas ni fotos de banco de imágenes con toga.
- Promesas de resultado ("ganamos su caso"). Hable de proceso, plazos y claridad.
- Más de dos tamaños de texto en una misma lámina.
""")

# ---------------------------------------------------------------- StoryIG + Destacados
st_css = ig_css + """
  .story{width:1080px;height:1920px;padding:220px var(--space-18) 260px;display:flex;flex-direction:column;background:var(--marca-bosque);color:var(--marca-papel)}
  .story .wm{width:420px;color:var(--marca-papel)}
  .story .h{font-size:96px;line-height:100px;margin:auto 0 40px}
  .story .b{color:var(--marca-papel);opacity:.85}
  .cta{margin-top:72px;background:var(--marca-lila);color:var(--marca-tinta);border-radius:20px;padding:40px 48px;font-size:40px;line-height:48px;font-weight:600;display:flex;justify-content:space-between}
  .hl{display:flex;flex-wrap:wrap;gap:18px}
  .hl figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:8px;width:76px}
  .hl .c{width:68px;height:68px;border-radius:50%;background:var(--marca-pino);color:var(--marca-lila);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 2px var(--papel),0 0 0 3.5px var(--linea)}
  .hl .c.alt{background:var(--marca-lila-suave);color:var(--marca-pino)}
  .hl .c .ic{width:30px;height:30px}
  .hl figcaption{font-size:12px;line-height:14px;color:var(--tinta)}
  .col{display:flex;flex-direction:column;gap:24px}
"""
story = """<div class="story">%s<p class="h">Una consulta a tiempo evita un proceso.</p>
<p class="b">Primera consulta de 45 minutos, presencial o virtual. Le digo qué opciones tiene y cuánto tardaría cada una.</p>
<div class="cta"><span>Agendar consulta</span><span>→</span></div></div>""" % stacked()
hls = [('consulta', 'Consultas', 0), ('procesal', 'Procesos', 0), ('laboral', 'Laboral', 1), ('familia', 'Familia', 1),
       ('sucesiones', 'Sucesiones', 1), ('contratos', 'Contratos', 1), ('terminos', 'Plazos', 0)]
hl = '<div class="hl">' + ''.join('<figure><div class="c%s">%s</div><figcaption>%s</figcaption></figure>' % (' alt' if a else '', icon(k), n) for k, n, a in hls) + '</div>'
st_body = '<div class="row"><div><p class="lbl">Historia 1080 × 1920</p>%s</div><div class="col" style="max-width:360px"><div><p class="lbl">Portadas de destacados</p>%s</div></div></div>' % (ab(1080, 1920, 0.18, story), hl)
write('StoryIG', doc('<!-- @dsCard group="Instagram" height=390 subtitle="Historia 9:16 y portadas de destacados" -->', 'Historias IG', st_css, st_body), """
# StoryIG

Plantilla de historia de Instagram (1080 × 1920) y portadas circulares de destacados con los íconos de área.

**Qué entrega el consumidor:** una frase de máximo 8 palabras, un texto de apoyo corto y el llamado a la acción.

- Deje libres 220 px arriba y 260 px abajo: ahí van la barra de progreso, el nombre de la cuenta y la caja de respuesta.
- Fondo `marca-bosque`, logotipo apilado en `marca-papel`, botón de llamado en `marca-lila` con texto `marca-tinta`.
- Destacados: círculo `marca-pino` con ícono `marca-lila` para lo propio del despacho (Consultas, Procesos, Plazos); círculo `marca-lila-suave` con ícono `marca-pino` para las áreas.
- Íconos del grupo `Iconos`, al 45 % del diámetro del círculo.
""")

# ---------------------------------------------------------------- TarjetaProfesional (85 x 55 mm @ 12 px/mm)
tp_css = """
  .card{width:1020px;height:660px;border-radius:24px;padding:72px;font-family:var(--font-sans);display:flex;flex-direction:column;position:relative;overflow:hidden}
  .fr{background:var(--marca-pino);color:var(--marca-papel)}
  .fr .wm{width:520px;color:var(--marca-papel)}
  .fr .nm{display:none}
  .fr .ro{font-size:21px;line-height:28px;letter-spacing:.16em;font-weight:600;text-transform:uppercase;margin:28px 0 0 4px;color:var(--marca-lila)}
  .fr .lg{margin-top:auto}
  .fr .tb2{position:absolute;right:72px;top:72px;display:grid;grid-template-columns:repeat(5,28px);gap:10px}
  .fr .tb2 i{height:28px;border-radius:5px;border:2px solid var(--marca-lila)} .fr .tb2 i.hecho{background:var(--marca-lila)}
  .bk{background:var(--marca-papel);color:var(--marca-tinta)}
  .bk .nm{font-size:44px;line-height:52px;font-weight:600;letter-spacing:-.025em;margin:0}
  .bk .ro{font-size:24px;line-height:32px;margin:8px 0 0;color:var(--marca-pino);font-weight:500}
  .bk .tp{font-size:20px;line-height:26px;color:var(--marca-gris);margin:6px 0 0}
  .bk .ct{margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:10px 28px;font-size:25px;line-height:34px}
  .bk .ct span:nth-child(odd){font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:var(--marca-gris);font-weight:500;line-height:34px}
  .bk .corner{position:absolute;right:64px;top:56px;width:190px;height:190px;color:var(--marca-pino)}
  .bk .ar{position:absolute;right:72px;bottom:72px;display:flex;gap:14px;color:var(--marca-pino)}
  .bk .ar .ic{width:34px;height:34px}
  .shadow{box-shadow:var(--sombra-tarjeta);border-radius:6px}
"""
front = '<div class="card fr"><div class="lg">%s</div><p class="ro">Abogada · Procesalista civil</p><div class="tb2">%s</div></div>' % (stacked(), ''.join('<i class="hecho"></i>' if i < 4 else '<i></i>' for i in range(5)))
back = ('<div class="card bk">%s'
        '<p class="nm" style="margin-top:20px">Tania Arroyo Guzmán</p><p class="ro">Abogada · Procesalista civil</p><p class="tp">T.P. 000.000 del C. S. de la J.</p>'
        '<div class="ct"><span>Tel</span><span>+57 300 000 0000</span><span>Correo</span><span>hola@arroyoguzman.co</span><span>IG</span><span>@arroyoguzman.abogada</span></div>'
        '<div class="ar">%s</div></div>') % (seal('mk corner'), ''.join(icon(k) for k in ['procesal', 'laboral', 'familia', 'sucesiones', 'contratos']))
tp_body = '<div class="row"><div><p class="lbl">Frente · 85 × 55 mm</p><div class="shadow">%s</div></div><div><p class="lbl">Dorso</p><div class="shadow">%s</div></div></div><p class="lbl" style="margin-top:14px">Datos de ejemplo: reemplace T.P., teléfono y correo reales antes de imprimir.</p>' % (ab(1020, 660, 0.34, front, ';border-radius:8px'), ab(1020, 660, 0.34, back, ';border-radius:8px'))
write('TarjetaProfesional', doc('<!-- @dsCard group="Aplicaciones" height=300 -->', 'Tarjeta profesional', tp_css, tp_body), """
# TarjetaProfesional

Tarjeta de presentación de 85 × 55 mm a dos caras: frente en `marca-pino` con el logotipo apilado, dorso en `marca-papel` con datos de contacto y número de tarjeta profesional.

**Qué entrega el consumidor:** número de Tarjeta Profesional del Consejo Superior de la Judicatura, teléfono, correo y usuario de Instagram reales. Los de la vista previa son de ejemplo.

## Especificación de impresión

- Tamaño final 85 × 55 mm, 3 mm de sangrado, margen interno de 6 mm.
- Papel: cartulina sin estucar de 350 g o más (tipo algodón o Conqueror), acabado mate.
- Frente: fondo `marca-pino` (pida prueba de color impresa antes del tiraje) y logotipo apilado en `marca-papel`; si el presupuesto lo permite, logotipo en relieve seco o *hot stamping* blanco.
- Dorso: tinta `marca-tinta` y `marca-pino` sobre papel natural blanco.
- Tipografía: Open Sans; nombre en 600, datos en 400.
- Las cinco casillas del frente son la barra de términos en miniatura: cuatro cumplidas y una por venir.
- Dorso: el sello notarial arriba a la derecha. Si se imprime con relieve seco, el sello queda como un sello de notaría real.
""")

# ---------------------------------------------------------------- Membrete + FirmaCorreo
mb_css = """
  .page{width:816px;height:1056px;background:var(--marca-papel);color:var(--marca-tinta);padding:72px 88px;display:flex;flex-direction:column;font-family:var(--font-sans)}
  .hd{display:flex;justify-content:space-between;align-items:center;padding-bottom:22px;border-bottom:1px solid var(--marca-pino)}
  .hd .lk{display:flex;align-items:center;gap:14px}
  .hd .wm{width:190px;color:var(--marca-tinta)}
  .hd .nm{display:none}
  .hd .sb{font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;margin:8px 0 0 1px;color:var(--marca-pino);font-weight:600}
  .hd .rf{font-size:11px;line-height:16px;text-align:right;color:var(--marca-gris);font-variant-numeric:tabular-nums}
  .bd{padding-top:44px;font-size:13.5px;line-height:21px}
  .bd p{margin:0 0 14px;max-width:62ch}
  .bd .as{font-weight:600}
  .bd .ln{height:9px;background:rgba(14,33,31,.08);border-radius:2px;margin:0 0 12px}
  .ft{margin-top:auto;display:flex;justify-content:space-between;font-size:10px;line-height:14px;color:var(--marca-gris);padding-top:14px;border-top:1px solid rgba(14,33,31,.15)}
  .sig{background:var(--superficie);border:1px solid var(--linea);border-radius:var(--radius-md);padding:20px 24px;display:flex;gap:16px;align-items:flex-start;max-width:440px}
  .sig .seal{width:44px;height:44px;border-radius:22%;background:var(--marca-pino);color:var(--marca-lila);display:flex;align-items:center;justify-content:center;flex:none}
  .sig .seal .mk{width:62%}
  .sig p{margin:0;font-size:14px;line-height:20px}
  .sig .n{font-weight:600;font-size:16px}
  .sig .r{color:var(--pino);font-weight:500}
  .sig .d{color:var(--tinta-suave);margin-top:6px}
  .sig .x{margin-top:10px;font-size:11px;line-height:15px;color:var(--tinta-suave);border-top:1px solid var(--linea);padding-top:10px}
"""
page = """<div class="page"><div class="hd"><div class="lk"><div>%s<p class="sb">Abogada · Procesalista civil</p></div></div>
<div class="rf">Bogotá D. C., 28 de septiembre de 2026<br>Ref.: TA-2026-041</div></div>
<div class="bd"><p>Señor<br><b>Juez Civil Municipal</b><br>E. S. D.</p>
<p class="as">Asunto: Contestación de la demanda · Proceso verbal · Rad. 11001-40-03-000-2026-00000-00</p>
<p>Tania Arroyo Guzmán, identificada como aparece al pie de mi firma, en calidad de apoderada de la parte demandada, dentro del término de traslado, me permito contestar la demanda en los siguientes términos:</p>
<div class="ln" style="width:92%%"></div><div class="ln" style="width:86%%"></div><div class="ln" style="width:90%%"></div><div class="ln" style="width:60%%"></div></div>
<div class="ft"><span>+57 300 000 0000 · hola@arroyoguzman.co</span><span>T.P. 000.000 del C. S. de la J.</span></div></div>""" % wordmark()
sig = """<div class="sig"><div class="seal">%s</div><div><p class="n">Tania Arroyo Guzmán</p><p class="r">Abogada · Procesalista civil</p>
<p class="d">+57 300 000 0000<br>hola@arroyoguzman.co · @arroyoguzman.abogada</p>
<p class="x">Este mensaje y sus anexos son confidenciales y están amparados por el secreto profesional.</p></div></div>""" % mark()
mb_body = '<div class="row"><div><p class="lbl">Membrete · carta</p>%s</div><div><p class="lbl">Firma de correo</p>%s</div></div>' % (ab(816, 1056, 0.36, page, ';box-shadow:var(--sombra-tarjeta)'), sig)
write('Membrete', doc('<!-- @dsCard group="Aplicaciones" height=420 subtitle="Memoriales, cartas y firma de correo" -->', 'Membrete', mb_css, mb_body), """
# Membrete

Hoja membreteada tamaño carta para memoriales, cartas y cotizaciones, más la firma de correo electrónico.

**Qué entrega el consumidor:** ciudad y fecha, referencia interna, destinatario, asunto con número de radicado y el cuerpo del escrito.

## Membrete

- Carta (216 × 279 mm), márgenes de 25 mm laterales; logotipo con descriptor de 50 mm arriba a la izquierda; fecha y referencia interna a la derecha.
- Un filete de 1 px en `marca-pino` bajo el encabezado; pie con contacto y número de T.P. en `marca-gris`.
- Cuerpo en Open Sans 400 a 10,5–11 pt, interlineado 1,5. El asunto en 600 con el radicado completo de 23 dígitos.
- Para radicar ante despachos que exigen formato plano, use la misma plantilla sin color: todo en `marca-tinta`.

## Firma de correo

- Monograma plumilla de 44 px, nombre completo en 600, cargo en `pino`, contacto en `tinta-suave` con números tabulares.
- Cierre con la nota de confidencialidad en 11 px. Sin frases motivacionales ni íconos de redes en color.
""")

# ---------------------------------------------------------------- Cover
cover_css = """
  body{padding:0;overflow:hidden}
  .cover{position:relative;width:960px;height:320px;overflow:hidden;background:var(--papel)}
  .art{position:absolute;top:0;left:480px;width:480px;height:320px}
  .art svg{display:block;width:480px;height:320px}
  .pino{fill:var(--pino)} .tinta{fill:var(--marca-bosque)} .lila{fill:var(--lila)} .menta{fill:var(--menta)} .mmenta{fill:var(--marca-menta)}
  .blk{rx:var(--radius-md)}
  .cel{rx:var(--radius-sm)}
  .cel.vacio{fill:none;stroke:var(--menta);stroke-width:1.5}
  .cel.lleno{fill:var(--lila)}
  .cel.hecha{fill:var(--menta)}
  .mkc{fill:var(--marca-lila)}
  .words{position:absolute;left:48px;bottom:40px;max-width:440px}
  .name{margin:0;font-size:100px;line-height:1;color:var(--tinta)}
  .tag{margin:18px 0 0 4px;font-size:14px;line-height:20px;color:var(--tinta-suave)}
"""
# grid of business-day cells on the pino slab: 5 columns (a work week) x 4 rows = 20 days, 13 done, today lila
cells = []
x0, y0, pitch, sz = 40, 64, 32, 24
for i in range(20):
    r, cidx = divmod(i, 5)
    k = 'hecha' if i < 13 else ('lleno' if i == 13 else 'vacio')
    cells.append('<rect class="cel %s" x="%d" y="%d" width="%d" height="%d" rx="4"/>' % (k, x0 + cidx * pitch, y0 + r * pitch, sz, sz))
cover_svg = """<svg viewBox="0 0 480 320" width="480" height="320">
<!--
  blocks      pino 216x288 slab bled off the top (the brand, largest) · marca-bosque 160x160 · lila 160x96 (youth accent) · menta 112x56 tint — about 40%% of 960x320
  arrangement one tall pino slab with satellites stacked right, bottoms on a line space-6 above the edge, space-4 gutters
  pattern     the barra de terminos: 20 business-day cells (5 per week x 4) at a space-8 pitch, 13 done in menta, today in lila, the rest outlined in menta, cut into the slab; chosen because the README says every piece is about a term met on time
  scales      cells space-6 with space-2 gaps; gutters space-4; corners radius-md, cells radius-sm
-->
<rect class="pino blk" x="16" y="-16" width="216" height="312" rx="10"/>
%s
<rect class="tinta blk" x="248" y="136" width="160" height="160" rx="10"/>
<g transform="translate(%.2f %.2f) scale(%.4f)"><path class="mkc" d="%s"/></g>
<rect class="lila blk" x="248" y="24" width="160" height="96" rx="10"/>
<rect class="mmenta blk" x="424" y="240" width="112" height="56" rx="10"/>
</svg>""" % (''.join(cells), 248 + (160 - MARKS['ag']['w'] * 0.9) / 2, 136 + (160 - MARKS['ag']['h'] * 0.9) / 2, 0.9, MARK_D)
cover_body = '<div class="cover"><div class="art" aria-hidden="true">%s</div><div class="words"><h1 class="name">%s</h1><p class="tag">Abogada procesalista civil. Cada término, cumplido.</p></div></div>' % (cover_svg, stacked('wm').replace('class="wm"', 'class="wm" style="width:360px"'))
cover_body = cover_body.replace('<br>', ' <br>')
open(P + '/components/Cover/preview.html', 'w').write(doc('<!-- @dsCard height=320 -->', 'Arroyo Guzmán', cover_css, cover_body)) if os.path.isdir(P + '/components/Cover') else None
os.makedirs(P + '/components/Cover', exist_ok=True)
open(P + '/components/Cover/preview.html', 'w').write(doc('<!-- @dsCard height=320 -->', 'Arroyo Guzmán', cover_css, cover_body))
print('ok', sorted(os.listdir(P + '/components')))
