# Arma el sitio de Arroyo Guzmán desde plantilla.html y el sistema de diseño.
#   index.html     -> documento completo para publicar en cualquier hosting
#   artefacto.html -> la misma página sin <html>/<head> (vista previa en claude.ai)
import json, os, re, base64
HERE = os.path.dirname(os.path.abspath(__file__))
DS = os.path.join(HERE, '..', 'design-system')
marks = json.load(open(os.path.join(DS, '_herramientas', 'marks.json')))
css = open(os.path.join(DS, 'tokens.css')).read()
css = re.sub(r'@font-face[^\n]*\n', '', css)            # Open Sans llega por Google Fonts
css = re.sub(r'^\.[\w-]+ \{[^\n]*\}\n', '', css, flags=re.M)  # clases de estilo: el sitio usa las suyas
css = css.replace('/* Generado por _herramientas/tokens_css.py desde tokens.json. No editar a mano. */\n', '/* tokens: design-system/tokens.css */\n')

def svg(key, cls, label):
    m = marks[key]
    extra = '<path class="pt" d="%s"/>' % m['dot'] if 'dot' in m else ''
    return '<svg class="%s" viewBox="0 0 %s %s" role="img" aria-label="%s"><path d="%s"/>%s</svg>' % (cls, m['w'], m['h'], label, m['d'], extra)

def icon(name):
    s = open(os.path.join(DS, 'assets', 'Iconos', name + '.svg')).read().strip()
    s = s.replace('stroke="#17433D"', 'stroke="currentColor"').replace(' width="24" height="24"', '')
    return s.replace('<svg ', '<svg class="ic" aria-hidden="true" ', 1)

def barra(n, hechos, hoy=True):
    return ''.join('<i class="h"></i>' if i < hechos else ('<i class="hoy"></i>' if hoy and i == hechos else '<i></i>') for i in range(n))

html = open(os.path.join(HERE, 'plantilla.html')).read()
html = html.replace('{{TOKENS}}', css)
html = html.replace('{{WORDMARK}}', svg('wordmark', 'wm', 'Arroyo Guzmán'))
html = html.replace('{{MONO}}', svg('ag', 'mono', 'ag.'))
html = html.replace('{{BARRA_20_13}}', barra(20, 13))
html = re.sub(r'\{\{ICON:([\w-]+)\}\}', lambda m: icon(m.group(1)), html)
assert '{{' not in html, re.findall(r'\{\{[^}]+\}\}', html)

open(os.path.join(HERE, 'artefacto.html'), 'w').write(html)
fav = base64.b64encode(open(os.path.join(DS, 'assets', 'Logos', 'ag-sello-pino.svg'), 'rb').read()).decode()
head = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="Tania Arroyo Guzmán, abogada procesalista civil. Procesos civiles, laborales, de familia, sucesiones y contratos. Citas presenciales y virtuales.">\n'
        '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,%s">\n' % fav)
title_end = html.index('</title>') + len('</title>')
style_end = html.index('</style>') + len('</style>')
doc = head + html[:style_end] + '\n</head>\n<body>\n' + html[style_end:] + '\n</body>\n</html>\n'
open(os.path.join(HERE, 'index.html'), 'w').write(doc)
print('ok', len(doc)//1024, 'KB')
