# Mini marks for Arroyo Guzmán with a legal nod
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wm2, uharfbuzz as hb
from fontTools.ttLib import TTFont
from shapely.geometry import box, Point, Polygon
from shapely.ops import unary_union
from shapely import affinity
UPM=2048
def glyph(ch, w='500'):
    tt=TTFont(wm2.FD%w); gs=tt.getGlyphSet(); name=tt.getBestCmap()[ord(ch)]
    return wm2.glyph_geom(gs,name,0), gs[name].width

def nib_A(w='600'):
    A,adv=glyph('A',w); minx,miny,maxx,maxy=A.bounds; cx=(minx+maxx)/2
    col=A.intersection(box(cx-4,miny,cx+4,maxy))
    parts=sorted(getattr(col,'geoms',[col]),key=lambda g:g.bounds[1])
    bar=parts[0].bounds  # crossbar is the lowest solid run at centre
    solid=unary_union([A, A.intersection(box(minx,bar[1],maxx,maxy)).convex_hull])
    hole_y=bar[3]+ (maxy-bar[3])*0.30; r=(maxx-minx)*0.055
    slit_w=(maxx-minx)*0.028
    cut=unary_union([Point(cx,hole_y).buffer(r,64), box(cx-slit_w/2,hole_y,cx+slit_w/2,maxy+10)])
    return solid.difference(cut), adv, (cx,hole_y,r,bar)

def mono(w='600', gap=-0.02):
    A,adv,info=nib_A(w); G,gadv=glyph('G',w)
    G=affinity.translate(G, adv+gap*UPM, 0)
    g=unary_union([A,G]); return g, info

def to_svg_path(g, s, ox, oy):
    return wm2.to_path(g,s,ox,oy)

if __name__=='__main__':
    out=[]
    for i,w in enumerate(['500','600','700']):
        g,_=mono(w); b=g.bounds; s=180/UPM
        out.append('<g><rect x="%d" y="20" width="300" height="300" rx="66" fill="#17433D"/><path fill="#B9A6F2" d="%s"/></g>'%(20+i*330,to_svg_path(g,s,20+i*330+150-(b[0]+b[2])/2*s,170+(b[1]+b[3])/2*s)))
    open(sys.argv[1],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="340" style="background:#F4F5F2">%s</svg>'%''.join(out))

def nib_A2(w='600', hole=0.075, slit=0.026, tip=260):
    """A as a fountain-pen nib: solid upper body, pointed tip, slit + breather hole."""
    A,adv=glyph('A',w); minx,miny,maxx,maxy=A.bounds; cx=(minx+maxx)/2
    col=A.intersection(box(cx-4,miny,cx+4,maxy))
    parts=sorted(getattr(col,'geoms',[col]),key=lambda g:g.bounds[1]); bar=parts[0].bounds
    def edge(y):  # outer x of the left and right legs at height y
        r=A.intersection(box(minx-1,y-1,maxx+1,y+1)).bounds; return r[0],r[2]
    y0,y1=bar[1],maxy-120
    l0,r0=edge(y0); l1,r1=edge(y1)
    kl=(l1-l0)/(y1-y0); kr=(r1-r0)/(y1-y0)
    yt=y0+(r0-l0)/(kl-kr)                      # where the two outer edges meet
    ypt=min(yt, maxy+tip); xl=l0+kl*(ypt-y0); xr=r0+kr*(ypt-y0)
    body=Polygon([(l0,y0),(xl,ypt),(xr,ypt),(r0,y0)]) if ypt<yt else Polygon([(l0,y0),(l0+kl*(yt-y0),yt),(r0,y0)])
    solid=unary_union([A,body])
    hy=bar[3]+(maxy-bar[3])*0.34; r=(maxx-minx)*hole; sw=(maxx-minx)*slit
    cut=unary_union([Point(cx,hy).buffer(r,64), box(cx-sw/2,hy,cx+sw/2,ypt+50)])
    return solid.difference(cut), adv

def mono2(w='600', gap=-0.01):
    A,adv=nib_A2(w); G,_=glyph('G',w)
    return unary_union([A, affinity.translate(G, adv+gap*UPM, 0)])

def ring_text(txt, cx, cy, radius, size, w='600', track=0.12, start=-90):
    """Outlined text set clockwise around a circle (glyph baselines on the circle)."""
    F=wm2.FD%w; font=hb.Font(hb.Face(open(F,'rb').read()))
    buf=hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties(); hb.shape(font,buf,{"kern":True})
    tt=TTFont(F); gs=tt.getGlyphSet(); order=tt.getGlyphOrder(); s=size/UPM
    total=sum(p.x_advance+track*UPM for p in buf.glyph_positions)*s
    circ=2*math.pi*radius; ang0=start-(total/circ*360)/2
    geoms=[]; acc=0
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        n=order[info.codepoint]; adv=(pos.x_advance+track*UPM)*s
        g=wm2.glyph_geom(gs,n,0)
        if g is not None and not g.is_empty:
            g=affinity.scale(g,s,-s,origin=(0,0))            # to svg coords (y down), baseline at 0
            g=affinity.translate(g,-adv/2+ (track*UPM*s)/2,0)
            a=math.radians(ang0+(acc+adv/2)/circ*360)
            g=affinity.rotate(g,math.degrees(a)+90,origin=(0,0))
            g=affinity.translate(g,cx+radius*math.cos(a),cy+radius*math.sin(a))
            geoms.append(g)
        acc+=adv
    return unary_union(geoms)

def svgpath(g):
    out=[]
    for p in getattr(g,'geoms',[g]):
        for ring in [p.exterior]+list(p.interiors):
            c=list(ring.coords); out.append('M'+' L'.join('%.2f %.2f'%xy for xy in c[:-1])+'Z')
    return ' '.join(out)

def place(g, s, cx, cy):
    b=g.bounds
    return affinity.translate(affinity.scale(g,s,-s,origin=(0,0)), cx-(b[0]+b[2])/2*s, cy+(b[1]+b[3])/2*s)

def seal_geom(R=256, mono_w=0.50):
    """Notarial-style seal: outer ring, legend around, AG nib monogram centred."""
    c=(R,R)
    outer=Point(c).buffer(R-6,128).difference(Point(c).buffer(R-16,128))
    inner=Point(c).buffer(R-86,128).difference(Point(c).buffer(R-92,128))
    top=ring_text('ARROYO GUZMÁN',R,R,R-66,40,'600',0.14,-90)
    bot=ring_text('ABOGADA',R,R,R-66,40,'600',0.22,90)  # bottom arc (reads upside down) -> build separately
    m=mono2('600'); mb=m.bounds; s=(2*R*mono_w)/(mb[2]-mb[0])
    mm=place(m,s,R,R+4)
    return outer, inner, top, mm

if __name__=='__main__' and len(sys.argv)>2:
    m=mono2('600'); s=190/UPM
    cells=[]
    for i,(bg,fg,rx) in enumerate([('#17433D','#B9A6F2',66),('#B9A6F2','#0E211F',66),('#F4F5F2','#17433D',66)]):
        g=place(m,s,170+i*330,170)
        cells.append('<rect x="%d" y="20" width="300" height="300" rx="%d" fill="%s"/><path fill="%s" d="%s"/>'%(20+i*330,rx,bg,fg,svgpath(g)))
    open(sys.argv[2],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="340" style="background:#ddd">%s</svg>'%''.join(cells))

def arc_text(txt, cx, cy, rmid, size, w='600', track=0.14, where='top'):
    F=wm2.FD%w; font=hb.Font(hb.Face(open(F,'rb').read()))
    buf=hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties(); hb.shape(font,buf,{"kern":True})
    tt=TTFont(F); gs=tt.getGlyphSet(); order=tt.getGlyphOrder(); s=size/UPM
    cap=tt['OS/2'].sCapHeight*s
    advs=[(pos.x_advance+track*UPM)*s for pos in buf.glyph_positions]; total=sum(advs)-track*UPM*s
    geoms=[]; acc=0
    for info,adv in zip(buf.glyph_infos,advs):
        g=wm2.glyph_geom(gs,order[info.codepoint],0)
        mid=acc+(adv-track*UPM*s)/2-total/2; acc+=adv
        if g is None or g.is_empty: continue
        g=affinity.scale(g,s,-s,origin=(0,0)); g=affinity.translate(g,-(adv-track*UPM*s)/2,0)
        if where=='top':
            r=rmid-cap/2; a=-90+math.degrees(mid/r); rot=a+90
            g=affinity.translate(g,0,0)
        else:
            r=rmid+cap/2; a=90-math.degrees(mid/r); rot=a-90
        g=affinity.rotate(g,rot,origin=(0,0))
        ar=math.radians(a); g=affinity.translate(g,cx+r*math.cos(ar),cy+r*math.sin(ar))
        geoms.append(g)
    return unary_union(geoms)

def seal2(R=256):
    c=(R,R)
    ring=Point(c).buffer(R-16,160).difference(Point(c).buffer(R-26,160))
    ring2=Point(c).buffer(R-116,160).difference(Point(c).buffer(R-122,160))
    rmid=R-71
    top=arc_text('ARROYO GUZMÁN',R,R,rmid,40,'600',0.16,'top')
    bot=arc_text('ABOGADA',R,R,rmid,40,'600',0.30,'bottom')
    dots=unary_union([Point(R-rmid,R).buffer(6,32),Point(R+rmid,R).buffer(6,32)])
    m=mono2('600'); mb=m.bounds; s=(2*(R-122)*0.62)/(mb[2]-mb[0])
    mm=place(m,s,R,R+2)
    return unary_union([ring,ring2,top,bot,dots]), mm

if __name__=='__main__' and len(sys.argv)>3:
    cells=[]
    for i,(bg,fg) in enumerate([('#17433D','#B9A6F2'),('#F4F5F2','#17433D')]):
        a,m=seal2()
        tr='translate(%d 20)'%(20+i*560)
        cells.append('<g transform="%s"><circle cx="256" cy="256" r="256" fill="%s"/><path fill="%s" d="%s %s"/></g>'%(tr,bg,fg,svgpath(a),svgpath(m)))
    open(sys.argv[3],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="552" style="background:#ddd">%s</svg>'%''.join(cells))
