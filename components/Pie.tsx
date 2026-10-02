import { CONTACTO } from '@/lib/contenido';
import { Monograma } from './Marca';

export function Pie() {
  return (
    <footer className="pie">
      <div className="envoltura">
        <div>
          <Monograma />
          <p className="lema">Cada término, cumplido.</p>
        </div>
        <nav aria-label="Pie de página">
          <a href="#areas">Áreas</a>
          <a href="#procesos">Procesos</a>
          <a href="#casos">Casos</a>
          <a href="#guia">Guía útil</a>
          <a href="#agendar">Agendar cita</a>
          <a href="#contacto">Contacto</a>
        </nav>
        <div className="legal">
          <span>{CONTACTO.nombre} · Abogada · {CONTACTO.ciudad}, {CONTACTO.departamento}</span>
          <span>La información de este sitio es general y no reemplaza la asesoría sobre su caso.</span>
        </div>
      </div>
    </footer>
  );
}
