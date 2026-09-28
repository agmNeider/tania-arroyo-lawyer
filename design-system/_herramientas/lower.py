# Lowercase "ag" monogram explorations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mini import glyph, UPM, svgpath, place
from fuse import runs, hruns
from shapely.geometry import box
from shapely.ops import unary_union
from shapely import affinity
from fontTools.ttLib import TTFont
import wm2

def xh(w): return TTFont(wm2.FD%w)['OS/2'].sxHeight

def pair(w='600', shift=0.0):
    a,aadv=glyph('a',w); g,gadv=glyph('g',w)
    return a, affinity.translate(g, aadv*(1-shift), 0), aadv

def plain(w='600', shift=0.06):
    a,g,_=pair(w,shift); return unary_union([a,g])

def ear_beam(w='600', shift=0.06):
    """The g's ear runs left across the top of the a: one straight line over both letters."""
    a,g,_=pair(w,shift); gb=g.bounds; ab=a.bounds
    top=hruns(g, gb[3]-20, gb[0], gb[2])            # the ear at the very top of the g
    ear_y=[b for b in runs(g, top[-1][2]-30, gb[1], gb[3]+10)][-1]
    y0,y1=ear_y[1],ear_y[3]
    # start the beam where the a's arch is already at full height, so no notch shows
    xs=None
    for k in range(40):
        x=ab[0]+(ab[2]-ab[0])*(0.15+k*0.01)
        r=runs(a,x,ab[1],ab[3]+20)
        if r and r[-1][3]>=y1-4: xs=x; break
    xs=xs or ab[0]+(ab[2]-ab[0])*0.3
    return unary_union([a,g,box(xs, y0, top[-1][2], y1)])

def shared_stem(w='600', shift=0.30):
    """The g slides left until its upper bowl rests on the a's stem."""
    a,g,_=pair(w,shift); return unary_union([a,g])

def tail_link(w='600', shift=0.10):
    """The a's foot runs along the baseline into the g's bowl."""
    a,g,aadv=pair(w,shift); ab=a.bounds; gb=g.bounds
    th=(ab[2]-ab[0])*0.13
    base=hruns(g, 30, gb[0], gb[2])
    return unary_union([a,g,box(ab[2]-th*1.2, 0, base[0][0]+th, th)])

if __name__=='__main__':
    opts=[('A · ag, junta',plain('600',0.06)),('B · Oreja de la g como viga',ear_beam('600',0.06)),
          ('C · Asta compartida',shared_stem('600',0.28)),('D · Asta compartida + viga',None),('E · peso 500 + viga',ear_beam('500',0.06))]
    g=shared_stem('600',0.28); gb=g.bounds
    top=hruns(g, gb[3]-20, gb[0], gb[2]); ey=runs(g, top[-1][2]-30, 0, gb[3]+10)[-1]
    opts[3]=('D · Asta compartida + viga', unary_union([g, box(gb[0]+(gb[2]-gb[0])*0.06, ey[1], top[-1][2], ey[3])]))
    cells=[]
    for i,(lab,g) in enumerate(opts):
        x=20+i*300; b=g.bounds; s=min(190/(b[2]-b[0]),150/(b[3]-b[1]))
        cells.append('<rect x="%d" y="20" width="280" height="280" rx="62" fill="#17433D"/><path fill="#B9A6F2" d="%s"/><text x="%d" y="330" font-family="sans-serif" font-size="15" fill="#0E211F">%s</text>'%(x,svgpath(place(g,s,x+140,160)),x,lab))
        cells.append('<rect x="%d" y="360" width="280" height="160" fill="#F4F5F2"/><path fill="#17433D" d="%s"/><path fill="#17433D" d="%s"/>'%(x,svgpath(place(g,s*0.55,x+90,440)),svgpath(place(g,s*0.16,x+220,440))))
    open(sys.argv[1],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1520" height="540" style="background:#ddd">%s</svg>'%''.join(cells))

if __name__=='__main__' and len(sys.argv)>2:
    import fuse
    up=fuse.level('600',0.40,True)
    opts=[('Mayúsculas (actual)',up),('B · viga, 600',ear_beam('600',0.06)),('E · viga, 500',ear_beam('500',0.06)),
          ('F · viga, 600, más junta',ear_beam('600',0.14)),('G · viga, 500, más junta',ear_beam('500',0.14))]
    cells=[]
    for i,(lab,g) in enumerate(opts):
        x=20+i*300; b=g.bounds; s=min(190/(b[2]-b[0]),150/(b[3]-b[1]))
        cells.append('<rect x="%d" y="20" width="280" height="280" rx="62" fill="#17433D"/><path fill="#B9A6F2" d="%s"/><text x="%d" y="330" font-family="sans-serif" font-size="15" fill="#0E211F">%s</text>'%(x,svgpath(place(g,s,x+140,160)),x,lab))
        cells.append('<rect x="%d" y="360" width="280" height="160" fill="#F4F5F2"/><circle cx="%d" cy="440" r="60" fill="#17433D"/><path fill="#B9A6F2" d="%s"/><path fill="#17433D" d="%s"/>'%(x,x+90,svgpath(place(g,s*0.36,x+90,440)),svgpath(place(g,s*0.16,x+220,440))))
    open(sys.argv[2],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1520" height="540" style="background:#ddd">%s</svg>'%''.join(cells))
