# Wordmark "Arroyo Guzmán" in Open Sans with a joined "rr" ligature (the arm of the first r runs into the second r)
import uharfbuzz as hb, os
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
FD=os.path.dirname(os.path.abspath(__file__))+'/../fonts/OpenSans-%s.ttf'

class FlatPen(BasePen):
    def __init__(self, gs, steps=12):
        super().__init__(gs); self.rings=[]; self.cur=[]; self.steps=steps
    def _moveTo(self,p): self.cur=[p]
    def _lineTo(self,p): self.cur.append(p)
    def _curveToOne(self,p1,p2,p3):
        p0=self.cur[-1]
        for i in range(1,self.steps+1):
            t=i/self.steps; mt=1-t
            self.cur.append((mt**3*p0[0]+3*mt*mt*t*p1[0]+3*mt*t*t*p2[0]+t**3*p3[0], mt**3*p0[1]+3*mt*mt*t*p1[1]+3*mt*t*t*p2[1]+t**3*p3[1]))
    def _qCurveToOne(self,p1,p2):
        p0=self.cur[-1]
        for i in range(1,self.steps+1):
            t=i/self.steps; mt=1-t
            self.cur.append((mt*mt*p0[0]+2*mt*t*p1[0]+t*t*p2[0], mt*mt*p0[1]+2*mt*t*p1[1]+t*t*p2[1]))
    def _closePath(self):
        if len(self.cur)>2: self.rings.append(self.cur)
        self.cur=[]
    _endPath=_closePath

def glyph_geom(gs,name,dx):
    pen=FlatPen(gs); gs[name].draw(pen)
    polys=[Polygon([(x+dx,y) for x,y in r]).buffer(0) for r in pen.rings]
    # even-odd: sort by area, xor
    g=None
    for p in sorted(polys,key=lambda p:-p.area):
        g=p if g is None else g.symmetric_difference(p)
    return g

def wordmark(txt, weight='500', track=-0.03, join_rr=True):
    data=open(FD%weight,'rb').read(); font=hb.Font(hb.Face(data))
    buf=hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties(); hb.shape(font,buf,{"kern":True})
    tt=TTFont(FD%weight); gs=tt.getGlyphSet(); upm=tt['head'].unitsPerEm; order=tt.getGlyphOrder()
    cx=0; parts=[]; placed=[]
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        n=order[info.codepoint]; parts.append(glyph_geom(gs,n,cx+pos.x_offset)); placed.append((n,cx)); cx+=pos.x_advance+track*upm
    width=cx-track*upm
    if join_rr:
        for i in range(len(placed)-1):
            if placed[i][0]=='r' and placed[i+1][0]=='r':
                r1=parts[i]; minx,miny,maxx,maxy=r1.bounds
                # stem of r: left part; find stem right edge by scanning at y=400
                stem=[g for g in [r1.intersection(box(minx,390,maxx,410))]][0].bounds
                stem_l,stem_r=stem[0],stem[2]
                r2=parts[i+1]; s2=r2.intersection(box(r2.bounds[0],390,r2.bounds[2],410)).bounds
                # find the arm apex: first column right of the stem whose top reaches the glyph top
                apex=None
                for xx in range(int(stem_r)+20,int(maxx),8):
                    c=r1.intersection(box(xx,0,xx+8,maxy+10))
                    if not c.is_empty and c.bounds[3]>=maxy-3: apex=xx; th=c.bounds[3]-c.bounds[1] if c.geom_type=='Polygon' else None; break
                col=r1.intersection(box(apex,600,apex+8,maxy+10)).bounds
                th=col[3]-col[1]; top=maxy
                cutx=apex+4
                r1=r1.difference(box(cutx,0,maxx+50,maxy+50))
                band=box(cutx-4,top-th,s2[2],top)
                fill=box(s2[0],top-th-40,s2[2],top)
                parts[i]=unary_union([r1,band]); parts[i+1]=unary_union([r2,fill])
    g=unary_union(parts)
    return g,width,tt

def to_path(g,s,ox,oy):
    geoms=getattr(g,'geoms',[g]); out=[]
    for p in geoms:
        for ring in [p.exterior]+list(p.interiors):
            c=list(ring.coords)
            out.append('M'+' L'.join('%.2f %.2f'%(ox+x*s,oy-y*s) for x,y in c[:-1])+'Z')
    return ' '.join(out)

if __name__=='__main__':
    import sys
    rows=[]; y=0
    for w,tr,j in [('500',-0.03,False),('500',-0.03,True),('600',-0.03,True)]:
        g,wd,tt=wordmark('Arroyo Guzmán',w,tr,j); s=110/2048; y+=150
        rows.append('<path d="%s"/>'%to_path(g,s,20,y))
    g,wd,tt=wordmark('Arroyo','500',-0.03,True); s=420/2048; y+=480
    rows.append('<path d="%s"/>'%to_path(g,s,20,y))
    open(sys.argv[1],'w').write('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="%d" style="background:#fff">%s</svg>'%(y+140,''.join(rows)))
