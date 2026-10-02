# Arma el manual de marca (A4) en HTML desde el sistema de diseño y lo exporta a PDF con Chromium.
#   python3 docs/manual/construir.py     -> docs/Manual-de-marca-Arroyo-Guzman.pdf
import json, os, subprocess, html, re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..'))
DS = os.path.join(RAIZ, 'design-system')
IMG = os.path.join(RAIZ, 'docs', 'img')
T = json.load(open(os.path.join(DS, 'tokens.json')))
M = json.load(open(os.path.join(DS, '_herramientas', 'marks.json')))
COL = {c['name']: c['value'] for c in T['color']['tokens']}
U = {c['name']: c['usage'] for c in T['color']['tokens']}

def img(nombre, estilo=''):
    return '<img src="file://%s/%s" alt="" style="%s">' % (IMG, nombre, estilo)
def logo(archivo, estilo=''):
    return '<img src="file://%s/assets/Logos/%s" alt="" style="%s">' % (DS, archivo, estilo)
def icono(nombre, color='#17433D', px=28):
    s = open(os.path.join(DS, 'assets', 'Iconos', nombre + '.svg')).read().replace('#17433D', color)
    return s.replace('width="24" height="24"', 'width="%d" height="%d"' % (px, px))
def svg(key, fill, w, dot=None):
    m = M[key]
    d2 = '<path fill="%s" d="%s"/>' % (dot or fill, m['dot']) if 'dot' in m else ''
    return '<svg viewBox="0 0 %s %s" style="width:%s;display:block"><path fill="%s" d="%s"/>%s</svg>' % (m['w'], m['h'], w, fill, m['d'], d2)

def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda x: x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def cr(a, b):
    A, B = sorted([lum(a), lum(b)], reverse=True); return (A + 0.05) / (B + 0.05)

paginas = []
def pagina(contenido, clase='', folio=True, seccion=''):
    n = len(paginas) + 1
    pie = '<div class="folio"><span>Arroyo Guzmán · Manual de marca</span><span>%s</span><span>%02d</span></div>' % (seccion, n) if folio else ''
    paginas.append('<section class="pag %s">%s%s</section>' % (clase, contenido, pie))

def cab(etq, titulo, intro=''):
    return '<p class="etq">%s</p><h2>%s</h2>%s' % (etq, titulo, '<p class="intro">%s</p>' % intro if intro else '')

# ------------------------------------------------------------------ 1. Portada
pagina('''
<div class="port-top">%s</div>
<div class="port-cas">%s</div>
<div class="port-txt">
  <p class="etq lila">Manual de marca y sistema de diseño</p>
  <h1>Cada término,<br>cumplido.</h1>
  <p class="port-sub">Tania Arroyo Guzmán · Abogada · Procesalista civil</p>
  <p class="port-ver">Versión 1.0 · Septiembre de 2026</p>
</div>''' % (svg('stacked', COL['marca-papel']['light'], '300px'),
             ''.join('<i class="%s"></i>' % ('h' if i < 13 else 'hoy' if i == 13 else '') for i in range(20))), 'portada', folio=False)

# ------------------------------------------------------------------ 2. Contenido
indice = [('La marca', 'Esencia, idea central y voz'), ('Referentes', 'Lo que tomamos de las firmas que se renovaron'),
          ('Logotipo', 'Versiones, la rr enlazada y reglas de uso'), ('Monograma', 'ag. y el punto de término cumplido'),
          ('Color', 'Paleta de marca y tokens de interfaz'), ('Tipografía', 'Open Sans y la escala de estilos'),
          ('Recursos gráficos', 'Barra de términos e íconos'), ('Voz y tono', 'Cómo escribe Arroyo Guzmán'),
          ('Instagram', 'Publicaciones, historias y destacados'), ('Aplicaciones', 'Tarjeta, membrete y firma de correo'),
          ('Sitio web', 'Estructura, agenda de citas y versión móvil'), ('Implementación', 'Archivos, tokens y lista de revisión')]
pagina(cab('Contenido', 'Qué encontrará en este manual') + '<ol class="indice">%s</ol>' % ''.join(
    '<li><b>%s</b><span>%s</span></li>' % x for x in indice), seccion='Contenido')

# ------------------------------------------------------------------ 3. La marca
pagina(cab('01 · La marca', 'Una abogada joven que cumple cada plazo',
           'Arroyo Guzmán es la imagen legal de Tania Arroyo Guzmán, abogada independiente especialista en derecho procesal civil, que atiende casos civiles, laborales, de familia, sucesiones y contratos.') + '''
<div class="idea"><p class="etq lila">Idea central</p><p class="grande">“Cada término, cumplido.”</p>
<p>Los términos procesales son el oficio de una procesalista. La marca los vuelve imagen con la barra de términos y los repite en el punto del monograma.</p></div>
<div class="tres">
 <div><h3>Responsable antes que solemne</h3><p>Nada de mármol, columnas, martillos ni dorados. La seriedad se nota en la precisión: fechas, normas citadas, pasos claros.</p></div>
 <div><h3>Joven por el color, no por el tono</h3><p>El lila y los fondos de relieve aportan frescura; el texto sigue siendo sobrio y claro.</p></div>
 <div><h3>Una voz, muchas áreas</h3><p>Procesal civil es la especialidad y encabeza todo. Las demás áreas se presentan con la misma estructura y su propio ícono.</p></div>
</div>''', seccion='La marca')

# ------------------------------------------------------------------ 4. Referentes
filas = [('A&O Shearman', '2024 · Landor', 'Dejó los azules y rojos del sector por un verde vibrante, mucho espacio en blanco y titulares cortos.', 'El verde como color de marca y el espacio en blanco como señal de orden.'),
         ('Freshfields', '2024', 'Acortó su nombre a "Freshfields", el nombre que el mercado ya usaba.', 'Un nombre corto y propio: "Arroyo Guzmán", sin siglas ni "& Asociados".'),
         ('Clifford Chance', '2025', 'Logotipo sans serif humanista, en caja baja, espaciado apretado y una ff enlazada.', 'La base del logotipo: Open Sans como equivalente libre y la rr enlazada.'),
         ('Mishcon de Reya', 'October Associates', 'Mantuvo el logo y amplió una paleta que tenía dos colores.', 'Una paleta amplia (pino, bosque, lila, menta) para dar ritmo en redes.'),
         ('Hogan Lovells', '', 'Un único gráfico propio que se invierte y recorta según el contenido.', 'La barra de términos: un recurso con muchas variaciones.')]
pagina(cab('02 · Referentes', 'Lo que aprendimos de los grandes',
           'Revisamos firmas internacionales que renovaron su marca entre 2023 y 2025. Estas son las ideas que adaptamos a una abogada independiente.') +
       '<table class="tabla"><tr><th style="width:24%%">Firma</th><th style="width:38%%">Qué hizo</th><th>Qué tomamos</th></tr>%s</table>' % ''.join(
           '<tr><td><b>%s</b><span class="nota">%s</span></td><td>%s</td><td>%s</td></tr>' % f for f in filas) +
       '<div class="tres" style="margin-top:9mm"><div><h3>Menos solemnidad</h3><p>La confianza se transmite con orden y lenguaje claro.</p></div><div><h3>Un color que no sea azul</h3><p>El verde se asocia con cumplimiento; el lila lo rejuvenece.</p></div><div><h3>Un símbolo del oficio</h3><p>La barra de términos habla de la especialidad procesal.</p></div></div>',
       seccion='Referentes')

# ------------------------------------------------------------------ 5. Logotipo
pagina(cab('03 · Logotipo', 'Un nombre bien escrito',
           'Logotipo tipográfico en Open Sans 500, con espaciado de -0,03 em. Su rasgo propio es la rr enlazada: el brazo de la primera r corre recto hasta la segunda.') + '''
<div class="caja clara" style="padding:14mm 12mm">%s</div>
<div class="dos" style="margin-top:6mm">
 <div class="caja oscura" style="padding:10mm">%s<p class="descr lila">Abogada · Procesalista civil</p></div>
 <div class="caja clara" style="padding:10mm;display:flex;align-items:center">%s</div>
</div>
<div class="dos" style="margin-top:6mm;align-items:center">
 <div class="caja clara" style="padding:6mm 8mm;overflow:hidden;height:46mm"><svg viewBox="0 0 %s %s" style="width:230mm;display:block"><path fill="#0E211F" d="%s"/></svg></div>
 <div><h3>La rr enlazada</h3><p>Es el equivalente a la ff compartida de Clifford Chance. Hace que el nombre sea una firma dibujada y no un texto escrito: <b>por eso el logotipo nunca se reescribe con la fuente</b>, siempre se usan los archivos SVG.</p></div>
</div>''' % (svg('wordmark', COL['marca-tinta']['light'], '140mm'), svg('wordmark', COL['marca-papel']['light'], '70mm'),
             svg('stacked', COL['marca-pino']['light'], '46mm'), M['wordmark']['w'], M['wordmark']['h'], M['wordmark']['d']), seccion='Logotipo')

# ------------------------------------------------------------------ 6. Reglas del logotipo
pagina(cab('03 · Logotipo', 'Reglas de uso') + '''
<div class="dos">
 <div><h3>Área de respeto</h3><p>El alto de la "o" por los cuatro lados. Nada entra en ese espacio.</p>
  <div class="caja clara" style="padding:8mm;margin-top:4mm"><div style="outline:1px dashed #B9A6F2;padding:5mm;display:inline-block">%s</div></div></div>
 <div><h3>Tamaño mínimo</h3><p>Logotipo: 110 px en pantalla o 30 mm impreso. Por debajo, use el monograma ag. (mínimo 16 px).</p>
  <div class="caja clara" style="padding:8mm;margin-top:4mm;display:flex;align-items:flex-end;gap:8mm">%s%s%s</div></div>
</div>
<h3 style="margin-top:9mm">Combinaciones permitidas</h3>
<div class="cuatro">
 <div class="muestra" style="background:#F4F5F2">%s<span>Tinta sobre papel</span></div>
 <div class="muestra" style="background:#F4F5F2">%s<span>Pino sobre papel</span></div>
 <div class="muestra" style="background:#17433D">%s<span style="color:#F4F5F2">Papel sobre pino</span></div>
 <div class="muestra" style="background:#B9A6F2">%s<span>Tinta sobre lila</span></div>
</div>
<h3 style="margin-top:9mm">No haga esto</h3>
<ul class="no">
 <li>Reescribir el nombre con la fuente: se pierde la rr enlazada.</li>
 <li>Ponerlo en mayúsculas, en negrita, en itálica o estirado.</li>
 <li>Usar el lila como color del nombre sobre fondos claros: no alcanza contraste.</li>
 <li>Agregar sombras, contornos, degradados o fotos detrás sin una capa sólida.</li>
</ul>''' % (svg('wordmark', '#17433D', '56mm'), svg('wordmark', '#17433D', '34mm'), svg('wordmark', '#17433D', '26mm'), svg('ag', '#17433D', '7mm'),
             svg('wordmark', '#0E211F', '34mm'), svg('wordmark', '#17433D', '34mm'), svg('wordmark', '#F4F5F2', '34mm'), svg('wordmark', '#0E211F', '34mm')),
       seccion='Logotipo')

# ------------------------------------------------------------------ 7. Monograma
pagina(cab('04 · Monograma', 'ag., con punto de término cumplido',
           'Las iniciales de los dos apellidos, en minúsculas y una al lado de la otra, seguidas de un punto cuadrado. El punto es la última casilla de la barra de términos: dice "término cumplido" sin escribirlo.') + '''
<div class="caja oscura" style="padding:16mm;display:flex;align-items:center;gap:14mm">%s
 <div><p class="lila etq">Cómo se lee</p><p style="color:#F4F5F2">Letras en papel, punto en lila. Sobre lila, letras en tinta y punto en pino. Sobre papel, todo en pino.</p></div></div>
<div class="cuatro" style="margin-top:7mm">
 <div class="muestra" style="background:#F4F5F2">%s<span>Favicon · ícono de app</span></div>
 <div class="muestra" style="background:#F4F5F2">%s<span>Sobre lila</span></div>
 <div class="muestra" style="background:#F4F5F2">%s<span>Avatar de redes</span></div>
 <div class="muestra" style="background:#F4F5F2">%s<span>Sin fondo, sobre claro</span></div>
</div>
<div class="dos" style="margin-top:8mm">
 <div><h3>Dónde se usa</h3><p>Donde el logotipo no cabe: foto de perfil de Instagram, WhatsApp y LinkedIn, favicon, ícono de app, firma de correo y dorso de la tarjeta.</p></div>
 <div><h3>No haga esto</h3><p>Redondear el punto, cambiarlo de color, escribir el monograma en mayúsculas o separar las letras.</p></div>
</div>''' % (svg('ag', '#F4F5F2', '70mm', '#B9A6F2'), logo('ag-sello-pino.svg', 'width:26mm'), logo('ag-sello-lila.svg', 'width:26mm'),
             logo('ag-avatar-circulo.svg', 'width:26mm'), svg('ag', '#17433D', '26mm')), seccion='Monograma')

# ------------------------------------------------------------------ 8. Color de marca
marca = [('marca-pino', 'Pino'), ('marca-bosque', 'Bosque'), ('marca-lila', 'Lila'), ('marca-lila-suave', 'Lila suave'), ('marca-menta', 'Menta'), ('marca-papel', 'Papel'), ('marca-tinta', 'Tinta'), ('marca-gris', 'Gris')]
def rgb(h): h = h.lstrip('#'); return ', '.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))
chips = ''.join('<div class="chip-col"><div class="sw" style="background:%s;%s"></div><b>%s</b><span>%s</span><span>RGB %s</span><span class="tok">%s</span></div>' % (
    COL[k]['light'], 'box-shadow:inset 0 0 0 1px #D3DAD6' if k in ('marca-papel',) else '', n, COL[k]['light'].upper(), rgb(COL[k]['light']), k) for k, n in marca)
pagina(cab('05 · Color', 'La paleta de marca',
           'Verde pino como base, lila como acento joven, menta y lila suave como fondos de relieve. Estos colores son fijos: no cambian con el modo oscuro del teléfono y se usan en redes, impresos, tarjeta y membrete.') +
       '<div class="paleta">%s</div>' % chips + '''
<h3 style="margin-top:9mm">Proporción en una pieza</h3>
<div class="prop"><i style="flex:60;background:#F4F5F2;box-shadow:inset 0 0 0 1px #D3DAD6">Papel 60 %%</i><i style="flex:25;background:#17433D;color:#F4F5F2">Pino o bosque 25 %%</i><i style="flex:10;background:#DCEBE5">Menta 10 %%</i><i style="flex:5;background:#B9A6F2">5 %%</i></div>
<div class="dos" style="margin-top:8mm"><div><h3>Reglas</h3><ul class="si"><li>El lila es relleno o acento, nunca texto sobre papel.</li><li>Sobre lila y lila suave, el texto va en tinta.</li><li>Los estados (cumplido, por vencer) siempre llevan palabra, no solo color.</li></ul></div>
<div><h3>Para impresión</h3><p>Pida siempre una prueba de color impresa antes del tiraje. Los valores RGB son la referencia; la imprenta los convierte a su perfil de color.</p></div></div>''',
       seccion='Color')

# ------------------------------------------------------------------ 9. Tokens de interfaz
ui = ['pino', 'on-pino', 'lila', 'lila-suave', 'menta', 'papel', 'superficie', 'linea', 'tinta', 'tinta-suave', 'plazo', 'cumplido', 'foco']
filas = ''.join('<tr><td><span class="pt" style="background:%s"></span><b>%s</b></td><td class="hex"><span class="pt" style="background:%s"></span>%s</td><td class="hex"><span class="pt" style="background:%s"></span>%s</td><td>%s</td></tr>' % (
    COL[k]['light'], k, COL[k]['light'], COL[k]['light'].upper(), COL[k]['dark'], COL[k]['dark'].upper(), html.escape(re.sub(r'\s*\([^)]*\)', '', U[k].replace('`', '')).split('. ')[0].rstrip('.') + '.')) for k in ui)
pares = [('tinta', 'papel'), ('tinta-suave', 'papel'), ('on-pino', 'pino'), ('on-lila', 'lila'), ('plazo', 'superficie'), ('cumplido', 'papel')]
cont = ''.join('<tr><td>%s sobre %s</td><td class="hex">%.1f : 1</td><td class="hex">%.1f : 1</td></tr>' % (a, b, cr(COL[a]['light'], COL[b]['light']), cr(COL[a]['dark'], COL[b]['dark'])) for a, b in pares)
pagina(cab('05 · Color', 'Tokens para web y apps',
           'En la interfaz digital los colores tienen versión clara y oscura. Se usan por su nombre (token), nunca por su valor, así el sitio cambia de tema sin errores.') +
       '<table class="tabla peq"><tr><th style="width:22%%">Token</th><th style="width:15%%">Claro</th><th style="width:15%%">Oscuro</th><th>Uso</th></tr>%s</table>' % filas +
       '<h3 style="margin-top:7mm">Contraste verificado (WCAG 2)</h3><table class="tabla peq"><tr><th style="width:50%%">Par</th><th>Claro</th><th>Oscuro</th></tr>%s</table><p class="nota">Todo el texto supera 4,5 : 1 en ambos temas.</p>' % cont,
       seccion='Color')

# ------------------------------------------------------------------ 10. Tipografía
estilos = [s for g in T['type']['groups'] for s in g['styles'] if not s['name'].startswith('ig-')]
muestras = ''.join('<div class="estilo"><span class="tok">%s · %spx / %s · %s%s</span><p style="font-size:%spx;line-height:%s;font-weight:%s;%s%s">%s</p></div>' % (
    s['name'], s['fontSize'], s['lineHeight'], s['fontWeight'], (' · ' + s['letterSpacing']) if s.get('letterSpacing') else '',
    min(s['fontSize'], 44) * 0.75, '1.2', s['fontWeight'], ('letter-spacing:%s;' % s['letterSpacing']) if s.get('letterSpacing') else '',
    'font-style:italic;' if s.get('fontStyle') == 'italic' else ('text-transform:uppercase;' if s['name'] == 'etiqueta' else ''), html.escape(s.get('sample', ''))) for s in estilos)
pagina(cab('06 · Tipografía', 'Una sola familia: Open Sans',
           'Sans serif humanista, libre (licencia OFL) y la más cercana al logotipo de Clifford Chance. Se usa en 400, 500, 600, 700 e itálica 400. Viene en Google Docs y se instala gratis desde Google Fonts.') + '''
<div class="caja clara" style="padding:9mm 10mm;display:flex;align-items:flex-end;justify-content:space-between"><p style="font-size:64pt;line-height:1;font-weight:500;letter-spacing:-.03em">Aa Gg Rr</p>
<p class="nota" style="text-align:right">Open Sans<br>400 · 500 · 600 · 700<br><i>Itálica 400</i></p></div>
<div class="estilos">%s</div>
<p class="nota" style="margin-top:4mm">Los titulares siempre llevan espaciado negativo. En Instagram se usan los estilos ig-titular (80 px), ig-cuerpo (32 px) e ig-etiqueta (22 px) sobre un lienzo de 1080 px.</p>''' % muestras,
       seccion='Tipografía')

# ------------------------------------------------------------------ 11. Recursos gráficos
iconos = ['procesal', 'civil', 'laboral', 'familia', 'sucesiones', 'contratos', 'terminos', 'consulta', 'oficina', 'videollamada']
pagina(cab('07 · Recursos gráficos', 'La barra de términos',
           'Una casilla por día hábil de un término procesal: las transcurridas en pino, la de hoy en lila, las que faltan solo con borde. Es el sello visual de la marca.') +
       '<div class="caja clara" style="padding:8mm">%s</div>' % img('barra-terminos.png', 'width:100%') + '''
<div class="tres" style="margin-top:6mm"><div><h3>Cuándo</h3><p>Cuando una pieza habla de un plazo real: contestar una demanda, un recurso, una prescripción.</p></div>
<div><h3>Cómo</h3><p>Filas de 10 casillas, cada una de 24 px con 8 px de separación y esquinas de 4 px. Cite la norma debajo.</p></div>
<div><h3>Dónde</h3><p>Publicaciones de plazos, frente de la tarjeta (5 casillas), portada del sitio y el punto del monograma.</p></div></div>
<h3 style="margin-top:9mm">Íconos de áreas</h3><p>Juego propio: trazo de 1,75 px en grilla de 24, esquinas rectas y sin relleno. No se mezclan con íconos de otros juegos.</p>
<div class="iconos">%s</div>''' % ''.join('<div>%s<span>%s</span></div>' % (icono(n, px=34), n.capitalize()) for n in iconos),
       seccion='Recursos gráficos')

# ------------------------------------------------------------------ 12. Voz
pagina(cab('08 · Voz y tono', 'Cómo escribe Arroyo Guzmán',
           'Clara, cercana y precisa. Tania habla en primera persona y trata al cliente de usted.') + '''
<div class="dos">
 <div class="caja si-caja"><p class="etq">Así sí</p>
  <p class="cita">“¿Le notificaron una demanda? Tiene 20 días hábiles para contestarla.”</p>
  <p class="cita">“Le explico su caso en palabras claras y le digo qué sigue, con fechas.”</p>
  <p class="cita">“Una consulta a tiempo evita un proceso.”</p></div>
 <div class="caja no-caja"><p class="etq">Así no</p>
  <p class="cita tach">“Ganamos su caso, garantizado.”</p>
  <p class="cita tach">“Nuestro bufete de expertos…”</p>
  <p class="cita tach">“Se le corrió traslado conforme al artículo 369 ibídem.”</p></div>
</div>
<div class="tres" style="margin-top:8mm">
 <div><h3>Usted y yo</h3><p>Trato de usted. Primera persona del singular: "reviso", "le explico", nunca "nosotros".</p></div>
 <div><h3>Palabra común primero</h3><p>"El plazo para contestar (traslado de la demanda)". Frases cortas y en voz activa.</p></div>
 <div><h3>Cite la norma</h3><p>Cada dato lleva su fuente: "Código General del Proceso, art. 369". Verifique la norma antes de publicar.</p></div>
 <div><h3>Sin promesas</h3><p>Se promete proceso, plazos y claridad, nunca un resultado. Así lo exige la ética profesional.</p></div>
 <div><h3>Sin emojis</h3><p>En las piezas no se usan. En el texto de la publicación, como máximo uno, al final.</p></div>
 <div><h3>Tipo oración</h3><p>"Sucesiones y herencias", no "Sucesiones Y Herencias". Mayúsculas solo en etiquetas.</p></div>
</div>''', seccion='Voz y tono')

# ------------------------------------------------------------------ 13. Instagram
pagina(cab('09 · Instagram', 'Cuatro plantillas, un ritmo',
           'Publicaciones de 1080 × 1350 px (4:5) con margen de 72 px, logotipo arriba a la izquierda y la etiqueta del área a la derecha.') + '''
<div class="cuatro ig">%s%s%s%s</div>
<table class="tabla peq" style="margin-top:6mm"><tr><th style="width:24%%">Plantilla</th><th style="width:22%%">Fondo</th><th>Para qué</th></tr>
<tr><td><b>Dato útil</b></td><td>Lila suave</td><td>Plazos, requisitos y preguntas frecuentes. Lleva la barra de términos cuando hay un plazo.</td></tr>
<tr><td><b>Frase</b></td><td>Pino</td><td>Forma de trabajo y valores. Máximo una por semana.</td></tr>
<tr><td><b>Portada de carrusel</b></td><td>Papel</td><td>Guías de 5 a 8 láminas; el número grande dice cuántos puntos hay.</td></tr>
<tr><td><b>Área de práctica</b></td><td>Bosque</td><td>Presentar un servicio: laboral, familia, sucesiones, contratos.</td></tr></table>
<div class="dos" style="margin-top:6mm;align-items:center"><div>%s</div><div><h3>Historias y destacados</h3><p>Historias de 1080 × 1920 px, dejando libres 220 px arriba y 260 px abajo. Destacados en círculos pino (lo propio del despacho) y lila suave (las áreas).</p><p style="margin-top:3mm"><b>Ritmo del feed:</b> en cada fila de tres publicaciones, al menos una oscura.</p></div></div>''' % (
    img('ig-dato.png', 'width:100%'), img('ig-frase.png', 'width:100%'), img('ig-carrusel.png', 'width:100%;box-shadow:0 0 0 1px #D3DAD6'), img('ig-area.png', 'width:100%'),
    img('historia-destacados.png', 'width:100%')), seccion='Instagram')

# ------------------------------------------------------------------ 14. Aplicaciones
pagina(cab('10 · Aplicaciones', 'Tarjeta, membrete y firma') + '''
<div class="dos">%s%s</div>
<div class="tres" style="margin-top:4mm"><div><h3>Tarjeta profesional</h3><p>85 × 55 mm con 3 mm de sangrado. Cartulina sin estucar de 350 g o más, acabado mate. Frente en pino con el logotipo apilado; dorso en papel con el monograma.</p></div>
<div><h3>Membrete</h3><p>Carta, márgenes de 25 mm, logotipo con descriptor de 50 mm. Asunto con el radicado completo de 23 dígitos. Versión sin color para despachos que la exijan.</p></div>
<div><h3>Firma de correo</h3><p>Monograma de 44 px, nombre completo en 600, cargo en pino y la nota de confidencialidad al final.</p></div></div>
<div class="caja clara" style="padding:6mm;margin-top:6mm">%s</div>''' % (img('tarjeta-frente.png', 'width:100%;border-radius:3mm'), img('tarjeta-dorso.png', 'width:100%;border-radius:3mm;box-shadow:0 0 0 1px #D3DAD6'),
                                                                        img('membrete-firma.png', 'width:100%')), seccion='Aplicaciones')

# ------------------------------------------------------------------ 15. Sitio web
pagina(cab('11 · Sitio web', 'Una página que explica, orienta y agenda',
           'Sitio de una sola página hecho con Next.js y el sistema de diseño. Presenta a Tania, explica los procesos más comunes con su plazo y su norma, y permite agendar una cita presencial o virtual.') +
       '<div class="pantalla">%s</div>' % img('sitio-portada.png', 'width:100%') + '''
<table class="tabla peq" style="margin-top:6mm"><tr><th style="width:28%%">Sección</th><th>Qué hace</th></tr>
<tr><td><b>Portada</b></td><td>"Cada término, cumplido." y una tarjeta que muestra cómo sigue el cliente su caso.</td></tr>
<tr><td><b>Áreas de práctica</b></td><td>La especialidad destacada y las cinco áreas con sus temas.</td></tr>
<tr><td><b>Cómo trabajo</b></td><td>Cuatro pasos con tiempos: consulta, diagnóstico por escrito, actuación y seguimiento.</td></tr>
<tr><td><b>Procesos típicos</b></td><td>15 situaciones por área: qué proceso aplica, qué hacer ahora, el plazo y la norma.</td></tr>
<tr><td><b>Casos resueltos</b></td><td>Situación, qué se hizo, resultado y una lección práctica, con invitación a agendar.</td></tr>
<tr><td><b>Guía útil</b></td><td>Tabla de plazos, qué traer a la consulta y preguntas frecuentes.</td></tr>
<tr><td><b>Agendar y contacto</b></td><td>Cita presencial o virtual en días hábiles, y todos los canales de contacto.</td></tr></table>''',
       seccion='Sitio web')

pagina(cab('11 · Sitio web', 'Agenda de citas, móvil y tema oscuro') + '''
<div class="pantalla">%s</div>
<div class="sitio-fila" style="margin-top:6mm"><div class="pantalla movil">%s</div><div class="pantalla movil">%s</div>
<div><h3>Cómo funciona la agenda</h3><ul class="si"><li>El calendario de Cal.com va dentro del sitio, con los colores de la marca.</li><li>Solo muestra las horas libres del calendario de Tania.</li><li>Dos tipos de cita: presencial y virtual, de una hora.</li><li>Cal.com envía la confirmación, los recordatorios y el enlace de la videollamada.</li><li>Si no carga, el sitio ofrece el enlace directo y WhatsApp.</li></ul>
<h3 style="margin-top:5mm">Tema oscuro</h3><div class="pantalla">%s</div></div></div>''' % (img('sitio-agenda.png', 'width:100%'), img('sitio-movil.png', 'width:100%'), img('sitio-movil-agenda.png', 'width:100%'),
                                                                                   img('sitio-portada-oscuro.png', 'width:100%')), seccion='Sitio web')

# ------------------------------------------------------------------ 16. Implementación
pagina(cab('12 · Implementación', 'Dónde está cada cosa',
           'Todo vive en el repositorio github.com/agmNeider/tania-arroyo-lawyer. El sistema de diseño es la fuente única: los logos, los colores y los íconos del sitio se generan desde ahí.') + '''
<table class="tabla peq"><tr><th style="width:38%%">Archivo</th><th>Qué contiene</th></tr>
<tr><td class="hex">design-system/README.md</td><td>El manual de marca en texto, para equipos y agentes.</td></tr>
<tr><td class="hex">design-system/tokens.json · tokens.css</td><td>Colores, tipografía, espaciado, radios y sombra.</td></tr>
<tr><td class="hex">design-system/assets/Logos</td><td>Logotipo, apilado, monograma, sellos y avatar en SVG.</td></tr>
<tr><td class="hex">design-system/assets/Iconos</td><td>Los 10 íconos de áreas y citas.</td></tr>
<tr><td class="hex">design-system/components</td><td>Plantillas de Instagram, tarjeta, membrete y elementos web.</td></tr>
<tr><td class="hex">app · components · lib</td><td>El sitio web en Next.js. El texto se edita en lib/contenido.ts.</td></tr>
<tr><td class="hex">.claude/skills/arroyo-guzman-marca</td><td>Instrucciones para que Claude use la marca en cualquier pieza nueva.</td></tr></table>
<div class="dos" style="margin-top:8mm"><div class="caja clara" style="padding:7mm"><h3>Espaciado y radios</h3><p>Grilla de 4 px: 4, 8, 12, 16, 24, 32, 48 y 72 px. Radios de 4 px (etiquetas), 10 px (botones y tarjetas) y 22 %% (ícono de app). Una sola sombra; la jerarquía se hace con filetes de 1 px.</p></div>
<div class="caja clara" style="padding:7mm"><h3>Lista de revisión</h3><ul class="si"><li>Logotipo y monograma desde los SVG.</li><li>Solo Open Sans, titulares con espaciado negativo.</li><li>Texto con contraste de 4,5 : 1.</li><li>Una idea por pieza y cada dato con su norma.</li><li>Usted, primera persona, sin promesas.</li><li>Datos de contacto reales.</li></ul></div></div>
<div class="cierre">%s<p>Cada término, cumplido.</p></div>''' % svg('ag', '#17433D', '22mm', '#B9A6F2'), seccion='Implementación')

# ------------------------------------------------------------------ HTML
FUENTES = ''.join("@font-face{font-family:'Open Sans';src:url('file://%s/fonts/OpenSans-%s.ttf');font-weight:%s;font-style:%s}" % (DS, f, w, s)
                  for f, w, s in [('400', 400, 'normal'), ('500', 500, 'normal'), ('600', 600, 'normal'), ('700', 700, 'normal'), ('400-italic', 400, 'italic')])
CSS = FUENTES + '''
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Open Sans',sans-serif;color:#0E211F;background:#F4F5F2;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:9.6pt;line-height:1.55}
.pag{width:210mm;height:297mm;padding:20mm 18mm 22mm;position:relative;overflow:hidden;background:#FFFFFF;page-break-after:always;display:flex;flex-direction:column}
.folio{position:absolute;left:18mm;right:18mm;bottom:10mm;display:flex;justify-content:space-between;font-size:7.5pt;color:#4F5E5A;border-top:1px solid #D3DAD6;padding-top:3mm}
.etq{font-size:7.5pt;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#17433D;margin-bottom:3mm}
.lila{color:#B9A6F2!important}
h1{font-size:44pt;line-height:1.02;font-weight:500;letter-spacing:-.03em}
h2{font-size:26pt;line-height:1.1;font-weight:500;letter-spacing:-.025em;margin-bottom:5mm;max-width:150mm}
h3{font-size:11.5pt;line-height:1.3;font-weight:600;letter-spacing:-.01em;margin-bottom:1.5mm}
.intro{font-size:11pt;line-height:1.6;color:#4F5E5A;max-width:155mm;margin-bottom:8mm}
p b{font-weight:600}
.nota{font-size:8pt;color:#4F5E5A;display:block}
.dos{display:grid;grid-template-columns:1fr 1fr;gap:7mm}
.tres{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm}
.cuatro{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}
.caja{border-radius:3mm}
.clara{background:#F4F5F2}
.oscura{background:#17433D;color:#F4F5F2}
.descr{font-size:7.5pt;font-weight:600;letter-spacing:.16em;text-transform:uppercase;margin-top:3mm}
.muestra{height:30mm;border-radius:3mm;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm;box-shadow:inset 0 0 0 1px #D3DAD6}
.muestra span{font-size:7.5pt;color:#4F5E5A}
.tabla{width:100%;border-collapse:collapse;font-size:9pt;line-height:1.45}
.tabla th{text-align:left;font-size:7pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#4F5E5A;padding:2.5mm 3mm;border-bottom:1.5px solid #0E211F}
.tabla td{padding:2.6mm 3mm;border-bottom:1px solid #D3DAD6;vertical-align:top}
.tabla.peq{font-size:8.4pt}
.tabla.peq td{padding:1.6mm 3mm}
.tabla.peq{font-size:8.2pt;line-height:1.4}
.hex{font-variant-numeric:tabular-nums;white-space:nowrap}
.pt{display:inline-block;width:3.2mm;height:3.2mm;border-radius:.8mm;vertical-align:-.5mm;margin-right:2mm;box-shadow:inset 0 0 0 .3mm rgba(0,0,0,.12)}
ul.si,ul.no{list-style:none;display:flex;flex-direction:column;gap:1.8mm}
ul.si li,ul.no li{padding-left:5mm;position:relative}
ul.si li::before{content:"";position:absolute;left:0;top:1.6mm;width:2.4mm;height:2.4mm;border-radius:.5mm;background:#17433D}
ul.no li::before{content:"";position:absolute;left:0;top:2.6mm;width:2.8mm;height:.5mm;background:#A94F17}
.indice{list-style:none;counter-reset:i;display:grid;grid-template-columns:1fr 1fr;gap:0 10mm;margin-top:4mm}
.indice li{counter-increment:i;display:grid;grid-template-columns:12mm 1fr;padding:4.2mm 0;border-top:1px solid #D3DAD6}
.indice li::before{content:counter(i,decimal-leading-zero);font-size:9pt;font-weight:600;color:#17433D;grid-row:span 2}
.indice b{font-size:13pt;font-weight:600;letter-spacing:-.01em}
.indice span{color:#4F5E5A;font-size:9pt}
.idea{background:#ECE6FC;border-radius:3mm;padding:10mm;margin-bottom:8mm}
.idea .etq{color:#17433D!important}
.grande{font-size:30pt;line-height:1.1;font-weight:500;letter-spacing:-.025em;margin-bottom:3mm}
.paleta{display:grid;grid-template-columns:repeat(4,1fr);gap:6mm 4mm}
.chip-col{display:flex;flex-direction:column;gap:.6mm;font-size:8pt}
.chip-col .sw{height:26mm;border-radius:3mm;margin-bottom:2mm}
.chip-col b{font-size:10pt;font-weight:600}
.chip-col span{color:#4F5E5A;font-variant-numeric:tabular-nums}
.tok{font-size:7.2pt;color:#4F5E5A;font-variant-numeric:tabular-nums}
.prop{display:flex;height:14mm;border-radius:3mm;overflow:hidden;margin-top:2mm}
.prop i{font-style:normal;display:flex;align-items:center;padding-left:3mm;font-size:7.5pt;font-weight:600;white-space:nowrap;overflow:hidden}
.estilos{display:flex;flex-direction:column;margin-top:5mm}
.estilo{display:grid;grid-template-columns:52mm 1fr;align-items:baseline;gap:4mm;padding:2.6mm 0;border-top:1px solid #D3DAD6}
.iconos{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:4mm}
.iconos div{background:#F4F5F2;border-radius:3mm;padding:5mm 0;display:flex;flex-direction:column;align-items:center;gap:2mm;font-size:8pt;color:#4F5E5A}
.cita{font-size:11.5pt;line-height:1.45;font-style:italic;padding:3mm 0;border-top:1px solid rgba(14,33,31,.12)}
.si-caja{background:#DCEBE5;padding:8mm}
.no-caja{background:#F4F5F2;padding:8mm}
.tach{text-decoration:line-through;text-decoration-color:#A94F17;color:#4F5E5A}
.ig img{border-radius:1.5mm}
.pantalla{border-radius:2.5mm;overflow:hidden;box-shadow:0 0 0 1px #D3DAD6,0 3mm 8mm rgba(14,33,31,.08);line-height:0}
.sitio-fila{display:grid;grid-template-columns:36mm 36mm 1fr;gap:6mm;align-items:start}
.movil{border-radius:4mm}
.cierre{margin-top:auto;display:flex;align-items:center;gap:6mm;padding-top:8mm}
.cierre p{font-size:16pt;font-weight:500;letter-spacing:-.02em}
.portada{background:#0F2E2A;color:#F4F5F2;padding:22mm 20mm}
.port-top{margin-bottom:auto}
.port-cas{display:grid;grid-template-columns:repeat(10,11mm);gap:3mm;margin:0 0 16mm}
.port-cas i{height:11mm;border-radius:1.5mm;border:.5mm solid #7CC2B1}
.port-cas i.h{background:#17433D;border-color:#17433D;box-shadow:inset 0 0 0 .5mm #7CC2B1}
.port-cas i.hoy{background:#B9A6F2;border-color:#B9A6F2}
.port-txt h1{color:#F4F5F2;font-size:50pt}
.port-sub{font-size:12pt;margin-top:8mm}
.port-ver{font-size:9pt;opacity:.75;margin-top:2mm}
'''
doc = '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Manual de marca · Arroyo Guzmán</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(paginas))
sal_html = os.path.join(AQUI, 'manual.html')
open(sal_html, 'w').write(doc)
pdf = os.path.join(RAIZ, 'docs', 'Manual-de-marca-Arroyo-Guzman.pdf')
js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage();await p.goto('file://%s');await p.waitForTimeout(800);await p.pdf({path:'%s',format:'A4',printBackground:true,preferCSSPageSize:true});await b.close();})();" % (sal_html, pdf)
subprocess.run(['node', '-e', js], check=True, cwd=os.environ.get('PW_DIR', AQUI))
print('PDF:', pdf, len(paginas), 'páginas')
