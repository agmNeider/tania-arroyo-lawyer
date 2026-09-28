# Compile tokens.json into tokens.css (light on :root, dark via prefers-color-scheme and [data-theme="dark"])
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(HERE + '/../tokens.json'))
def colors(theme):
    return ''.join('  --%s: %s;\n' % (c['name'], c['value'][theme]) for c in T['color']['tokens'])
out = ['/* Generado por _herramientas/tokens_css.py desde tokens.json. No editar a mano. */\n']
for f in T['type']['fonts']:
    out.append("@font-face { font-family: '%s'; src: url('fonts/%s') format('truetype'); font-weight: %s; font-style: %s; font-display: swap; }\n"
               % (f['family'], os.path.basename(f['file']), f['weight'], f.get('style', 'normal')))
rest = ''.join('  --%s: %s;\n' % (x['name'], x['value']) for fam in ('spacing', 'radius') for x in T[fam]['tokens'])
rest += ''.join('  --font-%s: %s;\n' % (k, v) for k, v in T['type']['families'].items())
sh = lambda th: ''.join('  --%s: %s;\n' % (x['name'], x['value'][th]) for x in T['shadow']['tokens'])
out.append(':root {\n' + colors('light') + sh('light') + rest + '}\n')
dark = colors('dark') + sh('dark') + '  color-scheme: dark;\n'
out.append('@media (prefers-color-scheme: dark) {\n:root:not([data-theme="light"]) {\n' + dark + '}\n}\n')
out.append(':root[data-theme="dark"] {\n' + dark + '}\n')
for g in T['type']['groups']:
    for s in g['styles']:
        css = 'font-family: var(--font-%s); font-size: %spx; line-height: %s; font-weight: %s;' % (s.get('family', g['family']), s['fontSize'], s['lineHeight'], s['fontWeight'])
        if s.get('letterSpacing'): css += ' letter-spacing: %s;' % s['letterSpacing']
        if s.get('fontStyle'): css += ' font-style: %s;' % s['fontStyle']
        if s['name'] in ('etiqueta', 'ig-etiqueta'): css += ' text-transform: uppercase;'
        out.append('.%s { %s }\n' % (s['name'], css))
open(HERE + '/../tokens.css', 'w').write(''.join(out))
print('tokens.css ok')
