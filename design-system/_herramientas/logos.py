# Logos for "Arroyo Guzmán": typographic wordmark in Open Sans 500 with the joined "rr"
import os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wm2, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.environ.get('DS_ROOT', HERE+'/..')
OUT=ROOT+'/assets/Logos'; os.makedirs(OUT,exist_ok=True)
C={'pino':'#17433D','tinta':'#0E211F','lila':'#B9A6F2','papel':'#F4F5F2'}
UPM=2048

def geom(txt,w='500',tr=-0.03):
    g,wd,_=wm2.wordmark(txt,w,tr,True); return g
def path_of(g,size,ox,oy): return wm2.to_path(g,size/UPM,ox,oy)

def text_path(txt,weight,size,x,y,track=0.0):
    F=wm2.FD%weight; data=open(F,'rb').read(); font=hb.Font(hb.Face(data))
    buf=hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties(); hb.shape(font,buf,{"kern":True})
    tt=TTFont(F); gs=tt.getGlyphSet(); order=tt.getGlyphOrder(); s=size/UPM; pen=SVGPathPen(gs); cx=0
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        gs[order[info.codepoint]].draw(TransformPen(pen,(s,0,0,-s,x+(cx+pos.x_offset)*s,y))); cx+=pos.x_advance+track*UPM
    return pen.getCommands(),(cx-track*UPM)*s

def svg(w,h,body): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" width="%g" height="%g">%s</svg>\n'%(w,h,w,h,body)
def P(d,fill): return '<path fill="%s" d="%s"/>'%(fill,d)

marks={}
# one-line wordmark, tight box: cap height ~1462 units, descender of y ~ -492
g=geom('Arroyo Guzmán'); b=g.bounds  # minx,miny,maxx,maxy in font units
SZ=100; s=SZ/UPM; pad=0
W=(b[2]-b[0])*s; H=(b[3]-b[1])*s
d=path_of(g,SZ,-b[0]*s,b[3]*s)
marks['wordmark']={'d':d,'w':round(W,2),'h':round(H,2)}
for nm,fill in [('ag-logotipo-pino.svg',C['pino']),('ag-logotipo-tinta.svg',C['tinta']),('ag-logotipo-papel.svg',C['papel'])]:
    open(OUT+'/'+nm,'w').write(svg(round(W,2),round(H,2),P(d,fill)))
# with descriptor
sub,ws=text_path('ABOGADA  ·  PROCESALISTA CIVIL','600',15,1,H+30,0.16)
Hs=H+36
for nm,a,bcol in [('ag-firma-pino.svg',C['tinta'],C['pino']),('ag-firma-papel.svg',C['papel'],C['lila'])]:
    open(OUT+'/'+nm,'w').write(svg(round(max(W,ws)+2,2),round(Hs,2),P(d,a)+P(sub,bcol)))
# stacked: Arroyo / Guzmán, left aligned
g1=geom('Arroyo'); g2=geom('Guzmán')
SZ2=100; s2=SZ2/UPM; cap=1462*s2; lead=SZ2*1.0
b1=g1.bounds; b2=g2.bounds
d1=path_of(g1,SZ2,-b1[0]*s2,b1[3]*s2)
d2=path_of(g2,SZ2,-b2[0]*s2,b1[3]*s2+lead)
Wst=max(b1[2]-b1[0],b2[2]-b2[0])*s2; Hst=b1[3]*s2+lead-b2[1]*s2
marks['stacked']={'d':d1+' '+d2,'w':round(Wst,2),'h':round(Hst,2)}
for nm,fill in [('ag-apilado-pino.svg',C['pino']),('ag-apilado-papel.svg',C['papel'])]:
    open(OUT+'/'+nm,'w').write(svg(round(Wst,2),round(Hst,2),P(d1+' '+d2,fill)))
# AG short mark (for avatar, favicon)
ga=geom('AG','500',-0.02); ba=ga.bounds; sa=100/UPM
da=path_of(ga,100,-ba[0]*sa,ba[3]*sa); Wa=(ba[2]-ba[0])*sa; Ha=(ba[3]-ba[1])*sa
marks['ag']={'d':da,'w':round(Wa,2),'h':round(Ha,2)}
def seal(nm,bg,fg,r):
    k=0.62*512/Wa; ox=(512-Wa*k)/2; oy=(512-Ha*k)/2
    body='<rect width="512" height="512" rx="%d" fill="%s"/><g transform="translate(%.2f %.2f) scale(%.4f)">%s</g>'%(r,bg,ox,oy,k,P(da,fg))
    open(OUT+'/'+nm,'w').write(svg(512,512,body))
seal('ag-sello-pino.svg',C['pino'],C['lila'],112)
seal('ag-sello-lila.svg',C['lila'],C['tinta'],112)
seal('ag-avatar-circulo.svg',C['pino'],C['lila'],256)
json.dump(marks,open(HERE+'/marks.json','w'))
print(sorted(os.listdir(OUT)))
