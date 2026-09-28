import uharfbuzz as hb, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
ROOT=os.path.dirname(os.path.abspath(__file__))+'/..'
F=ROOT+'/fonts/SchibstedGrotesk-%s.ttf'
OUT=ROOT+'/assets'
os.makedirs(OUT+'/Logos',exist_ok=True)
C={'pino':'#17433D','tinta':'#0E211F','lila':'#B9A6F2','papel':'#F4F5F2','blanco':'#FFFFFF'}

def text_path(txt, weight, size, x, y, track=0.0):
    data=open(F%weight,'rb').read()
    face=hb.Face(data); font=hb.Font(face)
    buf=hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties()
    hb.shape(font,buf,{"kern":True,"liga":True})
    tt=TTFont(F%weight); gs=tt.getGlyphSet(); upm=tt['head'].unitsPerEm
    order=tt.getGlyphOrder(); s=size/upm
    pen=SVGPathPen(gs); cx=0
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        name=order[info.codepoint]
        tp=TransformPen(pen,(s,0,0,-s,x+(cx+pos.x_offset)*s,y-pos.y_offset*s))
        gs[name].draw(tp)
        cx+=pos.x_advance+track*upm
    width=(cx-track*upm)*s
    return pen.getCommands(), width

def mark(ox,oy,sc,fill):
    # T+A monogram on a 64 grid: the beam (T crossbar / balance beam) over an A
    def p(pts): return 'M'+' L'.join('%.2f %.2f'%(ox+a*sc,oy+b*sc) for a,b in pts)+'Z'
    beam=p([(6,8),(58,8),(58,14),(6,14)])
    a=p([(28.5,14),(35.5,14),(53.5,57),(46,57),(32,23.5),(18,57),(10.5,57)])
    bar=p([(21,40.5),(43,40.5),(43,46),(21,46)])
    return '<path fill="%s" d="%s %s %s"/>'%(fill,beam,a,bar)

def svg(w,h,body,bg=None):
    b='<rect width="%s" height="%s" fill="%s"/>'%(w,h,bg) if bg else ''
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s">%s%s</svg>\n'%(w,h,w,h,b,body)

def write(name,s): open(OUT+'/Logos/'+name,'w').write(s)

# monogram
for nm,fill,bg in [('ta-monograma-pino.svg',C['pino'],None),('ta-monograma-tinta.svg',C['tinta'],None),('ta-monograma-papel.svg',C['papel'],None)]:
    write(nm,svg(64,64,mark(0,0,1,fill)))
# app/avatar seals
def seal(nm,bg,fg,r):
    body='<rect width="512" height="512" rx="%d" fill="%s"/>'%(r,bg)+mark(96,96+ -8,5,fg)
    write(nm,svg(512,512,body))
seal('ta-sello-pino.svg',C['pino'],C['lila'],112)
seal('ta-sello-lila.svg',C['lila'],C['tinta'],112)
seal('ta-avatar-circulo.svg',C['pino'],C['lila'],256)

# horizontal lockup
def horiz(nm,markc,namec,subc):
    H=120
    m=mark(0,4,1.75,markc)  # mark 112 tall (0..112)
    n,wn=text_path('Tania Arroyo','600',50,132,62,-0.012)
    s,ws=text_path('ABOGADA  ·  PROCESALISTA CIVIL','500',15.5,134,96,0.16)
    W=int(132+max(wn,ws)+6)
    write(nm,svg(W,H,m+'<path fill="%s" d="%s"/><path fill="%s" d="%s"/>'%(namec,n,subc,s)))
    return W
horiz('ta-horizontal-pino.svg',C['pino'],C['tinta'],C['pino'])
horiz('ta-horizontal-papel.svg',C['lila'],C['papel'],C['lila'])
# vertical lockup
def vert(nm,markc,namec,subc):
    n,wn=text_path('Tania Arroyo','600',56,0,0,-0.012)
    s,ws=text_path('ABOGADA','500',17,0,0,0.22)
    W=int(max(wn,ws,140)+40)
    n,_=text_path('Tania Arroyo','600',56,(W-wn)/2,196,-0.012)
    s,_=text_path('ABOGADA','500',17,(W-ws)/2,236,0.22)
    m=mark((W-128)/2,0,2,markc)
    write(nm,svg(W,250,m+'<path fill="%s" d="%s"/><path fill="%s" d="%s"/>'%(namec,n,subc,s)))
vert('ta-vertical-pino.svg',C['pino'],C['tinta'],C['pino'])
vert('ta-vertical-papel.svg',C['lila'],C['papel'],C['lila'])
# wordmark only
n,wn=text_path('Tania Arroyo','600',56,4,56,-0.012)
write('ta-wordmark-tinta.svg',svg(int(wn+8),72,'<path fill="%s" d="%s"/>'%(C['tinta'],n)))
print('ok',os.listdir(OUT+'/Logos'))
