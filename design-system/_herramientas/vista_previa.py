# Build standalone previews of every component (light and dark) in _vista/, injecting tokens.css.
# Screenshot them with Playwright/Chromium to review changes before publishing.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(HERE + '/..')
OUT = ROOT + '/_vista'; os.makedirs(OUT, exist_ok=True)
css = open(ROOT + '/tokens.css').read().replace("url('fonts/", "url('file://%s/fonts/" % ROOT)
for comp in sorted(os.listdir(ROOT + '/components')):
    f = ROOT + '/components/%s/preview.html' % comp
    if not os.path.exists(f): continue
    html = open(f).read()
    for theme in ('light', 'dark'):
        h = html.replace('<html lang="es">', '<html lang="es" data-theme="%s">' % theme, 1).replace('<style>', '<style>' + css, 1)
        open(OUT + '/%s-%s.html' % (comp, theme), 'w').write(h)
print('vista previa en', OUT)
