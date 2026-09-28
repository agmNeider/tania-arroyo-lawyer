# "ag" lowercase side by side, with small legal details
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mini import glyph, UPM, svgpath, place
from fuse import runs, hruns
from lower import pair
from shapely.geometry import box, Point
from shapely.ops import unary_union

W='600'; SH=0.06
def base():
    a,g,_=pair(W,SH); return a,g
def stem_w(a):
    ab=a.bounds; r=hruns(a,(ab[1]+ab[3])*0.45,ab[0],ab[2]); return r[-1][2]-r[-1][0]

def plain():
    a,g=base(); return unary_union([a,g]), None

def punto():
    """A square full stop in lila: the barra de términos' last cell, 'término cumplido'."""
    a,g=base(); t=stem_w(a)*1.05; gb=g.bounds
    return unary_union([a,g]), box(gb[2]+t*0.55, 0, gb[2]+t*1.55, t)

def rubrica():
    """The g's tail runs back under the a: the underline of a signature (firma con rúbrica)."""
    a,g=base(); ab=a.bounds; gb=g.bounds
    low=runs(g,(gb[0]+gb[2])/2,gb[1]-5,0)[0]           # bottom of the g's loop
    th=low[3]-low[1]
    return unary_union([a,g,box(ab[0]+th*0.2, low[1], (gb[0]+gb[2])/2, low[3])]), None

def igualdad():
    """The g's ear doubled into '=': equality before the law."""
    a,g=base(); gb=g.bounds
    top=hruns(g,gb[3]-20,gb[0],gb[2]); ear_end=top[-1][2]
    ey=runs(g,ear_end-30,0,gb[3]+10)[-1]; th=ey[3]-ey[1]
    stem=hruns(g,(ey[1])-th*2.2,gb[0],gb[2])[-1]       # g's right stem just under the ear
    ext=th*1.4
    bar1=box(stem[0]+10, ey[1], ear_end+ext, ey[3])
    gap=th*0.85
    bar2=box(stem[2]+th*0.35, ey[1]-gap-th, ear_end+ext, ey[1]-gap)
    return unary_union([a,g,bar1]), bar2

def parrafo():
    """A small section sign (§), the mark of articles and statutes, set as a superior after the g."""
    from shapely import affinity
    a,g=base(); gb=g.bounds; ab=a.bounds
    sec,_=glyph('§',W); sb=sec.bounds
    k=(ab[3]-ab[1])*0.62/(sb[3]-sb[1])
    sec=affinity.scale(sec,k,k,origin=(0,0)); sb=sec.bounds
    sec=affinity.translate(sec, gb[2]+stem_w(a)*0.35-sb[0], ab[3]-sb[3])
    return unary_union([a,g]), sec

def rubrica_punto():
    m,_=rubrica(); _,p=punto(); return m,p

if __name__=='__main__':
    opts=[('A · ag',plain()),('A1 · punto de término cumplido',punto()),('A2 · rúbrica de firma',rubrica()),
          ('A3 · igualdad ante la ley',igualdad()),('A5 · párrafo §',parrafo())]
    cells=[]
    for i,(lab,(g,p)) in enumerate(opts):
        allg=unary_union([g]+([p] if p is not None else [])); b=allg.bounds
        s=min(190/(b[2]-b[0]),150/(b[3]-b[1]))
        def pl(geom,sc,cx,cy):
            from shapely import affinity
            return svgpath(affinity.translate(affinity.scale(geom,sc,-sc,origin=(0,0)), cx-(b[0]+b[2])/2*sc, cy+(b[1]+b[3])/2*sc))
        x=20+i*300
        c='<rect x="%d" y="20" width="280" height="280" rx="62" fill="#17433D"/><path fill="#F4F5F2" d="%s"/>'%(x,pl(g,s,x+140,160))
        if p is not None: c+='<path fill="#B9A6F2" d="%s"/>'%pl(p,s,x+140,160)
        c+='<text x="%d" y="330" font-family="sans-serif" font-size="15" fill="#0E211F">%s</text>'%(x,lab)
        c+='<rect x="%d" y="360" width="280" height="160" fill="#F4F5F2"/><circle cx="%d" cy="440" r="60" fill="#17433D"/><path fill="#B9A6F2" d="%s"/>'%(x,x+90,pl(g,s*0.36,x+90,440))
        if p is not None: c+='<path fill="#F4F5F2" d="%s"/>'%pl(p,s*0.36,x+90,440)
        c+='<path fill="#17433D" d="%s"/>'%pl(g,s*0.16,x+220,440)
        if p is not None: c+='<path fill="#17433D" d="%s"/>'%pl(p,s*0.16,x+220,440)
        cells.append(c)
    open(sys.argv[1],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1520" height="540" style="background:#ddd">%s</svg>'%''.join(cells))
