import { APILADO, ICONOS, LOGOTIPO, MONOGRAMA, type NombreIcono } from '@/lib/marca.generada';

// El logotipo y el monograma salen de design-system/: nunca se reescriben con la fuente.
export function Logotipo({ className = 'wm' }: { className?: string }) {
  return (
    <svg className={className} viewBox={`0 0 ${LOGOTIPO.w} ${LOGOTIPO.h}`} role="img" aria-label="Arroyo Guzmán">
      <path d={LOGOTIPO.d} />
    </svg>
  );
}

export function LogotipoApilado({ className = 'wm' }: { className?: string }) {
  return (
    <svg className={className} viewBox={`0 0 ${APILADO.w} ${APILADO.h}`} role="img" aria-label="Arroyo Guzmán">
      <path d={APILADO.d} />
    </svg>
  );
}

/** Monograma "ag.": el punto cuadrado es la última casilla de la barra de términos. */
export function Monograma({ className = 'mono' }: { className?: string }) {
  return (
    <svg className={className} viewBox={`0 0 ${MONOGRAMA.w} ${MONOGRAMA.h}`} role="img" aria-label="ag.">
      <path d={MONOGRAMA.d} />
      <path className="pt" d={MONOGRAMA.dot} />
    </svg>
  );
}

export function Icono({ nombre, className = 'ic' }: { nombre: NombreIcono; className?: string }) {
  return (
    <svg
      className={className}
      aria-hidden="true"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="square"
      strokeLinejoin="miter"
      dangerouslySetInnerHTML={{ __html: ICONOS[nombre] }}
    />
  );
}

/** Barra de términos: una casilla por día hábil; las cumplidas en pino y la de hoy en lila. */
export function BarraTerminos({ total, cumplidos, className = 'barra' }: { total: number; cumplidos: number; className?: string }) {
  return (
    <div className={className} aria-hidden="true">
      {Array.from({ length: total }, (_, i) => (
        <i key={i} className={i < cumplidos ? 'h' : i === cumplidos ? 'hoy' : undefined} />
      ))}
    </div>
  );
}
