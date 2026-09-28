import json,os
P=os.path.dirname(os.path.abspath(__file__))+'/../tokens.json'
def c(n,l,d,u): return {"name":n,"value":{"light":l,"dark":d},"usage":u}
colors=[
 c("pino","#17433D","#7CC2B1","Color de marca. Logotipo, botones primarios, fondos de piezas de IG y frente de la tarjeta. En claro lleva texto `on-pino`; en oscuro se aclara y lleva texto oscuro `on-pino`."),
 c("on-pino","#FFFFFF","#0D1917","Texto e íconos sobre `pino` (11:1 en claro, 8,7:1 en oscuro)."),
 c("lila","#B9A6F2","#C4B4F6","Acento de juventud en la interfaz: la casilla de hoy en la barra de términos, subrayados y fondos con texto `on-lila`. Nunca texto sobre `papel`. Para el punto del monograma o el descriptor sobre verde use `marca-lila` sobre `marca-pino`."),
 c("on-lila","#0E211F","#0E211F","Texto sobre `lila` y `lila-suave` claro (7,8:1 en claro, 8,9:1 en oscuro)."),
 c("lila-suave","#ECE6FC","#2A2442","Fondo de relieve: publicaciones de tip, destacados, notas al margen. Texto `tinta`."),
 c("menta","#DCEBE5","#1B332E","Tinte de `pino` para bloques secundarios y filas alternas. Texto `tinta`."),
 c("papel","#F4F5F2","#0D1917","Fondo de página, tarjetas en papel y membrete. Neutro con sesgo verde, no crema."),
 c("superficie","#FFFFFF","#142421","Tarjetas y campos elevados sobre `papel`."),
 c("linea","#D3DAD6","#2A3D39","Filetes de 1px, bordes de tarjetas y divisores de tabla."),
 c("tinta","#0E211F","#ECF1EE","Texto principal sobre `papel`, `superficie`, `menta` y `lila-suave`."),
 c("tinta-suave","#4F5E5A","#A3B3AE","Texto secundario, pies de foto y citas normativas sobre `papel` y `superficie` (6,2:1 en claro, 8,2:1 en oscuro)."),
 c("plazo","#A94F17","#F0A06B","Estado: término por vencer o requisito pendiente. Siempre con palabra (\"Vence en 3 días\"). Texto sobre `papel` y `superficie`."),
 c("cumplido","#1F5E4D","#8FD3BE","Estado: término cumplido o documento radicado. Siempre con palabra o ícono. Texto sobre `papel` y `superficie`."),
 c("foco","#5B3FC4","#C4B4F6","Anillo de foco sólido de 2px en web: 6,5:1 o más sobre `papel` y `superficie`. Sobre un fondo `pino` el anillo usa `on-pino`."),
 c("marca-pino","#17433D","#17433D","FIJO en ambos temas. Piezas de marca que no cambian con la pantalla: logotipo, publicaciones de IG, tarjeta, sello, avatar."),
 c("marca-bosque","#0F2E2A","#0F2E2A","FIJO. Fondo más profundo de historias de IG y del frente alterno de la tarjeta."),
 c("marca-lila","#B9A6F2","#B9A6F2","FIJO. Punto del monograma ag. y descriptor del logotipo sobre `marca-pino` o `marca-bosque` (5,1:1 y 6,8:1) y fondos de piezas con texto `marca-tinta`."),
 c("marca-lila-suave","#ECE6FC","#ECE6FC","FIJO. Fondo de publicaciones de tip y portadas de destacados; texto `marca-tinta`."),
 c("marca-menta","#DCEBE5","#DCEBE5","FIJO. Fondo alterno de carruseles; texto `marca-tinta`."),
 c("marca-papel","#F4F5F2","#F4F5F2","FIJO. Papel de impresos e IG; también texto claro sobre `marca-pino` (10:1) y `marca-bosque` (13:1)."),
 c("marca-tinta","#0E211F","#0E211F","FIJO. Texto de piezas sobre `marca-papel`, `marca-lila`, `marca-lila-suave` y `marca-menta`."),
 c("marca-gris","#4F5E5A","#4F5E5A","FIJO. Texto secundario y citas normativas en piezas sobre `marca-papel` y `marca-lila-suave` (6,2:1 y 5,6:1)."),
]
fam='"Open Sans", "Segoe UI", "Helvetica Neue", Arial, sans-serif'
fonts=[{"family":"Open Sans","file":"fonts/OpenSans-%s.ttf"%w,"weight":w} for w in ["400","500","600","700"]]
fonts.append({"family":"Open Sans","file":"fonts/OpenSans-400-italic.ttf","weight":"400","style":"italic"})
def st(n,fs,lh,fw,ls=None,usage="",sample=None,style=None):
    d={"name":n,"fontSize":fs,"lineHeight":lh,"fontWeight":fw,"usage":usage}
    if ls: d["letterSpacing"]=ls
    if sample: d["sample"]=sample
    if style: d["fontStyle"]=style
    return d
tokens={"name":"Arroyo Guzmán","version":1,
 "color":{"themes":[{"id":"light","name":"Claro"},{"id":"dark","name":"Oscuro"}],"tokens":colors},
 "type":{"fonts":fonts,"families":{"sans":fam},
  "groups":[
   {"name":"Titulares","family":"sans","styles":[
     st("display",60,"64px",500,"-0.03em","Portada del sitio y titular único de una pieza. Una vez por vista.","Cada término, cumplido."),
     st("titulo-1",38,"44px",500,"-0.025em","Título de página o sección principal.","Derecho procesal civil"),
     st("titulo-2",27,"34px",600,"-0.015em","Subsecciones, nombre en la tarjeta, títulos de tarjetas de servicio.","Sucesiones y herencias"),
     st("titulo-3",20,"28px",600,"-0.01em","Encabezados menores y preguntas en listas de preguntas frecuentes.","¿Cuánto tarda un proceso ejecutivo?")]},
   {"name":"Texto","family":"sans","styles":[
     st("cuerpo",16,"26px",400,None,"Texto corrido en web y documentos. Máximo 65 caracteres por línea.","Le explico su caso en palabras claras y le digo qué sigue, con fechas."),
     st("cuerpo-sm",14,"21px",400,None,"Texto de apoyo, formularios, firma de correo.","Consulta inicial de 45 minutos, presencial o virtual."),
     st("cita",21,"32px",400,"-0.01em","Frases y testimonios, en itálica.","Un proceso bien llevado empieza por un plazo bien contado.","italic"),
     st("etiqueta",11,"16px",600,"0.16em","Antetítulos y áreas de práctica, SIEMPRE en mayúsculas.","PROCESAL CIVIL · DATO ÚTIL"),
     st("norma",13,"18px",400,"0.01em","Citas normativas y letra de soporte (artículo, ley, radicado).","Código General del Proceso, art. 369")]},
   {"name":"Instagram (lienzo 1080 px)","family":"sans","styles":[
     st("ig-titular",80,"88px",600,"-0.03em","Titular de publicación 1080×1350. Máximo 12 palabras.","Tiene 20 días para contestar."),
     st("ig-cuerpo",32,"46px",400,None,"Texto de apoyo en publicaciones y carruseles. Máximo 30 palabras por lámina.","Cuente los días hábiles desde la notificación."),
     st("ig-etiqueta",22,"28px",600,"0.14em","Antetítulo de pieza de IG en mayúsculas.","LABORAL")]}]},
 "spacing":{"tokens":[{"name":"space-1","value":"4px","usage":"Separación entre ícono y texto en etiquetas."},
   {"name":"space-2","value":"8px","usage":"Casillas de la barra de términos y su separación."},
   {"name":"space-3","value":"12px","usage":"Relleno vertical de botones y etiquetas."},
   {"name":"space-4","value":"16px","usage":"Margen lateral mínimo en móvil; relleno de campos."},
   {"name":"space-6","value":"24px","usage":"Relleno de tarjetas; separación entre bloques de texto."},
   {"name":"space-8","value":"32px","usage":"Separación entre tarjetas en una grilla."},
   {"name":"space-12","value":"48px","usage":"Separación entre secciones en web."},
   {"name":"space-18","value":"72px","usage":"Margen de seguridad de publicaciones IG (a 1080 px)."}]},
 "radius":{"tokens":[{"name":"radius-sm","value":"4px","usage":"Etiquetas de área y casillas de la barra de términos."},
   {"name":"radius-md","value":"10px","usage":"Botones, campos y tarjetas."},
   {"name":"radius-lg","value":"22%","usage":"Ícono de app y sello del monograma (proporción del lado)."},
   {"name":"radius-pill","value":"999px","usage":"Solo indicadores de estado (Cumplido, Vence pronto)."}]},
 "shadow":{"tokens":[{"name":"sombra-tarjeta","value":{"light":"0 1px 2px rgba(14,33,31,0.08), 0 8px 24px rgba(14,33,31,0.08)","dark":"0 1px 2px rgba(0,0,0,0.4), 0 8px 24px rgba(0,0,0,0.35)"},"usage":"Única sombra del sistema: tarjeta profesional en mockups y tarjetas flotantes en web. La jerarquía se hace con filetes, no con sombras."}]}
}
json.dump(tokens,open(P,'w'),ensure_ascii=False,indent=1)
# contrast check
def lum(h):
    h=h.lstrip('#');r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda x:x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    A,B=sorted([lum(a),lum(b)],reverse=True);return (A+0.05)/(B+0.05)
V={t["name"]:t["value"] for t in colors}
pairs=[("tinta","papel"),("tinta","superficie"),("tinta","menta"),("tinta","lila-suave"),("tinta-suave","papel"),("tinta-suave","superficie"),("on-pino","pino"),("on-lila","lila"),("plazo","papel"),("plazo","superficie"),("cumplido","papel"),("foco","papel"),("foco","superficie"),("foco","pino"),("lila","pino"),("marca-lila","marca-bosque"),("marca-papel","marca-bosque"),("marca-papel","marca-pino"),("marca-gris","marca-lila-suave"),("marca-lila","marca-pino"),("pino","papel")]
for th in ("light","dark"):
    print(th,' '.join('%s/%s=%.1f'%(a,b,cr(V[a][th],V[b][th])) for a,b in pairs))
