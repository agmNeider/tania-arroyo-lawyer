# Fused AG monogram explorations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mini
from mini import glyph, UPM, svgpath, place
from shapely.geometry import box, Polygon
from shapely.ops import unary_union
from shapely import affinity

def runs(g, x, y0, y1):
    c=g.intersection(box(x-3,y0,x+3,y1))
    return sorted([p.bounds for p in getattr(c,'geoms',[c]) if not p.is_empty], key=lambda b:b[1])

def parts(w='600'):
    A,aadv=glyph('A',w); G,gadv=glyph('G',w)
    ab=A.bounds; cx=(ab[0]+ab[2])/2
    bar=runs(A,cx,ab[1],ab[3])[0]                     # A crossbar (y1,y3)
    gb=G.bounds
    # G horizontal bar: scan a column just left of the G stem
    col=runs(G,gb[2]-160,gb[1]+100,gb[3]-100)
    return A,aadv,G,gadv,bar,col

def hruns(g, y, x0, x1):
    c=g.intersection(box(x0,y-3,x1,y+3))
    return sorted([p.bounds for p in getattr(c,'geoms',[c]) if not p.is_empty], key=lambda b:b[0])

def g_bar(G):
    gb=G.bounds; h=gb[3]-gb[1]
    for b in runs(G, gb[2]-(gb[2]-gb[0])*0.28, gb[1], gb[3]):
        if gb[1]+h*0.3 < (b[1]+b[3])/2 < gb[1]+h*0.7: return b
    raise ValueError('no G bar')

def shared_bar(w='600', shift=0.0, reach=1.0):
    """The A's crossbar is lifted to the G's bar height and runs straight into it: one line through both letters."""
    A,aadv,G,gadv,bar,col=parts(w); ab=A.bounds
    Gs=affinity.translate(G, aadv*(1-shift), 0)
    gy=g_bar(Gs); y0,y1=gy[1],gy[3]
    # remove the original crossbar between the legs
    lg=hruns(A,(bar[1]+bar[3])/2+0,ab[0],ab[2])
    below=hruns(A,bar[1]-30,ab[0],ab[2])
    legs=A.difference(box(below[0][2]+1,bar[1]-1,below[-1][0]-1,bar[3]+1))
    # new line: from the left leg's inner edge to the G's stem
    at=hruns(legs,(y0+y1)/2,ab[0],ab[2])
    x_start=at[0][0] if reach>=1 else at[0][2]-5
    line=box(x_start, y0, gy[2], y1)
    return unary_union([legs, Gs, line])
def shared_leg(w='600', shift=0.30):
    """G slides left until its bowl meets the A's right leg."""
    A,aadv,G,gadv,bar,col=parts(w)
    return unary_union([A, affinity.translate(G, aadv*(1-shift), 0)])

def inside(w='600'):
    """A set inside the G's counter."""
    A,_,G,_,_,_=parts(w); gb=G.bounds; ab=A.bounds
    s=0.50; a=affinity.scale(A,s,s,origin=(0,0)); a2=a.bounds
    a=affinity.translate(a, gb[0]+(gb[2]-gb[0])*0.47-(a2[0]+a2[2])/2, gb[1]+(gb[3]-gb[1])*0.24-a2[1])
    return unary_union([G.difference(a.buffer(40)), a])

if __name__=='__main__':
    opts=[('1 · Línea que cruza',shared_bar('600',0.02,0)),('2 · Línea que cruza, solapada',shared_bar('600',0.20,0)),
          ('3 · Pierna compartida',shared_leg('600',0.28)),('4 · Pierna + línea',shared_bar('600',0.28,0)),('5 · Pierna + línea larga',shared_bar('600',0.28,1))]
    cells=[]
    for i,(lab,g) in enumerate(opts):
        x=20+i*300; b=g.bounds; s=min(190/(b[2]-b[0]),150/(b[3]-b[1]))
        cells.append('<rect x="%d" y="20" width="280" height="280" rx="62" fill="#17433D"/><path fill="#B9A6F2" d="%s"/><path fill="#17433D" d="%s"/><text x="%d" y="330" font-family="sans-serif" font-size="15" fill="#0E211F">%s</text>'%(x,svgpath(place(g,s,x+140,160)),svgpath(place(g,s*0.2,x+140,440)),x,lab))
        cells.append('<rect x="%d" y="360" width="280" height="160" fill="#F4F5F2"/><path fill="#17433D" d="%s"/><path fill="#17433D" d="%s"/>'%(x,svgpath(place(g,s*0.55,x+90,440)),svgpath(place(g,s*0.16,x+220,440))))
    open(sys.argv[1],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1520" height="540" style="background:#ddd">%s</svg>'%''.join(cells))

def leg_level(w='600', shift=0.28, mode='aligned'):
    """Shared leg; the A's crossbar lifted to the G's bar height so both bars sit on one level (the balance's pointer line)."""
    A,aadv,G,gadv,bar,col=parts(w); ab=A.bounds
    Gs=affinity.translate(G, aadv*(1-shift), 0)
    gy=g_bar(Gs); y0,y1=gy[1],gy[3]
    below=hruns(A,bar[1]-30,ab[0],ab[2])
    legs=A.difference(box(below[0][2]+1,bar[1]-1,below[-1][0]-1,bar[3]+1))
    at=hruns(legs,(y0+y1)/2,ab[0],ab[2])
    if mode=='aligned':
        line=box(at[0][2]-5, y0, at[-1][0]+5, y1)
    else:  # continuous: from the A's left leg to the G's stem
        line=box(at[0][2]-5, y0, gy[2], y1)
    return unary_union([legs, Gs, line])

def deep(w='600', shift=0.42):
    A,aadv,G,gadv,bar,col=parts(w)
    return unary_union([A, affinity.translate(G, aadv*(1-shift), 0)])

if __name__=='__main__' and len(sys.argv)>2:
    opts=[('3 · Pierna compartida',shared_leg('600',0.28)),('6 · Barras a nivel',leg_level('600',0.28,'aligned')),
          ('7 · Línea continua',leg_level('600',0.28,'cont')),('8 · Fusión profunda',deep('600',0.40)),('9 · Profunda + nivel',leg_level('600',0.40,'aligned'))]
    cells=[]
    for i,(lab,g) in enumerate(opts):
        x=20+i*300; b=g.bounds; s=min(190/(b[2]-b[0]),150/(b[3]-b[1]))
        cells.append('<rect x="%d" y="20" width="280" height="280" rx="62" fill="#17433D"/><path fill="#B9A6F2" d="%s"/><text x="%d" y="330" font-family="sans-serif" font-size="15" fill="#0E211F">%s</text>'%(x,svgpath(place(g,s,x+140,160)),x,lab))
        cells.append('<rect x="%d" y="360" width="280" height="160" fill="#F4F5F2"/><path fill="#17433D" d="%s"/><path fill="#17433D" d="%s"/>'%(x,svgpath(place(g,s*0.55,x+90,440)),svgpath(place(g,s*0.16,x+220,440))))
    open(sys.argv[2],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1520" height="540" style="background:#ddd">%s</svg>'%''.join(cells))

def legs_only(A, bar):
    """The A without its crossbar, cut along the legs' own inner edges (no stubs)."""
    ab=A.bounds
    ya,yb=bar[3]+60, bar[1]-60
    ra=hruns(A,ya,ab[0],ab[2]); rb=hruns(A,yb,ab[0],ab[2])
    def line_x(xa,xb,y): return xa+(xb-xa)*(y-ya)/(yb-ya)
    lo,hi=ab[1]-10,ab[3]+10
    lx=lambda y: line_x(ra[0][2],rb[0][2],y); rx=lambda y: line_x(ra[-1][0],rb[-1][0],y)
    left=Polygon([(ab[0]-10,lo),(lx(lo),lo),(lx(hi),hi),(ab[0]-10,hi)])
    right=Polygon([(rx(lo),lo),(ab[2]+10,lo),(ab[2]+10,hi),(rx(hi),hi)])
    top=box(ab[0],bar[3]+120,ab[2],ab[3]+10)
    return A.intersection(unary_union([left,right,top])), lx, rx

def level(w='600', shift=0.40, join=False, thin=1.0):
    A,aadv,G,gadv,bar,col=parts(w)
    Gs=affinity.translate(G, aadv*(1-shift), 0); gy=g_bar(Gs); y0,y1=gy[1],gy[3]
    if thin!=1.0:
        m=(y0+y1)/2; h=(y1-y0)*thin; y0,y1=m-h/2,m+h/2
    legs,lx,rx=legs_only(A,bar)
    ym=(y0+y1)/2
    x1=gy[0] if join else rx(ym)+ (A.bounds[2]-A.bounds[0])*0.06
    line=box(lx(ym)-20, y0, x1+5, y1)
    return unary_union([legs, Gs, line])

if __name__=='__main__' and len(sys.argv)>3:
    opts=[('8 · Fusión profunda',deep('600',0.40)),('10 · A y G a nivel',level('600',0.40,False)),
          ('11 · Una sola línea',level('600',0.40,True)),('12 · A nivel, más junta',level('600',0.48,True)),('13 · Una línea, peso 500',level('500',0.42,True))]
    cells=[]
    for i,(lab,g) in enumerate(opts):
        x=20+i*300; b=g.bounds; s=min(190/(b[2]-b[0]),150/(b[3]-b[1]))
        cells.append('<rect x="%d" y="20" width="280" height="280" rx="62" fill="#17433D"/><path fill="#B9A6F2" d="%s"/><text x="%d" y="330" font-family="sans-serif" font-size="15" fill="#0E211F">%s</text>'%(x,svgpath(place(g,s,x+140,160)),x,lab))
        cells.append('<rect x="%d" y="360" width="280" height="160" fill="#F4F5F2"/><path fill="#17433D" d="%s"/><path fill="#17433D" d="%s"/>'%(x,svgpath(place(g,s*0.55,x+90,440)),svgpath(place(g,s*0.16,x+220,440))))
    open(sys.argv[3],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1520" height="540" style="background:#ddd">%s</svg>'%''.join(cells))
